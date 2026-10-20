"""Safe simulation of password attempts and temporary MAC banning."""
from collections import defaultdict, deque
from datetime import datetime, timedelta

THRESHOLD = 5
WINDOW_MINUTES = 2
BLOCK_MINUTES = 10
EXPECTED_PASSWORD = "lab-password"


class ResourceAccessSimulator:
    def __init__(self):
        self.failures = defaultdict(deque)
        self.banned_until = {}

    def process(self, timestamp, mac_address, password):
        now = datetime.fromisoformat(timestamp)
        if mac_address in self.banned_until and now >= self.banned_until[mac_address]:
            del self.banned_until[mac_address]
            print(f"[INFO] Temporary ban expired for {mac_address}.")
        if mac_address in self.banned_until:
            print(f"[BANNED] {mac_address}: resource access refused.")
            return
        if password == EXPECTED_PASSWORD:
            self.failures[mac_address].clear()
            print(f"[OK] {mac_address}: resource access granted.")
            return

        attempts = self.failures[mac_address]
        attempts.append(now)
        cutoff = now - timedelta(minutes=WINDOW_MINUTES)
        while attempts and attempts[0] < cutoff:
            attempts.popleft()
        print(f"[FAIL] {mac_address}: incorrect password ({len(attempts)} in window).")
        if len(attempts) >= THRESHOLD:
            self.banned_until[mac_address] = now + timedelta(minutes=BLOCK_MINUTES)
            attempts.clear()
            print(f"[ALERT] simulated MAC ban until {self.banned_until[mac_address]}.")


def main():
    print("Resource access and MAC-ban simulation — NO NETWORK CHANGES")
    simulator = ResourceAccessSimulator()
    base = "2026-10-20T10:00:"
    events = [(f"{base}{second:02d}", "AA:BB:CC:DD:EE:01", "wrong")
              for second in (0, 10, 20, 30, 40)]
    events.append((f"{base}50", "AA:BB:CC:DD:EE:01", "lab-password"))
    for event in events:
        simulator.process(*event)


if __name__ == "__main__":
    main()
