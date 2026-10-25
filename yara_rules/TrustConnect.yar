rule TrustConnect
{
    meta:
        description = "TrustConnect Payload"
        author = "enzok"
        cape_type = "TrustConnect Payload"
        hash = "51f62d2477d26446102aab3b9755532a54bc21cae24242bf51e275d701bf3c97"

    strings:
        $s1  = "/api/agent/register" ascii wide
        $s2  = "/api/agent/check-update?version=" ascii wide
        $s3  = "/ws/agent" ascii wide
        $s4  = "request_system_info" ascii wide
        $s5  = "request_screenshot" ascii wide
        $s6  = "set_clipboard" ascii wide
        $s7  = "send_sas" ascii wide
        $s8  = "terminal_input" ascii wide
        $s9  = "terminal_output" ascii wide
        $s10 = "Screen capture successful: " ascii wide

        $log1 = "<deviceId>" ascii wide
        $log2 = "<installToken>" ascii wide
        $log3 = "<RunAgent>" ascii wide
        $log4 = "<agentVersion>" ascii wide

        $pdb = "/obj/Release/net8.0-windows/win-x64/" ascii wide

    condition:
        8 of ($s*) and
        2 of ($log*) and
        $pdb
}
