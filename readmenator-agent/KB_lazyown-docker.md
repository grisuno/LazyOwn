# Subsystem: lazyown-docker

## lazyown-docker/entrypoint.sh
- Layer: utility
- Doc: LazyOwn Entrypoint Script Initializes LazyOwn framework in a Docker container with tmux sessions
- Language: sh

## lazyown-docker/hostdiscover.sh
- Layer: infrastructure
- Language: sh
- Symbols:
  - `extract_ips_from_arp` (function, line 21)
  - `extract_listening_ips_from_netstat` (function, line 26)

## lazyown-docker/init.sh
- Layer: utility
- Language: sh
- Imported by: `static/js/chart.min.js`, `static/js/chart.min.js`, `static/js/chart.min.js`, `static/js/chart.min.js`, `static/js/chart.min.js`, `static/js/chart.min.js`, `static/js/chart.min.js`, `static/js/chart.min.js`, `static/js/html2pdf.bundle.min.js`, `static/js/jquery-3.5.1.slim.min.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/particles.js`, `static/js/quill-2.0.3.js`, `static/js/quill-2.0.3.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network-9.1.2.min.js`, `static/js/vis-network.min.js`, `static/js/vis-network.min.js`, `static/js/vis-network.min.js`, `static/js/vis-network.min.js`, `static/js/xterm.js`, `static/js/xterm.js`, `static/js/xterm.js`

## lazyown-docker/mkdocker.sh
- Layer: utility
- Doc: LazyOwn Dockerizer Script Builds, runs, and manages Docker containers for LazyOwn red teaming framework
- Language: sh
- Symbols:
  - `usage` (function, line 23)
  - `log` (function, line 36)
  - `check_docker` (function, line 41)
  - `check_file` (function, line 49)
  - `container_exists` (function, line 58)
  - `image_exists` (function, line 63)
  - `get_ports` (function, line 68)
  - `build_image` (function, line 93)
  - `validate_payload` (function, line 109)
  - `run_container` (function, line 117)
  - `stop_container` (function, line 187)
  - `clean_container_and_image` (function, line 197)
