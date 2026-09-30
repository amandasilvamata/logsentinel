import sys

from backend.parser import read_failed_attempts
from backend.detector import detect_brute_force, detect_root_attacks, detect_success_after_failures

if len(sys.argv) < 2:
    print("Usage: python3 src/main.py <log_file>")
    sys.exit()


log_file = sys.argv[1]

try:
    events = read_failed_attempts(log_file)

except FileNotFoundError:
    print(f"Error: file not found: {log_file}")
    sys.exit()

except PermissionError:
    print(f"Error: permission denied: {log_file}")
    sys.exit()

brute_force_alerts = detect_brute_force(events)
root_alerts = detect_root_attacks(events)
success_after_failures_alerts = detect_success_after_failures(events)


for alert in brute_force_alerts:
    print()
    print("[ALERT] Possible brute-force attack")
    print(f"IP: {alert['ip']}")
    print(f"Failed attempts: {alert['attempts']}")
    print(f"Time window: {alert['time_window']} seconds")


for alert in root_alerts:
    print()
    print("[ALERT] Repeated attempts against root account")
    print(f"IP: {alert['ip']}")
    print(f"User: {alert['user']}")
    print(f"Failed attempts: {alert['attempts']}")

for alert in success_after_failures_alerts:
    print()
    print("[ALERT] Successful login after repeated failures")
    print(f"IP: {alert['ip']}")
    print(f"User: {alert['user']}")
    print(f"Previous failed attempts: {alert['failed_attempts']}")
    print(f"Successful login at: {alert['timestamp']}")