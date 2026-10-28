# LazyOwn data knowledge bases

Static, local-first datasets consumed by LazyOwn modules. Nothing here
phones home; every consumer reads from disk only.

## default_creds.csv

Vendor/product default-credential pairs (`productvendor,username,password`)
seeded from the open [DefaultCreds-Cheat-Sheet](https://github.com/ihebski/DefaultCreds-Cheat-Sheet)
(MIT) as curated by [threekiii/awesome-redteam](https://github.com/threekiii/awesome-redteam).
Consumed by `modules/lazy_creds.py` (`lazycreds` shell command) for
lookups and lab credential-spray planning. Lab fixtures keep using their
own documented passwords; this file is reference data, not a policy
change.
