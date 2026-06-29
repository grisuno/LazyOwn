# Dependabot Alert #47: python-socketio

- **State:** open
- **Severity:** high
- **CVE:** CVE-2026-48804
- **Created:** 2026-06-29T09:59:21Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/47

## Summary
python-socketio: Binary attachment accumulation can cause denial of service

## Description
### Impact
The python-socketio server stores binary `EVENT` and `ACK` messages in memory while it waits to receive their binary attachments. Once all the attachments are received, these messages are then processed. An attacker can submit a binary message and intentionally omit sending one or more of its attachments to cause the message along with the partial list of received attachments to stay in memory for a long time.

### Patches
Version 5.16.2 takes the following measures to address this issue:
- Binary packets are only accepted from authenticated clients.
- When a client disconnects, the server checks if there is a partial binary message being held for the client and deletes it.
