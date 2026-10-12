# `modules/lazyatack.sh`

> Source: [modules/lazyatack.sh:1](../../modules/lazyatack.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

Nombre del script: lazyatack.sh Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Descripción: Este script contiene la lógica principal de la aplicación.

LazyAtack Licencia: GPL v3   Banner

## Contents

- **Functions:** [`mostrar_ayuda`](#mostrar_ayuda), [`validar_ip`](#validar_ip), [`validar_url`](#validar_url), [`descargar_seclists`](#descargar_seclists), [`escanear_puertos`](#escanear_puertos), [`escanear_puertos_especificos`](#escanear_puertos_especificos), [`enumerar_http`](#enumerar_http), [`iniciar_servidor_http`](#iniciar_servidor_http), [`configurar_netcat`](#configurar_netcat), [`enviar_archivo_netcat`](#enviar_archivo_netcat), [`verificar_conectividad`](#verificar_conectividad), [`verificar_curl`](#verificar_curl), [`configurar_shell_reversa`](#configurar_shell_reversa), [`escuchar_shell`](#escuchar_shell), [`monitorear_procesos`](#monitorear_procesos), [`ejecutar_wfuzz`](#ejecutar_wfuzz), [`comprobar_sudo`](#comprobar_sudo), [`explotar_lfi`](#explotar_lfi), [`configurar_tty`](#configurar_tty), [`eliminar_archivos`](#eliminar_archivos), [`obtener_root_shell`](#obtener_root_shell), [`enumerar_suid`](#enumerar_suid), [`listar_timers`](#listar_timers), [`comprobar_rutas`](#comprobar_rutas), [`abusar_tar`](#abusar_tar), [`enumerar_puertos`](#enumerar_puertos), [`eliminar_contenedores_docker`](#eliminar_contenedores_docker), [`escanear_red`](#escanear_red), [`menu_servidor`](#menu_servidor), [`menu_cliente`](#menu_cliente)

## Functions

<a id="mostrar_ayuda"></a>

### `mostrar_ayuda`

`function` | [modules/lazyatack.sh:21](../../modules/lazyatack.sh#L21)

```bash
function mostrar_ayuda
```

Función para mostrar ayuda

---

<a id="validar_ip"></a>

### `validar_ip`

`function` | [modules/lazyatack.sh:33](../../modules/lazyatack.sh#L33)

```bash
function validar_ip
```

Función para validar una dirección IP

---

<a id="validar_url"></a>

### `validar_url`

`function` | [modules/lazyatack.sh:49](../../modules/lazyatack.sh#L49)

```bash
function validar_url
```

Función para validar URL

---

<a id="descargar_seclists"></a>

### `descargar_seclists`

`function` | [modules/lazyatack.sh:107](../../modules/lazyatack.sh#L107)

```bash
function descargar_seclists
```

Función para descargar y extraer SecLists

---

<a id="escanear_puertos"></a>

### `escanear_puertos`

`function` | [modules/lazyatack.sh:115](../../modules/lazyatack.sh#L115)

```bash
function escanear_puertos
```

Función para ejecutar escaneo de puertos con nmap

---

<a id="escanear_puertos_especificos"></a>

### `escanear_puertos_especificos`

`function` | [modules/lazyatack.sh:121](../../modules/lazyatack.sh#L121)

```bash
function escanear_puertos_especificos
```

Función para escanear puertos específicos

---

<a id="enumerar_http"></a>

### `enumerar_http`

`function` | [modules/lazyatack.sh:127](../../modules/lazyatack.sh#L127)

```bash
function enumerar_http
```

Función para enumerar servicios HTTP

---

<a id="iniciar_servidor_http"></a>

### `iniciar_servidor_http`

`function` | [modules/lazyatack.sh:133](../../modules/lazyatack.sh#L133)

```bash
function iniciar_servidor_http
```

Función para iniciar servidor HTTP con Python

---

<a id="configurar_netcat"></a>

### `configurar_netcat`

`function` | [modules/lazyatack.sh:139](../../modules/lazyatack.sh#L139)

```bash
function configurar_netcat
```

Función para configurar netcat

---

<a id="enviar_archivo_netcat"></a>

### `enviar_archivo_netcat`

`function` | [modules/lazyatack.sh:145](../../modules/lazyatack.sh#L145)

```bash
function enviar_archivo_netcat
```

Función para enviar archivo mediante bash a netcat

---

<a id="verificar_conectividad"></a>

### `verificar_conectividad`

`function` | [modules/lazyatack.sh:151](../../modules/lazyatack.sh#L151)

```bash
function verificar_conectividad
```

Función para verificar conectividad con ping y tcpdump

---

<a id="verificar_curl"></a>

### `verificar_curl`

`function` | [modules/lazyatack.sh:158](../../modules/lazyatack.sh#L158)

```bash
function verificar_curl
```

Función para verificar conectividad con curl

---

<a id="configurar_shell_reversa"></a>

### `configurar_shell_reversa`

`function` | [modules/lazyatack.sh:165](../../modules/lazyatack.sh#L165)

```bash
function configurar_shell_reversa
```

Función para configurar una shell reversa

---

<a id="escuchar_shell"></a>

### `escuchar_shell`

`function` | [modules/lazyatack.sh:171](../../modules/lazyatack.sh#L171)

```bash
function escuchar_shell
```

Función para escuchar shell con netcat

---

<a id="monitorear_procesos"></a>

### `monitorear_procesos`

`function` | [modules/lazyatack.sh:177](../../modules/lazyatack.sh#L177)

```bash
function monitorear_procesos
```

Función para monitorear procesos

---

<a id="ejecutar_wfuzz"></a>

### `ejecutar_wfuzz`

`function` | [modules/lazyatack.sh:188](../../modules/lazyatack.sh#L188)

```bash
function ejecutar_wfuzz
```

Función para ejecutar wfuzz

---

<a id="comprobar_sudo"></a>

### `comprobar_sudo`

`function` | [modules/lazyatack.sh:194](../../modules/lazyatack.sh#L194)

```bash
function comprobar_sudo
```

Función para comprobar permisos sudo

---

<a id="explotar_lfi"></a>

### `explotar_lfi`

`function` | [modules/lazyatack.sh:200](../../modules/lazyatack.sh#L200)

```bash
function explotar_lfi
```

Función para explotar LFI

---

<a id="configurar_tty"></a>

### `configurar_tty`

`function` | [modules/lazyatack.sh:206](../../modules/lazyatack.sh#L206)

```bash
function configurar_tty
```

Función para configurar TTY

---

<a id="eliminar_archivos"></a>

### `eliminar_archivos`

`function` | [modules/lazyatack.sh:217](../../modules/lazyatack.sh#L217)

```bash
function eliminar_archivos
```

Función para eliminar archivos de forma segura

---

<a id="obtener_root_shell"></a>

### `obtener_root_shell`

`function` | [modules/lazyatack.sh:223](../../modules/lazyatack.sh#L223)

```bash
function obtener_root_shell
```

Función para obtener root shell mediante Docker

---

<a id="enumerar_suid"></a>

### `enumerar_suid`

`function` | [modules/lazyatack.sh:230](../../modules/lazyatack.sh#L230)

```bash
function enumerar_suid
```

Función para enumerar archivos con SUID

---

<a id="listar_timers"></a>

### `listar_timers`

`function` | [modules/lazyatack.sh:236](../../modules/lazyatack.sh#L236)

```bash
function listar_timers
```

Función para listar timers de systemd

---

<a id="comprobar_rutas"></a>

### `comprobar_rutas`

`function` | [modules/lazyatack.sh:242](../../modules/lazyatack.sh#L242)

```bash
function comprobar_rutas
```

Función para comprobar rutas de comandos

---

<a id="abusar_tar"></a>

### `abusar_tar`

`function` | [modules/lazyatack.sh:248](../../modules/lazyatack.sh#L248)

```bash
function abusar_tar
```

Función para abusar de tar

---

<a id="enumerar_puertos"></a>

### `enumerar_puertos`

`function` | [modules/lazyatack.sh:254](../../modules/lazyatack.sh#L254)

```bash
function enumerar_puertos
```

Función para enumerar puertos abiertos

---

<a id="eliminar_contenedores_docker"></a>

### `eliminar_contenedores_docker`

`function` | [modules/lazyatack.sh:260](../../modules/lazyatack.sh#L260)

```bash
function eliminar_contenedores_docker
```

Función para eliminar contenedores Docker

---

<a id="escanear_red"></a>

### `escanear_red`

`function` | [modules/lazyatack.sh:266](../../modules/lazyatack.sh#L266)

```bash
function escanear_red
```

Función para escanear red

---

<a id="menu_servidor"></a>

### `menu_servidor`

`function` | [modules/lazyatack.sh:272](../../modules/lazyatack.sh#L272)

```bash
function menu_servidor
```

Función para mostrar menú en modo servidor

---

<a id="menu_cliente"></a>

### `menu_cliente`

`function` | [modules/lazyatack.sh:307](../../modules/lazyatack.sh#L307)

```bash
function menu_cliente
```

Función para mostrar menú en modo cliente

---
