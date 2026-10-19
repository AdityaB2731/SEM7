import logging
import re
from collections import defaultdict

# Step 1: Log Capturing
# Configure the logging system
logging.basicConfig(filename='system_logs.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log different events
logging.info("System started")
logging.warning("Low memory warning")
logging.error("Failed login attempt from IP: 192.168.1.10")
logging.info("User admin logged in successfully")
logging.error("Disk space error on /dev/sda1")
logging.info("System shutdown initiated")
logging.info("Failed login attempt from IP: 192.168.1.11")

# Step 2: Event Correlation
def correlate_events(logfile):
    event_patterns = {
        'failed_login': r'Failed login attempt from IP: ([\d\.]+)',
        'disk_error': r'Disk space error on (.+)',
        'shutdown': r'System shutdown initiated',
    }

    correlated_events = defaultdict(list)

    with open(logfile, 'r') as f:
        for line in f:
            # Check for failed login attempts
            if re.search(event_patterns['failed_login'], line):
                ip = re.findall(event_patterns['failed_login'], line)[0]
                correlated_events['failed_login'].append(ip)
            
            # Check for disk space errors
            elif re.search(event_patterns['disk_error'], line):
                disk = re.findall(event_patterns['disk_error'], line)[0]
                correlated_events['disk_error'].append(disk)

            # Check for system shutdown events
            elif re.search(event_patterns['shutdown'], line):
                correlated_events['shutdown'].append("System shutdown detected")

    return correlated_events

# Step 3: Display the Correlated Events
correlated_data = correlate_events('system_logs.log')

# Output the correlated events
print("Correlated Event Summary:")
for event, details in correlated_data.items():
    if event == 'failed_login':
        print(f"Failed login attempts from IPs: {', '.join(details)}")
    elif event == 'disk_error':
        print(f"Disk errors detected on: {', '.join(details)}")
    elif event == 'shutdown':
        print(f"{len(details)} shutdown events detected")