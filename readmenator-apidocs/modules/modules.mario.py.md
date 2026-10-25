# `modules.mario`

> Source: [modules/mario.py:1](../../modules/mario.py#L1) | language `py` | coverage 0.0% | [API index](../index.md)

## Contents

- **Functions:** [`check_collision`](#check_collision)
- **Constants:** [`SCREEN_WIDTH`](#screen_width), [`SCREEN_HEIGHT`](#screen_height), [`FONT_PATH`](#font_path), [`MARIO`](#mario), [`BLOCK`](#block), [`PIPE`](#pipe), [`GOOMBA`](#goomba), [`TURTLE`](#turtle), [`GROUND`](#ground), [`SKY`](#sky), [`CLOUD`](#cloud), [`BUSH`](#bush), [`MOUNTAIN`](#mountain), [`COIN`](#coin), [`BRICK`](#brick), [`FLAGPOLE`](#flagpole), [`CASTLE`](#castle), [`SUN`](#sun), [`FLOWER`](#flower), [`TREE`](#tree), [`TILE_SIZE`](#tile_size), [`LEVEL_WIDTH`](#level_width), [`LEVEL_HEIGHT`](#level_height), [`BACKGROUND`](#background), [`MIDDLEGROUND`](#middleground), [`FOREGROUND`](#foreground), [`GRAVITY`](#gravity), [`JUMP_SPEED`](#jump_speed), [`MAX_VX`](#max_vx), [`ACCEL`](#accel), [`FRICTION`](#friction)

## Functions

<a id="check_collision"></a>

### `check_collision`

`function` | [modules/mario.py:105](../../modules/mario.py#L105)

```python
def check_collision(x, y, layer=FOREGROUND)
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `x` |  |  |  |
| `y` |  |  |  |
| `layer` |  | `FOREGROUND` |  |

---

## Constants

<a id="screen_width"></a>

### `SCREEN_WIDTH`

`constant` | [modules/mario.py:8](../../modules/mario.py#L8)

```python
SCREEN_WIDTH = 800
```

---

<a id="screen_height"></a>

### `SCREEN_HEIGHT`

`constant` | [modules/mario.py:9](../../modules/mario.py#L9)

```python
SCREEN_HEIGHT = 480
```

---

<a id="font_path"></a>

### `FONT_PATH`

`constant` | [modules/mario.py:15](../../modules/mario.py#L15)

```python
FONT_PATH = os.path.join(os.path.dirname(__file__), 'NotoEmoji-Regular.ttf')
```

---

<a id="mario"></a>

### `MARIO`

`constant` | [modules/mario.py:26](../../modules/mario.py#L26)

```python
MARIO = '🏃'
```

---

<a id="block"></a>

### `BLOCK`

`constant` | [modules/mario.py:27](../../modules/mario.py#L27)

```python
BLOCK = '🧱'
```

---

<a id="pipe"></a>

### `PIPE`

`constant` | [modules/mario.py:28](../../modules/mario.py#L28)

```python
PIPE = '🚪'
```

---

<a id="goomba"></a>

### `GOOMBA`

`constant` | [modules/mario.py:29](../../modules/mario.py#L29)

```python
GOOMBA = '👾'
```

---

<a id="turtle"></a>

### `TURTLE`

`constant` | [modules/mario.py:30](../../modules/mario.py#L30)

```python
TURTLE = '🐢'
```

---

<a id="ground"></a>

### `GROUND`

`constant` | [modules/mario.py:31](../../modules/mario.py#L31)

```python
GROUND = '⬜'
```

---

<a id="sky"></a>

### `SKY`

`constant` | [modules/mario.py:32](../../modules/mario.py#L32)

```python
SKY = '  '
```

---

<a id="cloud"></a>

### `CLOUD`

`constant` | [modules/mario.py:33](../../modules/mario.py#L33)

```python
CLOUD = '☁️'
```

---

<a id="bush"></a>

### `BUSH`

`constant` | [modules/mario.py:34](../../modules/mario.py#L34)

```python
BUSH = '🌳'
```

---

<a id="mountain"></a>

### `MOUNTAIN`

`constant` | [modules/mario.py:35](../../modules/mario.py#L35)

```python
MOUNTAIN = '🏔️'
```

---

<a id="coin"></a>

### `COIN`

`constant` | [modules/mario.py:36](../../modules/mario.py#L36)

```python
COIN = '🪙'
```

---

<a id="brick"></a>

### `BRICK`

`constant` | [modules/mario.py:37](../../modules/mario.py#L37)

```python
BRICK = '🟫'
```

---

<a id="flagpole"></a>

### `FLAGPOLE`

`constant` | [modules/mario.py:38](../../modules/mario.py#L38)

```python
FLAGPOLE = '🏁'
```

---

<a id="castle"></a>

### `CASTLE`

`constant` | [modules/mario.py:39](../../modules/mario.py#L39)

```python
CASTLE = '🏰'
```

---

<a id="sun"></a>

### `SUN`

`constant` | [modules/mario.py:40](../../modules/mario.py#L40)

```python
SUN = '☀️'
```

---

<a id="flower"></a>

### `FLOWER`

`constant` | [modules/mario.py:41](../../modules/mario.py#L41)

```python
FLOWER = '🌸'
```

---

<a id="tree"></a>

### `TREE`

`constant` | [modules/mario.py:42](../../modules/mario.py#L42)

```python
TREE = '🌲'
```

---

<a id="tile_size"></a>

### `TILE_SIZE`

`constant` | [modules/mario.py:45](../../modules/mario.py#L45)

```python
TILE_SIZE = 32
```

---

<a id="level_width"></a>

### `LEVEL_WIDTH`

`constant` | [modules/mario.py:46](../../modules/mario.py#L46)

```python
LEVEL_WIDTH = 150 * TILE_SIZE
```

---

<a id="level_height"></a>

### `LEVEL_HEIGHT`

`constant` | [modules/mario.py:47](../../modules/mario.py#L47)

```python
LEVEL_HEIGHT = 15 * TILE_SIZE
```

---

<a id="background"></a>

### `BACKGROUND`

`constant` | [modules/mario.py:50](../../modules/mario.py#L50)

```python
BACKGROUND = [[SKY] * (LEVEL_WIDTH // TILE_SIZE) for _ in range(LEVEL_HEIGHT // TILE_SIZE)]
```

---

<a id="middleground"></a>

### `MIDDLEGROUND`

`constant` | [modules/mario.py:51](../../modules/mario.py#L51)

```python
MIDDLEGROUND = [[SKY] * (LEVEL_WIDTH // TILE_SIZE) for _ in range(LEVEL_HEIGHT // TILE_SIZE)]
```

---

<a id="foreground"></a>

### `FOREGROUND`

`constant` | [modules/mario.py:52](../../modules/mario.py#L52)

```python
FOREGROUND
```

---

<a id="gravity"></a>

### `GRAVITY`

`constant` | [modules/mario.py:90](../../modules/mario.py#L90)

```python
GRAVITY = 500.0
```

---

<a id="jump_speed"></a>

### `JUMP_SPEED`

`constant` | [modules/mario.py:91](../../modules/mario.py#L91)

```python
JUMP_SPEED = -300.0
```

---

<a id="max_vx"></a>

### `MAX_VX`

`constant` | [modules/mario.py:92](../../modules/mario.py#L92)

```python
MAX_VX = 200.0
```

---

<a id="accel"></a>

### `ACCEL`

`constant` | [modules/mario.py:93](../../modules/mario.py#L93)

```python
ACCEL = 800.0
```

---

<a id="friction"></a>

### `FRICTION`

`constant` | [modules/mario.py:94](../../modules/mario.py#L94)

```python
FRICTION = 600.0
```

---
