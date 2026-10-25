# Extended Parameters

Every `.yaml` file in this directory is loaded at shell startup and merged
into `self.params`. This allows adding new configuration keys for lazyaddons,
aliases, and pipelines without modifying `payload.json` or Python source.

## How to add a parameter

1. Create a new `.yaml` file in this directory (or edit an existing one).
2. Add your key-value pair:
   ```yaml
   my_custom_key: "my_default_value"
   ```
3. Reference it as `{my_custom_key}` in any lazyaddon `execute_command`,
   `install_command`, `lazycommand`, or alias template.

A mapping entry contributes its `default` value; a flat entry contributes its
value as-is:

```yaml
my_custom_key:
  kind: string          # string|integer|boolean|url|path|ip|port|hostname
  default: "my_default_value"
  description: "What the operator is expected to set"
  category: general
```

## Declared parameters (recommended)

`operator.yaml` is the operator-managed registry. Declare a parameter there
and it is reusable by every addon, alias and pipeline — no source edit, no
addon-branded key:

```bash
param create c2_profile --kind string --default "default" --desc "C2 profile name"
# or: lazy_orchestrator -> Params tab -> a
```

The registry is the single source of truth for operator parameters:
`core/param_registry.py` owns the CRUD, `core/payload_schema.py` projects the
declarations into the payload schema and `lazyc2/addon_creator.py` accepts
them as addon placeholders. Never hand-edit those files to register an
operator parameter.

## Load order

Files are loaded in alphabetical order and merged shallowly. Later files
override earlier ones. The built-in `payload.json` keys take precedence
over extended params (loaded first, so extended params cannot override payload.json).
