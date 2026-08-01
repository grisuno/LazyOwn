# external/

Directory stores external tool dependencies that cannot be pip-installed.
Each subdirectory contains one tool, typically a compiled exploit, a C
source tree with Makefile, or a vendored Go/Rust binary.

## Layout

```
external/
  .exploit/           # Third-party exploit PoCs and tooling
    CVE-YYYY-NNNNN/   # One CVE per directory
    <tool-name>/      # One tool per directory
```

## Adding a new external tool

1. Create a subdirectory under `external/.exploit/<tool-name>/`.
2. Place all tool files (source, binaries, Makefiles, README) inside it.
3. If the tool requires compilation, include a Makefile and document build
   dependencies in the tool's own README.
4. Run `bash external/install_external.sh` or follow the tool's own build
   instructions.
5. Do not commit large binaries to git. Add them to `.gitignore` if needed.

## Updating existing tools

1. Navigate to the tool's subdirectory.
2. Pull or download the latest release from the upstream repository.
3. Rebuild if necessary (follow the tool's Makefile or build docs).
4. Test the updated tool against a lab target before using in an engagement.
