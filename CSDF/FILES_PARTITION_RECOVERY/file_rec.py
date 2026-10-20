"""Safely inspect an existing forensic image.

Default mode only explains requirements. With --image, this script can list
an existing image using The Sleuth Kit; it never reads a live device or runs
dd. Use --execute only to inspect an image you are authorized to examine.
"""
import argparse
import shutil
import subprocess
from pathlib import Path


def explain():
    print("SAFE MODE: no device or image was opened.")
    print("The original workflow needs Linux, lsblk, dd, and The Sleuth Kit")
    print("(fls, istat, and icat), plus an authorized forensic image.")
    print("Never enter a Windows system-drive path or a live device path.")
    print("Prefer a copy of a test image stored in the CSDF folder.")


def inspect_image(image, inode=None):
    image_path = Path(image).resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f"Image does not exist: {image_path}")
    if shutil.which("fls") is None:
        raise RuntimeError("The Sleuth Kit is not installed; fls was not found.")

    subprocess.run(["fls", str(image_path)], check=True)
    if inode:
        if not inode.isdigit():
            raise ValueError("The inode must contain digits only.")
        if shutil.which("istat") is None or shutil.which("icat") is None:
            raise RuntimeError("The Sleuth Kit istat/icat commands are required.")
        subprocess.run(["istat", str(image_path), inode], check=True)
        subprocess.run(["icat", str(image_path), inode], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="existing forensic image; never a live device")
    parser.add_argument("--inode", help="optional inode to inspect from --image")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="inspect the supplied image using Sleuth Kit",
    )
    args = parser.parse_args()
    if not args.execute:
        explain()
    elif not args.image:
        raise SystemExit("--execute requires --image PATH")
    else:
        inspect_image(args.image, args.inode)
