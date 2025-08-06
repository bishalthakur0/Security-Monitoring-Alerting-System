#!/bin/bash

# This script manages UFW rules for blocking malicious IPs.

BLOCK_LIST_FILE="/etc/security_monitoring/blocked_ips.txt"

mkdir -p $(dirname $BLOCK_LIST_FILE)

# Function to block an IP address
block_ip() {
    IP=$1
    if [[ -z "$IP" ]]; then
        echo "Error: No IP address provided to block_ip."
        return 1
    fi

    # Check if IP is already blocked
    if ufw status | grep -q "${IP} DENY"; then
        echo "IP ${IP} is already blocked."
    else
        echo "Blocking IP: ${IP}"
        ufw deny from ${IP} to any
        if [ $? -eq 0 ]; then
            echo "${IP}" >> "$BLOCK_LIST_FILE"
            echo "IP ${IP} blocked successfully."
        else
            echo "Failed to block IP ${IP}. Check UFW status and permissions."
        fi
    fi
}

# Function to unblock an IP address (optional, for management)
unblock_ip() {
    IP=$1
    if [[ -z "$IP" ]]; then
        echo "Error: No IP address provided to unblock_ip."
        return 1
    fi

    if ufw status | grep -q "${IP} DENY"; then
        echo "Unblocking IP: ${IP}"
        ufw delete deny from ${IP} to any
        if [ $? -eq 0 ]; then
            sed -i "/${IP}/d" "$BLOCK_LIST_FILE"
            echo "IP ${IP} unblocked successfully."
        else
            echo "Failed to unblock IP ${IP}. Check UFW status and permissions."
        fi
    else
        echo "IP ${IP} is not currently blocked by UFW."
    fi
}

# Function to list blocked IPs
list_blocked_ips() {
    echo "Currently blocked IPs (from ${BLOCK_LIST_FILE}):"
    if [ -f "$BLOCK_LIST_FILE" ]; then
        cat "$BLOCK_LIST_FILE"
    else
        echo "No IPs blocked yet."
    fi
}

# Main logic for script execution
case "$1" in
    block)
        block_ip $2
        ;;
    unblock)
        unblock_ip $2
        ;;
    list)
        list_blocked_ips
        ;;
    *)
        echo "Usage: $0 {block|unblock} <IP_ADDRESS> | list"
        echo "Example: $0 block 192.168.1.100"
        echo "Example: $0 list"
        ;;
esac