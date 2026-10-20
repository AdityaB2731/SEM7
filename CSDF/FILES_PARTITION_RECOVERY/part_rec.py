"""Explain partition recovery requirements without touching a disk by default."""
import argparse


def explain():
    print("SAFE MODE: no disk commands were executed.")
    print("This Linux-only exercise needs lsblk, fdisk, sudo, and a")
    print("separate disposable test disk or virtual disk.")
    print("The original workflow can write a partition table and destroy data.")
    print("Create a backup or VM snapshot before any authorized experiment.")
    print("Use --execute only after selecting a disposable device deliberately.")


def execute():
    import subprocess

    print("Devices (review carefully; no changes yet):")
    subprocess.run(["lsblk"], check=True)
    device = input("Disposable device name, for example sdb: ").strip()
    if not device or "/" in device or "\\" in device:
        raise ValueError("Enter a device name such as sdb, not a path.")
    print("The original fdisk write operation is intentionally not automated.")
    print("Use a VM or lab guide to create a test partition manually.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    execute() if args.execute else explain()
