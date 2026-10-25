"""Store file writes stay atomic under parallel workers (race regression)."""

from __future__ import annotations

import threading


def test_save_json_survives_parallel_writers(tmp_path, monkeypatch):
    """BDD: concurrent round workers never crash on a shared temp file."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    path = tmp_path / "shared.json"
    errors: list[Exception] = []

    def writer(worker: int) -> None:
        try:
            for index in range(25):
                loop._save_json(path, {"worker": worker, "index": index})
        except Exception as exc:  # noqa: BLE001 - collected and asserted
            errors.append(exc)

    threads = [threading.Thread(target=writer, args=(n,)) for n in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)
    assert not errors
    assert path.exists()
    assert loop._load_json(path, {})["worker"] in range(4)
    leftovers = [p.name for p in tmp_path.iterdir() if p.name.endswith(".tmp")]
    assert leftovers == []
