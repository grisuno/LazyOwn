# `modules/rootkit/rootkit.c`

> Source: [modules/rootkit/rootkit.c:1](../../modules/rootkit/rootkit.c#L1) | language `c` | coverage 14.3% | [API index](../index.md)

Define the process name and file name to hide Operable values are provided via the Makefile (ccflags-y defines); the defaults below are inert placeholders so the artifact never embeds a hard-coded attacker IP or operator username.

## Contents

- **Macros:** [`HIDDEN_PROCESS_NAME`](#hidden_process_name), [`HIDDEN_FILE_NAME`](#hidden_file_name), [`LISTENER_IP`](#listener_ip), [`LISTENER_PORT`](#listener_port), [`SPECIAL_STRING`](#special_string), [`SPECIAL_STRING_PORT`](#special_string_port)

## Macros

<a id="hidden_process_name"></a>

### `HIDDEN_PROCESS_NAME`

`macro` | [modules/rootkit/rootkit.c:30](../../modules/rootkit/rootkit.c#L30)

```c
#define HIDDEN_PROCESS_NAME
```

---

<a id="hidden_file_name"></a>

### `HIDDEN_FILE_NAME`

`macro` | [modules/rootkit/rootkit.c:33](../../modules/rootkit/rootkit.c#L33)

```c
#define HIDDEN_FILE_NAME
```

---

<a id="listener_ip"></a>

### `LISTENER_IP`

`macro` | [modules/rootkit/rootkit.c:36](../../modules/rootkit/rootkit.c#L36)

```c
#define LISTENER_IP
```

---

<a id="listener_port"></a>

### `LISTENER_PORT`

`macro` | [modules/rootkit/rootkit.c:39](../../modules/rootkit/rootkit.c#L39)

```c
#define LISTENER_PORT
```

---

<a id="special_string"></a>

### `SPECIAL_STRING`

`macro` | [modules/rootkit/rootkit.c:42](../../modules/rootkit/rootkit.c#L42)

```c
#define SPECIAL_STRING
```

---

<a id="special_string_port"></a>

### `SPECIAL_STRING_PORT`

`macro` | [modules/rootkit/rootkit.c:45](../../modules/rootkit/rootkit.c#L45)

```c
#define SPECIAL_STRING_PORT
```

---
