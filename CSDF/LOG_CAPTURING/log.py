"""Generate and correlate safe sample security events or a CSV export."""
import argparse
import csv
import logging
import re
from collections import defaultdict
from pathlib import Path


def create_sample_log(path):
    logging.basicConfig(
        filename=path,
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )
    logging.info("File opened: report.txt by user=student")
    logging.error("Failed login attempt from IP: 192.168.1.10")
    logging.info("File deleted: temporary.txt by user=student")
    logging.info("User student logged in successfully")
    logging.error("Disk space error on test-volume")
    logging.info("System shutdown initiated")
    logging.error("Failed login attempt from IP: 192.168.1.11")


def correlate_events(logfile):
    patterns = {
        "failed_login": r"Failed login attempt from IP: ([\d.]+)",
        "disk_error": r"Disk space error on (.+)",
        "file_activity": r"File (opened|deleted): (.+?) by user=(\w+)",
        "shutdown": r"System shutdown initiated",
    }
    events = defaultdict(list)
    with open(logfile, encoding="utf-8") as handle:
        for line in handle:
            for name, pattern in patterns.items():
                match = re.search(pattern, line)
                if match:
                    events[name].append(match.groups() or ("detected",))
                    break
    return events


def correlate_csv(csv_file):
    events = defaultdict(list)
    with open(csv_file, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            event_type = row.get("event", "unknown")
            events[event_type].append(row)
    return events


def display(events):
    print("Correlated Event Summary:")
    for event, details in events.items():
        print(f"- {event}: {len(details)} event(s)")
        for detail in details:
            print(f"  {detail}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, help="CSV with an event column")
    parser.add_argument("--log", type=Path, default=Path("system_logs.log"))
    args = parser.parse_args()
    if args.csv:
        display(correlate_csv(args.csv))
    else:
        create_sample_log(args.log)
        display(correlate_events(args.log))


if __name__ == "__main__":
    main()
