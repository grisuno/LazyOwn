
rule PHP_WebShell_Generic {
    meta:
        description = "Detects common PHP webshell patterns"
        author = "LazyOwn"
        severity = "high"
        category = "webshell"
    strings:
        $eval_cmd = "eval(" ascii wide
        $system_cmd = "system(" ascii wide
        $exec_cmd = "exec(" ascii wide
        $passthru = "passthru(" ascii wide
        $shell_exec = "shell_exec(" ascii wide
        $popen = "popen(" ascii wide
        $proc_open = "proc_open(" ascii wide
    condition:
        (filesize < 50KB) and (2 of them)
}
