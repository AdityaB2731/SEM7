#!/usr/bin/env python3
"""Coursework simulation of repeated Wi-Fi authentication failures. No real network changes."""
from collections import defaultdict, deque
from datetime import datetime, timedelta

THRESHOLD = 5
WINDOW_MINUTES = 2
BLOCK_MINUTES = 10

def parse_time(value):
    return datetime.fromisoformat(value)

class WiFiAttemptDetector:
    def __init__(self):
        self.failures = defaultdict(deque)
        self.blocked_until = {}

    def process(self, timestamp, device_id, success):
        now = parse_time(timestamp)
        # Remove expired blocks.
        if device_id in self.blocked_until and now >= self.blocked_until[device_id]:
            del self.blocked_until[device_id]
            print(f"[INFO] Temporary block expired for {device_id}.")

        if device_id in self.blocked_until and now < self.blocked_until[device_id]:
            print(f"[BLOCKED] {timestamp} {device_id}: attempt rejected (simulated block).")
            return

        if success:
            self.failures[device_id].clear()
            print(f"[OK] {timestamp} {device_id}: authentication succeeded.")
            return

        q = self.failures[device_id]
        q.append(now)
        cutoff = now - timedelta(minutes=WINDOW_MINUTES)
        while q and q[0] < cutoff:
            q.popleft()

        print(f"[FAIL] {timestamp} {device_id}: failed authentication ({len(q)} in window).")
        if len(q) >= THRESHOLD:
            self.blocked_until[device_id] = now + timedelta(minutes=BLOCK_MINUTES)
            q.clear()
            print(f"[ALERT] {device_id} flagged; simulated block until "
                  f"{self.blocked_until[device_id].isoformat(sep=' ')}.")

def main():
    print("Wi-Fi failed-login detector — SIMULATION ONLY")
    print("Threshold: 5 failures within 2 minutes; simulated block: 10 minutes.\n")
    detector = WiFiAttemptDetector()
    events = [
        ("2026-10-19T10:00:00", "device-A", False),
        ("2026-10-19T10:00:10", "device-A", False),
        ("2026-10-19T10:00:20", "device-A", False),
        ("2026-10-19T10:00:30", "device-A", False),
        ("2026-10-19T10:00:40", "device-A", False),
        ("2026-10-19T10:00:45", "device-A", False),
        ("2026-10-19T10:01:00", "device-B", True),
    ]
    for timestamp, device_id, success in events:
        detector.process(timestamp, device_id, success)

    print("\nFor a real access point, consult its authorized admin interface and logs.")
    print("This script does not capture 802.11 traffic or block real Wi-Fi clients.")

if __name__ == "__main__":
    main()
