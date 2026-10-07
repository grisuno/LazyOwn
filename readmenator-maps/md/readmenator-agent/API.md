# API (page 1 of 20)
Pages: [API.md](API.md), [API_p2.md](API_p2.md), [API_p3.md](API_p3.md), [API_p4.md](API_p4.md), [API_p5.md](API_p5.md), [API_p6.md](API_p6.md), [API_p7.md](API_p7.md), [API_p8.md](API_p8.md), [API_p9.md](API_p9.md), [API_p10.md](API_p10.md), [API_p11.md](API_p11.md), [API_p12.md](API_p12.md), [API_p13.md](API_p13.md), [API_p14.md](API_p14.md), [API_p15.md](API_p15.md), [API_p16.md](API_p16.md), [API_p17.md](API_p17.md), [API_p18.md](API_p18.md), [API_p19.md](API_p19.md), [API_p20.md](API_p20.md)

## DEPLOY.sh
- `increment_version` (function) `DEPLOY.sh:19`
- `update_section_html` (function) `DEPLOY.sh:86` -- Función para actualizar una sección específica
- `get_commit_type` (function) `DEPLOY.sh:190` -- Función para obtener el tipo de cambio basado en el mensaje del commit

## banner.py
Depends on: `utils.py`
- `image_to_bash` (function) `banner.py:25` `def image_to_bash(image_path, image_res)`
- `list_png_files` (function) `banner.py:47` `def list_png_files()`
- `main` (function) `banner.py:56` `def main()`

## bootstrap.sh
- `usage` (function) `bootstrap.sh:70`
- `log` (function) `bootstrap.sh:74`
- `fail` (function) `bootstrap.sh:92`
- `spin_run` (function) `bootstrap.sh:97`
- `can_prompt` (function) `bootstrap.sh:239`
- `ask` (function) `bootstrap.sh:250`
- `update_checkout` (function) `bootstrap.sh:259`
- `backup_payload` (function) `bootstrap.sh:268`
- `clone_fresh` (function) `bootstrap.sh:280`
- `clean_checkout` (function) `bootstrap.sh:286`
- `confirm_clean` (function) `bootstrap.sh:293`
- `ask_new_dir` (function) `bootstrap.sh:303`
- `ask_existing_checkout_action` (function) `bootstrap.sh:315`
- `ask_existing_path_action` (function) `bootstrap.sh:336`
- `resolve_target_dir` (function) `bootstrap.sh:355`
- `ask_launch_mode` (function) `bootstrap.sh:432`

## cli/aliases.py
Depends on: `core/config.py`
Imported by: `cli/__init__.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/mcp_bridge.py`, `cli/commands/misc_migrated.py`, `cli/commands/recon_migrated.py`, `cli/commands/session_ops.py`, `lazyown.py`, `tests/test_cli_command_sets.py`, `tests/test_cli_enhancements.py`
- `_SafeFormatDict.template_placeholders` (method) `cli/aliases.py:56` `def template_placeholders(template)` -- Return the ``{name}`` placeholders referenced by ``template``.
- `_SafeFormatDict.empty_placeholders` (method) `cli/aliases.py:72` `def empty_placeholders(template, context)` -- Return placeholders whose rendered value against ``context`` is empty.
- `_SafeFormatDict.load_aliases` (method) `cli/aliases.py:77` `def load_aliases(payload, path, lazy)` -- Return the cmd2 alias map.

## cli/assign.py
Depends on: `core/payload_schema.py`
Imported by: `cli/commands/command_and_control_migrated.py`, `cli/commands/help_ui.py`, `cli/commands/misc_migrated.py`, `cli/commands/recon_migrated.py`, `cli/commands/session_ops.py`, `static/js/bootstrap-5.3.0.bundle.min.js`, `static/js/chart.min.js`, `static/js/html2pdf.bundle.min.js`, `static/js/popper-2.5.4.min.js`, `static/js/tippy-6.js`, `tests/test_cli_assign.py`, `tests/test_payload_schema.py`
- `apply_assign` (function) `cli/assign.py:36` `def apply_assign(params, key, value)` -- Validate, mutate and persist a single payload assignment.

## cli/auto_crypto.py
Depends on: `core/crypto.py`, `core/logging.py`, `modules/cli_auth.py`
Imported by: `lazyc2.py`, `lazyown.py`, `tests/test_auto_crypto.py`
- `AutoCryptoEngine.__init__` (method) `cli/auto_crypto.py:85` `def __init__(self, config)`
- `AutoCryptoEngine.enabled` (method) `cli/auto_crypto.py:90` `def enabled(self)` -- Whether the engine performs any I/O.
- `AutoCryptoEngine.is_encrypted` (method) `cli/auto_crypto.py:95` `def is_encrypted(self)` -- Check whether session data appears encrypted.
- `AutoCryptoEngine.encrypt_session` (method) `cli/auto_crypto.py:124` `def encrypt_session(self)` -- Encrypt all protected session files.
- `AutoCryptoEngine.decrypt_session` (method) `cli/auto_crypto.py:174` `def decrypt_session(self)` -- Decrypt all protected session files.
- `AutoCryptoEngine.build_password_provider_from_cli_login` (method) `cli/auto_crypto.py:285` `def build_password_provider_from_cli_login()` -- Return a password provider that reads the CLI login session.

## cli/autosuggest.py
Depends on: `core/console.py`, `core/text_utils.py`
Imported by: `cli/commands/misc_migrated.py`, `cli/commands/session_ops.py`, `cli/tips_engine.py`, `lazyown.py`, `tests/test_autosuggest.py`
- `SuggestionProvider.suggest` (method) `cli/autosuggest.py:95` `def suggest(self, context)`
- `CompositeProvider.__init__` (method) `cli/autosuggest.py:105` `def __init__(self, providers)` -- Store the provider chain.
- `CompositeProvider.suggest` (method) `cli/autosuggest.py:115` `def suggest(self, context)` -- Return the best suggestion across the chain, or ``None``.
- `KillChainProvider.__init__` (method) `cli/autosuggest.py:143` `def __init__(self, chain, phase_priority)` -- Configure the provider.
- `KillChainProvider.suggest` (method) `cli/autosuggest.py:162` `def suggest(self, context)` -- Return the first unseen adjacency, or phase fallback, or ``None``.
- `GraphProvider.__init__` (method) `cli/autosuggest.py:197` `def __init__(self, advisor)` -- Configure the provider.
- `GraphProvider.suggest` (method) `cli/autosuggest.py:221` `def suggest(self, context)` -- Query the advisor and adapt the top result to a :class:`Suggestion`.
- `AutoSuggestEngine.__init__` (method) `cli/autosuggest.py:254` `def __init__(self, provider)` -- Store the provider and enabled flag.
- `AutoSuggestEngine.enabled` (method) `cli/autosuggest.py:270` `def enabled(self)` -- Whether the engine refreshes suggestions on each command.
- `AutoSuggestEngine.set_enabled` (method) `cli/autosuggest.py:274` `def set_enabled(self, value)` -- Toggle the engine without losing the provider chain.
- `AutoSuggestEngine.current` (method) `cli/autosuggest.py:284` `def current(self)` -- Return the suggestion last computed, or ``None`` when cleared.
- `AutoSuggestEngine.clear` (method) `cli/autosuggest.py:288` `def clear(self)` -- Drop the active suggestion (called after accept or abort).
- `AutoSuggestEngine.refresh` (method) `cli/autosuggest.py:292` `def refresh(self, context)` -- Recompute the suggestion from the provider chain.
- `AutoSuggestEngine.accept` (method) `cli/autosuggest.py:309` `def accept(self)` -- Return the active command string and clear the suggestion.
- `AutoSuggestEngine.display_text` (method) `cli/autosuggest.py:317` `def display_text(self)` -- Return the ANSI-coloured ghost-text fragment for legacy callers.
- `AutoSuggestEngine.format_hint_line` (method) `cli/autosuggest.py:342` `def format_hint_line(suggestion)` -- Build the dim hint string surfaced after each command.
- `AutoSuggestEngine.render_hint_line` (method) `cli/autosuggest.py:375` `def render_hint_line(engine)` -- Print one dim hint line for the engine's active suggestion.
- `AutoSuggestEngine.build_default_engine` (method) `cli/autosuggest.py:427` `def build_default_engine(advisor, chain, phase_priority)` -- Wire the canonical provider chain used by the cmd2 shell.

## cli/banner_config.py
Depends on: `cli/engagement_hooks.py`, `core/parsers.py`, `core/safe_exec.py`, `modules/cli_auth.py`
Imported by: `cli/commands/misc_migrated.py`, `tests/test_banner_config.py`, `tests/test_fuzzy_picker.py`, `tests/test_prompt_readline_markers.py`, `tests/test_prompt_refresh.py`, `utils.py`
- `ColorRegistry.names` (method) `cli/banner_config.py:170` `def names(self)`
- `ColorRegistry.has` (method) `cli/banner_config.py:173` `def has(self, name)`
- `ColorRegistry.resolve` (method) `cli/banner_config.py:176` `def resolve(self, name)`
- `ColorRegistry.cycle` (method) `cli/banner_config.py:179` `def cycle(self, current, direction)`
- `ColorRegistry.default_name` (method) `cli/banner_config.py:187` `def default_name(self)`
- `GlyphRegistry.slots` (method) `cli/banner_config.py:212` `def slots(self)`
- `GlyphRegistry.choices` (method) `cli/banner_config.py:215` `def choices(self, slot)`
- `GlyphRegistry.has` (method) `cli/banner_config.py:218` `def has(self, slot)`
- `GlyphRegistry.default` (method) `cli/banner_config.py:221` `def default(self, slot)`
- `GlyphRegistry.cycle` (method) `cli/banner_config.py:225` `def cycle(self, slot, current, direction)`
- `SegmentRenderer.spec` (method) `cli/banner_config.py:319` `def spec(self)`
- `SegmentRenderer.render` (method) `cli/banner_config.py:322` `def render(self, ctx, cfg, color, glyphs)`
- `UserHostSegment.render` (method) `cli/banner_config.py:336` `def render(self, ctx, cfg, color, glyphs)`
- `IfaceSegment.render` (method) `cli/banner_config.py:351` `def render(self, ctx, cfg, color, glyphs)`
- `LhostSegment.render` (method) `cli/banner_config.py:370` `def render(self, ctx, cfg, color, glyphs)`
- `RhostSegment.render` (method) `cli/banner_config.py:387` `def render(self, ctx, cfg, color, glyphs)`
- `DomainSegment.render` (method) `cli/banner_config.py:404` `def render(self, ctx, cfg, color, glyphs)`
- `PublicIpSegment.render` (method) `cli/banner_config.py:421` `def render(self, ctx, cfg, color, glyphs)`
- `CwdSegment.render` (method) `cli/banner_config.py:438` `def render(self, ctx, cfg, color, glyphs)`
- `GitSegment.render` (method) `cli/banner_config.py:454` `def render(self, ctx, cfg, color, glyphs)`
- `VenvSegment.render` (method) `cli/banner_config.py:476` `def render(self, ctx, cfg, color, glyphs)`
- `TimeSegment.render` (method) `cli/banner_config.py:493` `def render(self, ctx, cfg, color, glyphs)`
- `KernelSegment.render` (method) `cli/banner_config.py:508` `def render(self, ctx, cfg, color, glyphs)`
- `VersionSegment.render` (method) `cli/banner_config.py:525` `def render(self, ctx, cfg, color, glyphs)`
- `KarmaSegment.render` (method) `cli/banner_config.py:542` `def render(self, ctx, cfg, color, glyphs)`
- `BatteryLoadSegment.render` (method) `cli/banner_config.py:572` `def render(self, ctx, cfg, color, glyphs)`
- `SegmentRegistry.__init__` (method) `cli/banner_config.py:581` `def __init__(self)`
- `SegmentRegistry.register` (method) `cli/banner_config.py:584` `def register(self, segment)`
- `SegmentRegistry.get` (method) `cli/banner_config.py:587` `def get(self, segment_id)`
- `SegmentRegistry.all` (method) `cli/banner_config.py:590` `def all(self)`
- `SegmentRegistry.by_group` (method) `cli/banner_config.py:600` `def by_group(self, group)`
- `SegmentRegistry.build_default_registry` (method) `cli/banner_config.py:604` `def build_default_registry()` -- Return the registry populated with the canonical segment set.
- `BannerSettings.defaults` (method) `cli/banner_config.py:636` `def defaults(cls, registry, color_registry, glyph_registry)`
- `BannerSettings.from_payload` (method) `cli/banner_config.py:651` `def from_payload(cls, registry, payload, key, color_registry, glyph_registry)`
- `BannerSettings.is_enabled` (method) `cli/banner_config.py:685` `def is_enabled(self, segment_id)`
- `BannerSettings.toggle` (method) `cli/banner_config.py:688` `def toggle(self, segment_id)`
- `BannerSettings.enable_all` (method) `cli/banner_config.py:694` `def enable_all(self, registry)`
- `BannerSettings.disable_all` (method) `cli/banner_config.py:697` `def disable_all(self)`
- `BannerSettings.reset_segments` (method) `cli/banner_config.py:700` `def reset_segments(self, registry)`
- `BannerSettings.reset_colors` (method) `cli/banner_config.py:703` `def reset_colors(self, registry)`
- `BannerSettings.reset_color_for` (method) `cli/banner_config.py:706` `def reset_color_for(self, segment_id, registry)`
- `BannerSettings.reset_glyphs` (method) `cli/banner_config.py:711` `def reset_glyphs(self, glyph_registry)`
- `BannerSettings.reset_glyph_for` (method) `cli/banner_config.py:714` `def reset_glyph_for(self, slot, glyph_registry)`
- `BannerSettings.cycle_color` (method) `cli/banner_config.py:718` `def cycle_color(self, segment_id, color_registry, direction)`
- `BannerSettings.cycle_glyph` (method) `cli/banner_config.py:722` `def cycle_glyph(self, slot, glyph_registry, direction)`
- `BannerSettings.to_payload_block` (method) `cli/banner_config.py:726` `def to_payload_block(self)`
- `ContextResolver.__init__` (method) `cli/banner_config.py:741` `def __init__(self, cfg, palette)`
- `ContextResolver.resolve` (method) `cli/banner_config.py:745` `def resolve(self, payload, network)`
- `ContextResolver.default_palette` (method) `cli/banner_config.py:948` `def default_palette()` -- Box-chrome palette used around segment values.
- `BannerRenderer.__init__` (method) `cli/banner_config.py:964` `def __init__(self, config, registry, color_registry, glyph_registry)`
- `BannerRenderer.render` (method) `cli/banner_config.py:976` `def render(self, settings, ctx)`
- `BannerConfigurator.__init__` (method) `cli/banner_config.py:1047` `def __init__(self, config, registry, color_registry, glyph_registry, renderer, ctx, initial)`
- `BannerConfigurator.run` (method) `cli/banner_config.py:1071` `def run(self)`
- `BannerConfigurator.strip_readline_markers` (method) `cli/banner_config.py:1382` `def strip_readline_markers(text, config)` -- Remove readline zero-width markers from prompt text.
- `BannerConfigurator.render_prompt` (method) `cli/banner_config.py:1396` `def render_prompt(payload, config, readline_safe)` -- Render the Neon Box prompt from a payload dictionary.
- `BannerConfigurator.configure_banner_interactive` (method) `cli/banner_config.py:1436` `def configure_banner_interactive(payload, config)` -- Open the multi-tab curses wizard and return updated settings on save.
- `BannerConfigurator.banner_summary` (method) `cli/banner_config.py:1456` `def banner_summary(settings, registry)` -- Return a single-line summary listing enabled segment ids.

## cli/chain_mode.py
Depends on: `cli/noise_verbs.py`, `core/logging.py`
Imported by: `cli/commands/session_ops.py`, `lazyown.py`, `tests/test_chain_mode.py`
- `ChainSuggestion.from_step` (method) `cli/chain_mode.py:191` `def from_step(cls, step)` -- Build a suggestion from a duck-typed resolver step object.
- `ChainModeStore.__init__` (method) `cli/chain_mode.py:250` `def __init__(self, sessions_dir)` -- Store the sessions directory that owns the state file.
- `ChainModeStore.load` (method) `cli/chain_mode.py:258` `def load(self)` -- Return the persisted enabled flag, or ``None`` when unset.
- `ChainModeStore.save` (method) `cli/chain_mode.py:275` `def save(self, enabled)` -- Persist the enabled flag atomically.
- `ChainPromptEngine.__init__` (method) `cli/chain_mode.py:301` `def __init__(self, config, resolver)` -- Wire the engine with its config, resolver and I/O functions.
- `ChainPromptEngine.enabled` (method) `cli/chain_mode.py:335` `def enabled(self)` -- Whether the chain prompt loop is currently active.
- `ChainPromptEngine.steps_run` (method) `cli/chain_mode.py:340` `def steps_run(self)` -- Number of commands executed through the chain this activation.
- `ChainPromptEngine.set_enabled` (method) `cli/chain_mode.py:344` `def set_enabled(self, value, persist)` -- Toggle chain mode and optionally persist the choice.
- `ChainPromptEngine.step` (method) `cli/chain_mode.py:358` `def step(self, last_cmd, phase)` -- Run one chain prompt round for the command that just executed.

## cli/cli_enhancements.py
Imported by: `cli/commands/audit.py`, `lazyown.py`, `tests/test_cli_enhancements.py`
- `PayloadProvider.get` (method) `cli/cli_enhancements.py:43` `def get(self, key, default)`
- `PayloadProvider.keys` (method) `cli/cli_enhancements.py:44` `def keys(self)`
- `CommandLister.commands` (method) `cli/cli_enhancements.py:50` `def commands(self)`
- `TerminalIO.prompt` (method) `cli/cli_enhancements.py:56` `def prompt(self, message, default)`
- `TerminalIO.emit` (method) `cli/cli_enhancements.py:57` `def emit(self, line)`
- `FuzzyCommandIndex.__init__` (method) `cli/cli_enhancements.py:91` `def __init__(self, source)`
- `FuzzyCommandIndex.search` (method) `cli/cli_enhancements.py:94` `def search(self, query, limit)` -- Return the top ``limit`` matches ordered by descending score.
- `PayloadAwareCompleter.__init__` (method) `cli/cli_enhancements.py:164` `def __init__(self, payload, addon_lister, plugin_lister, credential_lister)`
- `PayloadAwareCompleter.complete` (method) `cli/cli_enhancements.py:176` `def complete(self, command, partial)` -- Return suggestions for ``partial`` given the leading ``command``.
- `AliasResolver.expand` (method) `cli/cli_enhancements.py:238` `def expand(self, alias_name, raw_template, payload)` -- Return the alias rendered against the current payload.
- `DynamicAliasResolver.expand` (method) `cli/cli_enhancements.py:255` `def expand(self, alias_name, raw_template, payload)`
- `HotReloader.start` (method) `cli/cli_enhancements.py:274` `def start(self)`
- `HotReloader.stop` (method) `cli/cli_enhancements.py:277` `def stop(self)`
- `AddonHotReloader.__init__` (method) `cli/cli_enhancements.py:288` `def __init__(self, directories, on_change, tick_seconds)`
- `AddonHotReloader.start` (method) `cli/cli_enhancements.py:301` `def start(self)`
- `AddonHotReloader.stop` (method) `cli/cli_enhancements.py:313` `def stop(self)`
- `AddonHotReloader.poll_once` (method) `cli/cli_enhancements.py:319` `def poll_once(self)` -- Run a single scan, fire callbacks for changed paths, return them.
- `LiveStatusTail.parse` (method) `cli/cli_enhancements.py:382` `def parse(self, content)`
- `TranscriptStore.__init__` (method) `cli/cli_enhancements.py:437` `def __init__(self, sessions_dir, capacity, max_output_chars)`
- `TranscriptStore.append` (method) `cli/cli_enhancements.py:451` `def append(self, command, output, artefacts)`
- `TranscriptStore.grep` (method) `cli/cli_enhancements.py:465` `def grep(self, pattern, command_filter, limit, case_insensitive)` -- Return matching lines across all stored outputs.
- `TranscriptStore.list` (method) `cli/cli_enhancements.py:497` `def list(self, limit)`
- `_DefaultTerminalIO.prompt` (method) `cli/cli_enhancements.py:577` `def prompt(self, message, default)`
- `_DefaultTerminalIO.emit` (method) `cli/cli_enhancements.py:584` `def emit(self, line)`
- `InteractiveForm.__init__` (method) `cli/cli_enhancements.py:595` `def __init__(self, io)`
- `InteractiveForm.render` (method) `cli/cli_enhancements.py:598` `def render(self, spec, defaults)`
- `DictPayloadProvider.__init__` (method) `cli/cli_enhancements.py:638` `def __init__(self, data)`
- `DictPayloadProvider.get` (method) `cli/cli_enhancements.py:641` `def get(self, key, default)`
- `DictPayloadProvider.keys` (method) `cli/cli_enhancements.py:644` `def keys(self)`
- `DictPayloadProvider.update` (method) `cli/cli_enhancements.py:647` `def update(self, data)`
- `StaticCommandLister.__init__` (method) `cli/cli_enhancements.py:654` `def __init__(self, commands)`
- `StaticCommandLister.commands` (method) `cli/cli_enhancements.py:657` `def commands(self)`
- `StaticCommandLister.commands_from_cmd2_shell` (method) `cli/cli_enhancements.py:661` `def commands_from_cmd2_shell(shell)` -- Best-effort extraction of CommandInfo entries from a live cmd2 shell.

## cli/command_chain.py
Depends on: `cli/exploration.py`, `cli/reactive_hints.py`
Imported by: `cli/commands/misc_migrated.py`, `lazyown.py`, `skills/lazyown_mcp.py`, `tests/test_command_chain.py`
- `NextStep.to_dict` (method) `cli/command_chain.py:139` `def to_dict(self)` -- Return a JSON-friendly representation of the step.
- `PrerequisiteRegistry.__init__` (method) `cli/command_chain.py:159` `def __init__(self, config)` -- Store the configuration that owns the prerequisite table.
- `PrerequisiteRegistry.prerequisites` (method) `cli/command_chain.py:164` `def prerequisites(self, cmd)` -- Return the ordered list of prerequisite commands for ``cmd``.
- `PrerequisiteRegistry.missing` (method) `cli/command_chain.py:170` `def missing(self, cmd, history)` -- Return prerequisites that have **not** yet appeared in ``history``.
- `StaticNextRegistry.next_for` (method) `cli/command_chain.py:180` `def next_for(self, cmd)` -- Return the deterministic kill-chain successors of ``cmd``.
- `StaticNextRegistry.phase_priority` (method) `cli/command_chain.py:186` `def phase_priority(self, phase)` -- Return the phase-priority verbs used as a fallback.
- `ServiceNextResolver.__init__` (method) `cli/command_chain.py:196` `def __init__(self, config)` -- Store the configuration providing the service follow-up table.
- `ServiceNextResolver.followups` (method) `cli/command_chain.py:201` `def followups(self, services)` -- Return ``(verb, reason)`` pairs for every triggered follow-up.
- `DynamicNextResolver.__init__` (method) `cli/command_chain.py:222` `def __init__(self, config, static_registry, service_resolver, exploration_engine)` -- Wire collaborators together.
- `DynamicNextResolver.resolve` (method) `cli/command_chain.py:236` `def resolve(self, cmd, params, target, phase, limit)` -- Return the ordered, de-duplicated next-step recommendations.
- `CommandChain.__init__` (method) `cli/command_chain.py:338` `def __init__(self, config, prerequisites, next_resolver)` -- Wire collaborators together using the supplied configuration.
- `CommandChain.prev` (method) `cli/command_chain.py:350` `def prev(self, cmd)` -- Return the ordered prerequisite commands for ``cmd``.
- `CommandChain.missing_prerequisites` (method) `cli/command_chain.py:355` `def missing_prerequisites(self, cmd, history)` -- Return prerequisites of ``cmd`` not present in ``history``.
- `CommandChain.next` (method) `cli/command_chain.py:360` `def next(self, cmd, params, target, phase, limit)` -- Return ordered next-step recommendations.
- `CommandChain.chain` (method) `cli/command_chain.py:372` `def chain(self, cmd, params, target, phase, limit)` -- Return a serialisable ``{prev, next}`` view for the given command.

## cli/command_explorer.py
Depends on: `cli/palette.py`, `core/console.py`
Imported by: `cli/commands/help_ui.py`
- `CommandExplorer.__init__` (method) `cli/command_explorer.py:216` `def __init__(self, aliases, params, config)`
- `CommandExplorer.render_goals_overview` (method) `cli/command_explorer.py:227` `def render_goals_overview(self)` -- Print the goals table showing all available categories.
- `CommandExplorer.render_goal_commands` (method) `cli/command_explorer.py:240` `def render_goal_commands(self, goal_key)` -- Print commands for a specific goal.
- `CommandExplorer.render_search` (method) `cli/command_explorer.py:260` `def render_search(self, query)` -- Search commands by keyword across all goals.

## cli/command_form.py
Depends on: `cli/commands/containers.py`, `cli/palette.py`, `cli/themes.py`
Imported by: `tests/test_command_form.py`
- `CommandFormState.fields` (method) `cli/command_form.py:131` `def fields(self)` -- Return the fields associated with :attr:`command_name`.
- `CommandFormState.summary` (method) `cli/command_form.py:139` `def summary(self)` -- Return the command summary from the index, or an empty string.
- `CommandFormState.set_value` (method) `cli/command_form.py:150` `def set_value(self, identifier, value)` -- Update the value of one field.
- `CommandFormState.set_extra_args` (method) `cli/command_form.py:154` `def set_extra_args(self, value)` -- Replace the extra-args buffer.
- `CommandFormState.build_command` (method) `cli/command_form.py:158` `def build_command(self)` -- Return the cmd-line preview string the operator sees.
- `CommandFormState.overrides` (method) `cli/command_form.py:173` `def overrides(self)` -- Return ``[(payload_key, value), ...]`` for fields the operator changed.
- `CommandFormState.verb_line` (method) `cli/command_form.py:188` `def verb_line(self)` -- Return ``"<verb> <extra_args>"`` ready for the shell.
- `CommandFormState.is_valid` (method) `cli/command_form.py:195` `def is_valid(self)` -- Return ``True`` when the command name is known in the index.
- `CommandFormState.build_state` (method) `cli/command_form.py:247` `def build_state(command_name, payload, index, config)` -- Wire the canonical state used by :func:`launch_form`.
- `CommandFormState.launch_form` (method) `cli/command_form.py:262` `def launch_form(command_name, payload, state, runner)` -- Open the form and return the populated state on submit.
- `_CommandFormApp.__init__` (method) `cli/command_form.py:325` `def __init__(self)`
- `_CommandFormApp.compose` (method) `cli/command_form.py:330` `def compose(self)`
- `_CommandFormApp.on_mount` (method) `cli/command_form.py:348` `def on_mount(self)`
- `_CommandFormApp.on_input_changed` (method) `cli/command_form.py:351` `def on_input_changed(self, event)`
- `_CommandFormApp.on_input_submitted` (method) `cli/command_form.py:360` `def on_input_submitted(self, event)`
- `_CommandFormApp.action_submit` (method) `cli/command_form.py:363` `def action_submit(self)`
- `_CommandFormApp.action_cancel` (method) `cli/command_form.py:366` `def action_cancel(self)`

## cli/commands/_base.py
Depends on: `utils.py`
Imported by: `cli/commands/_dormancy.py`, `cli/commands/active_directory.py`, `cli/commands/ai.py`, `cli/commands/anti_forensics.py`, `cli/commands/applocker_bypass.py`, `cli/commands/audit.py`, `cli/commands/automation.py`, `cli/commands/bitm.py`, `cli/commands/bof_registry.py`, `cli/commands/c2_profile.py`, `cli/commands/caldera.py`, `cli/commands/campaign.py`, `cli/commands/catalog.py`, `cli/commands/cicd.py`, `cli/commands/cli_auth.py`, `cli/commands/cloud.py`, `cli/commands/cloud_attacks.py`, `cli/commands/collaboration.py`, `cli/commands/command_and_control.py`, `cli/commands/command_and_control_migrated.py`, `cli/commands/containers.py`, `cli/commands/cred.py`, `cli/commands/cred_migrated.py`, `cli/commands/crystal_ball.py`, `cli/commands/daemon_ctl.py`, `cli/commands/database.py`, `cli/commands/diagnostics.py`, `cli/commands/dns_exfil.py`, `cli/commands/dpapi.py`, `cli/commands/edr_detect.py`, `cli/commands/encoding.py`, `cli/commands/enum.py`, `cli/commands/estorides.py`, `cli/commands/evasive_payload.py`, `cli/commands/exfiltration.py`, `cli/commands/exploit.py`, `cli/commands/exploit_migrated.py`, `cli/commands/exploitgym.py`, `cli/commands/help_ui.py`, `cli/commands/infra.py`, `cli/commands/lab.py`, `cli/commands/lateral.py`, `cli/commands/lateral_migrated.py`, `cli/commands/marketplace.py`, `cli/commands/mcp_bridge.py`, `cli/commands/misc_migrated.py`, `cli/commands/mobile_macos.py`, `cli/commands/module_manager.py`, `cli/commands/nethelpers.py`, `cli/commands/opsec_cleanup.py`, `cli/commands/orchestration.py`, `cli/commands/payload_arsenal.py`, `cli/commands/payload_generation.py`, `cli/commands/persist.py`, `cli/commands/persist_migrated.py`, `cli/commands/phishing_wizard.py`, `cli/commands/pivoting.py`, `cli/commands/postexp.py`, `cli/commands/postexp_migrated.py`, `cli/commands/privilege_escalation.py`, `cli/commands/purple_team.py`, `cli/commands/pwn.py`, `cli/commands/recon.py`, `cli/commands/recon_migrated.py`, `cli/commands/redteam_gym.py`, `cli/commands/resource_scripting.py`, `cli/commands/scan.py`, `cli/commands/scan_migrated.py`, `cli/commands/security.py`, `cli/commands/session_ops.py`, `cli/commands/shellsys.py`, `cli/commands/sleep_obfuscation.py`, `cli/commands/socks_proxy.py`, `cli/commands/supply_chain.py`, `cli/commands/ux.py`, `tests/test_cli_command_sets.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_nethelpers_command_set.py`, `tests/test_prompt_refresh.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
- `extract_flag` (function) `cli/commands/_base.py:34` `def extract_flag(args, flag)` -- Extract ``--flag <value>`` pair shared by CommandSets.
- `LazyOwnCommandSet.params` (method) `cli/commands/_base.py:86` `def params(self)` -- Return the live ``params`` dict owned by the parent shell.
- `LazyOwnCommandSet.payload` (method) `cli/commands/_base.py:97` `def payload(self)` -- Return the parent shell's ``Config`` wrapper when available.

## cli/commands/_dormancy.py
Depends on: `cli/commands/_base.py`
Imported by: `cli/registry.py`, `tests/test_command_set_migration.py`, `tests/test_daemon_ctl_command_set.py`, `tests/test_encoding_command_set.py`, `tests/test_help_ui_command_set.py`, `tests/test_improvements_spec.py`, `tests/test_nethelpers_command_set.py`, `tests/test_session_ops_command_set.py`, `tests/test_shellsys_command_set.py`
- `PendingCommandSet.is_pending` (method) `cli/commands/_dormancy.py:52` `def is_pending(cs_class)` -- Return ``True`` when ``cs_class`` is flagged as a pending migration.

## cli/commands/active_directory.py
Depends on: `cli/commands/_base.py`, `modules/dacl_abuse.py`, `modules/delegation_attacks.py`, `modules/gpo_abuse.py`, `modules/kerberoasting.py`, `modules/kerberos_tickets.py`
- `ActiveDirectoryCommandSet.do_kerberos_ticket` (method) `cli/commands/active_directory.py:24` `def do_kerberos_ticket(self, line)` -- Forge Kerberos tickets for persistence and lateral movement.
- `ActiveDirectoryCommandSet.do_delegation_enum` (method) `cli/commands/active_directory.py:139` `def do_delegation_enum(self, line)` -- Enumerate Kerberos delegation configurations.
- `ActiveDirectoryCommandSet.do_delegation_attack` (method) `cli/commands/active_directory.py:175` `def do_delegation_attack(self, line)` -- Display computed delegation attack paths with exploitation commands.
- `ActiveDirectoryCommandSet.do_dacl_abuse` (method) `cli/commands/active_directory.py:199` `def do_dacl_abuse(self, line)` -- Enumerate and exploit dangerous AD DACL/SACL entries.
- `ActiveDirectoryCommandSet.do_gpo_abuse` (method) `cli/commands/active_directory.py:233` `def do_gpo_abuse(self, line)` -- Enumerate and exploit Group Policy Objects.
- `ActiveDirectoryCommandSet.do_kerberoast` (method) `cli/commands/active_directory.py:277` `def do_kerberoast(self, line)` -- Advanced Kerberoasting — AES-only mode, targeted SPN enumeration.
- `ActiveDirectoryCommandSet.do_adcs_esc` (method) `cli/commands/active_directory.py:324` `def do_adcs_esc(self, line)` -- Check Active Directory Certificate Services for ESC1-ESC13 vulnerabilities.

## cli/commands/ai.py
Depends on: `cli/commands/_base.py`, `cli/confirm.py`, `core/llm_budget.py`, `modules/killchain.py`, `modules/llm_adapter.py`, `modules/llm_factory.py`, `modules/llm_prompts.py`, `utils.py`
Imported by: `tests/test_ai_commands_llm.py`
- `AiCommandSet.do_ask` (method) `cli/commands/ai.py:77` `def do_ask(self, line)` -- Ask the AI a question with current session context pre-loaded.
- `AiCommandSet.do_groq` (method) `cli/commands/ai.py:146` `def do_groq(self, line)` -- Generate a single-line command through the Groq backend.
- `AiCommandSet.do_ai_playbook` (method) `cli/commands/ai.py:177` `def do_ai_playbook(self, line)` -- Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `AiCommandSet.do_ai_toggle` (method) `cli/commands/ai.py:284` `def do_ai_toggle(self, _arg)` -- Toggle the in-process AI assistant on or off.
- `AiCommandSet.do_llm_budget` (method) `cli/commands/ai.py:301` `def do_llm_budget(self, line)` -- Show the LLM daily cost budget, per call token cap, and current spend.

## cli/commands/anti_forensics.py
Depends on: `cli/commands/_base.py`, `cli/confirm.py`, `cli/output_mode.py`, `core/hardening.py`, `utils.py`
- `AntiForensicsCommandSet.do_wipe_logs` (method) `cli/commands/anti_forensics.py:38` `def do_wipe_logs(self, line)` -- Clear system log files on the remote target.
- `AntiForensicsCommandSet.do_wipe_timeline` (method) `cli/commands/anti_forensics.py:103` `def do_wipe_timeline(self, line)` -- Scrub file timestamps and shell history on the target.
- `AntiForensicsCommandSet.do_shred` (method) `cli/commands/anti_forensics.py:150` `def do_shred(self, line)` -- Securely delete files by overwriting before removal.
- `AntiForensicsCommandSet.do_wipe_free` (method) `cli/commands/anti_forensics.py:205` `def do_wipe_free(self, line)` -- Wipe free disk space to prevent forensic file recovery.
- `AntiForensicsCommandSet.do_clean_ad` (method) `cli/commands/anti_forensics.py:242` `def do_clean_ad(self, line)` -- Clear Active Directory event logs and cached Kerberos tickets.
- `AntiForensicsCommandSet.do_cover_tracks` (method) `cli/commands/anti_forensics.py:303` `def do_cover_tracks(self, line)` -- Run all anti-forensics operations in sequence.

## cli/commands/applocker_bypass.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `AppLockerBypassCommandSet.do_applocker_installutil` (method) `cli/commands/applocker_bypass.py:109` `def do_applocker_installutil(self, line)` -- Generate an InstallUtil.exe AppLocker bypass payload.
- `AppLockerBypassCommandSet.do_applocker_msbuild` (method) `cli/commands/applocker_bypass.py:146` `def do_applocker_msbuild(self, line)` -- Generate an MSBuild.exe AppLocker bypass payload.
- `AppLockerBypassCommandSet.do_applocker_regsvcs` (method) `cli/commands/applocker_bypass.py:173` `def do_applocker_regsvcs(self, line)` -- Generate a Regsvcs.exe/Regasm.exe AppLocker bypass payload.
- `AppLockerBypassCommandSet.do_applocker_csc` (method) `cli/commands/applocker_bypass.py:209` `def do_applocker_csc(self, line)` -- Generate a csc.exe compile-and-execute AppLocker bypass.
- `AppLockerBypassCommandSet.do_applocker_mshta` (method) `cli/commands/applocker_bypass.py:240` `def do_applocker_mshta(self, line)` -- Generate an mshta.exe AppLocker bypass payload.
- `AppLockerBypassCommandSet.do_applocker_rundll32` (method) `cli/commands/applocker_bypass.py:269` `def do_applocker_rundll32(self, line)` -- Generate a rundll32.exe AppLocker bypass via SCT scriptlet.
- `AppLockerBypassCommandSet.do_applocker_presentation` (method) `cli/commands/applocker_bypass.py:298` `def do_applocker_presentation(self, line)` -- Generate a PresentationHost.exe AppLocker bypass reference.

## cli/commands/audit.py
Depends on: `cli/cli_enhancements.py`, `cli/commands/_base.py`
Imported by: `tests/test_cli_enhancements.py`
- `AuditCommandSet.__init__` (method) `cli/commands/audit.py:101` `def __init__(self)`
- `AuditCommandSet.do_fz` (method) `cli/commands/audit.py:160` `def do_fz(self, statement)` -- Fuzzy command finder.
- `AuditCommandSet.do_form` (method) `cli/commands/audit.py:178` `def do_form(self, statement)` -- Open an interactive form for a known command.
- `AuditCommandSet.do_status_tail` (method) `cli/commands/audit.py:196` `def do_status_tail(self, statement)` -- Print live progress from the latest sessions/scan_*.partial file.
- `AuditCommandSet.do_grep_log` (method) `cli/commands/audit.py:234` `def do_grep_log(self, statement)` -- Grep recent command outputs.
- `AuditCommandSet.do_reload_addons` (method) `cli/commands/audit.py:263` `def do_reload_addons(self, _statement)` -- Re-scan lazyaddons/ and plugins/ for changes; reloads what's new.
- `AuditCommandSet.do_audit_complete_keys` (method) `cli/commands/audit.py:288` `def do_audit_complete_keys(self, statement)` -- Print payload-aware completion suggestions for a partial command.

## cli/commands/automation.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `modules/conditional_hooks.py`, `modules/credential_reuse.py`, `modules/operator_profiles.py`, `modules/state_manager.py`
- `AutomationCommandSet.do_cred_reuse` (method) `cli/commands/automation.py:24` `def do_cred_reuse(self, line)` -- Analyze captured credentials and suggest spray targets.
- `AutomationCommandSet.do_cred_mark_failed` (method) `cli/commands/automation.py:57` `def do_cred_mark_failed(self, line)` -- Mark a credential as failed against a host.
- `AutomationCommandSet.do_hooks_list` (method) `cli/commands/automation.py:78` `def do_hooks_list(self, line)` -- List all conditional hook rules.
- `AutomationCommandSet.do_hooks_enable` (method) `cli/commands/automation.py:101` `def do_hooks_enable(self, line)` -- Enable or disable a hook rule.
- `AutomationCommandSet.do_hooks_add` (method) `cli/commands/automation.py:129` `def do_hooks_add(self, line)` -- Add a new conditional hook rule (JSON string).
- `AutomationCommandSet.do_hooks_remove` (method) `cli/commands/automation.py:150` `def do_hooks_remove(self, line)` -- Remove a hook rule by name.
- `AutomationCommandSet.do_hooks_fire` (method) `cli/commands/automation.py:172` `def do_hooks_fire(self, line)` -- Manually fire a hook event for testing.
- `AutomationCommandSet.do_operators` (method) `cli/commands/automation.py:202` `def do_operators(self, line)` -- List all operator profiles.
- `AutomationCommandSet.do_operator_create` (method) `cli/commands/automation.py:229` `def do_operator_create(self, line)` -- Create a new operator profile.
- `AutomationCommandSet.do_operator_load` (method) `cli/commands/automation.py:264` `def do_operator_load(self, line)` -- Load effective config for an operator (team baseline + overrides).
- `AutomationCommandSet.do_operator_delete` (method) `cli/commands/automation.py:292` `def do_operator_delete(self, line)` -- Delete an operator profile.
- `AutomationCommandSet.do_hooks` (method) `cli/commands/automation.py:314` `def do_hooks(self, line)` -- Conditional hooks management — list, enable, disable, add, remove rules.

## cli/commands/bitm.py
Depends on: `cli/commands/_base.py`, `modules/bitm_engine.py`, `utils.py`
- `BitMCommandSet.do_bitm` (method) `cli/commands/bitm.py:31` `def do_bitm(self, line)` -- Browser-in-the-Middle attack manager.

## cli/commands/bof_registry.py
Depends on: `cli/commands/_base.py`, `core/config.py`, `modules/beacon_config_builder.py`, `modules/bof_registry.py`, `utils.py`
- `BofMarketplaceCommandSet.do_bof_search` (method) `cli/commands/bof_registry.py:142` `def do_bof_search(self, line)` -- Search the BOF catalog by keyword.
- `BofMarketplaceCommandSet.do_bof_info` (method) `cli/commands/bof_registry.py:163` `def do_bof_info(self, line)` -- Show detailed information about a BOF.
- `BofMarketplaceCommandSet.do_bof_install` (method) `cli/commands/bof_registry.py:196` `def do_bof_install(self, line)` -- Install and compile a BOF, staging it for beacon delivery.
- `BofMarketplaceCommandSet.do_bof_run` (method) `cli/commands/bof_registry.py:226` `def do_bof_run(self, line)` -- Execute a BOF on a connected beacon.
- `BofMarketplaceCommandSet.do_bof_uninstall` (method) `cli/commands/bof_registry.py:267` `def do_bof_uninstall(self, line)` -- Uninstall a BOF and remove its staged file.
- `BofMarketplaceCommandSet.do_bof_list` (method) `cli/commands/bof_registry.py:289` `def do_bof_list(self, line)` -- List all installed and staged BOFs.
- `BofMarketplaceCommandSet.do_bof_catalog` (method) `cli/commands/bof_registry.py:321` `def do_bof_catalog(self, line)` -- List all BOFs available in the curated catalog.

## cli/commands/c2_profile.py
Depends on: `cli/commands/_base.py`, `modules/c2_profile_engine.py`, `utils.py`
- `C2ProfileCommandSet.do_c2_profiles` (method) `cli/commands/c2_profile.py:25` `def do_c2_profiles(self, line)` -- List all available C2 transport profiles.
- `C2ProfileCommandSet.do_c2_tls` (method) `cli/commands/c2_profile.py:50` `def do_c2_tls(self, line)` -- Display the current TLS C2 profile.
- `C2ProfileCommandSet.do_c2_dns` (method) `cli/commands/c2_profile.py:69` `def do_c2_dns(self, line)` -- Configure or display the DNS beacon profile.
- `C2ProfileCommandSet.do_c2_rotate` (method) `cli/commands/c2_profile.py:90` `def do_c2_rotate(self, line)` -- Rotate to the next C2 transport profile in the rotation queue.

## cli/commands/caldera.py
Depends on: `cli/commands/_base.py`, `modules/operation.py`, `modules/planner.py`, `modules/playbook_engine.py`, `modules/ttp_coverage.py`, `utils.py`
- `CalderaCommandSet.do_op_list` (method) `cli/commands/caldera.py:80` `def do_op_list(self, line)` -- List all operations.
- `CalderaCommandSet.do_op_create` (method) `cli/commands/caldera.py:96` `def do_op_create(self, line)` -- Create a new planned operation.
- `CalderaCommandSet.do_op_plan` (method) `cli/commands/caldera.py:114` `def do_op_plan(self, line)` -- Populate operation steps from a playbook YAML or via MITRE derive.
- `CalderaCommandSet.do_op_start` (method) `cli/commands/caldera.py:141` `def do_op_start(self, line)` -- Start (or resume) an operation.
- `CalderaCommandSet.do_op_pause` (method) `cli/commands/caldera.py:166` `def do_op_pause(self, line)` -- Pause a running operation.
- `CalderaCommandSet.do_op_resume` (method) `cli/commands/caldera.py:183` `def do_op_resume(self, line)` -- Resume a paused operation.
- `CalderaCommandSet.do_op_stop` (method) `cli/commands/caldera.py:200` `def do_op_stop(self, line)` -- Stop a running operation.
- `CalderaCommandSet.do_op_status` (method) `cli/commands/caldera.py:217` `def do_op_status(self, line)` -- Show the status of an operation.
- `CalderaCommandSet.do_op_timeline` (method) `cli/commands/caldera.py:249` `def do_op_timeline(self, line)` -- Show the event timeline of an operation.
- `CalderaCommandSet.do_op_report` (method) `cli/commands/caldera.py:272` `def do_op_report(self, line)` -- Generate a full report for an operation.
- `CalderaCommandSet.do_ttp_matrix` (method) `cli/commands/caldera.py:290` `def do_ttp_matrix(self, line)` -- Render the MITRE ATT&CK coverage matrix across all operations.
- `CalderaCommandSet.do_ttp_rebuild` (method) `cli/commands/caldera.py:299` `def do_ttp_rebuild(self, line)` -- Re-walk the operations directory to refresh the coverage matrix.
- `CalderaCommandSet.do_ttp_show` (method) `cli/commands/caldera.py:309` `def do_ttp_show(self, line)` -- Show details for a single MITRE technique.
- `CalderaCommandSet.do_plan` (method) `cli/commands/caldera.py:336` `def do_plan(self, line)` -- Pick the next best technique to run for a target.
- `CalderaCommandSet.do_plan_detail` (method) `cli/commands/caldera.py:364` `def do_plan_detail(self, line)` -- Show the full ranked plan (all candidates) for a target.
- `CalderaCommandSet.do_plan_apply` (method) `cli/commands/caldera.py:391` `def do_plan_apply(self, line)` -- Run the planner, then auto-create and start an operation.

## cli/commands/campaign.py
Depends on: `cli/commands/_base.py`, `modules/db.py`, `utils.py`
- `CampaignCommandSet.do_campaign` (method) `cli/commands/campaign.py:43` `def do_campaign(self, line)` -- Export or import an entire campaign as a portable package.

## cli/commands/catalog.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `CatalogCommandSet.do_catalog` (method) `cli/commands/catalog.py:33` `def do_catalog(self, line)` -- Browse the command catalog.
- `CatalogCommandSet.shlex_split` (method) `cli/commands/catalog.py:111` `def shlex_split(text)` -- Split text like shlex.split but handle empty strings gracefully.

## cli/commands/cicd.py
Depends on: `cli/commands/_base.py`, `modules/cicd_enumerator.py`, `modules/mfa_bypass.py`, `utils.py`
- `CICDCommandSet.do_cicd_scan` (method) `cli/commands/cicd.py:34` `def do_cicd_scan(self, line)` -- Scan CI/CD platform for security misconfigurations.
- `CICDCommandSet.do_cicd_secrets` (method) `cli/commands/cicd.py:97` `def do_cicd_secrets(self, line)` -- Scan build log for leaked secrets.
- `CICDCommandSet.do_jenkins_enum` (method) `cli/commands/cicd.py:140` `def do_jenkins_enum(self, line)` -- Enumerate a Jenkins instance.
- `CICDCommandSet.do_gitlab_enum` (method) `cli/commands/cicd.py:185` `def do_gitlab_enum(self, line)` -- Enumerate a GitLab instance.
- `CICDCommandSet.do_mfa_bypass` (method) `cli/commands/cicd.py:231` `def do_mfa_bypass(self, line)` -- Enumerate and test MFA bypass techniques.

## cli/commands/cli_auth.py
Depends on: `cli/commands/_base.py`, `modules/cli_auth.py`, `utils.py`
- `CliAuthCommandSet.do_login` (method) `cli/commands/cli_auth.py:34` `def do_login(self, line)` -- Authenticate against users.json (same users as lazyc2.py).
- `CliAuthCommandSet.do_register` (method) `cli/commands/cli_auth.py:117` `def do_register(self, line)` -- Register a new operator account in users.json.
- `CliAuthCommandSet.do_logout` (method) `cli/commands/cli_auth.py:191` `def do_logout(self, line)` -- Log out the current CLI operator and clear the remember-me token.
- `CliAuthCommandSet.do_whoami` (method) `cli/commands/cli_auth.py:224` `def do_whoami(self, line)` -- Show the currently logged-in CLI operator.

## cli/commands/cloud.py
Depends on: `cli/commands/_base.py`, `cli/confirm.py`, `core/hardening.py`, `modules/cloud_enum.py`, `modules/lazycloud.py`, `utils.py`
Imported by: `cli/commands/exfiltration.py`
- `CloudCommandSet.do_cloud_metadata` (method) `cli/commands/cloud.py:49` `def do_cloud_metadata(self, _line)` -- Harvest cloud instance metadata (AWS IMDS, Azure, GCP).
- `CloudCommandSet.do_cloud_buckets` (method) `cli/commands/cloud.py:98` `def do_cloud_buckets(self, line)` -- Enumerate cloud storage buckets for a given prefix.
- `CloudCommandSet.do_cloud_scan` (method) `cli/commands/cloud.py:148` `def do_cloud_scan(self, line)` -- Full cloud security scan: metadata + buckets + IAM enumeration.
- `CloudCommandSet.do_cloud_iam` (method) `cli/commands/cloud.py:187` `def do_cloud_iam(self, _line)` -- Enumerate cloud IAM roles and policies.
- `CloudCommandSet.do_cloud_enum` (method) `cli/commands/cloud.py:239` `def do_cloud_enum(self, line)` -- Enumerate cloud provider metadata, storage, and IAM.

## cli/commands/cloud_attacks.py
Depends on: `cli/commands/_base.py`, `modules/aws_attacks.py`, `modules/cross_cloud.py`, `modules/entra_id_attacks.py`, `modules/gcp_attacks.py`, `modules/k8s_attacks.py`, `modules/saas_attacks.py`
- `CloudAttackCommandSet.do_entra_attack` (method) `cli/commands/cloud_attacks.py:23` `def do_entra_attack(self, line)` -- Microsoft Entra ID / Azure AD attack operations.
- `CloudAttackCommandSet.do_aws_privesc` (method) `cli/commands/cloud_attacks.py:125` `def do_aws_privesc(self, line)` -- AWS privilege escalation and enumeration.
- `CloudAttackCommandSet.do_gcp_privesc` (method) `cli/commands/cloud_attacks.py:215` `def do_gcp_privesc(self, line)` -- GCP privilege escalation and enumeration.
- `CloudAttackCommandSet.do_k8s_attack` (method) `cli/commands/cloud_attacks.py:302` `def do_k8s_attack(self, line)` -- Kubernetes attack — RBAC enumeration, pod escape, etcd, persistence.
- `CloudAttackCommandSet.do_cross_cloud` (method) `cli/commands/cloud_attacks.py:387` `def do_cross_cloud(self, line)` -- Cross-cloud identity federation attacks.
- `CloudAttackCommandSet.do_saas_enum` (method) `cli/commands/cloud_attacks.py:470` `def do_saas_enum(self, line)` -- Enumerate SaaS platforms — M365, Google Workspace, Salesforce, Slack, ServiceNow.

## cli/commands/collaboration.py
Depends on: `cli/commands/_base.py`, `modules/collab_bp.py`, `modules/db.py`, `utils.py`
- `CollaborationCommandSet.do_lock_target` (method) `cli/commands/collaboration.py:48` `def do_lock_target(self, line)` -- Acquire an advisory lock on a target to prevent tool collisions.
- `CollaborationCommandSet.do_unlock_target` (method) `cli/commands/collaboration.py:89` `def do_unlock_target(self, line)` -- Release an advisory lock on a target.
- `CollaborationCommandSet.do_team_status` (method) `cli/commands/collaboration.py:114` `def do_team_status(self, line)` -- Show active operators and target locks.
- `CollaborationCommandSet.do_team_chat` (method) `cli/commands/collaboration.py:169` `def do_team_chat(self, line)` -- Send a message to all connected operators.
- `CollaborationCommandSet.do_share_finding` (method) `cli/commands/collaboration.py:199` `def do_share_finding(self, line)` -- Share a finding or credential discovery with the team.

## cli/commands/command_and_control.py
Depends on: `cli/commands/_base.py`, `utils.py`
- `CommandAndControlCommandSet.do_c2_status` (method) `cli/commands/command_and_control.py:41` `def do_c2_status(self, _line)` -- Show consolidated C2 status: listeners, beacons, implants, and sessions.
- `CommandAndControlCommandSet.do_c2_beacons` (method) `cli/commands/command_and_control.py:98` `def do_c2_beacons(self, _line)` -- List all active beacon sessions with their last-seen timestamps.
- `CommandAndControlCommandSet.do_c2_keygen` (method) `cli/commands/command_and_control.py:134` `def do_c2_keygen(self, _line)` -- Generate a fresh AES-256 key for beacon encryption.
- `CommandAndControlCommandSet.do_c2_quickstart` (method) `cli/commands/command_and_control.py:151` `def do_c2_quickstart(self, _line)` -- Quick C2 setup: generate key, prepare implant dir, print beacon commands.
- `CommandAndControlCommandSet.do_c2_beacon_cmd` (method) `cli/commands/command_and_control.py:198` `def do_c2_beacon_cmd(self, line)` -- Queue a command for execution on a connected beacon.
- `CommandAndControlCommandSet.do_c2_implant` (method) `cli/commands/command_and_control.py:233` `def do_c2_implant(self, line)` -- Generate a compiled implant payload for the target platform.

## cli/commands/command_and_control_migrated.py
Depends on: `cli/aliases.py`, `cli/assign.py`, `cli/commands/_base.py`, `core/config.py`, `core/hardening.py`, `modules/apt_playbooks.py`, `modules/c2_builder.py`, `modules/listener_manager.py`, `utils.py`
- `CommandAndControlMigratedCommandSet.do_msf` (method) `cli/commands/command_and_control_migrated.py:42` `def do_msf(self, line)` -- Automates various Metasploit tasks including scanning for vulnerabilities, setting up reverse shells, and creating...
- `CommandAndControlMigratedCommandSet.do_c2` (method) `cli/commands/command_and_control_migrated.py:392` `def do_c2(self, line)` -- Handle C2 server setup and agent compilation.
- `CommandAndControlMigratedCommandSet.do_listener` (method) `cli/commands/command_and_control_migrated.py:507` `def do_listener(self, line)` -- Manage C2 listeners: list, add, start, stop, remove.
- `CommandAndControlMigratedCommandSet.do_sandbox` (method) `cli/commands/command_and_control_migrated.py:635` `def do_sandbox(self, line)` -- Toggle or query Docker sandbox mode.
- `CommandAndControlMigratedCommandSet.do_msfrpc` (method) `cli/commands/command_and_control_migrated.py:677` `def do_msfrpc(self, line)` -- Connects to the msfrpcd daemon and allows remote control of Metasploit.
- `CommandAndControlMigratedCommandSet.do_sliver_server` (method) `cli/commands/command_and_control_migrated.py:701` `def do_sliver_server(self, line)` -- Starts the Sliver server and generates a client configuration file for connecting clients.
- `CommandAndControlMigratedCommandSet.do_empire` (method) `cli/commands/command_and_control_migrated.py:818` `def do_empire(self, line)` -- Generates payloads using PowerShell Empire with various options.
- `CommandAndControlMigratedCommandSet.do_automsf` (method) `cli/commands/command_and_control_migrated.py:868` `def do_automsf(self, line)` -- Try to check if Vulnerable using the module passed by argument of lazyown example automsf...
- `CommandAndControlMigratedCommandSet.do_iis_webdav_upload_asp` (method) `cli/commands/command_and_control_migrated.py:904` `def do_iis_webdav_upload_asp(self, line)` -- (CVE-2017-7269).
- `CommandAndControlMigratedCommandSet.do_duckyspark` (method) `cli/commands/command_and_control_migrated.py:939` `def do_duckyspark(self, line)` -- duckyspark Compiles and uploads an .ino sketch to a Digispark device using Arduino CLI and Micronucleus.
- `CommandAndControlMigratedCommandSet.do_emp3r0r` (method) `cli/commands/command_and_control_migrated.py:1140` `def do_emp3r0r(self, line)` -- Command emp3r0r Downloads and sets up the Emperor server for local exploitation.
- `CommandAndControlMigratedCommandSet.do_atomic_tests` (method) `cli/commands/command_and_control_migrated.py:1204` `def do_atomic_tests(self, line)` -- Executes Atomic Red Team tests based on user-selected platform and test.
- `CommandAndControlMigratedCommandSet.do_atomic_gen` (method) `cli/commands/command_and_control_migrated.py:1364` `def do_atomic_gen(self, line)` -- Generates test and cleanup scripts for a given Atomic Red Team technique ID.
- `CommandAndControlMigratedCommandSet.do_atomic_agent` (method) `cli/commands/command_and_control_migrated.py:1548` `def do_atomic_agent(self, line)` -- Generates and synchronizes atomic agent scripts.
- `CommandAndControlMigratedCommandSet.do_attack_plan` (method) `cli/commands/command_and_control_migrated.py:1648` `def do_attack_plan(self, line)` -- Executes a multi-step APT simulation plan based on Atomic Red Team test IDs.
- `CommandAndControlMigratedCommandSet.do_apt_playbook` (method) `cli/commands/command_and_control_migrated.py:1772` `def do_apt_playbook(self, line)` -- List, validate, and run APT playbooks based on public threat reports.
- `CommandAndControlMigratedCommandSet.do_mitre_test` (method) `cli/commands/command_and_control_migrated.py:1892` `def do_mitre_test(self, line)` -- Interacts with the MITRE ATT&CK framework using the STIX 2.0 format.
- `CommandAndControlMigratedCommandSet.do_generate_playbook` (method) `cli/commands/command_and_control_migrated.py:1995` `def do_generate_playbook(self, line)` -- Generates a playbook that integrates Atomic Red Team tests and MITRE ATT&CK techniques.
- `CommandAndControlMigratedCommandSet.do_my_playbook` (method) `cli/commands/command_and_control_migrated.py:2174` `def do_my_playbook(self, line)` -- Generates a playbook from your custom technique database.
- `CommandAndControlMigratedCommandSet.do_caldera` (method) `cli/commands/command_and_control_migrated.py:2231` `def do_caldera(self, line)` -- Installs and starts the Caldera server.
- `CommandAndControlMigratedCommandSet.do_caldera_import` (method) `cli/commands/command_and_control_migrated.py:2280` `def do_caldera_import(self, line)` -- Import CALDERA abilities into LazyOwn playbooks.
- `CommandAndControlMigratedCommandSet.do_caldera_export` (method) `cli/commands/command_and_control_migrated.py:2372` `def do_caldera_export(self, line)` -- Export a LazyOwn playbook to CALDERA ability YAML.

## cli/commands/containers.py
Depends on: `cli/commands/_base.py`, `modules/lazyk8s.py`, `utils.py`
Imported by: `cli/command_form.py`, `cli/dashboard_tui.py`, `cli/graph_overlay.py`, `cli/palette_overlay.py`, `cli/purple_tui.py`, `cli/sessions_browser.py`, `cli/surface_tui.py`, `cli/timeline_browser.py`, `poc_tui/app.py`
- `ContainerCommandSet.do_docker_enum` (method) `cli/commands/containers.py:37` `def do_docker_enum(self, _line)` -- Enumerate Docker host: containers, images, privileges, mounts.
- `ContainerCommandSet.do_k8s_enum` (method) `cli/commands/containers.py:101` `def do_k8s_enum(self, _line)` -- Enumerate Kubernetes cluster: pods, secrets, SAs, RBAC.
- `ContainerCommandSet.do_container_escape` (method) `cli/commands/containers.py:169` `def do_container_escape(self, _line)` -- Check current container for known escape vectors.
- `ContainerCommandSet.do_k8s_pods` (method) `cli/commands/containers.py:239` `def do_k8s_pods(self, line)` -- List Kubernetes pods with security-relevant details.
- `ContainerCommandSet.do_k8s_secrets` (method) `cli/commands/containers.py:283` `def do_k8s_secrets(self, line)` -- List and decode Kubernetes secrets.
- `ContainerCommandSet.do_container_detect` (method) `cli/commands/containers.py:334` `def do_container_detect(self, _line)` -- Auto-detect container runtime and escape primitives.

## cli/commands/cred.py
Depends on: `cli/commands/_base.py`, `modules/categories.py`, `utils.py`
- `CredentialAccessCommandSet.do_hashcat` (method) `cli/commands/cred.py:30` `def do_hashcat(self, line)` -- Run hashcat password cracking.
- `CredentialAccessCommandSet.do_john2hash` (method) `cli/commands/cred.py:39` `def do_john2hash(self, line)` -- Convert a hash to John the Ripper format.
- `CredentialAccessCommandSet.do_hydra` (method) `cli/commands/cred.py:47` `def do_hydra(self, line)` -- Run Hydra for online password attacks.
- `CredentialAccessCommandSet.do_medusa` (method) `cli/commands/cred.py:59` `def do_medusa(self, line)` -- Run Medusa for online password attacks.
- `CredentialAccessCommandSet.do_crunch` (method) `cli/commands/cred.py:67` `def do_crunch(self, line)` -- Generate wordlists with crunch.
- `CredentialAccessCommandSet.do_cewl` (method) `cli/commands/cred.py:75` `def do_cewl(self, line)` -- Generate a wordlist from a website with cewl.
- `CredentialAccessCommandSet.do_sshkey` (method) `cli/commands/cred.py:87` `def do_sshkey(self, line)` -- Generate an SSH key pair.
- `CredentialAccessCommandSet.do_creds_py` (method) `cli/commands/cred.py:93` `def do_creds_py(self, line)` -- Extract credentials from a file or command output.
- `CredentialAccessCommandSet.do_spraykatz` (method) `cli/commands/cred.py:98` `def do_spraykatz(self, line)` -- Run SprayKatz for credential spraying.

## cli/commands/cred_migrated.py
Depends on: `cli/commands/_base.py`, `utils.py`
Imported by: `tests/test_credentials_rotation.py`
- `CredMigratedCommandSet.do_createhash` (method) `cli/commands/cred_migrated.py:61` `def do_createhash(self, line)` -- Creates a `hash.txt` file in the `sessions` directory with the specified hash value and analyzes it using...
- `CredMigratedCommandSet.do_createcredentials` (method) `cli/commands/cred_migrated.py:115` `def do_createcredentials(self, line)` -- Creates a `credentials.txt` file in the `sessions` directory with the specified username and password.
- `CredMigratedCommandSet.do_cred` (method) `cli/commands/cred_migrated.py:163` `def do_cred(self, line)` -- Display the credentials stored in the `credentials.txt` file and copy the password to the clipboard.
- `CredMigratedCommandSet.do_searchhash` (method) `cli/commands/cred_migrated.py:216` `def do_searchhash(self, line)` -- Helps to find hash types in Hashcat by searching through its help output.
- `CredMigratedCommandSet.do_smalldic` (method) `cli/commands/cred_migrated.py:252` `def do_smalldic(self, list)` -- Handles the creation of temporary files for users and passwords based on a small dictionary.
- `CredMigratedCommandSet.do_dacledit` (method) `cli/commands/cred_migrated.py:290` `def do_dacledit(self, line)` -- Execute the dacledit.py command for a specific user or all users listed in the users.txt file.
- `CredMigratedCommandSet.do_generatedic` (method) `cli/commands/cred_migrated.py:360` `def do_generatedic(self, line)` -- Generates a wordlist based on a target name and a list of characters, with various combinations.
- `CredMigratedCommandSet.single_combo` (method) `cli/commands/cred_migrated.py:385` `def single_combo(name, characters, file, total, flag)` -- Generates single character combinations with the target name.
- `CredMigratedCommandSet.double_combo` (method) `cli/commands/cred_migrated.py:408` `def double_combo(name, characters, file, total, flag)` -- Generates double character combinations with the target name.
- `CredMigratedCommandSet.triple_combo` (method) `cli/commands/cred_migrated.py:432` `def triple_combo(name, characters, file, total, flag)` -- Generates triple character combinations with the target name.
- `CredMigratedCommandSet.fourth_combo` (method) `cli/commands/cred_migrated.py:457` `def fourth_combo(name, characters, file, total, flag)` -- Generates fourth character combinations with the target name.
- `CredMigratedCommandSet.fifth_combo` (method) `cli/commands/cred_migrated.py:483` `def fifth_combo(name, characters, file, total, flag)` -- Generates fifth character combinations with the target name.
- `CredMigratedCommandSet.sixth_combo` (method) `cli/commands/cred_migrated.py:510` `def sixth_combo(name, characters, file, total, flag)` -- Generates sixth character combinations with the target name, adding uppercase characters.
- `CredMigratedCommandSet.intercalate_combo` (method) `cli/commands/cred_migrated.py:535` `def intercalate_combo(name, characters, file, total, flag)` -- Generates combinations of the target name and character list, intercalating uppercase and lowercase characters.
- `CredMigratedCommandSet.alternate_case` (method) `cli/commands/cred_migrated.py:551` `def alternate_case(s)` -- Helper function to alternate the case of characters in a string.
- `CredMigratedCommandSet.expand_regex` (method) `cli/commands/cred_migrated.py:567` `def expand_regex(regex)` -- Expands a regular expression into a list of characters.
- `CredMigratedCommandSet.do_createmail` (method) `cli/commands/cred_migrated.py:625` `def do_createmail(self, line)` -- Generate email permutations based on a full name and self.params['domain'], then save them to a file.
- `CredMigratedCommandSet.do_passwordspray` (method) `cli/commands/cred_migrated.py:673` `def do_passwordspray(self, line)` -- Perform password spraying using crackmapexec with the provided parameters.
- `CredMigratedCommandSet.do_addusers` (method) `cli/commands/cred_migrated.py:705` `def do_addusers(self, line)` -- Opens or creates the users.txt file in the sessions directory for editing using nano.
- `CredMigratedCommandSet.do_passtightvnc` (method) `cli/commands/cred_migrated.py:727` `def do_passtightvnc(self, line)` -- Decrypts TightVNC passwords using Metasploit.
- `CredMigratedCommandSet.do_transform` (method) `cli/commands/cred_migrated.py:774` `def do_transform(self, line)` -- Transforms the input string based on user-defined casing style.
- `CredMigratedCommandSet.do_username_anarchy` (method) `cli/commands/cred_migrated.py:802` `def do_username_anarchy(self, line)` -- Generate usernames using the username-anarchy tool based on user input.
- `CredMigratedCommandSet.do_john2keepas` (method) `cli/commands/cred_migrated.py:903` `def do_john2keepas(self, line)` -- List all .kdbx files in the 'sessions' directory, let the user select one, and run the command `sudo keepass2john...
- `CredMigratedCommandSet.do_keepass` (method) `cli/commands/cred_migrated.py:952` `def do_keepass(self, line)` -- Open a .kdbx file and print the titles and contents of all entries.
- `CredMigratedCommandSet.do_crack_cisco_7_password` (method) `cli/commands/cred_migrated.py:1016` `def do_crack_cisco_7_password(self, line)` -- Crack a Cisco Type 7 password hash and display the plaintext.
- `CredMigratedCommandSet.do_cubespraying` (method) `cli/commands/cred_migrated.py:1038` `def do_cubespraying(self, line)` -- Command cubespraying: Automates the installation and usage of CubeSpraying for performing credential spraying attacks.
- `CredMigratedCommandSet.do_john2zip` (method) `cli/commands/cred_migrated.py:1100` `def do_john2zip(self, line)` -- List all .zip files in the 'sessions' directory, let the user select one, and run the command `zip2john...
- `CredMigratedCommandSet.do_createusers_and_hashs` (method) `cli/commands/cred_migrated.py:1161` `def do_createusers_and_hashs(self, line)` -- Command createusers_and_hashs: Extracts usernames and hashes from a dump file.
- `CredMigratedCommandSet.do_refill_password` (method) `cli/commands/cred_migrated.py:1204` `def do_refill_password(self, line)` -- Generate a list of possible passwords by filling each asterisk in the input with user-specified characters.
- `CredMigratedCommandSet.do_rocky` (method) `cli/commands/cred_migrated.py:1240` `def do_rocky(self, line)` -- Reduces a wordlist based on the specified password length.
- `CredMigratedCommandSet.do_adsso_spray` (method) `cli/commands/cred_migrated.py:1276` `def do_adsso_spray(self, line)` -- Performs a password spray attack on Azure Active Directory Seamless Single Sign-On (SSO) using a specified list of...

## cli/commands/crystal_ball.py
Depends on: `cli/commands/_base.py`, `modules/privesc_predictor.py`, `utils.py`
- `CrystalBallCommandSet.do_crystal_ball` (method) `cli/commands/crystal_ball.py:27` `def do_crystal_ball(self, line)` -- Analyze linpeas/winpeas output and rank privesc vectors with exact commands.
- `CrystalBallCommandSet.do_privesc_suggest` (method) `cli/commands/crystal_ball.py:110` `def do_privesc_suggest(self, line)` -- Quick alias for crystal_ball --auto.


Next: [API_p2.md](API_p2.md)
