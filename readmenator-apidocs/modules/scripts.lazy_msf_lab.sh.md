# `scripts/lazy_msf_lab.sh`

> Source: [scripts/lazy_msf_lab.sh:1](../../scripts/lazy_msf_lab.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

lazy_msf_lab.sh — Metasploitable2 smoke lab manager for LazyOwn.

The lab image is operator-provided (Rapid7 license): place metasploitable-linux-2.0.0.zip next to this script's install dir or pass its path via MSF_LAB_ZIP. The script never downloads the image itself.  Usage: lazy_msf_lab.sh setup [zip-path]  # unzip + import guidance lazy_msf_lab.sh up                # start VM headless lazy_msf_lab.sh status            # VM state + guest IP lazy_msf_lab.sh down              # stop VM lazy_msf_lab.sh smoke [target]    # loop smoke run, prints verdict  Non-interactive except setup's import guidance (operator imports once in VirtualBox; thereafter everything is CLI-driven).
