# `lazyown-docker/mkdocker.sh`

> Source: [lazyown-docker/mkdocker.sh:1](../../lazyown-docker/mkdocker.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

LazyOwn Dockerizer Script Builds, runs, and manages Docker containers for LazyOwn red teaming framework

## Contents

- **Functions:** [`usage`](#usage), [`log`](#log), [`check_docker`](#check_docker), [`check_file`](#check_file), [`container_exists`](#container_exists), [`image_exists`](#image_exists), [`get_ports`](#get_ports), [`build_image`](#build_image), [`validate_payload`](#validate_payload), [`run_container`](#run_container), [`stop_container`](#stop_container), [`clean_container_and_image`](#clean_container_and_image)

## Functions

<a id="usage"></a>

### `usage`

`function` | [lazyown-docker/mkdocker.sh:23](../../lazyown-docker/mkdocker.sh#L23)

```bash
usage()
```

Help message

---

<a id="log"></a>

### `log`

`function` | [lazyown-docker/mkdocker.sh:36](../../lazyown-docker/mkdocker.sh#L36)

```bash
log()
```

Log function

---

<a id="check_docker"></a>

### `check_docker`

`function` | [lazyown-docker/mkdocker.sh:41](../../lazyown-docker/mkdocker.sh#L41)

```bash
check_docker()
```

Check if Docker is running

---

<a id="check_file"></a>

### `check_file`

`function` | [lazyown-docker/mkdocker.sh:49](../../lazyown-docker/mkdocker.sh#L49)

```bash
check_file()
```

Check if file exists

---

<a id="container_exists"></a>

### `container_exists`

`function` | [lazyown-docker/mkdocker.sh:58](../../lazyown-docker/mkdocker.sh#L58)

```bash
container_exists()
```

Check if container exists

---

<a id="image_exists"></a>

### `image_exists`

`function` | [lazyown-docker/mkdocker.sh:63](../../lazyown-docker/mkdocker.sh#L63)

```bash
image_exists()
```

Check if image exists

---

<a id="get_ports"></a>

### `get_ports`

`function` | [lazyown-docker/mkdocker.sh:68](../../lazyown-docker/mkdocker.sh#L68)

```bash
get_ports()
```

Get ports from payload.json

---

<a id="build_image"></a>

### `build_image`

`function` | [lazyown-docker/mkdocker.sh:93](../../lazyown-docker/mkdocker.sh#L93)

```bash
build_image()
```

Build Docker image

---

<a id="validate_payload"></a>

### `validate_payload`

`function` | [lazyown-docker/mkdocker.sh:109](../../lazyown-docker/mkdocker.sh#L109)

```bash
validate_payload()
```

Validate payload.json exists

---

<a id="run_container"></a>

### `run_container`

`function` | [lazyown-docker/mkdocker.sh:117](../../lazyown-docker/mkdocker.sh#L117)

```bash
run_container()
```

Run container

---

<a id="stop_container"></a>

### `stop_container`

`function` | [lazyown-docker/mkdocker.sh:187](../../lazyown-docker/mkdocker.sh#L187)

```bash
stop_container()
```

Stop container

---

<a id="clean_container_and_image"></a>

### `clean_container_and_image`

`function` | [lazyown-docker/mkdocker.sh:197](../../lazyown-docker/mkdocker.sh#L197)

```bash
clean_container_and_image()
```

Clean container and image

---
