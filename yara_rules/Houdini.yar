rule MALWARE_Win_HoudiniConfig {
    meta:
        author = "ditekshen"
        description = "Detects Houdini Trojan configurations"
        cape_type = "Houdini Payload"
        reference = "https://github.com/ditekshen/back-in-2017"
    strings:
        $s1 = "install_name="
        $s2 = "nick_name="
        $s3 = "install_folder="
        $s4 = "reg_startup="
        $s5 = "startup_folder_startup="
        $s6 = "task_startup="
        $s7 = "injection="
        $s8 = "injection_process"
    condition:
        (uint16(0) == 0x5a4d and 5 of them) or (all of them)
}

rule MALWARE_Win_Houdini {
    meta:
        author = "ditekshen"
        description = "Detects the raw binary of the Houdini Trojan Delphi variant"
        cape_type = "Houdini Payload"
        reference = "https://github.com/ditekshen/back-in-2017"
     strings:
         $hc = "houdiniclient" ascii wide nocase
         // module keylogger
         $mk1 = "keylogger_thread" fullword ascii
         $mk2 = "keyloger_host" fullword ascii
         $mk3 = "keylogger_port" fullword ascii
         $mk4 = "keylogger_thread" fullword ascii
         $mk5 = "keylogger_init" fullword wide
         $mk6 = "keylogger_stop" fullword wide
         $mk7 = "keylogger_offline" fullword wide
         $mk8 = "silence_keylogger" fullword wide
         // module screenshot
         $ms1 = "screenshot_thread" fullword ascii
         $ms2 = "screen_host" fullword ascii
         $ms3 = "screen_port" fullword ascii
         $ms4 = "screenshot_init" fullword wide
         $ms5 = "screenshot_start" fullword wide
         $ms6 = "screenshot_stop" fullword wide
         $ms7 = "screen_thumb" fullword wide
         $ms8 = "silence_screenshot" fullword wide
         // module file
         $mf1 = "file_manager_init" fullword wide
         $mf2 = "file_manager_root" fullword wide
         $mf3 = "file_manager_faf" fullword wide
         $mf4 = "file_manager_download" fullword wide
         $mf5 = "file_manager_upload" fullword wide
         $mf6 = "file_manager_stop" fullword wide
         $mf7 = "file_manager_delete_folder" fullword wide
         $mf8 = "file_manager_rename_folder" fullword wide
         $mf9 = "file_manager_rename_file" fullword wide
         $mf10 = "file_manager_delete_file" fullword wide
         $mf11 = "file_manager_execute_file" fullword wide
         $mf12 = "file_manager_thumb" fullword wide
         $mf13 = "file_manager_upload_http" fullword wide
         $mf14 = "file_manager_upload_tcp" fullword wide
         $mf15 = "upload_file_tcp" fullword wide
         $mf16 = "download_file_tcp" fullword wide
         $mf17 = "upload_file_http" fullword wide
         $mf18 = "filemanager_host" fullword ascii
         $mf19 = "filemanager_port" fullword ascii
         $mf20 = "filemanager_thread" fullword ascii
         // module password
         $mp1 = "password_value" fullword wide
         $mp2 = "password_init" fullword wide
         $mp3 = "password_stop" fullword wide
         $mp4 = "password_firefox" fullword wide
         $mp5 = "password_chrome" fullword wide
         $mp6 = "password_all" fullword wide
         $mp7 = "password_host" fullword ascii
         $mp8 = "password_port" fullword ascii
         $mp9 = "password_thread" fullword ascii
         // module miscellaneous 
         $mm1 = "misc_init" fullword wide
         $mm2 = "misc_stop" fullword wide
         $mm3 = "misc_process_list" fullword wide
         $mm4 = "misc_module_list" fullword wide
         $mm5 = "misc_process_terminate" fullword wide
         $mm6 = "misc_host" fullword ascii
         $mm7 = "misc_port" fullword ascii
         $mm8 = "misc_thread" fullword ascii
         // plugins
         $pl1 = "plugin_file_init" fullword wide
         $pl2 = "plugin_url_init" fullword wide
         $pl3 = "plugin_stop" fullword wide
     condition:
         uint16(0) == 0x5a4d and 4 of them
}
