# `modules.dashboard_bp`

> Source: [modules/dashboard_bp.py:1](../../modules/dashboard_bp.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

modules/dashboard_bp.py ======================== Real-time SOC dashboard as a Flask Blueprint.

Registration (one line in lazyc2.py after app creation):
    from modules.dashboard_bp import dashboard_bp
    app.register_blueprint(dashboard_bp)

Then visit: http://localhost:4444/dashboard/

## Contents

- **Functions:** [`dashboard_index`](#dashboard_index), [`dashboard_api_data`](#dashboard_api_data), [`dashboard_loot`](#dashboard_loot), [`dashboard_timeline`](#dashboard_timeline)
- **Constants:** [`TACTICS`](#tactics)

## Functions

<a id="dashboard_index"></a>

### `dashboard_index`

`function` | [modules/dashboard_bp.py:778](../../modules/dashboard_bp.py#L778)

Decorators: `@dashboard_bp.route('/')`

```python
def dashboard_index()
```

Render the main SOC dashboard HTML page.

---

<a id="dashboard_api_data"></a>

### `dashboard_api_data`

`function` | [modules/dashboard_bp.py:784](../../modules/dashboard_bp.py#L784)

Decorators: `@dashboard_bp.route('/api/data')`

```python
def dashboard_api_data()
```

JSON snapshot of all dashboard data.

Reads directly from sessions/ files so it can be used even without
the full lazyc2.py runtime context (e.g. during testing).

---

<a id="dashboard_loot"></a>

### `dashboard_loot`

`function` | [modules/dashboard_bp.py:902](../../modules/dashboard_bp.py#L902)

Decorators: `@dashboard_bp.route('/loot')`

```python
def dashboard_loot()
```

Render the loot browser: captured credentials, hashes and files.

---

<a id="dashboard_timeline"></a>

### `dashboard_timeline`

`function` | [modules/dashboard_bp.py:1017](../../modules/dashboard_bp.py#L1017)

Decorators: `@dashboard_bp.route('/timeline')`

```python
def dashboard_timeline()
```

Render the campaign timeline: commands and events, newest first.

---

## Constants

<a id="tactics"></a>

### `TACTICS`

`constant` | [modules/dashboard_bp.py:46](../../modules/dashboard_bp.py#L46)

```python
TACTICS
```

---
