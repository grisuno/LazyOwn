rule Unrecom
{
	meta:
		author = " Kevin Breen <kevin@techanarchy.net>"
		ref = "http://malwareconfig.com/stats/AAR"
		maltype = "Remote Access Trojan"
		filetype = "exe"
        cape_type = "Unrecom Payload"

	strings:
		$meta = "META-INF"
		$conf = "load/ID"
		$a = "load/JarMain.class"
		$b = "load/MANIFEST.MF"
        $c = "plugins/UnrecomServer.class"

	condition:
		all of them
}
