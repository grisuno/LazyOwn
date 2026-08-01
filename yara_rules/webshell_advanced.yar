rule php_webshell_advanced {
    meta:
        description = "Detects advanced PHP webshell patterns beyond eval/system"
        author = "LazyOwn RedTeam"
        severity = "critical"
        category = "webshell"
    strings:
        $assert = "$_REQUEST" nocase ascii
        $create_func = "create_function" nocase ascii
        $preg = "preg_replace" nocase ascii
        $backtick = "`$_GET" nocase ascii
        $include_wrapper = "include" nocase ascii
        $data_wrapper = "data://" nocase ascii
        $phar_wrapper = "phar://" nocase ascii
        $filter_wrapper = "php://filter" nocase ascii
        $rotate = "str_rot13" nocase ascii
        $gzinflate = "gzinflate" nocase ascii
        $gzuncompress = "gzuncompress" nocase ascii
        $rawdeflate = "gzinflate(base64_decode" nocase ascii
    condition:
        (any of ($assert, $create_func, $preg, $backtick)) or
        (($include_wrapper and ($data_wrapper or $phar_wrapper or $filter_wrapper))) or
        ($rotate and (any of ($gzinflate, $rawdeflate)))
}

rule asp_webshell {
    meta:
        description = "Detects ASP/ASPX webshell patterns"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "webshell"
    strings:
        $cmd_exe = "cmd.exe" nocase wide ascii
        $powershell = "powershell.exe" nocase wide ascii
        $exec_1 = "Server.CreateObject" nocase ascii
        $exec_2 = "WScript.Shell" nocase ascii
        $exec_3 = "Shell.Application" nocase ascii
        $exec_4 = "Scripting.FileSystemObject" nocase ascii
        $exec_5 = "Microsoft.XMLHTTP" nocase ascii
        $proc = "Process.Start" nocase ascii
        $out = "StandardOutput" nocase ascii
    condition:
        2 of ($exec*) and ($cmd_exe or $powershell or $proc)
}

rule jsp_webshell {
    meta:
        description = "Detects JSP webshell patterns"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "webshell"
    strings:
        $jsp1 = "Runtime.getRuntime().exec" nocase ascii
        $jsp2 = "ProcessBuilder" nocase ascii
        $jsp3 = "getInputStream()" nocase ascii
        $jsp4 = "BufferedReader" nocase ascii
        $jsp5 = "InputStreamReader" nocase ascii
        $class_loader = "Class.forName" nocase ascii
        $reflect = "getMethod" nocase ascii
    condition:
        $jsp1 and any of ($jsp*)
}
