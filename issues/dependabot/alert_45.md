# Dependabot Alert #45: python-engineio

- **State:** open
- **Severity:** high
- **CVE:** CVE-2026-48809
- **Created:** 2026-06-29T09:59:20Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/45

## Summary
python-engineio has possible denial of service due to maximum payload size sometimes not being enforced

## Description
### Impact
There are two specific configurations of the python-engineio server in which the size of incoming messages is not checked before the messages are loaded into memory. An attacker can take advantage of these to cause unnecessary memory allocations in the python-engineio server. The two cases are:

- POST requests, when using ASGI with the long polling transport
- WebSocket messages, when using Aiohttp with the WebSocket transport

### Patches
Version 4.13.2 addresses this issue as follows:

- ASGI severs now only load the body of incoming requests into memory after the client is confirmed to be known and authenticated, and the payload size is below the maximum allowed size. Requests that do not comply with these requirements are discarded.
- Aiohttp servers configure the maximum payload size in the underlying WebSocket layer from Aiohttp, so that large messages are discarded by Aiohttp before they are delivered to python-engineio.
