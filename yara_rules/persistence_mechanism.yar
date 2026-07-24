
rule Windows_Persistence {
    meta:
        description = "Detects Windows persistence mechanisms"
        author = "LazyOwn"
        severity = "high"
        category = "persistence"
    strings:
        $run_key = "CurrentVersion\\Run" ascii wide nocase
        $scheduled_task = "schtasks /create" ascii wide nocase
        $wmi_persist = "__EventFilter" ascii wide nocase
        $service_create = "sc create" ascii wide nocase
        $startup_folder = "Start Menu\\Programs\\Startup" ascii wide nocase
        $winlogon = "Winlogon\\Shell" ascii wide nocase
        $reg_add = "reg add" ascii wide nocase
        $dll_side = ".dll" ascii wide
    condition:
        (filesize < 200KB) and (2 of them)
}
