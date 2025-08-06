#!/bin/bash

# Script to run the Security Monitoring & Alerting System

# Make the firewall controller script executable
chmod +x firewall_controller.sh

# Run the main security system script with sudo
# It's important to run with sudo because it needs to read /var/log/auth.log
# and interact with UFW.

sudo python3 main_security_system.py