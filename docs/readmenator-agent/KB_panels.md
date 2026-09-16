# Subsystem: panels

## lazygui/panels/__init__.py
- Layer: presentation
- Language: py
- Depends on: `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`

## lazygui/panels/base.py
- Layer: presentation
- Language: py
- Symbols:
  - `PanelBase` (class, line 17) `class PanelBase(QDockWidget)`
  - `__init__` (method, line 20) `def __init__(self, constants, backend, identifier, title, parent)`
  - `identifier` (method, line 43) `def identifier(self)`
  - `backend` (method, line 48) `def backend(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/services/backend.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/registry.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`

## lazygui/panels/campaign_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `CampaignPanel` (class, line 28) `class CampaignPanel(PanelBase)`
  - `__init__` (method, line 31) `def __init__(self, constants, backend, parent)`
  - `_refresh` (method, line 99) `def _refresh(self)`
  - `_on_campaigns_changed` (method, line 102) `def _on_campaigns_changed(self, campaigns)`
  - `_populate_tree` (method, line 106) `def _populate_tree(self)`
  - `_request_new_campaign` (method, line 120) `def _request_new_campaign(self)`
  - `_request_view_campaign` (method, line 123) `def _request_view_campaign(self)`
  - `_request_run_playbook` (method, line 126) `def _request_run_playbook(self)`
  - `campaign_count` (method, line 133) `def campaign_count(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/credentials_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `CredentialsPanel` (class, line 27) `class CredentialsPanel(PanelBase)`
  - `__init__` (method, line 30) `def __init__(self, constants, backend, parent)`
  - `_build_ui` (method, line 50) `def _build_ui(self)`
  - `_refresh` (method, line 95) `def _refresh(self)`
  - `_copy_selected` (method, line 130) `def _copy_selected(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/cve_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `CVEPanel` (class, line 28) `class CVEPanel(PanelBase)`
  - `__init__` (method, line 31) `def __init__(self, constants, backend, parent)`
  - `_refresh` (method, line 102) `def _refresh(self)`
  - `_populate_tree` (method, line 145) `def _populate_tree(self)`
  - `_request_lookup` (method, line 160) `def _request_lookup(self)`
  - `_request_search_exploits` (method, line 166) `def _request_search_exploits(self)`
  - `cve_count` (method, line 173) `def cve_count(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/event_log_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `EventLogPanel` (class, line 24) `class EventLogPanel(PanelBase)`
  - `__init__` (method, line 27) `def __init__(self, constants, backend, event_log, parent)`
  - `_on_level_changed` (method, line 69) `def _on_level_changed(self, _index)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`, `lazygui/services/models.py`, `lazygui/widgets/event_log_view.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/graph_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `GraphPanel` (class, line 20) `class GraphPanel(PanelBase)`
  - `__init__` (method, line 23) `def __init__(self, constants, backend, parent)`
  - `_on_topology_changed` (method, line 50) `def _on_topology_changed(self, topology)`
  - `_on_node_context_menu` (method, line 54) `def _on_node_context_menu(self, node_id, position)`
  - `_on_node_selected` (method, line 105) `def _on_node_selected(self, node_id)`
  - `_find_node_info` (method, line 109) `def _find_node_info(self, node_id)`
  - `graph_view` (method, line 118) `def graph_view(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/graph_view.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/history_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `HistoryPanel` (class, line 30) `class HistoryPanel(PanelBase)`
  - `__init__` (method, line 33) `def __init__(self, constants, backend, parent)`
  - `_refresh` (method, line 87) `def _refresh(self)`
  - `_populate` (method, line 106) `def _populate(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/killchain_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `_get_phases` (function, line 23) `def _get_phases()`
  - `KillChainPanel` (class, line 34) `class KillChainPanel(PanelBase)`
  - `__init__` (method, line 37) `def __init__(self, constants, backend, parent)`
  - `_build_ui` (method, line 61) `def _build_ui(self)`
  - `_refresh` (method, line 97) `def _refresh(self)`
  - `_apply_visuals` (method, line 129) `def _apply_visuals(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `modules/killchain.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/listeners_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `ListenersPanel` (class, line 21) `class ListenersPanel(PanelBase)`
  - `__init__` (method, line 24) `def __init__(self, constants, backend, parent)`
  - `_on_listeners_changed` (method, line 65) `def _on_listeners_changed(self, listeners)`
  - `_on_filter_changed` (method, line 70) `def _on_filter_changed(self, text)`
  - `_populate_visible` (method, line 75) `def _populate_visible(self)`
  - `_matches_filter` (method, line 95) `def _matches_filter(self, listener)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/filter_bar.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/marketplace_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `MarketplacePanel` (class, line 29) `class MarketplacePanel(PanelBase)`
  - `__init__` (method, line 32) `def __init__(self, constants, backend, parent)`
  - `_make_tree` (method, line 94) `def _make_tree(headers)`
  - `_refresh` (method, line 106) `def _refresh(self)`
  - `_fetch_yara_rules` (method, line 112) `def _fetch_yara_rules(self)`
  - `_fetch_nuclei_templates` (method, line 127) `def _fetch_nuclei_templates(self)`
  - `_fetch_addons` (method, line 159) `def _fetch_addons(self)`
  - `_fetch_plugins` (method, line 187) `def _fetch_plugins(self)`
  - `_populate_yara_tree` (method, line 215) `def _populate_yara_tree(self)`
  - `_populate_nuclei_tree` (method, line 223) `def _populate_nuclei_tree(self)`
  - `_populate_addons_tree` (method, line 231) `def _populate_addons_tree(self)`
  - `_populate_plugins_tree` (method, line 239) `def _populate_plugins_tree(self)`
  - `_apply_filter` (method, line 247) `def _apply_filter(self)`
  - `_show_selected_info` (method, line 253) `def _show_selected_info(self)`
  - `_run_selected` (method, line 264) `def _run_selected(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/registry.py
- Layer: presentation
- Language: py
- Symbols:
  - `PanelRegistry` (class, line 34) `class PanelRegistry`
  - `build` (method, line 53) `def build(cls, constants, backend, event_log, parent)`
  - `all_panels` (method, line 83) `def all_panels(self)`
  - `by_identifier` (method, line 91) `def by_identifier(self, identifier)`
  - `__iter__` (method, line 98) `def __iter__(self)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/panels/campaign_panel.py`, `lazygui/panels/credentials_panel.py`, `lazygui/panels/cve_panel.py`, `lazygui/panels/event_log_panel.py`, `lazygui/panels/graph_panel.py`, `lazygui/panels/history_panel.py`, `lazygui/panels/killchain_panel.py`, `lazygui/panels/listeners_panel.py`, `lazygui/panels/marketplace_panel.py`, `lazygui/panels/sessions_panel.py`, `lazygui/panels/terminal_panel.py`, `lazygui/services/backend.py`, `lazygui/services/event_log.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/windows/main_window.py`

## lazygui/panels/sessions_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `SessionsPanel` (class, line 39) `class SessionsPanel(PanelBase)`
  - `__init__` (method, line 45) `def __init__(self, constants, backend, parent)`
  - `_refresh_initial` (method, line 85) `def _refresh_initial(self)`
  - `_on_sessions_changed` (method, line 91) `def _on_sessions_changed(self, sessions)`
  - `_on_filter_changed` (method, line 96) `def _on_filter_changed(self, text)`
  - `_on_selection_changed` (method, line 101) `def _on_selection_changed(self)`
  - `_on_item_double_clicked` (method, line 112) `def _on_item_double_clicked(self, item)`
  - `_on_context_menu` (method, line 120) `def _on_context_menu(self, position)`
  - `_populate_visible` (method, line 167) `def _populate_visible(self)`
  - `_matches_filter` (method, line 187) `def _matches_filter(self, session)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/services/models.py`, `lazygui/widgets/filter_bar.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`

## lazygui/panels/terminal_panel.py
- Layer: presentation
- Language: py
- Symbols:
  - `TerminalPanel` (class, line 22) `class TerminalPanel(PanelBase)`
  - `__init__` (method, line 25) `def __init__(self, constants, backend, parent)`
  - `focus_terminal` (method, line 78) `def focus_terminal(self)`
  - `set_target_session` (method, line 82) `def set_target_session(self, session_id)`
  - `_send_beacon_command` (method, line 90) `def _send_beacon_command(self)`
  - `_update_session_combo` (method, line 104) `def _update_session_combo(self, sessions)`
  - `_on_beacon_result` (method, line 119) `def _on_beacon_result(self, result)`
- Depends on: `lazygui/config/constants.py`, `lazygui/panels/base.py`, `lazygui/services/backend.py`, `lazygui/widgets/terminal_view.py`
- Imported by: `lazygui/panels/__init__.py`, `lazygui/panels/registry.py`
