rule obfuscated_powershell {
    meta:
        description = "Detects obfuscated PowerShell commands used by malware"
        author = "LazyOwn RedTeam"
        severity = "high"
        category = "obfuscation"
    strings:
        $enc = "-EncodedCommand" nocase wide ascii
        $enc2 = "-enc" nocase wide ascii
        $enc3 = "-e" nocase wide ascii
        $from_base = "[System.Convert]::FromBase64String" nocase wide ascii
        $to_base = "[System.Text.Encoding]::UTF8.GetString" nocase wide ascii
        $invoke_expr = "IEX" nocase wide ascii
        $invoke_expr2 = "Invoke-Expression" nocase wide ascii
        $download = "DownloadString" nocase ascii
        $download2 = "DownloadFile" nocase ascii
        $net_client = "Net.WebClient" nocase ascii
        $hidden = "-WindowStyle Hidden" nocase wide ascii
        $noprofile = "-NoProfile" nocase wide ascii
        $nologo = "-NoLogo" nocase wide ascii
    condition:
        (1 of ($enc, $enc2, $enc3) and ($hidden or $noprofile or $nologo)) or
        ($from_base and $to_base and ($invoke_expr or $invoke_expr2)) or
        (($download or $download2) and $net_client and ($invoke_expr or $invoke_expr2))
}

rule obfuscated_bash {
    meta:
        description = "Detects obfuscated bash commands indicative of malware"
        author = "LazyOwn RedTeam"
        severity = "medium"
        category = "obfuscation"
    strings:
        $bash_enc = "base64 -d" nocase ascii
        $bash_enc2 = "base64 --decode" nocase ascii
        $openssl_b64 = "openssl base64 -d" nocase ascii
        $xxd = "xxd -r -p" nocase ascii
        $pipe_exec = "| /bin/bash" nocase ascii
        $pipe_sh = "| /bin/sh" nocase ascii
        $eval_variable = "${" ascii
        $curl_pipe = "curl -s" nocase ascii
        $wget_pipe = "wget -qO-" nocase ascii
    condition:
        (any of ($curl_pipe, $wget_pipe) and any of ($pipe_exec, $pipe_sh) and any of ($bash_enc, $bash_enc2, $openssl_b64, $xxd)) or
        ($eval_variable and $bash_enc and $pipe_exec)
}
