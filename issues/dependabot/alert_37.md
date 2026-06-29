# Dependabot Alert #37: cryptography

- **State:** open
- **Severity:** high
- **CVE:** N/A
- **Created:** 2026-06-19T18:40:18Z
- **URL:** https://github.com/grisuno/LazyOwn/security/dependabot/37

## Summary
Vulnerable OpenSSL included in cryptography wheels

## Description
pyca/cryptography's wheels include a statically linked copy of OpenSSL. The versions of OpenSSL included in wheels prior to cryptograph 48.01 are vulnerable to a security issue. More details about the vulnerability itself can be found in https://openssl-library.org/news/secadv/20260609.txt.

If you are building cryptography source ("sdist") then you are responsible for upgrading your copy of OpenSSL. Only users installing from wheels built by the cryptography project (i.e., those distributed on PyPI) need to update their cryptography versions.
