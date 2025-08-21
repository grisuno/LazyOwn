#!/bin/bash

#-------------------------------------------------------------------------------
# iptables-port-forward.sh
#
# This script configures port forwarding using iptables. It can either set up
# the rules to redirect traffic or clean them up.
#
# Usage:
#   To set up: ./iptables-port-forward.sh -t <DESTINATION_IP> -p <PORT>
#   To clean:  ./iptables-port-forward.sh -t <DESTINATION_IP> -c
#
# Options:
#   -t <DESTINATION_IP>  : The IP address where traffic will be redirected.
#   -p <PORT>            : The destination port. Default is 80.
#   -c                   : Clean up all rules added by this script.
#-------------------------------------------------------------------------------

# Define script variables
DESTINATION_IP=""
DESTINATION_PORT="80"
CLEAN_MODE=false

#-------------------------------------------------------------------------------
# Function: display_usage
#
# Displays the correct usage of the script and exits.
#-------------------------------------------------------------------------------
display_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -t <DESTINATION_IP>  IP address to redirect traffic to."
    echo "  -p <PORT>            Destination port. Default is 80."
    echo "  -c                   Remove all iptables rules added by this script."
    echo ""
    exit 1
}

# Process command-line arguments
while getopts "t:p:c" opt; do
    case ${opt} in
        t)
            DESTINATION_IP=$OPTARG
            ;;
        p)
            DESTINATION_PORT=$OPTARG
            ;;
        c)
            CLEAN_MODE=true
            ;;
        *)
            display_usage
            ;;
    esac
done

# --- Script Logic ---

if [ "$CLEAN_MODE" = true ]; then
    echo "Cleaning up iptables rules..."

    if [ -z "$DESTINATION_IP" ]; then
        echo "Error: The destination IP (-t) is required to clean the rules."
        display_usage
    fi

    # Remove rules in reverse order of addition
    iptables -t nat -D POSTROUTING -j MASQUERADE
    iptables -t nat -D PREROUTING -p tcp --dport "$DESTINATION_PORT" -j DNAT --to-destination "$DESTINATION_IP":"$DESTINATION_PORT"
    iptables -D INPUT -p tcp -m tcp --dport "$DESTINATION_PORT" -j ACCEPT
    iptables -D FORWARD -j ACCEPT
    
    echo "Iptables rules for IP $DESTINATION_IP and port $DESTINATION_PORT have been removed."

else
    if [ -z "$DESTINATION_IP" ]; then
        echo "Error: The destination IP (-t) is required to set up the rules."
        display_usage
    fi

    echo "Setting up port forwarding to $DESTINATION_IP:$DESTINATION_PORT..."

    # 1. Enable IP forwarding in the kernel
    sysctl net.ipv4.ip_forward=1
    
    # 2. Allow incoming traffic to the port
    iptables -I INPUT -p tcp -m tcp --dport "$DESTINATION_PORT" -j ACCEPT
    
    # 3. Redirect traffic to the destination
    iptables -t nat -A PREROUTING -p tcp --dport "$DESTINATION_PORT" -j DNAT --to-destination "$DESTINATION_IP":"$DESTINATION_PORT"
    
    # 4. Masquerade the source IP for the destination to reply
    iptables -t nat -A POSTROUTING -j MASQUERADE
    
    # 5. Allow packet routing
    iptables -I FORWARD -j ACCEPT
    iptables -P FORWARD ACCEPT
    
    echo "Configuration complete. Traffic to port $DESTINATION_PORT is now forwarded to $DESTINATION_IP."
fi