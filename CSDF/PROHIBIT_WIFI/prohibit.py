"""Explain the Wi-Fi monitoring requirements without changing the system.

The default mode is safe and does not start monitor mode, capture traffic, or
change firewall rules. Real execution requires --execute and authorized Linux
hardware.
"""
import argparse
import re
import subprocess


def block_mac(mac):
    subprocess.run(
        ["sudo", "iptables", "-A", "INPUT", "-m", "mac",
         "--mac-source", mac, "-j", "DROP"],
        check=True,
    )
    print(f"Blocked MAC: {mac}")


def monitor(interface="wlan0mon"):
    proc = subprocess.Popen(
        ["airodump-ng", interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        for line in proc.stdout:
            if "Deauth" in line or "Disassoc" in line:
                mac = re.search(r"([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}", line)
                if mac:
                    block_mac(mac.group(0))
    finally:
        proc.terminate()


def explain():
    print("SAFE MODE: no Wi-Fi commands were executed.")
    print("This script needs Linux, sudo, aircrack-ng, iptables, and a")
    print("compatible USB Wi-Fi adapter that supports monitor mode.")
    print("It would change wireless mode and add firewall DROP rules.")
    print("Use only on equipment and networks you administer.")
    print("For a harmless demonstration, run wifi_detector.py instead.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually start monitor mode and modify firewall rules",
    )
    parser.add_argument("--interface", default="wlan0mon")
    args = parser.parse_args()

    if not args.execute:
        explain()
        return

    print("Explicit execution requested; ensure you have authorization.")
    subprocess.run(["sudo", "airmon-ng", "start", "wlan0"], check=True)
    try:
        monitor(args.interface)
    except KeyboardInterrupt:
        pass
    finally:
        subprocess.run(["sudo", "airmon-ng", "stop", args.interface], check=False)


if __name__ == "__main__":
    main()
