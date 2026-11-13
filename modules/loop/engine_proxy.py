from __future__ import annotations


class EngineProxyMixin:
    """Recorder-proxy lifecycle and traffic ingestion for the loop engine.

    Groups the engine's control of the shared recording proxy (start, stop,
    status, environment), the per-task mirroring of captured exchanges into
    the task traffic log, body search and retention sweeps. Every method binds
    to the host ``LazyLoopEngine`` through ``self`` and relies on the proxy
    retention attributes it sets in ``__init__`` (``proxy_gc_interval_sec``,
    ``proxy_gc_days``). Module-level helpers from :mod:`modules.lazy_loop` are
    imported lazily to avoid a circular import at module load time.
    """

    def proxy_start(
        self, host: str = "", port: int = 0, task_id: str = "", trust: bool = True, upstream: str = ""
    ) -> dict:
        """Start the shared recorder proxy and apply its trust environment.

        Args:
            host: Bind address (default 127.0.0.1).
            port: Bind port (default 8899).
            task_id: Task tag stored with each exchange.
            trust: Also install the CA into the system trust store,
                prompting sudo only when the anchor is missing or stale.
            upstream: Optional ``[user:pass@]host:port`` proxy to chain.

        Returns:
            Proxy status dict including the CA path and trust outcome.
        """
        from modules import lazy_proxy as _proxy

        status = _proxy.get_proxy().start(
            host=host or _proxy.DEFAULT_PROXY_HOST,
            port=port or _proxy.DEFAULT_PROXY_PORT,
            task_id=task_id,
            upstream=upstream,
        )
        _proxy.apply_env(status["ca_path"], status["host"], status["port"])
        if trust:
            try:
                status["trust"] = _proxy.install_ca_trust(status["ca_path"])
            except Exception as exc:
                status["trust"] = {"installed": False, "reason": str(exc)[:200], "anchor": ""}
            try:
                status["nss"] = _proxy.install_ca_nss(status["ca_path"])
            except Exception as exc:
                status["nss"] = {"installed": 0, "profiles": 0, "reason": str(exc)[:200]}
        return status

    def proxy_stop(self) -> dict:
        """Stop the recorder proxy and clear its trust environment."""
        from modules import lazy_proxy as _proxy

        status = _proxy.get_proxy().stop()
        _proxy.restore_env({key: None for key in _proxy.PROXY_ENV_KEYS})
        return status

    def proxy_status(self) -> dict:
        """Return recorder proxy state (running, address, CA, exchanges)."""
        from modules import lazy_proxy as _proxy

        return _proxy.get_proxy().status()

    def proxy_env(self) -> dict:
        """Return the environment overrides that route tools via proxy."""
        from modules import lazy_proxy as _proxy

        status = _proxy.get_proxy().status()
        if not status.get("running"):
            return {}
        return _proxy.env_for_ca(status["ca_path"], status["host"], status["port"])

    def ingest_proxy_traffic(self, task_id: str, limit: int = 200) -> int:
        """Mirror new recorder exchanges into the task traffic log.

        A per-task rowid watermark keeps repeated rounds cheap; the
        recorder exchange id rides in meta so ``lazy_traffic body`` can
        fetch stored request/response bodies from the proxy store.

        Args:
            task_id: Task receiving the mirrored rows.
            limit: Max rows per ingest page.

        Returns:
            Number of freshly ingested exchanges.
        """
        from modules import lazy_proxy as _proxy
        from modules.lazy_loop import ActivityLog, TrafficLog, _load_json, _save_json, _store_path

        recorder = _proxy.get_proxy().recorder()
        if recorder is None:
            return 0
        path = _store_path(f"proxy_ingest_{task_id}.json")
        watermark = int((_load_json(path, {"rowid": 0}) or {}).get("rowid", 0))
        try:
            rows = recorder.since(watermark, limit=limit)
        except Exception:
            return 0
        if not rows:
            return 0
        traffic = TrafficLog(task_id)
        count = 0
        for row in rows:
            url = str(row.get("url", ""))
            command = f"{row.get('method', 'GET')} {url}"
            output = (
                f"HTTP {row.get('status', 0)} {row.get('content_type', '')} "
                f"req={row.get('req_len', 0)}B resp={row.get('resp_len', 0)}B"
            )
            traffic.record(
                "http",
                command,
                output,
                {
                    "exchange_id": str(row.get("id", "")),
                    "recorder_path": str(row.get("path", "")),
                    "host": str(row.get("host", "")),
                    "status": int(row.get("status", 0) or 0),
                    "source": "proxy",
                },
            )
            count += 1
        _save_json(path, {"rowid": int(rows[-1].get("rowid", watermark))})
        if count:
            ActivityLog(task_id).emit("engine", "proxy", f"ingested {count} recorder exchange(s)")
        return count

    def search_proxy_body(self, task_id: str, query: str, limit: int = 20) -> list[dict]:
        """Full-text search proxy bodies scoped to one task's exchanges.

        Args:
            task_id: Task whose ingested exchanges are searched.
            query: Phrase to search for.
            limit: Max hits.

        Returns:
            Hits with exchange_id, url, status, host and snippet.
        """
        from modules import lazy_proxy as _proxy
        from modules.lazy_loop import TrafficLog

        controller = _proxy.get_proxy()
        recorder = controller.recorder()
        if recorder is None:
            from modules.traffic_recorder import TrafficRecorder

            recorder = TrafficRecorder(controller.traffic_dir)
        wanted = {str((row.get("meta") or {}).get("exchange_id", "")) for row in TrafficLog(task_id).read(2000)}
        wanted.discard("")
        if not wanted:
            return []
        hits = recorder.search_body(query, limit=max(limit * 4, 40))
        return [hit for hit in hits if str(hit.get("exchange_id", "")) in wanted][: max(1, limit)]

    def _maybe_proxy_gc(self) -> int:
        """Sweep recorder exchanges older than the retention window.

        Runs at most once every ``proxy_gc_interval_sec``; the last run
        stamp lives in the shared lazy store so restarts do not resweep.

        Returns:
            Removed exchange count (0 when skipped).
        """
        from modules import lazy_proxy as _proxy
        from modules.lazy_loop import _load_json, _now, _save_json, _store_path

        recorder = _proxy.get_proxy().recorder()
        if recorder is None:
            return 0
        path = _store_path("proxy_gc.json")
        state = _load_json(path, {"last_run": 0.0})
        now = _now()
        if now - float(state.get("last_run", 0.0) or 0.0) < float(self.proxy_gc_interval_sec):
            return 0
        try:
            removed = recorder.gc(
                older_than_sec=float(self.proxy_gc_days) * 86400,
                max_rows=int(getattr(self, "proxy_gc_max_rows", 500) or 500),
            )
        except Exception:
            removed = {"removed": 0}
        _save_json(path, {"last_run": now})
        return int(removed.get("removed", 0) or 0)
