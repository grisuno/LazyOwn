# `modules/win_rootkit/win_ring3_rootkit.cpp`

> Source: [modules/win_rootkit/win_ring3_rootkit.cpp:1](../../modules/win_rootkit/win_ring3_rootkit.cpp#L1) | language `cpp` | coverage 0.0% | [API index](../index.md)

## Contents

- **Functions:** [`get_username_from_pid`](#get_username_from_pid), [`should_hide_pid`](#should_hide_pid), [`hook_FindFirstFile`](#hook_findfirstfile), [`hook_CreateFile`](#hook_createfile), [`DllMain`](#dllmain)
- **Macros:** [`HIDDEN_DIR`](#hidden_dir), [`HIDDEN_FILE`](#hidden_file), [`HIDE_USER`](#hide_user), [`MAX_HIDE_PIDS`](#max_hide_pids)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_modules_win_rootkit_win_ring3_rootkit_cpp__should_hide_pid(["should_hide_pid"])
    n_modules_win_rootkit_win_ring3_rootkit_cpp__get_username_from_pid(["get_username_from_pid"])
    n_modules_win_rootkit_win_ring3_rootkit_cpp__should_hide_pid --> n_modules_win_rootkit_win_ring3_rootkit_cpp__get_username_from_pid
```

## Functions

<a id="get_username_from_pid"></a>

### `get_username_from_pid`

`function` | [modules/win_rootkit/win_ring3_rootkit.cpp:42](../../modules/win_rootkit/win_ring3_rootkit.cpp#L42)

```cpp
char* get_username_from_pid(DWORD pid)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pid` | `DWORD` |  |  |

**Returns:** `char*`

*Called by:* [`should_hide_pid`](#should_hide_pid)

---

<a id="should_hide_pid"></a>

### `should_hide_pid`

`function` | [modules/win_rootkit/win_ring3_rootkit.cpp:65](../../modules/win_rootkit/win_ring3_rootkit.cpp#L65)

```cpp
int should_hide_pid(const char* pid)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `pid` | `char*` |  |  |

**Returns:** `int`

*Calls:* [`get_username_from_pid`](#get_username_from_pid)

---

<a id="hook_findfirstfile"></a>

### `hook_FindFirstFile`

`function` | [modules/win_rootkit/win_ring3_rootkit.cpp:75](../../modules/win_rootkit/win_ring3_rootkit.cpp#L75)

```cpp
HANDLE WINAPI hook_FindFirstFile(CONST char* path, WIN32_FIND_DATA* find_data)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `CONST char*` |  |  |
| `find_data` | `WIN32_FIND_DATA*` |  |  |

**Returns:** `HANDLE WINAPI`

---

<a id="hook_createfile"></a>

### `hook_CreateFile`

`function` | [modules/win_rootkit/win_ring3_rootkit.cpp:85](../../modules/win_rootkit/win_ring3_rootkit.cpp#L85)

```cpp
HANDLE WINAPI hook_CreateFile(CONST char* path, DWORD access, DWORD share, LPSECURITY_ATTRIBUTES security, DWORD creation, DWORD flags, HANDLE template)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `CONST char*` |  |  |
| `access` | `DWORD` |  |  |
| `share` | `DWORD` |  |  |
| `security` | `LPSECURITY_ATTRIBUTES` |  |  |
| `creation` | `DWORD` |  |  |
| `flags` | `DWORD` |  |  |
| `template` | `HANDLE` |  |  |

**Returns:** `HANDLE WINAPI`

---

<a id="dllmain"></a>

### `DllMain`

`function` | [modules/win_rootkit/win_ring3_rootkit.cpp:94](../../modules/win_rootkit/win_ring3_rootkit.cpp#L94)

```cpp
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `hModule` | `HMODULE` |  |  |
| `ul_reason_for_call` | `DWORD` |  |  |
| `lpReserved` | `LPVOID` |  |  |

**Returns:** `BOOL APIENTRY`

---

## Macros

<a id="hidden_dir"></a>

### `HIDDEN_DIR`

`macro` | [modules/win_rootkit/win_ring3_rootkit.cpp:32](../../modules/win_rootkit/win_ring3_rootkit.cpp#L32)

```cpp
#define HIDDEN_DIR
```

---

<a id="hidden_file"></a>

### `HIDDEN_FILE`

`macro` | [modules/win_rootkit/win_ring3_rootkit.cpp:33](../../modules/win_rootkit/win_ring3_rootkit.cpp#L33)

```cpp
#define HIDDEN_FILE
```

---

<a id="hide_user"></a>

### `HIDE_USER`

`macro` | [modules/win_rootkit/win_ring3_rootkit.cpp:34](../../modules/win_rootkit/win_ring3_rootkit.cpp#L34)

```cpp
#define HIDE_USER
```

---

<a id="max_hide_pids"></a>

### `MAX_HIDE_PIDS`

`macro` | [modules/win_rootkit/win_ring3_rootkit.cpp:35](../../modules/win_rootkit/win_ring3_rootkit.cpp#L35)

```cpp
#define MAX_HIDE_PIDS
```

---
