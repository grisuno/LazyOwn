# `modules/iptables_portforward.sh`

> Source: [modules/iptables_portforward.sh:1](../../modules/iptables_portforward.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

------------------------------------------------------------------------------- iptables-port-forward.sh  This script configures port forwarding using iptables.

It can either set up the rules to redirect traffic or clean them up.  Usage: To set up: ./iptables-port-forward.sh -t <DESTINATION_IP> -p <PORT> To clean:  ./iptables-port-forward.sh -t <DESTINATION_IP> -c  Options: -t <DESTINATION_IP>  : The IP address where traffic will be redirected. -p <PORT>            : The destination port. Default is 80. -c                   : Clean up all rules added by this script. -------------------------------------------------------------------------------

## Contents

- **Functions:** [`display_usage`](#display_usage)

## Functions

<a id="display_usage"></a>

### `display_usage`

`function` | [modules/iptables_portforward.sh:29](../../modules/iptables_portforward.sh#L29)

```bash
display_usage()
```

Function: display_usage

Displays the correct usage of the script and exits.

---
