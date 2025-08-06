class AlertGenerator:
    def __init__(self, alert_type="console"):
        self.alert_type = alert_type

    def send_alert(self, message):
        if self.alert_type == "console":
            self._send_to_console(message)
        elif self.alert_type == "file":
            self._send_to_file(message)
        # Add more alert types (e.g., email, Slack) here
        else:
            print(f"[ERROR] Unknown alert type: {self.alert_type}")

    def _send_to_console(self, message):
        print(f"[ALERT] {message}")

    def _send_to_file(self, message, filename="alerts.log"):
        with open(filename, "a") as f:
            f.write(f"[ALERT] {message}\n")

if __name__ == "__main__":
    alert_console = AlertGenerator("console")
    alert_console.send_alert("Test alert to console!")

    alert_file = AlertGenerator("file")
    alert_file.send_alert("Test alert to file!")