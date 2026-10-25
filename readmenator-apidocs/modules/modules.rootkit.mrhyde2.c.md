# `modules/rootkit/mrhyde2.c`

> Source: [modules/rootkit/mrhyde2.c:1](../../modules/rootkit/mrhyde2.c#L1) | language `c` | coverage 2.8% | [API index](../index.md)

## Contents

- **Structs:** [`linux_dirent64`](#linux_dirent64)
- **Type Aliases:** [`original_dirent`](#original_dirent)
- **Functions:** [`load_hidden_pids`](#load_hidden_pids), [`unlink`](#unlink), [`kill`](#kill), [`remove`](#remove), [`unlinkat`](#unlinkat), [`get_username_from_pid`](#get_username_from_pid), [`should_hide_pid`](#should_hide_pid), [`readdir`](#readdir), [`fopen`](#fopen), [`my_open`](#my_open), [`my_openat`](#my_openat), [`stat`](#stat), [`lstat`](#lstat), [`fstat`](#fstat), [`getdents`](#getdents), [`getdents64`](#getdents64), [`main`](#main)
- **Macros:** [`HIDDEN_DIR`](#hidden_dir), [`HIDDEN_FILE`](#hidden_file), [`HIDDEN_FILE1`](#hidden_file1), [`HIDDEN_FILE2`](#hidden_file2), [`HIDDEN_FILE3`](#hidden_file3), [`HIDDEN_FILE4`](#hidden_file4), [`HIDDEN_FILE5`](#hidden_file5), [`HIDDEN_FILE6`](#hidden_file6), [`HIDDEN_FILE7`](#hidden_file7), [`HIDDEN_FILE8`](#hidden_file8), [`HIDDEN_FILE9`](#hidden_file9), [`PATHMRHYDE`](#pathmrhyde), [`HIDE_DIR`](#hide_dir), [`HIDE_USER`](#hide_user), [`MAX_HIDE_PIDS`](#max_hide_pids), [`PID_FILE_PATH`](#pid_file_path)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class original_dirent
    <<type_alias>> original_dirent
    class linux_dirent64
    <<struct>> linux_dirent64
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_rootkit_mrhyde2_c__load_hidden_pids(["load_hidden_pids"])
    n_modules_rootkit_mrhyde2_c__fopen(["fopen"])
    n_modules_rootkit_mrhyde2_c__kill(["kill"])
    n_modules_rootkit_mrhyde2_c__get_username_from_pid(["get_username_from_pid"])
    n_modules_rootkit_mrhyde2_c__stat(["stat"])
    n_modules_rootkit_mrhyde2_c__should_hide_pid(["should_hide_pid"])
    n_modules_rootkit_mrhyde2_c__readdir(["readdir"])
    n_modules_rootkit_mrhyde2_c__getdents(["getdents"])
    n_modules_rootkit_mrhyde2_c__getdents64(["getdents64"])
    n_modules_rootkit_mrhyde2_c__main(["main"])
    n_modules_rootkit_mrhyde2_c__load_hidden_pids --> n_modules_rootkit_mrhyde2_c__fopen
    n_modules_rootkit_mrhyde2_c__kill --> n_modules_rootkit_mrhyde2_c__load_hidden_pids
    n_modules_rootkit_mrhyde2_c__get_username_from_pid --> n_modules_rootkit_mrhyde2_c__stat
    n_modules_rootkit_mrhyde2_c__should_hide_pid --> n_modules_rootkit_mrhyde2_c__get_username_from_pid
    n_modules_rootkit_mrhyde2_c__should_hide_pid --> n_modules_rootkit_mrhyde2_c__load_hidden_pids
    n_modules_rootkit_mrhyde2_c__readdir --> n_modules_rootkit_mrhyde2_c__load_hidden_pids
    n_modules_rootkit_mrhyde2_c__readdir --> n_modules_rootkit_mrhyde2_c__should_hide_pid
    n_modules_rootkit_mrhyde2_c__getdents --> n_modules_rootkit_mrhyde2_c__should_hide_pid
    n_modules_rootkit_mrhyde2_c__getdents64 --> n_modules_rootkit_mrhyde2_c__should_hide_pid
    n_modules_rootkit_mrhyde2_c__main --> n_modules_rootkit_mrhyde2_c__get_username_from_pid
    n_modules_rootkit_mrhyde2_c__main --> n_modules_rootkit_mrhyde2_c__readdir
```

## Structs

<a id="linux_dirent64"></a>

### `linux_dirent64`

`struct` | [modules/rootkit/mrhyde2.c:465](../../modules/rootkit/mrhyde2.c#L465)

```c
struct linux_dirent64
```

---

## Type Aliases

<a id="original_dirent"></a>

### `original_dirent`

`type_alias` | [modules/rootkit/mrhyde2.c:52](../../modules/rootkit/mrhyde2.c#L52)

```c
typedef struct dirent original_dirent;
```

ifndef HIDE_DIR define HIDE_DIR ".rootkit_dir" endif ifndef HIDE_USER define HIDE_USER "rootkit_user" endif define MAX_HIDE_PIDS 140 define PID_FILE_PATH "/dev/shm/pid"

---

## Functions

<a id="load_hidden_pids"></a>

### `load_hidden_pids`

`function` | [modules/rootkit/mrhyde2.c:67](../../modules/rootkit/mrhyde2.c#L67)

```c
void load_hidden_pids()
```

*Calls:* [`fopen`](#fopen)

*Called by:* [`kill`](#kill), [`readdir`](#readdir), [`should_hide_pid`](#should_hide_pid)

---

<a id="unlink"></a>

### `unlink`

`function` | [modules/rootkit/mrhyde2.c:87](../../modules/rootkit/mrhyde2.c#L87)

```c
int unlink(const char *pathname)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pathname` | `char *` |  |  |

**Returns:** `int`

---

<a id="kill"></a>

### `kill`

`function` | [modules/rootkit/mrhyde2.c:99](../../modules/rootkit/mrhyde2.c#L99)

```c
int kill(pid_t pid, int sig)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pid` | `pid_t` |  |  |
| `sig` | `int` |  |  |

**Returns:** `int`

*Calls:* [`load_hidden_pids`](#load_hidden_pids)

---

<a id="remove"></a>

### `remove`

`function` | [modules/rootkit/mrhyde2.c:119](../../modules/rootkit/mrhyde2.c#L119)

```c
int remove(const char *pathname)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pathname` | `char *` |  |  |

**Returns:** `int`

---

<a id="unlinkat"></a>

### `unlinkat`

`function` | [modules/rootkit/mrhyde2.c:131](../../modules/rootkit/mrhyde2.c#L131)

```c
int unlinkat(int dirfd, const char *pathname, int flags)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `dirfd` | `int` |  |  |
| `pathname` | `char *` |  |  |
| `flags` | `int` |  |  |

**Returns:** `int`

---

<a id="get_username_from_pid"></a>

### `get_username_from_pid`

`function` | [modules/rootkit/mrhyde2.c:152](../../modules/rootkit/mrhyde2.c#L152)

```c
char* get_username_from_pid(pid_t pid)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pid` | `pid_t` |  |  |

**Returns:** `char*`

*Calls:* [`stat`](#stat)

*Called by:* [`main`](#main), [`should_hide_pid`](#should_hide_pid)

---

<a id="should_hide_pid"></a>

### `should_hide_pid`

`function` | [modules/rootkit/mrhyde2.c:171](../../modules/rootkit/mrhyde2.c#L171)

```c
int should_hide_pid(const char* pid)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pid` | `char*` |  |  |

**Returns:** `int`

*Calls:* [`get_username_from_pid`](#get_username_from_pid), [`load_hidden_pids`](#load_hidden_pids)

*Called by:* [`getdents`](#getdents), [`getdents64`](#getdents64), [`readdir`](#readdir)

---

<a id="readdir"></a>

### `readdir`

`function` | [modules/rootkit/mrhyde2.c:186](../../modules/rootkit/mrhyde2.c#L186)

```c
struct dirent* readdir(DIR* dirp)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `dirp` | `DIR*` |  |  |

**Returns:** `dirent*`

*Calls:* [`load_hidden_pids`](#load_hidden_pids), [`should_hide_pid`](#should_hide_pid)

*Called by:* [`main`](#main)

---

<a id="fopen"></a>

### `fopen`

`function` | [modules/rootkit/mrhyde2.c:242](../../modules/rootkit/mrhyde2.c#L242)

```c
FILE *fopen(const char *pathname, const char *mode)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pathname` | `char *` |  |  |
| `mode` | `char *` |  |  |

**Returns:** `FILE *`

*Called by:* [`load_hidden_pids`](#load_hidden_pids)

---

<a id="my_open"></a>

### `my_open`

`function` | [modules/rootkit/mrhyde2.c:279](../../modules/rootkit/mrhyde2.c#L279)

```c
int my_open(const char *pathname, int flags, mode_t mode)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pathname` | `char *` |  |  |
| `flags` | `int` |  |  |
| `mode` | `mode_t` |  |  |

**Returns:** `int`

---

<a id="my_openat"></a>

### `my_openat`

`function` | [modules/rootkit/mrhyde2.c:316](../../modules/rootkit/mrhyde2.c#L316)

```c
int my_openat(int dirfd, const char *pathname, int flags, mode_t mode)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `dirfd` | `int` |  |  |
| `pathname` | `char *` |  |  |
| `flags` | `int` |  |  |
| `mode` | `mode_t` |  |  |

**Returns:** `int`

---

<a id="stat"></a>

### `stat`

`function` | [modules/rootkit/mrhyde2.c:353](../../modules/rootkit/mrhyde2.c#L353)

```c
int stat(const char *pathname, struct stat *statbuf)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pathname` | `char *` |  |  |
| `statbuf` | `struct stat *` |  |  |

**Returns:** `int`

*Called by:* [`get_username_from_pid`](#get_username_from_pid)

---

<a id="lstat"></a>

### `lstat`

`function` | [modules/rootkit/mrhyde2.c:390](../../modules/rootkit/mrhyde2.c#L390)

```c
int lstat(const char *pathname, struct stat *statbuf)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pathname` | `char *` |  |  |
| `statbuf` | `struct stat *` |  |  |

**Returns:** `int`

---

<a id="fstat"></a>

### `fstat`

`function` | [modules/rootkit/mrhyde2.c:427](../../modules/rootkit/mrhyde2.c#L427)

```c
int fstat(int fd, struct stat *statbuf)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `fd` | `int` |  |  |
| `statbuf` | `struct stat *` |  |  |

**Returns:** `int`

---

<a id="getdents"></a>

### `getdents`

`function` | [modules/rootkit/mrhyde2.c:474](../../modules/rootkit/mrhyde2.c#L474)

```c
int getdents(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `fd` | `unsigned int` |  |  |
| `dirp` | `struct linux_dirent64 *` |  |  |
| `count` | `unsigned int` |  |  |

**Returns:** `int`

*Calls:* [`should_hide_pid`](#should_hide_pid)

---

<a id="getdents64"></a>

### `getdents64`

`function` | [modules/rootkit/mrhyde2.c:531](../../modules/rootkit/mrhyde2.c#L531)

```c
int getdents64(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `fd` | `unsigned int` |  |  |
| `dirp` | `struct linux_dirent64 *` |  |  |
| `count` | `unsigned int` |  |  |

**Returns:** `int`

*Calls:* [`should_hide_pid`](#should_hide_pid)

---

<a id="main"></a>

### `main`

`function` | [modules/rootkit/mrhyde2.c:587](../../modules/rootkit/mrhyde2.c#L587)

```c
int main()
```

**Returns:** `int`

*Calls:* [`get_username_from_pid`](#get_username_from_pid), [`readdir`](#readdir)

---

## Macros

<a id="hidden_dir"></a>

### `HIDDEN_DIR`

`macro` | [modules/rootkit/mrhyde2.c:31](../../modules/rootkit/mrhyde2.c#L31)

```c
#define HIDDEN_DIR
```

---

<a id="hidden_file"></a>

### `HIDDEN_FILE`

`macro` | [modules/rootkit/mrhyde2.c:32](../../modules/rootkit/mrhyde2.c#L32)

```c
#define HIDDEN_FILE
```

---

<a id="hidden_file1"></a>

### `HIDDEN_FILE1`

`macro` | [modules/rootkit/mrhyde2.c:33](../../modules/rootkit/mrhyde2.c#L33)

```c
#define HIDDEN_FILE1
```

---

<a id="hidden_file2"></a>

### `HIDDEN_FILE2`

`macro` | [modules/rootkit/mrhyde2.c:34](../../modules/rootkit/mrhyde2.c#L34)

```c
#define HIDDEN_FILE2
```

---

<a id="hidden_file3"></a>

### `HIDDEN_FILE3`

`macro` | [modules/rootkit/mrhyde2.c:35](../../modules/rootkit/mrhyde2.c#L35)

```c
#define HIDDEN_FILE3
```

---

<a id="hidden_file4"></a>

### `HIDDEN_FILE4`

`macro` | [modules/rootkit/mrhyde2.c:36](../../modules/rootkit/mrhyde2.c#L36)

```c
#define HIDDEN_FILE4
```

---

<a id="hidden_file5"></a>

### `HIDDEN_FILE5`

`macro` | [modules/rootkit/mrhyde2.c:37](../../modules/rootkit/mrhyde2.c#L37)

```c
#define HIDDEN_FILE5
```

---

<a id="hidden_file6"></a>

### `HIDDEN_FILE6`

`macro` | [modules/rootkit/mrhyde2.c:38](../../modules/rootkit/mrhyde2.c#L38)

```c
#define HIDDEN_FILE6
```

---

<a id="hidden_file7"></a>

### `HIDDEN_FILE7`

`macro` | [modules/rootkit/mrhyde2.c:39](../../modules/rootkit/mrhyde2.c#L39)

```c
#define HIDDEN_FILE7
```

---

<a id="hidden_file8"></a>

### `HIDDEN_FILE8`

`macro` | [modules/rootkit/mrhyde2.c:40](../../modules/rootkit/mrhyde2.c#L40)

```c
#define HIDDEN_FILE8
```

---

<a id="hidden_file9"></a>

### `HIDDEN_FILE9`

`macro` | [modules/rootkit/mrhyde2.c:41](../../modules/rootkit/mrhyde2.c#L41)

```c
#define HIDDEN_FILE9
```

---

<a id="pathmrhyde"></a>

### `PATHMRHYDE`

`macro` | [modules/rootkit/mrhyde2.c:42](../../modules/rootkit/mrhyde2.c#L42)

```c
#define PATHMRHYDE
```

---

<a id="hide_dir"></a>

### `HIDE_DIR`

`macro` | [modules/rootkit/mrhyde2.c:45](../../modules/rootkit/mrhyde2.c#L45)

```c
#define HIDE_DIR
```

---

<a id="hide_user"></a>

### `HIDE_USER`

`macro` | [modules/rootkit/mrhyde2.c:48](../../modules/rootkit/mrhyde2.c#L48)

```c
#define HIDE_USER
```

---

<a id="max_hide_pids"></a>

### `MAX_HIDE_PIDS`

`macro` | [modules/rootkit/mrhyde2.c:50](../../modules/rootkit/mrhyde2.c#L50)

```c
#define MAX_HIDE_PIDS
```

---

<a id="pid_file_path"></a>

### `PID_FILE_PATH`

`macro` | [modules/rootkit/mrhyde2.c:51](../../modules/rootkit/mrhyde2.c#L51)

```c
#define PID_FILE_PATH
```

---
