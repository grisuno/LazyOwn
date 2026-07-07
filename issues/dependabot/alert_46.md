# Dependabot Alert #46: python-engineio

- **State:** open
- **Severity:** high
- **CVE:** CVE-2026-48802
- **Created:** 2026-06-29T09:59:21Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/46

## Summary
python-engineio has unbound thread allocation that can cause denial of service

## Description
### Impact
An attacker can cause the creation of unnecessary background threads in the python-engineio server by exploiting the heartbeat mechanism, which launches a thread when a new connection is received, and when the client sends a PONG packet.

Note: this issue primarily affects synchronous servers. Asynchronous servers allocate background tasks instead of physical threads, which are lightweight and less likely to cause denial of service. However, the fix that was implemented was also applied to the asynchronous case.

### Patches
Version 4.13.2 addresses this issue as follows:

- The initial background thread (or async task( for heartbeat management is only launched if a client passes authentication in the `connect` handler.
- The server now ensures that there is only one background heatbeat thread (or async task) per client at a given point in time. Out of sequence PONG packets are now discarded when an active heartbeat thread is already running.
