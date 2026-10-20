# LP4 CSDF assignments: write-up and safe procedure

This document follows the five supplied guidelines. The demonstrations use
synthetic data where real email, Wi-Fi, registry, or storage evidence would
expose private information or risk changing a device. Replace the marked
sample evidence with instructor-approved evidence before submission.

## General format

For each assignment include: aim, theory, algorithm, requirements, procedure,
implementation, output, result, and safety/limitations.

## Assignment 1: Email header analysis

### Aim and theory

An RFC 822 message contains headers such as `From`, `Return-Path`, `Date`,
`Received`, `DKIM-Signature`, and `Authentication-Results`. `Received` headers
show mail hops. `Date` contains the sender's stated time and UTC offset.
`DKIM-Signature` identifies a signed message; it is not by itself proof that
DKIM verification passed. `Authentication-Results` records the receiving
server's SPF/DKIM/DMARC result.

### Algorithm

1. Read raw RFC 822 bytes.
2. Parse the headers with Python's `email` parser.
3. Print every header as a `(header-name, header-value)` pair.
4. Extract `From`, `Return-Path`, `Date`, DKIM, authentication results, and
   `Received` fields.
5. Parse the date and report its time-zone offset.
6. Extract SPF, DKIM, and DMARC results by header name, not by fixed position.
7. Extract IPv4 addresses from each `Received` field.

### Safe procedure

In Gmail, open an instructor-approved message, choose **More > Show original**,
and download/copy the original headers only. Do not commit or share a private
header. Save it locally as `sample.eml`, then run:

```powershell
.\.venv\Scripts\python.exe .\EMAIL_HEADER\email_header.py --file .\sample.eml
```

Paste the same header into MXToolbox RFC822 only if permitted by your
instructor and your institution's privacy policy. Record the result and remove
the file after grading. Without a real header, the program uses a safe
demonstration header:

```powershell
.\.venv\Scripts\python.exe .\EMAIL_HEADER\email_header.py
```

The implementation is similar to the basic `HeaderParser` example: it prints
all parsed headers first, then performs named-field analysis. Avoid code such
as `headers.items()[6]`; `items()` is not a list in Python 3, and header order
does not guarantee that position 6 contains SPF or DKIM. Use
`headers.get("Authentication-Results")` and inspect the named result instead.

## Assignment 2: CAPTCHA generation

### Aim and theory

CAPTCHA generation creates a challenge that is easy for a person to read but
hard for automated recognition. This implementation uses eight random digits,
a dark background, rotation (slant), overlapping placement, and interference
lines. Verification compares the entered value with the value kept in memory.

### Procedure and output

```powershell
.\.venv\Scripts\python.exe .\CAPTCHA\captcha_generator.py
```

The image is saved at `CAPTCHA\captcha.png`. Enter its eight digits. There are
three attempts; the program prints success or failure. The generated image is
ignored by Git.

## Assignment 3: Resource access and MAC-ban simulation

### Aim and theory

Repeated incorrect passwords can indicate a brute-force attempt. A sliding
two-minute window counts failures. At five failures, the simulation bans the
MAC address for ten minutes. A successful password clears that address's
failure count.

### Procedure and output

```powershell
.\.venv\Scripts\python.exe .\PROHIBIT_WIFI\wifi_detector.py
```

The output shows five failures, a simulated ban, and a rejected sixth request.
No Wi-Fi adapter, firewall, packet capture, or MAC address is modified.
Wireshark may be used only to inspect an instructor-provided capture; this
program does not capture live traffic.

## Assignment 4: Deleted-file recovery

### Aim and theory

Deleting a file usually removes directory metadata first; file blocks may
remain until reused. Forensic recovery works on a bit-for-bit image, not an
original device. The Sleuth Kit tools commonly used are `fls` (file listing),
`istat` (metadata), and `icat` (content extraction). FAT, ext3, and ext4 have
different metadata and journaling behavior.

### Safe procedure

Use a disposable virtual disk or instructor-provided image, never a personal
USB drive or Windows system disk. First work from the terminal in WSL:

```bash
sudo apt update
sudo apt install sleuthkit
fls -r ./test-image.dd
istat ./test-image.dd INODE
icat ./test-image.dd INODE > recovered.bin
```

The Python program safely inspects an existing image and never runs `dd`:

```bash
python3 FILES_PARTITION_RECOVERY/file_rec.py
python3 FILES_PARTITION_RECOVERY/file_rec.py \
  --execute --image ./test-image.dd --inode INODE
```

Do not pass `/dev/sda`, `/dev/nvme0n1`, `/mnt/c`, or a live Windows path.
Autopsy can be used as a graphical cross-check on the same copied image.
The partition exercise is described but does not automate a partition-table
write, because an incorrect device selection can destroy data.

## Assignment 5: Log capture and event correlation

### Aim and theory

Log correlation groups related events to reveal a sequence, such as failed
login attempts followed by file activity or shutdown. Windows Event Viewer can
export an instructor-approved CSV. Do not export private user data.

### Procedure and output

Run the safe generated-log demonstration:

```powershell
.\.venv\Scripts\python.exe .\LOG_CAPTURING\log.py
```

To correlate an approved CSV, it must contain an `event` column:

```powershell
.\.venv\Scripts\python.exe .\LOG_CAPTURING\log.py --csv .\events.csv
```

The program reports counts and records grouped by event type. The generated
`system_logs.log` is ignored by Git.

## Limitations and evidence statement

The email, registry, Wi-Fi, and storage demonstrations are not claims about
real systems. They demonstrate the algorithms using synthetic or
instructor-approved copied evidence. Real network monitoring, firewall
changes, partition edits, and recovery from physical media require explicit
authorization and should be performed in an isolated lab or virtual machine.
