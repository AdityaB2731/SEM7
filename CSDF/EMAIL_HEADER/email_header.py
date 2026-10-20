"""Analyze a saved RFC 822 email header without sending or contacting email."""
import argparse
import re
from email.parser import BytesParser
from email.policy import default
from email.utils import parsedate_to_datetime
from pathlib import Path


def extract_ip(header_value):
    return re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", header_value)


def print_all_headers(headers):
    print("Headers Found:")
    for name, value in headers.items():
        print(f"{name}: {value}")


def authentication_status(headers, method):
    authentication_results = headers.get("Authentication-Results", "")
    match = re.search(rf"\b{method}\s*=\s*([^\s;]+)", authentication_results, re.IGNORECASE)
    if match:
        return match.group(1)
    if method == "spf":
        received_spf = headers.get("Received-SPF", "")
        match = re.search(r"^\s*(\w+)", received_spf)
        if match:
            return match.group(1)
    return "not reported"


def analyze_email_header(raw_email):
    headers = BytesParser(policy=default).parsebytes(raw_email)
    print_all_headers(headers)
    print("\nSelected analysis:")
    date_value = headers.get("Date")
    timezone = "not present"
    if date_value:
        try:
            timezone = str(parsedate_to_datetime(date_value).tzinfo)
        except (TypeError, ValueError):
            timezone = "invalid Date header"

    print(f"From: {headers.get('From', 'not present')}")
    print(f"Return-Path: {headers.get('Return-Path', 'not present')}")
    print(f"To: {headers.get('To', 'not present')}")
    print(f"Subject: {headers.get('Subject', 'not present')}")
    print(f"Date: {date_value or 'not present'}")
    print(f"GMT/time-zone information: {timezone}")
    print(f"DKIM-Signature: {'present' if headers.get('DKIM-Signature') else 'not present'}")
    print(f"Authentication-Results: {headers.get('Authentication-Results', 'not present')}")
    print(f"SPF result: {authentication_status(headers, 'spf')}")
    print(f"DKIM result: {authentication_status(headers, 'dkim')}")
    print(f"DMARC result: {authentication_status(headers, 'dmarc')}")

    received_headers = headers.get_all("Received", [])
    print(f"Received headers: {len(received_headers)} entries found")
    for index, received in enumerate(received_headers, start=1):
        print(f"Received {index}: {received}")
        ips = extract_ip(str(received))
        if ips:
            print(f"IP addresses found: {ips}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, help="saved .eml or RFC 822 header file")
    args = parser.parse_args()
    if args.file:
        analyze_email_header(args.file.read_bytes())
        return

    sample = b"""From: example@domain.com
Return-Path: <example@domain.com>
To: recipient@domain.com
Subject: Demonstration header
Date: Tue, 20 Oct 2026 12:34:56 +0000
DKIM-Signature: v=1; d=domain.com; s=demo;
Authentication-Results: dkim=pass; spf=pass
Received: from mail.example.com [192.0.2.1]
"""
    # print("No file supplied; analyzing the safe demonstration header.\n")
    analyze_email_header(sample)


if __name__ == "__main__":
    main()
