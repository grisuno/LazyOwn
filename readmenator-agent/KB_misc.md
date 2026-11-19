# Subsystem: misc

## .claude/skills/run-lazyown/driver.sh
- Doc: Build and drive LazyOwn inside its Docker sandbox (Debian container).
- Layer: infrastructure
- Language: sh

## deploy/range/ad-mini/traffic-gen.py
- Doc: Fake network traffic generator for the AD mini range.
- Layer: utility
- Language: py
- Symbols:
  - `_probe` (function, line 21) `def _probe(host, port)`
  - `main` (function, line 35) `def main()`

## external/install_external.sh
- Doc: Nombre del script: download_resources.sh Autor: Gris Iscomeback Correo electrónico...
- Layer: utility
- Language: sh
- Symbols:
  - `download` (function, line 18)
  - `ctrl_c` (function, line 13)

## gyms/docker/php2shell/www/index.php
- Layer: utility
- Language: php

## modules/legacy/__init__.py
- Doc: Backward-compatibility shims for deprecated scripts.
- Layer: utility
- Language: py

## modules/scripts/clean_history.sh.sh
- Layer: utility
- Language: sh

## source/conf.py
- Doc: Configuration file for the Sphinx documentation builder.
- Layer: utility
- Language: py

## static/hexabot/hexabot-spinner.js
- Layer: utility
- Language: js
- Symbols:
  - `radialTexture` (function, line 209)
  - `createHexabotSpinner` (function, line 223)
  - `rand` (function, line 46)
  - `clamp` (function, line 47)
  - `setHappy` (function, line 365)
  - `ndc` (function, line 371)
  - `now` (function, line 375)
  - `onDown` (function, line 377)
  - `onMove` (function, line 395)
  - `onUp` (function, line 407)
  - `resize` (function, line 423)
  - `loop` (function, line 439)
  - `Terminal` (class, line 49)
  - `constructor` (method, line 50)
  - `push` (method, line 84)
  - `log` (method, line 92)
  - `run` (method, line 94)
  - `setProgress` (method, line 96)
  - `startCommand` (method, line 102)
  - `update` (method, line 107)
  - `colorFor` (method, line 139)
  - `drawPrompt` (method, line 146)
  - `draw` (method, line 152)
  - `dispose` (method, line 206)
- Depends on: `cli/assign.py`, `core/prompt.py`, `poc_tui/run.py`
