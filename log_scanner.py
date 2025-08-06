import re
import time

class LogScanner:
    def __init__(self, log_file_path="/var/log/auth.log", alert_threshold=5, time_window=60):
        self.log_file_path = log_file_path
        self.alert_threshold = alert_threshold
        self.time_window = time_window # seconds
        self.failed_attempts = {}
        self.alert_callback = None

    def set_alert_callback(self, callback):
        self.alert_callback = callback

    def _get_log_lines(self):
        try:
            # Open the file and seek to the end to only read new lines
            with open(self.log_file_path, 'r') as f:
                f.seek(0, 2) # Go to the end of the file
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(1) # Wait for new lines
                        continue
                    yield line
        except FileNotFoundError:
            print(f"Error: Log file not found at {self.log_file_path}")
            # Exit gracefully if the log file isn't found
            return
        except Exception as e:
            print(f"An error occurred while reading log file: {e}")
            return

    def scan_logs(self):
        print(f"[*] Starting log scanner for {self.log_file_path}...")
        for line in self._get_log_lines():
            self._process_line(line)

    def _process_line(self, line):
        # Detect failed SSH login attempts
        match = re.search(r'Failed password for (?:invalid user )?(\S+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port \d+', line)
        if match:
            username = match.group(1)
            ip_address = match.group(2)
            timestamp = time.time()

            if ip_address not in self.failed_attempts:
                self.failed_attempts[ip_address] = []
            self.failed_attempts[ip_address].append(timestamp)

            # Clean up old attempts outside the time window
            self.failed_attempts[ip_address] = [t for t in self.failed_attempts[ip_address] if timestamp - t < self.time_window]

            if len(self.failed_attempts[ip_address]) >= self.alert_threshold:
                alert_message = f"Possible brute-force attack from {ip_address} (failed attempts: {len(self.failed_attempts[ip_address])})"
                print(f"[!!!] ALERT: {alert_message}\n")
                if self.alert_callback:
                    self.alert_callback(ip_address, alert_message)
                self.failed_attempts[ip_address] = [] # Reset after alerting

        # Add more log parsing logic here for other suspicious activities (e.g., port scans)

if __name__ == "__main__":
    # This part is for standalone testing of LogScanner
    # In the full system, main_security_system.py will instantiate and run LogScanner.
    print("This script is intended to be run via main_security_system.py")
    print("To test standalone, ensure you have a log file (e.g., dummy_auth.log) and run:")
    print("scanner = LogScanner(log_file_path=\"./dummy_auth.log\")")
    print("scanner.set_alert_callback(lambda ip, msg: print(f\"[TEST ALERT] {msg} - IP: {ip}\"))")
    print("scanner.scan_logs()")