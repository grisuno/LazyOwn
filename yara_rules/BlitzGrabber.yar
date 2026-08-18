rule BlitzGrabber {
    meta:
        author = "ditekSHen"
        description = "Detects BlitzGrabber infostealer"
        cape_type = "BlitzGrabber Payload"
    strings:
       $x1 = "**BLITZED GRABBER V" wide
       $x2 = "\\BlitzedGrabberV" ascii
       $x3 = "Kyanite" ascii wide nocase
       $s1 = /;\/\/(SCREENSHOT|PASSWORDS|FORKBOMB|MELTSTUB)\/\// ascii wide
       $s2 = "KryptedWare" wide
       $s3 = "chckcopyTemp" wide
       $s4 = "chckscreenShot" wide
       $s5 = "Plugin.Banking." ascii
       $s6 = "sChromiumPswPaths" ascii
       $s7 = ".CreateDownloadLink(" ascii
       $s8 = "CaptureScreen()" ascii
       $s9 = ".UploadFile(\"https://api.anonfiles.com/upload\"" ascii
    condition:
        uint16(0) == 0x5a4d and (1 of ($x*) and 3 of ($s*)) or (7 of ($s*))
}
