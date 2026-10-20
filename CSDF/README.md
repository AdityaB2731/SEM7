# CSDF scripts

The assignment write-up, algorithms, safe procedures, and sample-output
format are in [CSDF_WRITEUP.md](./CSDF_WRITEUP.md).

## Windows setup

Open PowerShell in this folder:

```powershell
cd "D:\SEM7 MINI PROJECT\LP4\codes\CSDF"
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The `.venv` directory is ignored by Git. Use the explicit executable path above
so activation is not required. If activation is preferred, run
`.\.venv\Scripts\Activate.ps1` first and then use `python`.

## Run each script

Run these from the `CSDF` directory:

```powershell
# CAPTCHA: generates 8 dark, slanted, overlapping digits and verifies input
.\.venv\Scripts\python.exe .\CAPTCHA\captcha_generator.py

# Email header analysis: uses a safe sample; add --file .\sample.eml for real approved headers
.\.venv\Scripts\python.exe .\EMAIL_HEADER\email_header.py

# Log capture and event correlation: creates system_logs.log
.\.venv\Scripts\python.exe .\LOG_CAPTURING\log.py

# Password/resource access and temporary MAC-ban simulation (no network changes)
.\.venv\Scripts\python.exe .\PROHIBIT_WIFI\wifi_detector.py
```

The following scripts are Linux-only coursework tools and are not safe to run
on a normal Windows machine:

- `PROHIBIT_WIFI\prohibit.py` requires `airmon-ng`, `airodump-ng`, `iptables`,
  a compatible wireless adapter, and administrator privileges. It changes
  monitor mode and firewall rules.
- `FILES_PARTITION_RECOVERY\part_rec.py` requires Linux `lsblk` and `fdisk`,
  `sudo`, and a carefully selected disk. It can modify a partition table.
- `FILES_PARTITION_RECOVERY\file_rec.py` requires Linux `lsblk`, `dd`, and
  The Sleuth Kit commands `fls`, `istat`, and `icat`. It reads raw devices and
  should only be used against an authorized forensic image.

Do not run the Linux-only scripts against a disk or network without explicit
authorization. They now default to a safe explanation mode. You can inspect
that mode on Windows with:

```powershell
.\.venv\Scripts\python.exe .\PROHIBIT_WIFI\prohibit.py
.\.venv\Scripts\python.exe .\FILES_PARTITION_RECOVERY\part_rec.py
.\.venv\Scripts\python.exe .\FILES_PARTITION_RECOVERY\file_rec.py
```

## WSL guidance

WSL is useful for learning Linux commands, but it does not normally expose a
Windows laptop's internal Wi-Fi adapter for monitor mode. `prohibit.py` needs a
compatible external USB adapter, Linux support, `aircrack-ng`, and `iptables`;
do not use `--execute` on your normal network.

Do not pass Windows system disks or `/mnt/c` paths to disk-recovery commands.
For safe practice, use a disposable virtual machine and a copied forensic
image. The safe image inspection mode never runs `dd`:

```bash
python3 FILES_PARTITION_RECOVERY/file_rec.py
python3 FILES_PARTITION_RECOVERY/file_rec.py --execute --image ./test-image.dd
```

The partition script intentionally does not automate its destructive `fdisk`
write step, even with `--execute`; it only displays devices and explains the
lab requirements.

On Windows, use the compile check below instead:

```powershell
.\.venv\Scripts\python.exe -m py_compile `
  .\PROHIBIT_WIFI\prohibit.py `
  .\FILES_PARTITION_RECOVERY\part_rec.py `
  .\FILES_PARTITION_RECOVERY\file_rec.py
```
