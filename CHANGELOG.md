# Changelog

### Features

  * feat: one-liner installer, wiki publisher, slim README, profiles, tiers, API v1 (f4d63988) by grisun0
  * feat(adoption): viral README with 7 demo GIFs, onboarding smoke, drift CI (c1997ae3) by grisun0
  * feat(security): ban os.system, harden CI gates, close mypy gaps (fb6eb41d) by grisun0
  * feat(quality): add SDD/TDD/BDD gates, consumer docs, portability fixes (f2a3383f) by grisun0
  * feat(purple): add purple team closed loop with Sigma detection (18cd1129) by grisun0

### Bug Fixes

  * fix(tests): platform marker aware lock comparison (f888cc85) by grisun0
  * fix(tests): skill keys, medusa trigger, DNS regex, sentinel quotes, prompt flake, docker arm64 (c3c2cac1) by grisun0
  * fix(deps): declare textual+defusedxml, lock-based CI test env (1e16586f) by grisun0
  * fix: trailing comma in payload.example.json (bbf7234b) by grisun0
  * fix(tests): schema/validator/addon/packaging contract gaps (7e6f6c15) by grisun0
  * fix(ci): palette template quotes + mypy hook types-Markdown (5e7cf5ef) by grisun0
  * fix(ci): parsers typing, palette quote style, mypy hook env (c46e031b) by grisun0
  * fix(ci): stale wiring asserts + k8s yaml exclude (098dc2f8) by grisun0
  * fix(ci): pre-commit last mile (eof/yaml/mypy) + stale assign asserts (e75589f5) by grisun0
  * fix(ci): full-repo ruff clean, working pre-commit excludes, migrated test asserts (1c67bf4a) by grisun0
  * fix(ci): CLAUDE.md size budget + audit lock files (5e37eb83) by grisun0
  * fix(ci): test count doc + pip-audit editable skip (0ee4f565) by grisun0
  * fix(deps): resolve install conflicts blocking CI/tests/docker (7cbd7cfa) by grisun0
  * fix(py311): same-quote nested f-strings break 3.10/3.11 runtimes (15f15364) by grisun0
  * fix(ci): unbreak all main workflows (ruff scope+pin, test deps, audit, contract, docker) (45be9c60) by grisun0
  * fix(sandbox): make Dockerfile.sandbox build successfully (ae762cc0) by dzllopes
  * fix(prompt): remove the bracket-replace prompt hack in rhost/rrhost (660d620a) by grisun0
  * fix(prompt): refresh the Neon Box prompt after assign and banner changes (f4ec4ee8) by grisun0
  * fix(commands): repair eight @with_argparser commands and add a full audit (b808f7b4) by grisun0
  * fix(shell): restore shell semantics and colored output in generic runners (da50e0a9) by grisun0
  * fix(journal): send Int GraphQL variables with the typed flag (e4d6d7b6) by grisun0
  * fix(c2): require auth on operator dashboard and data endpoints (49e7fa46) by grisun0
  * fix(fastrun): dispatch commands via -c and stop log-file spam (f6aaf6bb) by grisun0
  * fix(killchain): revert heavy WorldModel construction in current_phase (177a7c19) by grisun0
  * fix(tests): resolve pre-existing test failures and lint debt (b2b92ed2) by grisun0

### Documentation

  * docs: regenerate COMMANDS.md UTILS.md COMMANDS.html after migrated fixes (8900b631) by grisun0
  * docs(skill): add run-lazyown skill (build + drive the sandbox) (c43c7816) by dzllopes

### Chores

  * a brand new deply.sh (146a5257) by grisun0
  * security fixes (6d143fab) by grisun0
  * security fixes (8783c87c) by grisun0
  * improvements in the autonomous loop (43ddc4b8) by grisun0
  * doc compressed (a7f47dc8) by grisun0
  * Update README.md (85c67d28) by Grisuno
  * new loop autonomous (205f2981) by grisun0
  * Merge pull request #308 from grisuno/dependabot/pip/ruff-0.16.10 (628e9596) by Grisuno
  * Merge pull request #309 from grisuno/dependabot/pip/unicorn-2.1.4 (fe1ebf41) by Grisuno
  * Merge pull request #311 from grisuno/dependabot/pip/nvidia-cuda-cupti-13.4.92 (2e642fd5) by Grisuno
  * Merge pull request #310 from grisuno/dependabot/pip/argon2-cffi-bindings-26.1.0 (9b005e1e) by Grisuno
  * Merge pull request #312 from grisuno/dependabot/pip/asttokens-3.0.2 (d28e5a27) by Grisuno
  * chore(deps): bump asttokens from 3.0.1 to 3.0.2 (df68ee5a) by dependabot[bot]
  * chore(deps): bump nvidia-cuda-cupti from 13.0.85 to 13.4.92 (bfee6d97) by dependabot[bot]
  * chore(deps): bump argon2-cffi-bindings from 25.1.0 to 26.1.0 (764a758b) by dependabot[bot]
  * chore(deps): bump unicorn from 2.1.2 to 2.1.4 (eaf2c7c6) by dependabot[bot]
  * chore(deps-dev): bump ruff from 0.16.8 to 0.16.10 (2a7ac4fd) by dependabot[bot]
  * test doc deply infered path (c3388686) by grisun0
  * test doc deply infered path (c9f10756) by grisun0
  * test doc (b56baeef) by grisun0
  * doc and refactoring (a922d093) by grisun0
  * 3d awesome vieew in doc sphere in attack and intel new endpoints to lazyown (269ed777) by grisun0
  * 3d awesome vieew in doc (1447b977) by grisun0
  * chore(security): refresh secrets baseline + scope detect hook (5a878aef) by grisun0
  * sqlite ve poc in debian bookworm (49a844d9) by grisun0
  * new addons to re ;D (16133c93) by grisun0
  * cairn talos more nuclei templates, god eye view reing reaper new skills and much much more love (bc6fc033) by grisun0
  * security fix in docs/index.html statics (9eff3f34) by grisun0
  * security fix / docs (9c2fbbbc) by grisun0
  * security fix (5529c6a6) by grisun0
  * Merge pull request #307 from grisuno/dependabot/pip/mako-1.4.2 (1cbc5446) by Grisuno
  * chore(deps): bump mako from 1.3.12 to 1.4.2 (76eb0bb9) by dependabot[bot]
  * new index :D fix (acf88c80) by grisun0
  * Create static.yml (25fd5ad0) by Grisuno
  * new index :D (fb9dd43c) by grisun0
  * new index :D (19ddb33d) by grisun0
  * new documentation :D (f0e78f0b) by grisun0
  * new documentation :D (72e50545) by grisun0
  * new documentation :D (5fbbe639) by grisun0
  * new yara rule (a68dbb08) by grisun0
  * 3 zero days to mysql, bad day to be oracle lover (2bf4531f) by grisun0
  * update demo, commands chain with ampersand, and some improvements (a8eff8fb) by grisun0
  * Merge pull request #304 from dzllopes/fix/sandbox-build-and-skill (5b659ed3) by Grisuno
  * ghidra mcp and brand new documentation (935426bf) by grisun0
  * chore: add lazyown.cmd Windows launcher for the Docker sandbox (7ff1989c) by dzllopes
  * Update README.md (45c4a670) by Grisuno
  * minios (ce967b81) by grisun0
  * Update README.md (5aee1102) by Grisuno
  * Update README.md (32f69c93) by Grisuno
  * Update README.md (8e8c3b7a) by Grisuno
  * ghidra mcp (6557f104) by grisun0
  * some dead imports, two lazyaddons news, two skills news, love to mcp, now we can reverse engeniering anyding with rea :D with love (9c871fec) by grisun0
  * Merge pull request #301 from grisuno/dependabot/pip/typing-inspection-0.4.4 (67d73f95) by Grisuno
  * Merge pull request #302 from grisuno/dependabot/pip/torchvision-0.29.1 (21a7d035) by Grisuno
  * Merge pull request #300 from grisuno/dependabot/pip/cssselect-1.5.0 (f87f3365) by Grisuno
  * Merge pull request #299 from grisuno/dependabot/pip/werkzeug-3.1.9 (142e6817) by Grisuno
  * Merge pull request #298 from grisuno/dependabot/pip/charset-normalizer-3.5.2 (48a04bd4) by Grisuno
  * chore(deps): bump torchvision from 0.27.1 to 0.29.1 (f3b943a1) by dependabot[bot]
  * chore(deps): bump typing-inspection from 0.4.2 to 0.4.4 (2b8541b5) by dependabot[bot]
  * chore(deps): bump cssselect from 1.4.0 to 1.5.0 (3e738d9a) by dependabot[bot]
  * chore(deps): bump werkzeug from 3.1.8 to 3.1.9 (3cf97096) by dependabot[bot]
  * chore(deps): bump charset-normalizer from 3.5.1 to 3.5.2 (9c1ac445) by dependabot[bot]
  * Merge pull request #297 from grisuno/dependabot/pip/virtualenv-21.7.13 (f18a0799) by Grisuno
  * chore(deps): bump virtualenv from 21.3.1 to 21.7.13 (e9887d5d) by dependabot[bot]
  * Merge pull request #296 from grisuno/dependabot/pip/pypdf-6.19.0 (2f77a5ee) by Grisuno
  * chore(deps): bump pypdf from 6.18.0 to 6.19.0 (10b08f2a) by dependabot[bot]
  * new bootstrap testing (27b6d48b) by grisun0
  * bootstrap (cc4b7992) by grisun0
  * spinner (ba9186c5) by grisun0
  * Update README.md (a62a1dcb) by Grisuno
  * doc (3fcf36ee) by grisun0
  * disposable infra, new ranger gym, disposable redirectors, golang updated (92cb1dd6) by grisun0
  * Merge pull request #291 from grisuno/dependabot/pip/nvidia-cufft-12.4.0.43 (a54094e8) by Grisuno
  * Merge pull request #292 from grisuno/dependabot/pip/fsspec-2026.9.0 (11d8579b) by Grisuno
  * Merge pull request #293 from grisuno/dependabot/pip/certifi-2026.7.22 (b5e794c8) by Grisuno
  * Merge pull request #294 from grisuno/dependabot/pip/joblib-1.6.0 (47dd355d) by Grisuno
  * Merge pull request #295 from grisuno/dependabot/pip/urllib3-2.8.0 (282d6483) by Grisuno
  * chore(deps): bump urllib3 from 2.7.0 to 2.8.0 (9adc7c45) by dependabot[bot]
  * chore(deps): bump joblib from 1.5.3 to 1.6.0 (e9ed6228) by dependabot[bot]
  * chore(deps): bump certifi from 2026.6.17 to 2026.7.22 (7af2db39) by dependabot[bot]
  * chore(deps): bump fsspec from 2026.4.0 to 2026.9.0 (6ebeb00c) by dependabot[bot]
  * chore(deps): bump nvidia-cufft from 12.0.0.61 to 12.4.0.43 (f9b14e7f) by dependabot[bot]
  * Dashboard with command execution ;) (963b199f) by grisun0
  * refactoring and delete dead code (c7de2b95) by grisun0
  * Merge pull request #286 from grisuno/dependabot/pip/cuda-toolkit-13.4.2 (023a3510) by Grisuno
  * Merge pull request #287 from grisuno/dependabot/pip/plumbum-2.0.2 (74e4020b) by Grisuno
  * Merge pull request #288 from grisuno/dependabot/pip/pydantic-2.13.5 (be721a9f) by Grisuno
  * Merge pull request #289 from grisuno/dependabot/pip/unicorn-2.1.4 (e154b364) by Grisuno
  * Merge pull request #290 from grisuno/dependabot/pip/python-engineio-4.14.0 (3eea7ff7) by Grisuno
  * chore(deps): bump python-engineio from 4.13.3 to 4.14.0 (6b01654b) by dependabot[bot]
  * chore(deps): bump unicorn from 2.1.2 to 2.1.4 (8ec00a23) by dependabot[bot]
  * chore(deps): bump pydantic from 2.13.3 to 2.13.5 (bd6f9311) by dependabot[bot]
  * chore(deps): bump plumbum from 1.10.0 to 2.0.2 (9fb7cd2c) by dependabot[bot]
  * chore(deps): bump cuda-toolkit from 13.0.2 to 13.4.2 (b3b0a056) by dependabot[bot]
  * moving some stufs to minifs (e8e8f686) by grisun0
  * love in documentation, gifs, refactoring, bug fixing, love (94b192b8) by grisun0
  * Merge pull request #284 from grisuno/dependabot/pip/soupsieve-2.9 (308fbd6a) by Grisuno
  * chore(deps): bump soupsieve from 2.8.4 to 2.9 (28500f70) by dependabot[bot]
  * refactoring (df5ffb2b) by grisun0
  * Merge pull request #275 from grisuno/dependabot/pip/torch-2.14.0 (3859dbfb) by Grisuno
  * Merge pull request #276 from grisuno/dependabot/pip/pypdf-6.18.0 (5a57a09b) by Grisuno
  * Merge pull request #277 from grisuno/dependabot/pip/python-discovery-1.6.0 (f9fb0fc0) by Grisuno
  * Merge pull request #278 from grisuno/dependabot/pip/nvidia-cuda-nvrtc-13.4.59 (f801e88d) by Grisuno
  * Merge pull request #279 from grisuno/dependabot/pip/pyopenssl-26.4.0 (7b0cb680) by Grisuno
  * chore(deps): bump pyopenssl from 26.3.0 to 26.4.0 (dd778561) by dependabot[bot]
  * chore(deps): bump nvidia-cuda-nvrtc from 13.0.88 to 13.4.59 (cdf7c28c) by dependabot[bot]
  * chore(deps): bump python-discovery from 1.3.0 to 1.6.0 (ca8fc409) by dependabot[bot]
  * chore(deps): bump pypdf from 6.16.1 to 6.18.0 (2732a046) by dependabot[bot]
  * chore(deps): bump torch from 2.13.0 to 2.14.0 (02cf96f3) by dependabot[bot]
  * hardening (622a05fd) by grisun0
  * ShieldCrash ShieldBreak CVE-2026-69414 demonstrates an arbitrary file read as SYSTEM with September 2026, all supported windows versions are affected. (6fe0bd91) by grisun0
  * linter errors fixed (31e3b48b) by grisun0
  * prompt bug fixing (8d871dcb) by grisun0
  * - CI (ci.yml): nuevos jobs hygiene (top_tier_check.py + sync --check) y sbom (genera y sube el artefacto por build). - scripts/generate_sbom.py nuevo: CycloneDX 1.5 sin dependencias ni red, 250 componentes desde requirements.txt. (3acd9277) by grisun0
  * doc (6a8117ce) by grisun0
  * - core/validators.py: check_rhost/check_lhost ya no aceptan ;;; o 8.8.8.8;id — rechazan shell-metachars y validan IP/hostname/CIDR. check_lport ahora valida rango 1-65535 vía check_port. - cli/assign.py: fail-closed ante inyección — valores con ;|& etc. se rechazan y no persisten. Formato inválido no-inyectable sigue lenient para no romper contrato (tests en verde). (1e072fc9) by grisun0
  * Merge pull request #259 from grisuno/dependabot/pip/matplotlib-inline-0.2.2 (be176fbc) by Grisuno
  * Merge pull request #260 from grisuno/dependabot/pip/ua-parser-builtins-202606 (dec5b091) by Grisuno
  * Merge pull request #261 from grisuno/dependabot/pip/pykeepass-4.2.0 (cefadfb2) by Grisuno
  * Merge pull request #262 from grisuno/dependabot/pip/anyio-4.15.0 (b6d1e979) by Grisuno
  * chore(deps): bump pykeepass from 4.1.1.post1 to 4.2.0 (9e8452bd) by dependabot[bot]
  * Merge pull request #263 from grisuno/dependabot/pip/pygments-2.21.0 (e43f2d0e) by Grisuno
  * Doc(auto) KNOWLEADGE_BASE.md README.md and agentic documentation (8fe2f472) by grisun0
  * llm provider unified (b1a6fe1a) by grisun0
  * chore(deps): bump pygments from 2.20.0 to 2.21.0 (311931d3) by dependabot[bot]
  * chore(deps): bump anyio from 4.14.2 to 4.15.0 (7bd8f400) by dependabot[bot]
  * chore(deps): bump ua-parser-builtins from 202603 to 202606 (4282c2a2) by dependabot[bot]
  * chore(deps): bump matplotlib-inline from 0.2.1 to 0.2.2 (2d5443c6) by dependabot[bot]
  * Refactoring llm, bug fixing in params, scorer refactored (d582d76d) by grisun0
  * hardening and refactoring (fa8e63df) by grisun0
  * PrettyPrague GenDigital Avast Antivirus ZeroDay Elevation of Privileges Vulnerability (777c8a19) by grisun0
  * Merge pull request #253 from grisuno/dependabot/pip/anyio-4.14.2 (6ec90df5) by Grisuno
  * Merge pull request #254 from grisuno/dependabot/pip/platformdirs-4.11.4 (a303f039) by Grisuno
  * Merge pull request #255 from grisuno/dependabot/pip/nvidia-cufile-1.18.1.6 (e4d8e0ba) by Grisuno
  * Merge pull request #256 from grisuno/dependabot/pip/networkx-gte-3.4.2 (164d8b6c) by Grisuno
  * Merge pull request #257 from grisuno/dependabot/pip/tinydb-4.9.0 (b1c3900d) by Grisuno
  * chore(deps): bump tinydb from 4.8.2 to 4.9.0 (b4f80122) by dependabot[bot]
  * chore(deps): update networkx requirement from >=3.0 to >=3.4.2 (4b2b285f) by dependabot[bot]
  * chore(deps): bump nvidia-cufile from 1.15.1.6 to 1.18.1.6 (1d677010) by dependabot[bot]
  * chore(deps): bump platformdirs from 4.9.6 to 4.11.4 (18c4b8c2) by dependabot[bot]
  * chore(deps): bump anyio from 4.13.0 to 4.14.2 (77d88af5) by dependabot[bot]
  * more hardening (e30735e5) by grisun0
  * more hardening (6489af6a) by grisun0
  * documentation :D (e124abe5) by grisun0
  * more hardining with love (9e55a8e0) by grisun0
  * hardening 3 (35f1e13a) by grisun0
  * hardening 2 (1838affc) by grisun0
  * hardening (44699c04) by grisun0
  * hardening in lazyown ;) with love (c6a223f3) by grisun0
  * a new TUI is a poc but maybe is the new CLI (a5d7c3e7) by grisun0
  * new commands and tutorials for newviews (e29c8d11) by grisun0
  * new commands and tutorials for newviews (ba3c2e01) by grisun0
  * some order in suggestions (6b38b3ed) by grisun0
  * Merge pull request #245 from grisuno/dependabot/pip/charset-normalizer-3.5.1 (436be201) by Grisuno
  * Merge pull request #246 from grisuno/dependabot/pip/pypdf-6.16.1 (732646b8) by Grisuno
  * Merge pull request #247 from grisuno/dependabot/pip/cyclonedx-python-lib-11.12.0 (11defe8a) by Grisuno
  * Merge pull request #248 from grisuno/dependabot/pip/argcomplete-3.7.2 (281630ea) by Grisuno
  * Merge pull request #249 from grisuno/dependabot/pip/jsonpickle-4.1.2 (350bfec4) by Grisuno
  * chore(deps): bump jsonpickle from 4.1.1 to 4.1.2 (c5b1f6ab) by dependabot[bot]
  * chore(deps): bump argcomplete from 3.7.0 to 3.7.2 (ef9eacf4) by dependabot[bot]
  * chore(deps): bump cyclonedx-python-lib from 11.7.0 to 11.12.0 (0f87ed8b) by dependabot[bot]
  * chore(deps): bump pypdf from 6.15.0 to 6.16.1 (ab79e791) by dependabot[bot]
  * chore(deps): bump charset-normalizer from 3.4.7 to 3.5.1 (2db1cff5) by dependabot[bot]


_Generated by [deploynator](https://github.com/grisuno/deploynator)_