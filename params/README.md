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

## Load order

Files are loaded in alphabetical order and merged shallowly. Later files
override earlier ones. The built-in `payload.json` keys take precedence
over extended params (loaded first, so extended params cannot override payload.json).
