import time
import subprocess
from log_scanner import LogScanner
from alert_generator import AlertGenerator

class SecuritySystem:
    def __init__(self, log_file="/var/log/auth.log", alert_threshold=5, time_window=60, alert_type="console"):
        self.log_scanner = LogScanner(log_file, alert_threshold, time_window)
        self.alert_generator = AlertGenerator(alert_type)
        # self.firewall_script = "./firewall_controller.sh"
        self.log_scanner.set_alert_callback(self._handle_alert)

    def _handle_alert(self, ip_address, message):
        self.alert_generator.send_alert(message)
        # self.block_ip(ip_address)

    def run(self):
        print("[*] Starting Security Monitoring & Alerting System...")
        try:
            # The log scanner runs in a blocking loop, so this main loop won't proceed
            # unless the log scanner is run in a separate thread/process or modified.
            # For now, let's just run the scanner and let it handle alerts internally.
            self.log_scanner.scan_logs() # This will block and continuously scan

        except KeyboardInterrupt:
            print("[*] Security Monitoring & Alerting System stopped.")



# To run this system:
# 1. Make sure you have `log_scanner.py`, `alert_generator.py`, and `firewall_controller.sh` in the same directory.
# 2. Make `firewall_controller.sh` executable: `chmod +x firewall_controller.sh`
# 3. Run this script as root or with sudo for `/var/log/auth.log` access and UFW commands:
#    `sudo python3 main_security_system.py`

if __name__ == "__main__":
    # Note: For testing on a non-Linux system or without root, you might need to:
    # - Change log_file to a dummy file you can write to.
    # - Comment out or mock the firewall_controller.sh calls.
    # Example for testing with a dummy log file:
    # system = SecuritySystem(log_file="./dummy_auth.log", alert_type="console")

    system = SecuritySystem(log_file="./dummy_auth.log", alert_type="console")
    system.run()