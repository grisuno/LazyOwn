"""Loops blueprint — autonomous loop control API for the dashboard.

Owns the whole ``/api/loops`` surface: starting an ``auto_loop`` or a
``lazynmap`` scan as an isolated subprocess, listing every loop, reading
one loop's output log and stopping a loop. This is one responsibility
sliced out of the former ``lazyc2.py`` god object; the loop manager
singleton and validation helpers come from :mod:`modules.loop_manager`
so the CLI and the dashboard share the same contract.

The blueprint is wired lazily through :func:`init_loops_bp`, which binds
the main application's auth, CSRF and rate-limiter decorators after that
module has finished loading, avoiding a circular import at module load.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from modules.loop_manager import (
    DEFAULT_ROUNDS,
    DEFAULT_WORKERS,
    KIND_AUTO_LOOP,
    KIND_LAZY_NMAP,
    MAX_ROUNDS,
    MAX_TIMEOUT_SECONDS,
    MAX_WORKERS,
    LoopManager,
    LoopNotFoundError,
    LoopSpec,
    LoopValidationError,
)
from modules.loop_manager import (
    clamp_float as _loop_clamp_float,
)
from modules.loop_manager import (
    clamp_int as _loop_clamp_int,
)
from modules.loop_manager import (
    sanitize_goal as _loop_sanitize_goal,
)
from modules.loop_manager import (
    validate_target as _loop_validate_target,
)

from modules.loop_manager import (
    default_manager,
)

loops_bp = Blueprint("loops", __name__)

_loop_manager = default_manager()


def _generic_loop_error():
    """Return the generic JSON error used for internal loop failures.

    Returns:
        Tuple of (payload, status) hiding internal details from clients.
    """
    return jsonify({"error": "loop request failed"}), 500


def _loops_start():
    """Start one autonomous loop subprocess from the dashboard.

    The request body must be a JSON object with a ``kind`` of either
    ``auto_loop`` or ``lazynmap``, a valid IP ``target`` and, for
    ``auto_loop``, optional ``goal``/``rounds``/``workers``/``timeout``
    knobs. Every field is validated by :mod:`modules.loop_manager`
    before a subprocess is spawned; failures answer with a generic
    error that never leaks internals.
    """
    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request body"}), 400
        kind = data.get("kind")
        if kind not in (KIND_AUTO_LOOP, KIND_LAZY_NMAP):
            return jsonify({"error": "kind must be auto_loop or lazynmap"}), 400
        try:
            spec = LoopSpec(
                kind=str(kind),
                target=_loop_validate_target(data.get("target")),
                goal=_loop_sanitize_goal(data.get("goal")) if kind == KIND_AUTO_LOOP else "",
                rounds=_loop_clamp_int(
                    data.get("rounds", DEFAULT_ROUNDS), "rounds", DEFAULT_ROUNDS, 1, MAX_ROUNDS
                ),
                workers=_loop_clamp_int(
                    data.get("workers", DEFAULT_WORKERS), "workers", DEFAULT_WORKERS, 1, MAX_WORKERS
                ),
                timeout=_loop_clamp_float(
                    data.get("timeout", 0), "timeout", 0.0, 0.0, MAX_TIMEOUT_SECONDS
                ),
            )
            from flask_login import current_user

            operator = str(getattr(current_user, "username", "") or "")
            record = _loop_manager.start(spec, operator=operator)
        except LoopValidationError as err:
            detail = str(err)
            return jsonify({"error": detail, "field": err.field}), 400
        except OSError:
            import logging

            logging.getLogger("loops").exception("loop spawn failed")
            return _generic_loop_error()
        return jsonify(record), 201
    except Exception:
        import logging

        logging.getLogger("loops").exception("loops_start failed")
        return _generic_loop_error()


def _loops_list():
    """List every autonomous loop with refreshed live status."""
    try:
        return jsonify({"loops": _loop_manager.list_loops()}), 200
    except Exception:
        return _generic_loop_error()


def _loop_log(loop_id):
    """Return one chunk of a loop's output log.

    Args:
        loop_id: Hex loop identifier from the URL.
    """
    try:
        offset = request.args.get("offset", 0)
        return jsonify(_loop_manager.read_log(loop_id, offset)), 200
    except LoopNotFoundError:
        return jsonify({"error": "loop not found"}), 404
    except LoopValidationError as err:
        detail = str(err)
        return jsonify({"error": detail}), 400
    except Exception:
        return _generic_loop_error()


def _loop_stop(loop_id):
    """Stop one running loop by terminating its process group.

    Args:
        loop_id: Hex loop identifier from the URL.
    """
    try:
        return jsonify(_loop_manager.stop(loop_id)), 200
    except LoopNotFoundError:
        return jsonify({"error": "loop not found"}), 404
    except LoopValidationError as err:
        detail = str(err)
        return jsonify({"error": detail}), 409
    except Exception:
        return _generic_loop_error()


def _default_guard(view, needs_csrf: bool):
    """Default guard: operator session required, no CSRF policy bound.

    Args:
        view: The plain view function.
        needs_csrf: Unused by the default guard (kept for signature parity).

    Returns:
        The wrapped view.
    """
    from flask_login import current_user

    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "operator session required"}), 401
        return view(*args, **kwargs)

    wrapper.__name__ = view.__name__
    return wrapper


def init_loops_bp(limiter=None, guard=None) -> None:
    """Bind the loop routes with the host application's guard decorators.

    Args:
        limiter: The application rate limiter; when provided each route
            is decorated with the same limits the former god object used.
        guard: Callable ``(view, needs_csrf) -> view`` wrapping each route
            with auth (and CSRF when ``needs_csrf``). Defaults to a
            strict operator-session guard when the host application does
            not inject one.
    """
    from flask import current_app

    if guard is None:
        guard = _default_guard

    def _limited(view, limit_string: str):
        if limiter is None:
            return view
        return limiter.limit(limit_string)(view)

    loops_bp.add_url_rule(
        "/api/loops",
        endpoint="loops_start",
        view_func=guard(_limited(_loops_start, "10 per minute"), True),
        methods=["POST"],
    )
    loops_bp.add_url_rule(
        "/api/loops",
        endpoint="loops_list",
        view_func=guard(_limited(_loops_list, "120 per minute"), False),
        methods=["GET"],
    )
    loops_bp.add_url_rule(
        "/api/loops/<loop_id>/log",
        endpoint="loop_log",
        view_func=guard(_limited(_loop_log, "300 per minute"), False),
        methods=["GET"],
    )
    loops_bp.add_url_rule(
        "/api/loops/<loop_id>/stop",
        endpoint="loop_stop",
        view_func=guard(_limited(_loop_stop, "30 per minute"), True),
        methods=["POST"],
    )
    try:
        current_app.logger.debug("loops blueprint bound")
    except RuntimeError:
        pass


__all__ = ["init_loops_bp", "loops_bp"]
