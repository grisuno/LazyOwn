# banners/

Splash artwork shown by the LazyOwn shell on startup. Selected at
random by `banner.py` unless the operator passes `./run --no-banner`.

## Files

PNG artwork referenced by `banner.py`. Add new banners by dropping a
PNG into this directory; the loader picks them up on next startup.

## Conventions

- Image-only — no ASCII art here (those live in `source/` and inside `banner.py`).
- Keep each file under 1 MB; the shell loads one at every launch.
- Do not commit operator-identifiable artwork (real screenshots, logos of real targets).
