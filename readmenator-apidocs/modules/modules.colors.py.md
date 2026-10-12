# `modules.colors`

> Source: [modules/colors.py:1](../../modules/colors.py#L1) | language `py` | coverage 25.0% | [API index](../index.md)

## Contents

- **Functions:** [`retModel`](#retmodel), [`delete_lines`](#delete_lines), [`no_html`](#no_html)
- **Constants:** [`RESET`](#reset), [`BOLD`](#bold), [`UNDERLINE`](#underline), [`INVERT`](#invert), [`BLINK`](#blink), [`BLACK`](#black), [`RED`](#red), [`GREEN`](#green), [`YELLOW`](#yellow), [`BLUE`](#blue), [`MAGENTA`](#magenta), [`CYAN`](#cyan), [`WHITE`](#white), [`BG_BLACK`](#bg_black), [`BG_RED`](#bg_red), [`BG_GREEN`](#bg_green), [`BG_YELLOW`](#bg_yellow), [`BG_BLUE`](#bg_blue), [`BG_MAGENTA`](#bg_magenta), [`BG_CYAN`](#bg_cyan), [`BG_WHITE`](#bg_white), [`BRIGHT_BLACK`](#bright_black), [`BRIGHT_RED`](#bright_red), [`BRIGHT_GREEN`](#bright_green), [`BRIGHT_YELLOW`](#bright_yellow), [`BRIGHT_BLUE`](#bright_blue), [`BRIGHT_MAGENTA`](#bright_magenta), [`BRIGHT_CYAN`](#bright_cyan), [`BRIGHT_WHITE`](#bright_white), [`COLOR_256`](#color_256), [`BG_COLOR_256`](#bg_color_256), [`TRUE_COLOR`](#true_color), [`BG_TRUE_COLOR`](#bg_true_color)

## Functions

<a id="retmodel"></a>

### `retModel`

`function` | [modules/colors.py:40](../../modules/colors.py#L40)

```python
def retModel()
```

gemma2-9b-it        Google  8,192   -       - llama-3.3-70b-versatile     Meta    128k    32,768  - llama-3.1-8b-instant        Meta    128k    8,192   - gemma2-9b-it        Meta    8,192   -       - llama3-70b-8192     Meta    8,192   -       - llama3-8b-8192      Meta    8,192   -       - mixtral-8x7b-32768  Mistral 32,768

*Called by:* [`resolve_model`](modules.llm_prompts.py.md#resolve_model)

---

<a id="delete_lines"></a>

### `delete_lines`

`function` | [modules/colors.py:68](../../modules/colors.py#L68)

```python
def delete_lines(content, to_delete)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `content` |  |  |  |
| `to_delete` |  |  |  |

---

<a id="no_html"></a>

### `no_html`

`function` | [modules/colors.py:74](../../modules/colors.py#L74)

```python
def no_html(content)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `content` |  |  |  |

---

## Constants

<a id="reset"></a>

### `RESET`

`constant` | [modules/colors.py:5](../../modules/colors.py#L5)

```python
RESET = '\x1b[0m'
```

---

<a id="bold"></a>

### `BOLD`

`constant` | [modules/colors.py:6](../../modules/colors.py#L6)

```python
BOLD = '\x1b[1m'
```

---

<a id="underline"></a>

### `UNDERLINE`

`constant` | [modules/colors.py:7](../../modules/colors.py#L7)

```python
UNDERLINE = '\x1b[4m'
```

---

<a id="invert"></a>

### `INVERT`

`constant` | [modules/colors.py:8](../../modules/colors.py#L8)

```python
INVERT = '\x1b[7m'
```

---

<a id="blink"></a>

### `BLINK`

`constant` | [modules/colors.py:9](../../modules/colors.py#L9)

```python
BLINK = '\x1b[5m'
```

---

<a id="black"></a>

### `BLACK`

`constant` | [modules/colors.py:10](../../modules/colors.py#L10)

```python
BLACK = '\x1b[30m'
```

---

<a id="red"></a>

### `RED`

`constant` | [modules/colors.py:11](../../modules/colors.py#L11)

```python
RED = '\x1b[31m'
```

---

<a id="green"></a>

### `GREEN`

`constant` | [modules/colors.py:12](../../modules/colors.py#L12)

```python
GREEN = '\x1b[32m'
```

---

<a id="yellow"></a>

### `YELLOW`

`constant` | [modules/colors.py:13](../../modules/colors.py#L13)

```python
YELLOW = '\x1b[33m'
```

---

<a id="blue"></a>

### `BLUE`

`constant` | [modules/colors.py:14](../../modules/colors.py#L14)

```python
BLUE = '\x1b[34m'
```

---

<a id="magenta"></a>

### `MAGENTA`

`constant` | [modules/colors.py:15](../../modules/colors.py#L15)

```python
MAGENTA = '\x1b[35m'
```

---

<a id="cyan"></a>

### `CYAN`

`constant` | [modules/colors.py:16](../../modules/colors.py#L16)

```python
CYAN = '\x1b[36m'
```

---

<a id="white"></a>

### `WHITE`

`constant` | [modules/colors.py:17](../../modules/colors.py#L17)

```python
WHITE = '\x1b[37m'
```

---

<a id="bg_black"></a>

### `BG_BLACK`

`constant` | [modules/colors.py:18](../../modules/colors.py#L18)

```python
BG_BLACK = '\x1b[40m'
```

---

<a id="bg_red"></a>

### `BG_RED`

`constant` | [modules/colors.py:19](../../modules/colors.py#L19)

```python
BG_RED = '\x1b[41m'
```

---

<a id="bg_green"></a>

### `BG_GREEN`

`constant` | [modules/colors.py:20](../../modules/colors.py#L20)

```python
BG_GREEN = '\x1b[42m'
```

---

<a id="bg_yellow"></a>

### `BG_YELLOW`

`constant` | [modules/colors.py:21](../../modules/colors.py#L21)

```python
BG_YELLOW = '\x1b[43m'
```

---

<a id="bg_blue"></a>

### `BG_BLUE`

`constant` | [modules/colors.py:22](../../modules/colors.py#L22)

```python
BG_BLUE = '\x1b[44m'
```

---

<a id="bg_magenta"></a>

### `BG_MAGENTA`

`constant` | [modules/colors.py:23](../../modules/colors.py#L23)

```python
BG_MAGENTA = '\x1b[45m'
```

---

<a id="bg_cyan"></a>

### `BG_CYAN`

`constant` | [modules/colors.py:24](../../modules/colors.py#L24)

```python
BG_CYAN = '\x1b[46m'
```

---

<a id="bg_white"></a>

### `BG_WHITE`

`constant` | [modules/colors.py:25](../../modules/colors.py#L25)

```python
BG_WHITE = '\x1b[47m'
```

---

<a id="bright_black"></a>

### `BRIGHT_BLACK`

`constant` | [modules/colors.py:26](../../modules/colors.py#L26)

```python
BRIGHT_BLACK = '\x1b[90m'
```

---

<a id="bright_red"></a>

### `BRIGHT_RED`

`constant` | [modules/colors.py:27](../../modules/colors.py#L27)

```python
BRIGHT_RED = '\x1b[91m'
```

---

<a id="bright_green"></a>

### `BRIGHT_GREEN`

`constant` | [modules/colors.py:28](../../modules/colors.py#L28)

```python
BRIGHT_GREEN = '\x1b[92m'
```

---

<a id="bright_yellow"></a>

### `BRIGHT_YELLOW`

`constant` | [modules/colors.py:29](../../modules/colors.py#L29)

```python
BRIGHT_YELLOW = '\x1b[93m'
```

---

<a id="bright_blue"></a>

### `BRIGHT_BLUE`

`constant` | [modules/colors.py:30](../../modules/colors.py#L30)

```python
BRIGHT_BLUE = '\x1b[94m'
```

---

<a id="bright_magenta"></a>

### `BRIGHT_MAGENTA`

`constant` | [modules/colors.py:31](../../modules/colors.py#L31)

```python
BRIGHT_MAGENTA = '\x1b[95m'
```

---

<a id="bright_cyan"></a>

### `BRIGHT_CYAN`

`constant` | [modules/colors.py:32](../../modules/colors.py#L32)

```python
BRIGHT_CYAN = '\x1b[96m'
```

---

<a id="bright_white"></a>

### `BRIGHT_WHITE`

`constant` | [modules/colors.py:33](../../modules/colors.py#L33)

```python
BRIGHT_WHITE = '\x1b[97m'
```

---

<a id="color_256"></a>

### `COLOR_256`

`constant` | [modules/colors.py:34](../../modules/colors.py#L34)

```python
COLOR_256 = '\x1b[38;5;{}m'
```

---

<a id="bg_color_256"></a>

### `BG_COLOR_256`

`constant` | [modules/colors.py:35](../../modules/colors.py#L35)

```python
BG_COLOR_256 = '\x1b[48;5;{}m'
```

---

<a id="true_color"></a>

### `TRUE_COLOR`

`constant` | [modules/colors.py:36](../../modules/colors.py#L36)

```python
TRUE_COLOR = '\x1b[38;2;{};{};{}m'
```

---

<a id="bg_true_color"></a>

### `BG_TRUE_COLOR`

`constant` | [modules/colors.py:37](../../modules/colors.py#L37)

```python
BG_TRUE_COLOR = '\x1b[48;2;{};{};{}m'
```

---
