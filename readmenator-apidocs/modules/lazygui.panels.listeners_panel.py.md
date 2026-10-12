# `lazygui.panels.listeners_panel`

> Source: [lazygui/panels/listeners_panel.py:1](../../lazygui/panels/listeners_panel.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

Panel that lists the listeners advertised by the backend.

## Contents

- **Classes:** [`ListenersPanel`](#listenerspanel)

## Type Diagram

```mermaid
classDiagram
    direction LR
    class ListenersPanel
    ListenersPanel : __init__()
    class PanelBase
    PanelBase <|-- ListenersPanel
```

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_lazygui_panels_listeners_panel_py__ListenersPanel___init__(["ListenersPanel.__init__"])
    n_lazygui_services_backend_py__Backend_known_listeners["backend.Backend.known_listeners"]
    n_lazygui_widgets_filter_bar_py__FilterBar___init__["filter_bar.FilterBar.__init__"]
    n_lazygui_panels_listeners_panel_py__ListenersPanel___init__ -.-> n_lazygui_services_backend_py__Backend_known_listeners
    n_lazygui_panels_listeners_panel_py__ListenersPanel___init__ -.-> n_lazygui_widgets_filter_bar_py__FilterBar___init__
```

## Classes

<a id="listenerspanel"></a>

### `ListenersPanel`

`class` | [lazygui/panels/listeners_panel.py:21](../../lazygui/panels/listeners_panel.py#L21)

```python
class ListenersPanel(PanelBase)
```

Bases: [`PanelBase`](lazygui.panels.base.py.md#panelbase)

Reactive list of `Listener` rows.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#listenerspanel-__init__) | constructor | Build the layout and subscribe to backend listener updates. |

<a id="listenerspanel-__init__"></a>

#### `ListenersPanel.__init__`

`constructor` | [lazygui/panels/listeners_panel.py:24](../../lazygui/panels/listeners_panel.py#L24)

```python
def __init__(self, constants: AppConstants, backend: Backend, parent: QWidget | None = None) -> None
```

Build the layout and subscribe to backend listener updates.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `constants` | `AppConstants` |  |  |
| `backend` | `Backend` |  |  |
| `parent` | `QWidget \| None` | `None` |  |

*Calls:* [`Backend.known_listeners`](lazygui.services.backend.py.md#backend-known_listeners), [`FilterBar.__init__`](lazygui.widgets.filter_bar.py.md#filterbar-__init__)

*Called by:* [`PanelRegistry.build`](lazygui.panels.registry.py.md#panelregistry-build)

---
