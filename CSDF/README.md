# Cyber Security and Digital Forensics (CSDF) assignments

This folder contains five coursework demonstrations. The programs use
synthetic data or copied evidence by default so they can be explained and
tested without changing a real network, disk, partition table, or firewall.

## Folder structure

| Assignment | File | Main concept |
|---|---|---|
| 1 | `EMAIL_HEADER/email_header.py` | RFC 822 email-header analysis |
| 2 | `CAPTCHA/captcha_generator.py` | CAPTCHA generation and verification |
| 3 | `PROHIBIT_WIFI/wifi_monitor.py` | CSV-based password-failure monitoring and simulated MAC blocklist |
| 4 | `FILES_PARTITION_RECOVERY/file_recovery.py` | Safe signature-based file recovery simulation |
| 5 | `LOG_CAPTURING/log.py` | Log capture and event correlation |

Supporting files are also retained:

- `PROHIBIT_WIFI/wifi_logs.csv`: synthetic login-event input for the main
  Wi-Fi monitor.
- `PROHIBIT_WIFI/wifi_detector.py`: password/resource-access simulation with a
  five-failure threshold.
- `PROHIBIT_WIFI/prohibit.py`: explanation-only outline of real monitor-mode
  tooling; it must not be used on a normal network.
- `FILES_PARTITION_RECOVERY/file_rec.py`: optional Sleuth Kit image-inspection
  workflow.
- `FILES_PARTITION_RECOVERY/part_rec.py`: explanation-only partition-recovery
  outline; it does not automate a destructive write.

## Setup on Windows

Run from the `CSDF` folder:

```powershell
cd "D:\SEM7 MINI PROJECT\LP4\codes\CSDF"
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The requirements are:

- `captcha`: CAPTCHA support and bundled font resources.
- `Pillow`: image creation, rotation, drawing, and saving.

The other assignments use Python's standard library.

## Assignment 1: email header analysis

### Objective and theory

An email is represented as an RFC 822 message containing headers and a body.
Headers record sender and routing information. Important security-related
headers include:

- `From`: displayed sender identity.
- `Return-Path`: address used for mail return handling.
- `Date`: sender-provided date and time-zone offset.
- `Received`: mail-server route and timestamps.
- `DKIM-Signature`: indicates that a DKIM signature is attached.
- `Authentication-Results`: records SPF, DKIM, and DMARC results reported by
  the receiving mail server.

The presence of a `DKIM-Signature` is not the same as a successful DKIM
verification. The program therefore reads the named authentication results.

### How the code works

1. Opens an `.eml` file as raw bytes.
2. Parses it with Python's `email` parser.
3. Prints every header.
4. Extracts important named headers.
5. Parses the `Date` field and reports its time zone.
6. Reads SPF, DKIM, and DMARC statuses from `Authentication-Results`.
7. Extracts IPv4 addresses from each `Received` header.

### Run with the included synthetic sample

```powershell
.\.venv\Scripts\python.exe `
  .\EMAIL_HEADER\email_header.py `
  --file .\EMAIL_HEADER\sample.eml
```

The sample contains documentation-only domains and IP addresses. It is safe
for classroom demonstration.

### Run with an approved real `.eml` file

```powershell
.\.venv\Scripts\python.exe `
  .\EMAIL_HEADER\email_header.py `
  --file "C:\path\to\approved-email.eml"
```

The analyzer never sends the email or contacts the mail server. Do not commit
private `.eml` files; the Git ignore file excludes `*.eml`.

## Assignment 2: CAPTCHA generation and verification

### Objective and theory

A CAPTCHA creates a challenge intended to be readable by a person but more
difficult for automated recognition. This implementation follows the
assignment requirements:

- Eight random digits.
- Dark background.
- Slanted characters using random rotation.
- Overlapping character placement.
- Interference lines.
- User input verification.

### How the code works

1. Generates an eight-digit random challenge.
2. Creates a dark image with Pillow.
3. Draws each digit using a bundled font.
4. Rotates and overlaps the digits.
5. Adds interference lines.
6. Saves the image as `CAPTCHA/captcha.png`.
7. Accepts up to three answers from the user.
8. Prints success or failure.

### Run

```powershell
.\.venv\Scripts\python.exe .\CAPTCHA\captcha_generator.py
```

Open `CAPTCHA/captcha.png`, read the eight digits, and enter them in the
terminal. The generated image is ignored by Git.

## Assignment 3: Wi-Fi login monitoring and MAC blocklist simulation

### Objective and theory

Repeated failed passwords may indicate a brute-force attempt. The main program
reads synthetic login events from `PROHIBIT_WIFI/wifi_logs.csv` and uses:

- Three failed attempts as the threshold.
- A MAC address as the device identity.
- A text blocklist instead of a real firewall rule.

### How the code works

1. Opens the CSV file using `csv.DictReader`.
2. Reads the `mac` and `status` columns from each row.
3. Counts `FAIL` events separately for each MAC address.
4. Prints each failed or successful login event.
5. Adds a MAC address to the simulated blocklist after three failures.
6. Writes blocked addresses to `PROHIBIT_WIFI/blocked_devices.txt`.

### Run

```powershell
.\.venv\Scripts\python.exe .\PROHIBIT_WIFI\wifi_monitor.py
```

The main input is [wifi_logs.csv](./PROHIBIT_WIFI/wifi_logs.csv). The current
sample contains three failed attempts for
`AA:BB:CC:11:22:33`, followed by another failure, so that address is added to
the simulated blocklist. A successful login for another address is also
shown.

This is a simulation. It does not change a MAC address, modify firewall rules,
capture Wi-Fi packets, or access a router. The output file is:

```text
PROHIBIT_WIFI\blocked_devices.txt
```

The file is only a report and is ignored by Git. Wireshark may be used only
with an instructor-approved capture file; this program does not perform live
packet capture.

The supporting [wifi_detector.py](./PROHIBIT_WIFI/wifi_detector.py) can be run
separately for a password-entry simulation:

```powershell
.\.venv\Scripts\python.exe .\PROHIBIT_WIFI\wifi_detector.py
```

It uses a five-failure threshold and a simulated ten-minute ban, but it is not
the primary Assignment 3 program.

## Assignment 4: recovery of permanently deleted data

### Objective and theory

Deleting a file commonly removes its directory reference while some file
content may remain until the storage blocks are reused. Forensic recovery
should be performed on a bit-for-bit image, not on the original device.

The procedure can be demonstrated with a disposable virtual disk or an
instructor-provided image formatted as FAT, ext3, or ext4. The Sleuth Kit
commands are:

- `fls`: lists files and directory entries, including deleted entries.
- `istat`: displays metadata for an inode.
- `icat`: extracts file content from an inode.

Autopsy provides a graphical interface for examining the same image.

### Safe terminal procedure in WSL

Install the tools:

```bash
sudo apt update
sudo apt install sleuthkit
```

Against an authorized copied image:

```bash
fls -r ./test-image.dd
istat ./test-image.dd INODE
icat ./test-image.dd INODE > recovered.bin
```

### Main Python program

[file_recovery.py](./FILES_PARTITION_RECOVERY/file_recovery.py) is the main
Assignment 4 program. It performs signature carving: it searches image bytes
for the start and end signatures of JPG, PNG, and PDF files, then writes each
matching byte range to a recovered file.

Run the completely safe synthetic simulation:

```powershell
.\.venv\Scripts\python.exe `
  .\FILES_PARTITION_RECOVERY\file_recovery.py `
  --demo
```

The demo creates a temporary synthetic image, recovers three fake files, and
writes them to `recovered_files_demo`. It does not read a disk, USB drive, or
personal file.

To scan an authorized copied forensic image:

```powershell
.\.venv\Scripts\python.exe `
  .\FILES_PARTITION_RECOVERY\file_recovery.py `
  .\test-image.dd
```

Recovered output is written to `recovered_files`. If no image is available,
run the program without arguments to display its usage instructions:

```powershell
.\.venv\Scripts\python.exe .\FILES_PARTITION_RECOVERY\file_recovery.py
```

### Supporting Sleuth Kit program

[file_rec.py](./FILES_PARTITION_RECOVERY/file_rec.py) is an optional
Sleuth-Kit-based workflow for an existing image. It does not run `dd` and does
not read a live device:

```bash
python3 FILES_PARTITION_RECOVERY/file_rec.py
python3 FILES_PARTITION_RECOVERY/file_rec.py \
  --execute --image ./test-image.dd --inode INODE
```

Never use a Windows system path, `/dev/sda`, `/dev/nvme0n1`, or `/mnt/c` as a
test target. The partition script intentionally does not automate a destructive
partition-table write.

There is also a simple signature-carving demonstration in
`FILES_PARTITION_RECOVERY/file_recovery.py`. It requires an existing image
file as its only argument:

```powershell
.\.venv\Scripts\python.exe `
  .\FILES_PARTITION_RECOVERY\file_recovery.py `
  .\test-image.dd
```

It searches the image bytes for JPG, PNG, and PDF start/end signatures and
writes recovered copies to `FILES_PARTITION_RECOVERY\recovered_files`.
Running it without an argument only displays the safe usage instructions:

```powershell
.\.venv\Scripts\python.exe .\FILES_PARTITION_RECOVERY\file_recovery.py
```

For a completely harmless demonstration, use its synthetic-image mode:

```powershell
.\.venv\Scripts\python.exe `
  .\FILES_PARTITION_RECOVERY\file_recovery.py `
  --demo
```

This creates a temporary synthetic byte file containing fake JPG, PNG, and
PDF signatures, recovers them, and writes the results to
`recovered_files_demo`. It does not inspect a real disk or personal file.

Do not provide a live disk path. Use a disposable lab image or an
instructor-provided copy.

## Assignment 5: log capturing and event correlation

### Objective and theory

Log correlation groups related events to identify a sequence, such as failed
logins followed by file activity or a shutdown. The program demonstrates the
same idea using generated security events or an approved CSV export.

### How the code works

1. Creates sample log entries for file access, login attempts, disk errors, and
   shutdown.
2. Reads the log line by line.
3. Uses regular expressions to identify event types.
4. Extracts useful values such as IP addresses and file names.
5. Groups matching events.
6. Prints a correlated summary.

It can also read a CSV file with an `event` column:

```text
timestamp,event,user,details
2026-10-20T10:00:00,login_failure,student,wrong password
```

### Run generated demonstration

```powershell
.\.venv\Scripts\python.exe .\LOG_CAPTURING\log.py
```

### Run with an approved CSV

```powershell
.\.venv\Scripts\python.exe `
  .\LOG_CAPTURING\log.py `
  --csv .\events.csv
```

Windows Event Viewer can export approved logs as CSV. Do not export or share
private user information without permission. The generated `system_logs.log`
is ignored by Git.

## Safety and limitations

The sample email, Wi-Fi events, logs, and forensic instructions are intended
for education. Real email headers, network monitoring, firewall rules,
partition editing, and physical-media recovery require authorization and an
isolated lab or virtual machine. The safe demonstrations do not claim to have
performed those real-world operations.
