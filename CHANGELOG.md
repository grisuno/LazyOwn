# Changelog

All notable changes to the LazyOwn RedTeam Framework are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.2.158] — vie 31 jul 2026

### Added

- new marketplace, auto_pwn, suggesters, yara rules, hunt, etc etc etc a lot of love

### Changed

- lazyreports and kill-chains :D
- watchdog
- marketplace
- blueprint in lazyc2
- login to cli
- karma, elo, gamified labs, so much love
- evento log
- applocker
- deleted dead code
- campaign and colab :D
- marketplace commands and labs commands
- install.sh siembra payload.json, documentation, mcp and love in install script

### Fixed

- banners and reports endpoints fixed

## [0.2.157] — mié 29 jul 2026

### Added

- Merge branch 'main' into feature/operator-ux-boost
- new dashboard topoloogy and exploit suggester
- new command chain :D
- new command hunt :D
- docs: add app API reference to plugins README
- test: add MCP smoke test (10 checks) + add mcp dep to pyproject.toml
- docs: add API reference page from openapi.yaml
- chore: update secrets baseline + add profiles README

### Changed

- unified dashboard
- unified dashboard, and some love
- steel migrating the monolithic
- Merge pull request #201 from grisuno/dependabot/pip/tqdm-4.69.1
- Merge pull request #202 from grisuno/dependabot/pip/argcomplete-3.7.0
- Merge pull request #203 from grisuno/dependabot/pip/pyelftools-0.33
- Merge pull request #204 from grisuno/dependabot/pip/cffi-2.1.0
- Merge pull request #205 from grisuno/dependabot/pip/pyarrow-25.0.0
- good by monolothic :D
- bump pyarrow from 24.0.0 to 25.0.0
- bump cffi from 2.0.0 to 2.1.0
- bump pyelftools from 0.32 to 0.33
- bump argcomplete from 3.6.3 to 3.7.0
- bump tqdm from 4.67.3 to 4.69.1
- auto_pwn
- some leetcode, better lining, refactoring, etc
- leetcode
- now we got YARA Rules :D
- Merge pull request #200 from grisuno/dependabot/pip/setuptools-83.0.0
- bump setuptools from 81.0.0 to 83.0.0
- Merge pull request #199 from grisuno/dependabot/pip/pyasn1-0.6.4
- bump pyasn1 from 0.6.3 to 0.6.4
- Merge pull request #198 from grisuno/dependabot/pip/pillow-12.3.0
- bump pillow from 12.2.0 to 12.3.0
- Merge pull request #197 from grisuno/dependabot/pip/torch-2.13.0
- bump torch from 2.12.1 to 2.13.0
- Merge pull request #193 from grisuno/dependabot/pip/python-engineio-4.13.3
- Merge pull request #194 from grisuno/dependabot/pip/triton-3.7.1
- Merge pull request #192 from grisuno/dependabot/pip/cuda-bindings-13.3.1
- Merge pull request #191 from grisuno/dependabot/pip/nvidia-nvtx-13.3.29
- Merge pull request #195 from grisuno/dependabot/pip/certifi-2026.6.17
- perf: defer heavy imports from module-level to __init__ time
- refactor: partial wildcard -> explicit import (reverted, too many deps)
- refactor: consolidate sys.path.insert patterns across modules/skills
- refactor: replace from utils import * with explicit imports (66 symbols)
- docs: truncate README.md from 20k to 2.1k lines
- chore: clean creds, changelog, and coverage threshold

### Security

- security bug fixing, and much much love

### Fixed

- some bug fixing
- modules/lazycloud.py — Cloud Attack Module (AWS, Azure, GCP), modules/lazyk8s.py — Container & Kubernetes Attack Module, and some bg fixing
- style: auto-fix 281 ruff issues in core/ and cli/

## [0.2.156] — dom 12 jul 2026

### Added

- Doc(creation documentation) a brand new KNOWLEDGE_BASE.md

### Changed

- multinenant, extended params, cloud native attacks, junescape and much much love more
- headless :D

### Fixed

- cloud boost with grype prowler trivy scoutsuite cloudsploit stratus, a brand new params extender yaml awesome, pipelines, profiles, some bugfixing, and much much more

## [0.2.155] — sáb 11 jul 2026

### Added

- Doc(creation documentation) a brand new KNOWLEDGE_BASE.md
- Doc(creation documentation) a brand new KNOWLEDGE_BASE.md

### Changed

- Multitentant, MFA, TOTP Generator, Multiusers, Colab and much much more
- Update README.md

## [0.2.154] — jue 09 jul 2026

### Added

- new skills, test, and new pytorch backdoor :D
- new rookit io_uring is a poc
- a brand new c keylogger :D
- add pompem in ss pipeline

### Changed

- docker
- shadow read the shadow file without trace
- windows sdk headers
- Update README.md
- junuscape :O
- Merge pull request #163 from grisuno/dependabot/pip/python-engineio-4.13.2
- bump python-engineio from 4.13.1 to 4.13.2
- Merge pull request #162 from grisuno/dependabot/pip/python-socketio-5.16.2
- bump python-socketio from 5.16.1 to 5.16.2
- updating lazyown.py do_form duplicated
- clean history command: clean_local_history
- thanks you very much to EQSTLab to provide the advisory :D thanks you bro changelog updated
- some warnings urlib deleted :D
- some love now we support curlfree command :D
- some love now we support mcp to opencode
- some love, aes_key in payload.json and some love to c2
- some tests of integration FreeDom in lazyown
- update deepseek prompts wink wink
- update prompts wink wink
- Estorides comes to LazyOwn RedTeam to Reconnaissance like a nation state level

### Security

- vulns-2026-fatfs-chance
- some security advisory patched thanks you very much to EQSTLab to provide the advisory :D thanks you bro

### Fixed

- hotfix in dockerfile, docker compose, docker sccript to build image, and more love :D
- hotfixing
- bug fixing

## [0.2.152] — mar 16 jun 2026

### Changed

- test pipe line deply
- Merge branch 'pp' into dev
- Merge branch 'docs/engage-fastpath' into dev
- Merge branch 'chore/cli-print-hygiene' into dev
- surface the engage one-command fast-path
- print hygiene + remove C2 credential leak in lazyown.py

## [0.2.151] — mar 09 jun 2026

### Added

- some love to the code, no features news, but refactor

### Changed

- updating main
- in recon command ss now work propertly

## [0.2.149] — dom 07 jun 2026

### Changed

- update pp

### Security

- some love to security issues

## [0.2.148] — sáb 06 jun 2026

### Changed

- some improvements in the code and graphify
- update dev
- refresh self-knowledge graph (AST update)
- suggest next commands

## [0.2.147] — mar 02 jun 2026

### Changed

- Stream de razonamiento del daemon

## [0.2.146] — mar 02 jun 2026

### Fixed

- ruff fix

## [0.2.145] — lun 01 jun 2026

### Changed

- some love to modularization

## [0.2.143] — mié 27 may 2026

### Added

- new l00t commands

## [0.2.141] — lun 25 may 2026

### Added

- new docs
- docs: add branching strategy (dev/pp/main) to CLAUDE.md, AGENTS.md, CONTRIBUTING.md, SKILL.md
- docs: translate all Spanish docstrings/UI to English, sync MCP tool count to 131, add phase guides
- feat: add Hermes-native MCP integration layer (hermes-lazyown)
- feat(themes to popups :D): with love

### Changed

- Create dependabot.yml

### Fixed

- fix: regenerate COMMANDS.md/UTILS.md, fix utils.py banner, translate remaining Spanish comments

## [0.2.139] — dom 24 may 2026

### Added

- new graphos

### Changed

- refactor(better contract in payload.json): better wizard --tutorial

## [0.2.138] — vie 22 may 2026

### Added

- some new feats

### Changed

- Batch A: migrate 22 do_* methods to phase-scoped CommandSets + Hermes-friendly docs

## [0.2.135] — jue 21 may 2026

### Changed

- refactor(refactor in tools): all green now

## [0.2.134] — jue 21 may 2026

### Changed

- refactor(some refactors in wizards): with love
- binding ips

## [0.2.132] — mié 20 may 2026

### Changed

- surface

### Security

- and security issues

## [0.2.131] — mar 19 may 2026

### Changed

- suggested commands

## [0.2.130] — mar 19 may 2026

### Added

- lazyaddons

## [0.2.129] — dom 17 may 2026

### Added

- new exploit

## [0.2.128] — dom 17 may 2026

### Added

- new orquestator

## [0.2.127] — dom 17 may 2026

### Changed

- pipeline

## [0.2.126] — sáb 16 may 2026

### Security

- fix(security bug fixing in lazybrp): with love

## [0.2.125] — sáb 16 may 2026

### Security

- security issues fixed

## [0.2.124] — sáb 16 may 2026

### Security

- security fixes

## [0.2.123] — sáb 16 may 2026

### Fixed

- bug fixing

## [0.2.122] — sáb 16 may 2026

### Security

- new features and security updates

## [0.2.120] — vie 15 may 2026

### Changed

- update CLAUDE.md with session learnings

## [0.2.119] — vie 15 may 2026

### Added

- add README to every project directory

## [0.2.118] — vie 15 may 2026

### Changed

- CLAUDE.md update with beacon family, collab, and onboarding
- gap2 team server UI and gap3 onboarding quickstart

## [0.2.117] — vie 15 may 2026

### Added

- blacksandbeacon Linux BOF addon

## [0.2.116] — jue 14 may 2026

### Changed

- some wizzards and some suggester

## [0.2.115] — jue 14 may 2026

### Changed

- recomended commands and some love

## [0.2.114] — mié 13 may 2026

### Changed

- some playbooks

## [0.2.113] — mié 13 may 2026

### Added

- new feature sandbox dockerized run and some other love

## [0.2.112] — mar 12 may 2026

### Added

- feature(features news): with love

## [0.2.111] — mar 12 may 2026

### Added

- new wizard and some refactor in LazyAddons

## [0.2.110] — lun 11 may 2026

### Changed

- some improvements in autonomous loop

## [0.2.109] — lun 11 may 2026

### Changed

- dashboards

## [0.2.107] — lun 11 may 2026

### Added

- feature(fuzzy tab): with love

### Fixed

- refactor(alto refactor con nuevo configurador, eliminacion de bugfixing de linter, nuevo prompt configurable): co namor para la comunidad

## [0.2.105] — dom 10 may 2026

### Changed

- some love

## [0.2.104] — sáb 09 may 2026

### Changed

- refactor to mcp
- some patchs

## [0.2.102] — sáb 09 may 2026

### Changed

- readme updates

## [0.2.101] — sáb 09 may 2026

### Added

- new features, and readme update
- Add files via upload

### Changed

- reasdme updates

## [0.2.100] — jue 07 may 2026

### Changed

- some love to autocomplete commands

## [0.2.99] — jue 07 may 2026

### Changed

- assign command with tabs

## [0.2.97] — mié 06 may 2026

### Changed

- corrige DEPLOY.sh para GPG opcional, gh releases y orden de variables
- Update README.md

### Security

- Merge pull request #139 from grisuno/feature/lazyc2-security-plan

### Fixed

- some bug fixing and refactors
- new features llm new bug fixing and new refactoring

## [0.2.95]

### Security

- a new way to search vulns in the context of mcp

## [0.2.94]

### Changed

- ReactiveSelector → pattern-matched decisions (AV/EDR, privesc hints, creds)

## [0.2.93]

### Changed

- hive command now from cli now

## [0.2.92]

### Changed

- some improves in the cicle

## [0.2.91]

### Changed

- autonomous lop is closed now

## [0.2.89]

### Changed

- some ideas from openclaw

### Security

- Add Codacy security scan workflow

## [0.2.86]

### Changed

- test

## [0.2.84]

### Changed

- some love

## [0.2.83]

### Changed

- test

## [0.2.82]

### Changed

- some refactors
- mcp
- mcp

## [0.2.81]

### Changed

- some improves and refactors in the lazyown env
- algunos retoques

## [0.2.80]

### Changed

- testing deployment and up the versioning semantic
- testing deplyment
- lazyown finally has soul

## [0.2.79]

### Changed

- the mcp can now anotate the succes or failure and the clasification of commands, so the sessions db can feed deeplearning models to improve or ai models

## [0.2.78]

### Changed

- a little changes in mcp

## [0.2.77]

### Changed

- some love to mcp

## [0.2.76]

### Added

- new utils into mcp

## [0.2.75]

### Added

- new readme
- Add LazyOwn MCP integration details to README
- new full mcp to interact with claude code with independent agents flow
- new feature to create new features :P
- mcp server to claude code like an apt xD now claud code can create new lazyaddons

### Changed

- readme
- readme
- Merge pull request #123 from grisuno/grisuno-patch-1
- Update README.md
- mcp server to claude code like an apt xD

## [0.2.74]

### Added

- new agent LazyOwn it's very dumb now but we work on it

## [0.2.68]

### Fixed

- hotfix():

## [0.2.67]

### Added

- feat():

### Fixed

- hotfix(install, key) some bug fixing and testing new keys to deploy

## [0.2.64]

### Changed

- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Merge pull request #119 from grisuno/grisuno-patch-1
- Update README.md

### Fixed

- new commands, new bofs, newbug fixing, etc
- more love to new beacon in https://github.com/grisuno/beacon, new commands LazyAddons, some bug fixing, now you can pass more than one commands in lazycommnds of lazyaddons comma separated

## [0.2.63]

### Fixed

- some love to the beacon, new bofs, bug fixing, new module of telemetry not invasive
- more love to new beacon, a little telemetry not invasive in module tel, some bug fixing

## [0.2.62]

### Added

- new bofs, new commands, new loader, and much much more
- more love to new beacon, much more bofs, new loader, new gui, new command aes_pe to encript a exe with aes, to use in LazyLoader to load for example Black Basalt Beacon

## [0.2.61]

### Added

- more love to new beacon, now with bof in memory from an url, new Windows escalate privileges with a self-made exploit, and now you can add alias with add2find and addalias, enjoy

### Fixed

- new black basalt beacon, bof coff execution in memory in windows new beacon experimental, new commands and, some bug fix

## [0.2.60]

### Added

- more love to new beacon, some love in the cli, and better gui, and some litte commands like cc beef_payload and new find instance to the beef payload

### Fixed

- some love in the beacon, bug fixing, better gui, and much more

## [0.2.59]

### Added

- new gui blackbasatl, new beacon, with load_modules from memory and one module a simple rev shell, hellsgate in inyection of new black basalt beacon bbb, new alias

## [0.2.58]

### Changed

- Merge pull request #113 from grisuno/grisuno-patch-1
- Update slack_c2_bot.py
- Update README.md

### Fixed

- new bug fixing new plugins, and hellbird, log live to hellbird
- new shellcode reverse shell custom no msfvenom, some bug fixing, fix some cve, fix bugs in lolbass commands, new test to testing implants, and the king hellbird was released

## [0.2.57]

### Added

- new lolbass, new stub more stealth, new gui code name black basalt
- new ideas, plugins lua, stubs more stealth, installers, lolbas integration, and new gui in tkinter nombre codigo black basalt o por su comando gui

## [0.2.56]

### Added

- new stubs to windows and linux, new stub in lolbas, and some new ideas
- new stub to more silent execution in fases, new plugins lolbird using lolbas and stub in lolbas

### Changed

- Update README.md
- deleting files
- files

## [0.2.55]

### Added

- some new ideas auto complete in c2 commands like upload_c2 donwload_cd and issue_commad_to_c2

### Changed

- autocomplete in c2

## [0.2.54]

### Added

- new injection technique in windows beacon

### Changed

- Update README.md
- the soul of ebird3 is now in our beacon, Long Life to Early bird APC Injctn

## [0.2.53]

### Added

- new amsi bypass, exeute multiplatform shellcode from url, OverWrite Process Hollowing variant from the baecon

### Changed

- shellcode execute, amsi bypass and process hollowing varian Process Overwrite
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update README.md

## [0.2.52]

### Added

- new addons and new reports and bots, new injection technique earli bird apc in pure c call ebird3
- new LazyAddons and some stuffs :) new github bot and reporting

### Changed

- Update README.md

## [0.2.51]

### Security

- new addons and new addon creator and new vulnbot
- new LazyAddons and some stuffs :) new vuln bot and lazyaddons ia generated

## [0.2.50]

### Added

- some new addons

### Changed

- Update README.md

### Fixed

- new LazyAddons and some stuffs :) and bug fix

## [0.2.49]

### Added

- new addons
- new LazyAddons and some stuffs :)

## [0.2.48]

### Added

- New LazyAddons cgoblin and gomulti_loader remote code execution in LazyAddons and much much more xd
- new LazyAddons to the family gmulti_loader and CGOblin, remote code execution from LazyAddons and much more

## [0.2.47]

### Added

- usign gum in shell scripting and new custom loader to windows for msf payload in c and asm

### Fixed

- some bug fixing

## [0.2.46]

### Changed

- some ideas

### Fixed

- new yamls and some fix

## [0.2.44]

### Added

- new addons sphinx to documentations, etc
- sphinx to docs, new addons, and new indeas to adversaries
- new ideas
- some new ideas

### Changed

- cloud support
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- some ideas and cloud support with stratus
- Update README.md
- Update .readthedocs.yaml
- Create .readthedocs.yaml
- Update README.md
- Update README.md
- Update README.md
- some ideas

### Fixed

- hotfix
- hotfix
- bugfixing and new phishing module :D

## [0.2.43]

### Added

- new phishing module

### Fixed

- bugfixing and new phishing module :D

## [0.2.42]

### Changed

- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update README.md

### Fixed

- bugfixing
- bugfixing
- bugfixing
- bugfixing and certipy_ad new options

## [0.2.41]

### Added

- new surface attack like bloodhound and decoy malicius try to share webcam, mic and screen

### Changed

- Update README.md
- decoy more agresive take snapshots of screen and video of webcam and bloodhound zip surface attack

## [0.2.40]

### Added

- new image
- some neww ideas

## [0.2.39]

### Added

- new cappabilities to the beacon documented at readme and some new surprices

### Fixed

- new beacon cappabilities documented at readme.md and some new surpices and layaddons and some bug fixing

## [0.2.38]

### Added

- new functionalities to discover in c2 and implant and exfiltration cap, portscanning, etc
- new cappabilities to the c2 to discovered the net surface and the implant can improve a network discover, portscan the discovered hosts, search for a files and exfiltrate and others

## [0.2.37]

### Added

- new offuscated implants go more maleable more undetectable, new command rev to automated get a revshell, cloudflare tunnel to get certified subdomain to the infra for free
- New addons, implant ofuscated by garble, tunnel cloudflare, host_discover at C2 diagram show the entire network , implant more maleable, some new ideas to ia and rag or cag

### Changed

- deleting large files

## [0.2.36]

### Added

- new commadn lazyownbt for blueteams, and cloudflare tunnel to c2 over inet

### Changed

- lazyownbt y cloudflare_tunnel

## [0.2.35]

### Added

- new categoried help and others things

### Changed

- Merge pull request #90 from grisuno/grisuno-patch-1
- Update README.md
- commands categorized

## [0.2.34]

### Changed

- file path traversal and some othstuff

### Fixed

- hotfix

## [0.2.33]

### Changed

- fully tty in local shell in web cli
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- fully tty local shell implementation in web cli

## [0.2.32]

### Added

- new system of plugins and addons
- new system plugins and addons and more

### Changed

- Merge branch 'main' of https://github.com/grisuno/LazyOwn

## [0.2.31]

### Added

- new plugin system and addons system
- new system plugins and addons

## [0.2.30]

### Added

- new ideas
- some new ideas

### Changed

- some things

### Fixed

- bug on readme

## [0.2.29]

### Added

- new version, new bots, new c2, new ai

### Changed

- LazyOwn RedTeam Framework: Command & Control, Reimagined. Now with Telegram & Discord C2 Bots

## [0.2.28]

### Added

- new fetures

### Changed

- Merge pull request #82 from grisuno/grisuno-patch-3
- Create FUNDING.yml
- telegram bot

### Fixed

- hotfix

## [0.2.27]

### Fixed

- hotfix

## [0.2.26]

### Added

- new C2 world class powered by AI
- new C2 con todas las características

### Changed

- Merge pull request #79 from grisuno/dev7

## [0.2.25]

### Added

- new commands documented at COMMANDS.md, new rootkit named LazyHyde, new malware, nad much much more
- new ring 3 rootkit, 3 new listeners go python and c, infect pid with shellcode, new style of c2, download_c2 and upload_c2 and much much more

### Changed

- Merge pull request #77 from grisuno/dev6

## [0.2.24]

### Changed

- Merge pull request #75 from grisuno/dev5
- some utils 9 jajaja?

### Fixed

- hotfix(hot fix): path

## [0.2.23]

### Added

- new release

### Changed

- Merge pull request #73 from grisuno/dev4
- some utils 8 jajaja?

## [0.2.22]

### Added

- new commands documented at commands.md

### Changed

- Merge pull request #71 from grisuno/dev2
- some utils 7 jajaja?

## [0.2.21]

### Added

- new commands

### Changed

- Merge pull request #69 from grisuno/dev
- some utils 6 jajaja?

## [0.2.20]

### Added

- new feats

### Changed

- Merge pull request #67 from grisuno/dev
- some utils 5 jajaja?

## [0.2.19]

### Added

- new feats documented at COMMANDS.md

### Changed

- Merge pull request #66 from grisuno/dev
- some utils 4 jajaja?

## [0.2.18]

### Added

- new commands documented at COMMANDS.md

### Changed

- Merge pull request #64 from grisuno/dev
- some utils 3 jajaja

## [0.2.17]

### Added

- add option 20 of lazymsfvenom module

## [0.2.16]

### Added

- new features

### Changed

- Merge pull request #62 from grisuno/dev
- some utils 2
- Merge pull request #61 from grisuno/dev
- some utils

## [0.2.15]

### Added

- mani commands new
- Merge pull request #59 from grisuno/feature/Certified

### Changed

- too many commands documented at COMMANDS.md

## [0.2.14]

### Added

- new tag
- Merge pull request #57 from grisuno/feature/Hackback

### Changed

- too many commands documented at COMMANDS.md

## [0.2.13]

### Added

- feat():
- Merge pull request #54 from grisuno/feature/jira-3
- Merge pull request #53 from grisuno/feature/jira-2
- feat History enabled, multiline commands and startup script
- Merge pull request #51 from grisuno/feature/1

### Changed

- too many commands documented at COMMANDS.md
- second
- first

### Fixed

- hotfix

## [0.1.66]

### Changed

- test
- openredirex, feroxbuster, gowitness, odat

## [0.1.65]

### Changed

- test
- monteverde machine

## [0.1.64]

### Added

- new commands documented at COMMANDS.md

### Changed

- test

## [0.1.63]

### Added

- new commands documented at COMMANDS.md

### Changed

- test
- no test
- test
- deply
- deploy
- hashs

## [0.1.62]

### Added

- new commands like emp3r0r, template_helper_serializer, gospherus, wpscan, createjsonmachine_batch this is so important, is for monetize your skills with hackerone.com

## [0.1.61]

### Added

- New Feature Automate Arduino Attacks or AAA the command is lazy_ducky_digispark

### Changed

- refactor of users.txt
- refactor lazy_ruberdigispark isnto duckyspark
- trasnlated nmap script
- nmap
- Update README.md

## [0.1.60]

### Changed

- finger_user_enum

## [0.1.59]

### Changed

- trasnform

## [0.1.58]

### Fixed

- bug fixing

## [0.1.57]

### Changed

- tags

## [0.1.56]

### Added

- feature(feature & refactor): new commands and refactor

### Changed

- refactor de find y nc

## [0.1.55]

### Changed

- automsf

## [0.1.54]

### Added

- test(new machine return): is a nice machine :P
- new machine yummy.htb found a command in find to reverse shell :P
- new attack mfscosole automated

## [0.1.53]

### Changed

- testing DEPLOY.sh script
- nueva documentacion comando evidence
- lazyown infinite glitch storage

### Fixed

- fix in find command

## [0.1.52]

### Changed

- refactor de credentials de evilwinrm de psexec, find
- eternalblue

## [0.1.51]

### Added

- new commands and functionalities

### Changed

- deleting users from ctf game from repo

## [0.1.50]

### Added

- new command Shadowsocks

## [0.1.49]

### Changed

- now we are vip

## [0.1.48]

### Added

- new commands documented at COMMANDS.md

## [0.1.47]

### Added

- some test and new resources and externals scripst to download :D
- new cool stuff xD

## [0.1.46]

### Added

- feat(win backdoor): undetectable

## [0.1.45]

### Changed

- c2 insecure filename

## [0.1.44]

### Added

- feature(new commands): documented at COMMANDS.md

### Changed

- documented resources, and externals, and one command dr0p1t

## [0.1.43]

### Added

- new commands: scarecrow, createmail, eyewitness, secretsdump, getuserspns, passwordspray

## [0.1.42]

### Changed

- install
- graph

## [0.1.41]

### Added

- 2 new commands

## [0.1.40]

### Changed

- install testing
- install wa broken

## [0.1.39]

### Changed

- emire
- veil
- now tord, trace, and generatedic to generate dictionary with params

## [0.1.38]

### Added

- testing new feature tord
- new alias
- new links

### Changed

- ivy shellcodes test
- corrections in text
- better docs
- msfpc

## [0.1.37]

### Changed

- comandos nuevos documentados en commands.md

## [0.1.36]

### Added

- new command apache_users & new options -p to use diferents payloads.json

## [0.1.35]

### Changed

- documented malwarebazar
- documentating
- Nuevos comandos documentados en COMMANDS.md

## [0.1.34]

### Changed

- nuevos comandos documetados en COMMANDS.md

## [0.1.33]

### Changed

- nuevos comandos documentados en COMMANDS.md

## [0.1.32]

### Changed

- deleted the insecure chat

## [0.1.31]

### Changed

- Nuevos comandos documentados en COMMANDS.md

## [0.1.29]

### Fixed

- some fixes in c2

## [0.1.28]

### Changed

- to kick from net some ip

## [0.1.27]

### Added

- feature(new command c2 documentad at COMMANDS.md): a little botnet over http :)

## [0.1.26]

### Fixed

- fix(fix auto exploit cacti rce logged): now the attack work automated

## [0.1.25]

### Added

- feature(new commands docummented at COMMANDS.md): waybackmachine, morse, powerserver, shellshock, wifipass, ngrok and smalldic

## [0.1.24]

### Added

- feature(2 new attacks): docummented at COMMANDS.md

## [0.1.23]

### Added

- test(new machine): monitorsthree.htb
- refactor(new payload): in msfvenom
- feat(new feature): padbuster

## [0.1.22]

### Added

- docs(new documentation): better documentation to commands and utils
- feat(new feat in createdll): new option 3 to run automate create dll blazor malware

### Changed

- nueva versiòn en la web reflejada en el banner

## [0.1.21]

### Changed

- blazormalware corrected now functional and armed :)

## [0.1.20]

### Added

- Translate README.md to English, enhancing clarity and structure for better understanding of the project features and usage
- feat(malware new): blazor malware

## [0.1.19]

### Changed

- se agrega la libreria colors en modules para usar colorines en los modulos
- dos comandos nuevos, skipfish y createdll, nuevo shellcode

## [0.1.18]

### Added

- create new command shellcode, run lazymsfvenom modified to create shellcode.sh

## [0.1.17]

### Added

- feat(new feat): new funcionality in proxy command, hexdump on screen, capacity to edit responces from client and server :) mitm ? xD now only prints the thata before sent

## [0.1.16]

### Added

- new prompt

## [0.1.15]

### Added

- new command set_proxychains

## [0.1.14]

### Fixed

- fix(bug fixing): bug fixing in vars of DEPLOY.sh

## [0.1.13]

### Added

- feature(new payload in msfvenom android): new options in msf rev android

## [0.1.12]

### Added

- feat(implement sicat libs): to ss command

### Changed

- agradecimientos

## [0.1.11]

### Fixed

- feat(some fixes): html and new patreon :)

## [0.1.10]

### Added

- feature(new tools): new commands, new payloads in find, new cves, new machine

## [0.1.9]

### Added

- feat(new feature): new command finalrecon docuemnted at COMMANDS.md

## [0.1.8]

### Added

- new commando swaks to abuse of smtp

## [0.1.7]

### Fixed

- fix(fix in vpn): new machine

## [0.1.6]

### Added

- feature(sessionssh y sessionsshstrace): nuevos comandos documentados en COMMANDS.md

### Changed

- test(deleted files): index.sh y dump_readme.sh
- refactor(refactor DEPLOY, sessionstrace): se crea todo en un solo archivo deploy y se eliminaran en el proximo commit index.sh ydump_readme.sh

## [0.1.5]

### Added

- test(testing Changelog): new method to create changelog

### Changed

- se crea el comando y el directorio lazyscripts el cual recive como parametro un nombre de chivo

## [0.1.4]

## [0.1.3]

### Changed

- nuevo tool a pwntomate medusa.tool

## [0.1.2]

### Changed

- nueco comando

## [0.1.1]

### Changed

- reload
- reload the history deleted by error holly git :P
- versionamiento
- command
- changelog
- tipo release

### Fixed

- fix
- fix en los tags
- fix(version file):
- fixin bug in formating of changelog
- fixing semantic version

## [0.1.0]

### Added

- creating new tag
- new library
- feat(semantic versioning): se implementa el versionamiento semantico utilizando el archivo versions.json y git en el archivo DEPLOY.sh
- testing deploy feature and semantic versioning
- feat(add scripts): - adding scripts on sessions/win directory a nc ps1 version
- feature(cambios en script fast_run_as_r00t.sh): se agrega la opción --vpn <NUM> para poder elegir parametricamente que vpn se elije para la ejecucion
- feature(actualizador de readme.md): con los nuevos cambios desde los scripts que generan documentaciòn
- feature(versionamiento semantico en script de deploy): mejora en DEPLOY.sh con versionamiento semantico
- feature(parametrizar el despliegue): se agrega el parametro --no-test para despliegues que no involucren cambios en la tool
- feature(nuevo creador de index.html): crea el html de manera automatizada con el script index.sh
- feature(mejora CHANGELOG.sh): ahora actualiza usando readmeneitor.py

### Changed

- deploy
- test(test of --no-test): and lolcat on clock command :P
- docs(se agrega el change log al readme): tambien se ejecutan pruebas del despliegue con el parametro --no-test
- deleting the tmp file but i cant sleep
- de organizaciòn de archivos ovpn dentro del directorio vpn
- probando el workflow de despliegue

### Fixed

- hotfix(error en parametro): deploy en el pandocpara generar documento de changelog
- feature(mejoras y fixes): - se agrega un pequeño diccionario en el comando hydra, se mejroa el comando clean, se arreglan algunos bugs
- hotfix(fix in vpn): dont work with arguments
- hotfix(delete qa command to option -c): bug: dont let beggin scriptfast_run_as_r00t.sh, instruction was deleted

## [0.0.14]

### Fixed

- fix(firma de commits con pgp): cree una firmita gpg para firmar los commits
- hotfix(bug in Deploy): not updated the index.html file in deploys

## [0.0.13]

### Added

- docs(add README.html to anchor tag in menu of index.html): - chenges in index.html in line 162
- new styles in html of documentation
- new changelog format

### Changed

- testing deploy script
- docs(mejora documentaciòn): se completan varios comandos con descripciones pobres
- bad tabs in index.html
- docs(cambio en index.html): tabulacion incorrecta del banner
- se cambia el nombre de readme.sh a dump_readme.sh para que no moleste cuando se escriba ./run junto al tab
- test
- testing changelog
- nuevo changelog
- deploy
- changelog
- saltos de linea en commit
- docs(class="neon-text" on ul): :)
- test(commits con fecha y hora :P): probando el despliegue
- test(test de index.html): testeando el despliegue automatizado del sitio web de LazyOwn
- test(test index.sh): se realizan cambios en index.sh
- Testeando el flujo de trabajo en los despliegues automatizados

## [0.0.1]

### Fixed

- fix(new version): new release

## [Nuevas características] — lun 21 oct 2024

### Added

- add forticlient CVE-2026-25089
- add animated splash overlay for first-run experience
- add tui_theme command logic with cycle/prev/reset
- add solarized, monokai, gruvbox, high_contrast themes
- add cli/style semantic token layer over themes
- add prev/next command-chain primitive + CLAUDE.md tech-debt law
- add blacksandbeacon lazyaddon with Linux BOF support
- new CLAUDE md FILE
- Merge pull request #138 from grisuno/feature/lazyllmchat-assistant
- add interactive LLM chatbot module and addon
- new features
- feat: Claude Code-style harness layer for LazyOwn MCP
- Add files via upload
- Add files via upload
- Merge pull request #137 from grisuno/feat/toposwarm-addon
- feat: online feedback loop for TopoSwarm routing (RL from user signal)
- Merge pull request #136 from grisuno/feat/toposwarm-addon
- feat: toposwarm lazyaddon — autonomous red team agent driven by TopoSwarm
- Merge pull request #135 from grisuno/feat/toposwarm-addon
- feat: TopoSwarm local brain — fallback when Claude Code / cloud APIs unavailable
- Merge pull request #134 from grisuno/feat/toposwarm-addon
- Add files via upload
- feat: add TopoSwarm AI router addon for LazyOwn MCP
- Merge pull request #133 from grisuno/feature/expand-cloud-rag-stealth-2106303999655273923
- feat
- new commands https://www.youtube.com/@KillerMonkyRecordz
- refactor and new features
- new payloads in winbase64payloads
- add cmd2 to install.sh
- feat(cambio en el versionamiento semantico): se agregan release y patch
- feat(mejorando el tipo): cambio en el script CHANGELOG.sh
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 new fancy proompt :) 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 New commands documented at COMMANDS.md and new ultis documented at ULTIS.md 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 New command launchpad to recon Linux OS 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 New Machine, New Session, New Look, New functions, New tools, New CVEs, NEW VERSION 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 new commands rulencode, urldecode, y lynis documented at COMMANDS.md 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 new commands documented at COMMANDS.md, now implement autocomplete at hashcat, more soon :) 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 new commands documented at COMMANDS.md
- 👽 new commands documented in COMMANDS.md or README.md and more documentation of the proyect thanks to readmineitor.py :D comming soon their own repo
- 👽 new machine magic gardens insane machine because resource was pwned and sea not was released yet
- 👽 new tools for pwntomate :D
- 👽 new command img2cookie :)
- 👽 new machine comprezzor.htb
- 👽 new script readmeneitor req updated
- 👽 new script readmeneitor to help me update the readme xD
- 👽 new command ssh 22 and if u have file sessions/credentials.txt this will open ssh conection :)
- 👽 new machine compiled :)
- 👽 new command disableav to create a aav.vbs to disable av if it's possible :)
- 👽 new brothers commands, LazyOwn> winbase64payload and asprevbase64 👽
- feat: somo testing and alias now you can run gpt alias :D
- feat: Now the GPT Client use Llama 70B and now can hack :)
- feat: more time to the nmap to finished and pyautomate autostart
- some new attacks exploits and new menu to download resources and exploits :D new msf autoroute :D
- some new attacks exploits and new menu to download resources adn exploits :D
- some new attacks
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new command getnpusers
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new command chisel to run chisel as server before run download_resource command
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new arguments :) -c command ex ping
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new aliases :D
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new command clock to see the time of the eternal now :) now in white xD
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new command clock to see the time of the eternal now :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 newhashcat
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new comands conptyshell better command nc noew with tty treatment createhash better now with recognice automate download_resource
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new commands ignorearp ignoreicmp acknowledgearp acknowledgeicmp ports cports
- HackTheBox https://app.hackthebox.com/teams/overview/6429 wfuzz command now search subdomains with wfuzz sub domain.htb new commands nc, vpn, rev, banner :D
- HackTheBox https://app.hackthebox.com/teams/overview/6429 New Colors :D
- HackTheBox https://app.hackthebox.com/teams/overview/6429 adding run script to run lazyown with virtual env activated to avoid errors
- HackTheBox https://app.hackthebox.com/teams/overview/6429 adding alias to exit as q :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 adding alias to commands its una shulada
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new command py3ttyup to upgrade to tty your rev shell :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new commands ip www to show ips and start webserver at sessions directory where lazyown dump scripts like revertshells, webshells, etc
- HackTheBox https://app.hackthebox.com/teams/overview/6429 solarlab pwned :D new machine MagicGardens
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine solarlab :D
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new revshell.c and machine powned xD axlle hard
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new commands createrevshell y createwinrevshell
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Freelancer Pwned :P new new new FormulaX :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Freelancer :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Skyfall Linux insane machine, Blazorized was powned :D
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Blazorized.htb
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Greenhorn.htb pwned
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new machine Greenhorn.htb
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new tool in external :) https://github.com/BloodHoundAD/SharpHound.git :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new MAchine Blazorized.htb :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new MAchine :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 New command to copy the exploits from exploitdb use cp relative/path/show/in/searchexploit when you use the flag -x :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 New command dsnmap :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 New machine Runner.htb
- HackTheBox https://app.hackthebox.com/teams/overview/6429 New command :) new resources in sessions, new module lazypsexec bruteforce :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 New command :) samrdump
- HackTheBox https://app.hackthebox.com/teams/overview/6429 news script bruteforce on modules :) :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 new command dnsenum :)
- join to our team https://app.hackthebox.com/teams/overview/6429 new command dig
- join to our team https://app.hackthebox.com/teams/overview/6429 new commands :)
- join to our team https://app.hackthebox.com/teams/overview/6429 new commands :) to se use tab tab or ?
- join to our team https://app.hackthebox.com/teams/overview/6429 and new payloads in sessions directory :) :) :)
- join to our team https://app.hackthebox.com/teams/overview/6429 and new exploits :)
- news exploits
- new hashcat :D
- new command dirsearch :D
- new proxy better :D
- new commands createhash, createwebshell, sqlmap, proxy, john2hash
- 1 new exploit
- 2 new exploit external :D working like a charm
- new command: exploits externals :D
- new command: smbmap whattomap ex: smbmap tmp :D
- go buster new parameter url to use url from payload not rhost
- parameter added to gospider url to use var url in payload not rhost and add the command addhost host.ext to add the domain with rhost parameter to /etc/hosts not now to windows sistems sorry
- path hijacking add line to temp bash script
- new command: gospider :D
- new command: gobuster :D
- new command: wfuzz :D and you can add example a hide line option like # wfuzz --hl=9 to hide responses with long line to 9
- new command: run lazyssh77enum to enum using a wordlist and exploit foound searchsploit as openssh 7.7
- new command: whatweb :D
- new command: psexec :D
- new command getseclist :D
- new commit to check if alsr is activated in the kernel
- new comand arpscan
- new path to diccionary to run by default in parrot
- new gitignore
- add #!/usr/bin/env python3 #_*_ coding: utf8 _*_
- new tags
- Create lazyclonewars.sh
- new honeypot
- New BotNet with Keylogger
- new netbios atack mode
- new comand payload :)
- Add files via upload

### Changed

- 
- 
- extract state.py and models.py from lazyc2.py
- 
- auto-generate 10 CommandSet files from lazyown.py via migration script
- bump certifi from 2026.4.22 to 2026.6.17
- bump triton from 3.6.0 to 3.7.1
- bump python-engineio from 4.13.2 to 4.13.3
- bump cuda-bindings from 13.2.0 to 13.3.1
- bump nvidia-nvtx from 13.0.85 to 13.3.29
- shadow a beacon over dns :D
- Merge pull request #182 from grisuno/dependabot/pip/yagmail-0.16.0
- Merge pull request #183 from grisuno/dependabot/pip/coverage-7.15.2
- Merge pull request #184 from grisuno/dependabot/pip/typing-extensions-4.16.0
- Merge pull request #185 from grisuno/dependabot/pip/parso-0.8.7
- Merge pull request #186 from grisuno/dependabot/pip/lxml-6.1.1
- bump lxml from 6.1.0 to 6.1.1
- bump parso from 0.8.6 to 0.8.7
- bump typing-extensions from 4.15.0 to 4.16.0
- bump coverage from 7.13.5 to 7.15.2
- bump yagmail from 0.15.293 to 0.16.0
- payloads refactos
- more modularization of lazyown.py file
- more modularization of lazyc2.py file
- decostruction of the monolitic
- some improvements in linting
- We changed graphify for ReadMenator
- Contrib
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Merge pull request #177 from grisuno/grisuno-patch-2
- Update CONTRIBUTING.md
- test
- test: test
- orquestator of playbooks
- test: test
- database, module manager, some payload generation, resource scripting, and love
- 
- 
- wire tui_theme command and first-run splash into the shell
- 
- 
- 
- 
- 
- 
- 
- unify next-best-action recommenders into one engine
- 
- 
- 
- 
- 
- 
- 
- generate recon plan from trigger catalog after scan
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- Update README.md
- 
- wire local-shell xterm to /pty namespace with websocket transport
- Final submission: Expand LazyOwn capabilities for Cloud/K8s and Multi-Index RAG
- Expand LazyOwn capabilities with Cloud/K8s support and Multi-Index RAG
- 
- SSE daemon transport + reliable restart script
- detect ABABAB oscillation + rebalance policy transitions
- ACL errors no longer trigger evasion advisor; stuck-loop blocks by base name
- stuck-loop recovery covers any repeated command, not just 'list'
- 
- self-healing autonomous loop — credential/domain auto-injection, nmap XML parse, stuck-loop recovery
- 
- world-class MCP expansion — 92 tools, 26 data sources, zero-gap operator autonomy
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- please subscribe :P
- 
- test
- 
- 
- rpcmap_py, serveralive2, john2zip, createusers_and_hashs, pykerbrute, reg_py
- 
- test
- 
- samdump2
- 
- cubespraying & magicrecon
- 
- shellcode2sylk
- 
- tes
- 
- tes
- 
- test
- tes
- test
- release: test
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- prueba de nuevos tipos de commits
- 
- 
- 
- El cierre de una imagen en la documentación estaba mal :)
- Nueva descripcion en el readme y probando el CHANGELOG.sh :)
- ahora el changelog a docs :D en formato html
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 some changes in the web pandoc README.md -f markdown -t html -s -o README.html madremia que comandazo 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 some changes in the web 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 comming soon tryhackme 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 3ast3r366 👽
- Merge pull request #27 from grisuno/clcthulhu-patch-1
- docs(update readme description): change of the description; Update README.md
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 mejorando la documentaciòn 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 command vpn now handle multiple ovpn files 👽
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 Magicgardens is so insane but pwned :)
- 👽 some love to readme
- 👽 some changes in nmap script now discovery have template html too and we have a little index2.html to navigate the reports
- 👽 some littles changes :)
- 👽 changing the command in venom :)
- 👽 holly jissus mist.htb now pwned with my user :P its rally insane amount of work to pwn
- 👽 holly jissus mist.htb machine cost to me one week and my mental health xD bu it's pwned xD
- 👽 todo readme
- Update README.md
- 👽 update gitignore
- 👽 command list to update the readme: todo
- 👽 no more prints ( 👽 we have 13 xD) now we have technologì we have print_msg, print_error & print_warn :) so much pretty
- Update README.md
- 👽 better prints 👽
- 👽 conptyshell better 👽
- some roder to prints, not finished yet but the storm its cut the electricity so commit
- Create sessions.sh
- some ideas
- HackTheBox https://app.hackthebox.com/teams/overview/6429 command smbserver now create file.scf to generate a attackto the victim try to charge an iccon from our smbserver and the hash is ours
- HackTheBox https://app.hackthebox.com/teams/overview/6429 the target was pwntomated 🍅 alias auto
- HackTheBox https://app.hackthebox.com/teams/overview/6429 the target was pwntomated 🍅. jejejjejej
- HackTheBox https://app.hackthebox.com/teams/overview/6429 now with pwntomate to automate with the command pyautomate
- HackTheBox https://app.hackthebox.com/teams/overview/6429 now command nmap or run lazynmap has a html and xml reports to more pleasssure. xD
- HackTheBox https://app.hackthebox.com/teams/overview/6429 some format
- HackTheBox https://app.hackthebox.com/teams/overview/6429
- HackTheBox https://app.hackthebox.com/teams/overview/6429 now options like --help, -v and --no-banner :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429
- HackTheBox https://app.hackthebox.com/teams/overview/6429 was banned from htb to spoiler jajjajaj xD
- HackTheBox https://app.hackthebox.com/teams/overview/6429 msf command
- HackTheBox https://app.hackthebox.com/teams/overview/6429 scripts to try attac cammeras not work with my cammera yet xD
- HackTheBox https://app.hackthebox.com/teams/overview/6429 clean command to clean up the mess and pwn the next machine :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 wfuzz commands pwd, sh
- HackTheBox https://app.hackthebox.com/teams/overview/6429 some love to list command :D
- HackTheBox https://app.hackthebox.com/teams/overview/6429 some love in form of colored strings :D
- HackTheBox https://app.hackthebox.com/teams/overview/6429 some love to some prints :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429 FormulaX pwned :)
- HackTheBox https://app.hackthebox.com/teams/overview/6429
- Update README.md
- Update lazyproxy.py
- join to our team https://app.hackthebox.com/teams/overview/6429
- little discover .sh
- Create internal_discover.sh
- Update README.md
- refactor global var rhost deleted other ones
- smbclient command and exploit to enum ssh i used in a machine of hackthebox to enum, i upload because i was lazy and dont deleted before xD
- Merge pull request #22 from grisuno/grisuno-patch-1
- Update README.md
- mariadb rce :)
- payload.json to play on hackthebox :D
- port a python del exploit archiconocido de meta exploit vsftpd 3.0.3
- shell payload in python generated by msfvenom automated by lazyown framework ;)
- deleted shells generated by the script
- upx to shells generated by msfvenom automated by lazyown framework ;)
- cambios en el miniburp
- Update index.html
- Update install.sh
- herramienta para ofuscar payloads y es usada en lazylogpoisoner ;) pronto extendida al resto de payloads ;)
- lazymitmap.py
- Update lazycurl.sh
- Update README.md
- lazycurl.sh
- Update install.sh
- Update requirements.txt
- Merge pull request #21 from grisuno/grisuno-patch-1
- Update CNAME
- Update install.sh
- Create CNAME
- metatags to seo
- Lazy ntlmv2 firstaproach using in hashes.txt the ouput smbserver command when the conection is established
- Lazy .gitignore
- Lazy get smbserver with impacket :) and then you can sudo impacket-smbserver smbfolder /home/gris/tools/LazyOwn -smb2support with simple smbserver in LazyOwn console
- LAzy get capabilities :P
- LazyOwn FTP sniff prety messages :)
- LazyOwn keygen to generate keys to use in payload.json to cypher the conections
- LazyOwn smbrelay
- LazyOwn http sniff :( not working fine yet
- Update README.md
- LazyOwn ftp sniff :)
- LazyOwn README
- LazyOwn ArpSpoofing README and banner :P [;,;]
- LazyOwn ArpSpoofing [;,;]
- Update README.md
- Lazy path hijacking :)
- Lazy msfvenom reverse :)
- Lazy Log more lfi list :)
- Lazy Log Poisonig more poison bro
- Lazy Log Poisonig in ssh first aproach
- Lazy Log Poisonig
- Delete lazylogpisoning.py
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update app.py
- Lazy Log Poisonig
- Update lazypwnkit.py
- Create lazyssh.py
- #!/usr/bin/env python3 #_*_ coding: utf8 _*_
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update README.md
- Update lazylfi2rce.py
- dic
- Update app.py
- dos2unix
- Update README.md
- better implementation
- tentativas de herramientas nuevas
- google analytics
- dos2unix
- Update index.html
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update .gitignore
- delete python librarys
- use of python3 env
- Update index.html
- Update README.md
- Update index.html
- banner
- nueva shell zsh :)
- index nuevo
- Create index.html
- Update app.py
- imlementacion de libreria pwn
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Create lazygalazy.py
- Update app.py
- Update README.md
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update lazywebshell.sh
- Update README.md
- Update app.py
- Create lazywebshell.sh
- mejora en la webshell de python
- webshells
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- comentarios necesarios
- Update README.md
- return jsonify({"error": "error"}), 500
- py2elf experimental
- nueva interfaz web experimental
- Update app.py
- nuevo bot de investigacion
- remove keys xD
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Merge pull request #13 from grisuno/grisuno-patch-7
- Update README.md
- Create pull_request_template.md
- Update README.md
- Create pull_request_template.md
- device to sniff parametric
- netbios atack
- Update lazynetbios.py
- update req*
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update README.md
- del
- mejoras en ncurses
- Update lazysniff.py
- nuevo modulo de sniffer
- Update lazyownclient.py
- Merge branch 'main' of https://github.com/grisuno/LazyOwn
- Update README.md
- nuevo modulo de gathering
- Update search.py
- nueva estructura de directorios
- Update app.py
- Update README.md
- Update lazyownserver.py
- Merge pull request #10 from grisuno/grisuno-patch-6
- Update lazyownclient.py
- Update README.md
- Update requirements.txt
- Update app.py
- Create lazyownclient.py
- Create lazyownserver.py
- Update app.py
- Update README.md
- Update app.py
- Update lazynmap.sh
- Update requirements.txt
- Update app.py
- Merge pull request #8 from grisuno/grisuno-patch-6
- Update requirements.txt
- Update README.md
- Update app.py
- Create lazyown_metaextract0r.py
- Update README.md
- Update lazygptcli.py
- Update README.md
- Update lazygptcli.py
- Update README.md
- Update app.py
- Update README.md
- Create app.py
- Update README.md
- Create lazyown_bprfuzzer.py
- Update lazygptcli.py
- Merge pull request #6 from grisuno/grisuno-patch-5
- Update update_db.sh
- Update requirements.txt
- Update README.md
- Update lazygptcli.py
- Create lazygptcli.py
- Update README.md
- Create lazynmap.sh
- Update lazyreverse_shell.sh
- Merge pull request #5 from grisuno/grisuno-patch-4
- Update README.md
- Create lazyreverse_shell.sh
- Update README.md
- Update requirements.txt
- Update README.md
- Update LazyOwnExplorer.py
- Update README.md
- Create LazyOwnExplorer.py
- Update README.md
- Merge pull request #4 from grisuno/grisuno-patch-3
- Create requirements.txt
- Create CODE_OF_CONDUCT.md
- Update issue templates
- Create CONTRIBUTING.md
- Merge pull request #3 from grisuno/grisuno-patch-2
- Create LICENSE
- Merge pull request #1 from grisuno/grisuno-patch-1
- Update lazyown.py
- Update README.md
- Create lazyatack.sh
- Update README.md
- Create lazysearch.py
- Update README.md
- Update update_db.sh
- Update README.md
- Create update_db.sh
- Update README.md
- Create lazyown.py
- Create bin_data_relevant.csv
- Create bin_data.csv
- Create detailed_search.py
- Create search.py
- Update README.md

### Security

- Security advisory some prints whit debug data :)
- Security Advisory from code scan in soupsieve
- Security Advisory from code scan
- feat(security,packaging): authorization scope guard + reproducible installs
- untrack runtime cache knowledge_base_vuln.json
- add lazyc2 security layer with validators, services, and pytest tests
- Create SECURITY.md

### Fixed

- some bug fixing :D
- Update install.sh for package installations and fixes
- Expand capabilities (Cloud/K8s/RAG) and fix CI
- Expand LazyOwn capabilities and fix CI
- some bugs xD
- fix
- 👽 HackTheBox: https://app.hackthebox.com/teams/overview/6429 👽 bug fixing 👽
- 👽 bug fixing in createhash, new wrappers, chisel command updated now can choice the payload, img2cookie new payloads
- 👽 bug fixing and replace command nc with pwncatcs more fancy and sharp :)
- 👽 bug fixing in wfuzz sub command wen you not pass the domain
- 👽 chisel fix copy to clipboard commad bug
- feat: Now the GPT Client use Llama 70B and now can hack :) fixing error path from json files :P
- HackTheBox https://app.hackthebox.com/teams/overview/6429 fix arguments little bug
- join to our team https://app.hackthebox.com/teams/overview/6429 and new command run lazywerkzeugdebug
- new exploit werkzeug in debug mode lettle retocated to run in python3 from searchsploit :D
- fix install
- Fix code scanning alert - Information exposure through an exception #16
- Fix code scanning alert - Flask app is run in debug mode #17
- new command fixperm

## [0.0.0]

### Changed

- test
- release
- release(release test): test
- migration from cmd to cmd2
