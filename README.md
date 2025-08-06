# Security Monitoring & Alerting System

## Problem Statement
Traditional server setups often lack lightweight, real-time monitoring solutions for intrusion attempts such as brute-force logins or port scans. This poses a security risk, especially for resource-constrained environments like personal or small business servers.

## Objective
To build an automated, lightweight intrusion detection and alerting system that continuously monitors server logs for suspicious activities and triggers timely alerts, enhancing server security.

## Key Features

### Log Monitoring:
Continuously scans system logs (e.g., `/var/log/auth.log`) for login anomalies and port scanning behavior.

### Real-Time Alerting:
Generates alerts (email/console/log-based) on detection of suspicious events like repeated failed SSH logins or port scan patterns.

### Firewall Integration:
Configures and validates UFW (Uncomplicated Firewall) rules to block unwanted IPs and ports.

### Brute-Force Detection:
Simulates attack scenarios to test system response to unauthorized login attempts.

### Automation:
Utilizes cron jobs and bash scripts for:
- Periodic firewall status checks
- Log rotation and archival
- Auto-blacklisting of malicious IPs

## Tech Stack
- **Language:** Python, Bash
- **Tools:** Prometheus (metrics monitoring), UFW (firewall), Cron (automation), AWS EC2 (deployment)
- **OS:** Linux (Ubuntu)

## Architecture Overview

### Log Scanner (Python Script):
Parses `/var/log/auth.log` to detect abnormal login patterns.

### Alert Generator:
Sends alerts via console or file (extendable to email/Slack integration).

### Firewall Controller (Bash):
Adds UFW rules to block malicious IPs on detection.

### Automation via Cron:
Scheduled tasks for:
- Health checks
- UFW status
- Log cleanup

## Validation & Testing
- Simulated brute-force and port scan attacks (e.g., with `hydra` or `nmap`) to verify detection and response accuracy.
- Logged and verified blocked IPs post simulation.

## Outcome
A functional, resource-efficient intrusion detection and alerting system suitable for deployment on cloud instances like AWS EC2. Successfully enhanced server security posture with automated threat detection and response mechanisms.