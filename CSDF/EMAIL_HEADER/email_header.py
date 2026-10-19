import email
import re
from email.parser import BytesParser
from email.policy import default

# Function to extract IP addresses from email headers
def extract_ip(header_value):
    ip_pattern = r'[0-9]+(?:\.[0-9]+){3}'  # Simple IP regex
    return re.findall(ip_pattern, header_value)

# Function to analyze email headers
def analyze_email_header(raw_email):
    # Parse the email
    headers = BytesParser(policy=default).parsebytes(raw_email)

    # Get common email header fields
    from_header = headers['From']
    to_header = headers['To']
    subject_header = headers['Subject']
    received_headers = headers.get_all('Received', [])

    # Output the parsed information
    print(f"From: {from_header}")
    print(f"To: {to_header}")
    print(f"Subject: {subject_header}")
    print(f"Received headers: {len(received_headers)} entries found\n")

    # Analyze the 'Received' headers to extract IP addresses and mail hops
    for i, received in enumerate(received_headers, start=1):
        print(f"Received {i}:")
        print(received)
        ips = extract_ip(received)
        if ips:
            print(f"IP Addresses found: {ips}")
        print("----\n")

# Example email header (replace with your own raw email header in bytes)
raw_email_data = b"""\
From: example@domain.com
To: recipient@domain.com
Subject: Test Email
Received: from mail.example.com (mail.example.com [192.168.1.1])
        by mail.domain.com (Postfix) with ESMTP id 12345
        for <recipient@domain.com>; Wed, 27 Oct 2024 12:34:56 +0000 (UTC)
Received: from another-server.com (another-server.com [203.0.113.2])
        by mail.example.com (Postfix) with ESMTP id 67890
        for <recipient@domain.com>; Wed, 27 Oct 2024 12:32:10 +0000 (UTC)
"""

# Analyze the provided email header
analyze_email_header(raw_email_data)