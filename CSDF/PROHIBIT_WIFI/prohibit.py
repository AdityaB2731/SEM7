import os, re, subprocess

# Block MAC address using iptables
def block_mac(mac):
    os.system(f"sudo iptables -A INPUT -m mac --mac-source {mac} -j DROP")
    print(f"Blocked MAC: {mac}")

# Monitor WiFi for suspicious activity
def monitor(interface='wlan0mon'):
    proc = subprocess.Popen(['airodump-ng', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = proc.stdout.readline().decode('utf-8')
        if "Deauth" in line or "Disassoc" in line:
            mac = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
            if mac:
                block_mac(mac.group(0))

if __name__ == "__main__":
    os.system('sudo airmon-ng start wlan0')  # Enable monitor mode
    try:
        monitor()  # Start monitoring
    except KeyboardInterrupt:
        os.system('sudo airmon-ng stop wlan0mon')  # Stop monitor mode