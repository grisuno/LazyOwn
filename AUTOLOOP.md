# Your first auto loop

#1 lab above (ISO container, IP by docker bridge)

```bash
lab start metasploitable # note the IP: 172.17.x.x
lab status metasploitable # confirm up + ports
```

#2 target in payload

```bash
assign rhost <IP> # ex: assign rhost 172.17.0.2
```

#3 gym sanitation

```bash
gym_ms2 validate # mapping index↔exploits↔chains consistent
gym_ms2 chains # catalog: vsftpd, distcc, unreal, tomcat, dvwa...
```

#4 gamified full kill-chain (recon→enum→exploit→postexp→privesc→exfil, root + /etc/shadow)

```bash
gym start metasploitable_full_chain --target <IP>
gym status # run_id + phases
gym hint # if you get stuck
```
#5 autonomous loop (new engine + ledger + handoff)

```bash
auto_loop --target <IP> --rounds 8 --workers 3 'gain root on metasploitable and exfiltrate /etc/shadow'
```

# demo-friendly: for when there is proven exploitability (does not compile exploits or root shell)

```bash
auto_loop --mode pentest --target <IP> --rounds 8 --workers 2 'demonstrate exploitability on metasploitable'
```

#6 a concrete vector per chain (without LLM, deterministic)

```bash
apt_chain gym_metasploitable_ms2_distcc_exec <IP>
apt_chain gym_metasploitable_ms2_apache_trace <IP>
apt_chain gym_metasploitable_ms2_dns_recursion <IP>
```

#7 resume if you interrupt

```bash
apt_chain checkpoints
apt_chain summarizes <run_id> <IP>
```

#8 verification/results

```bash
lazy_status <task_id> # overview + budget
lazy_findings <task_id> # states vstate/level/technique_id ATT&CK
lazy_findings <task_id> handoff # durable handoff: confirmed + discarded + decision
lazy_trace <task_id> list # command audit
gym submit <run_id> --techniques service_enum,exploit,privesc_linux,data_exfil
gym leaderboard 10 # ELO karma
```
