# modules_ext

External module extensions that ship as separate subprojects. Each
subdirectory is an independent component with its own build system, designed
to be cloned or updated independently of the main framework.

## Subdirectories

| Directory | Description |
|-----------|-------------|
| `lazyown_infinitestorage/` | Infinite storage proof-of-concept module. Encodes and decodes arbitrary data into alternative storage channels. See its own `README.md`. |
| `rustrevmaker/` | Rust-based reverse shell generator. Produces small, statically-linked ELF and PE binaries. Faster startup and smaller footprint than Go alternatives. |

## Integration

Modules in `modules_ext/` are not imported automatically. Each one provides
a standalone binary or script that the CLI invokes via `run_command()` or
a dedicated `do_*` command in `lazyown.py`.

To use `rustrevmaker`:

```bash
cd modules_ext/rustrevmaker
cargo build --release
cp target/release/rustrevmaker ../../sessions/
```

Then from the CLI:

```
(LazyOwn) > run sessions/rustrevmaker --lhost {lhost} --lport {lport}
```

## Adding a new external module

1. Create a subdirectory with a descriptive name.
2. Include a `README.md` that documents the build process and usage.
3. Add a `lazyaddon` YAML if the module should be accessible via
   `lazyaddons/` and the standard addon install flow.
4. Do not add the subdirectory's build artefacts to `.gitignore` at the repo
   root — manage them inside the subdirectory.
