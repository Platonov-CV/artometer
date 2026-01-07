#!/usr/bin/env python3
"""
Debug script to extract exact headers from working curl command
"""

import re
import urllib.parse

def parse_curl_command():
    print("=" * 60)
    print("PASTE YOUR WORKING CURL COMMAND FROM BROWSER DEV TOOLS")
    print("Make sure it's the exact curl command for the search/projects.json request")
    print("=" * 60)
    print()

    # Read multi-line curl command
    lines = []
    print("Paste your curl command (end with empty line):")
    while True:
        try:
            line = input().strip()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break

    curl_command = " ".join(lines)
    print(f"\nReceived curl command ({len(curl_command)} chars)\n")

    # Extract headers
    headers = {}

    # Find all -H flags
    header_matches = re.findall(r'-H\s+[\'"]([^\'"]+)[\'"]', curl_command)
    for header_str in header_matches:
        if ':' in header_str:
            name, value = header_str.split(':', 1)
            name = name.strip()
            value = value.strip()
            headers[name] = value

    # Extract URL
    url_match = re.search(r'[\'"]?([^\'"\s]+\.artstation\.com/api/v2/search/projects\.json[^\'"\s]*)[\'"]?', curl_command)
    url = url_match.group(1) if url_match else "https://www.artstation.com/api/v2/search/projects.json"

    # Extract data
    data_match = re.search(r'--data-raw\s+[\'"]([^\'"]+)[\'"]', curl_command)
    data = data_match.group(1) if data_match else None

    print("=" * 60)
    print("EXTRACTED HEADERS:")
    print("=" * 60)

    for name, value in headers.items():
        if name.lower() == 'cookie':
            print(f"{name}:")
            # Parse cookies
            cookies = value.split('; ')
            for cookie in cookies:
                if '=' in cookie:
                    cname, cval = cookie.split('=', 1)
                    print(f"  {cname}: {cval}")
        else:
            print(f"{name}: {value}")

    print(f"\nURL: {url}")

    if data:
        print(f"\nDATA: {data}")

    print("\n" + "=" * 60)
    print("COPY THIS TO YOUR SCRIPT:")
    print("=" * 60)

    # Generate Python code
    print("# Headers for your script:")
    print("headers = {")
    for name, value in headers.items():
        if name.lower() != 'cookie':  # Handle cookies separately
            print(f'    "{name}": "{value}",')
    print("}")

    print("\n# Cookies for your session:")
    print("cookies = {")
    if 'Cookie' in headers:
        cookies = headers['Cookie'].split('; ')
        for cookie in cookies:
            if '=' in cookie:
                cname, cval = cookie.split('=', 1)
                print(f'    "{cname}": "{cval}",')
    print("}")

    # Extract X-CSRF-Token if present
    if 'X-CSRF-Token' in headers:
        print(f"\n# X-CSRF-Token:")
        print(f'x_csrf_token = "{headers["X-CSRF-Token"]}"')

if __name__ == "__main__":
    parse_curl_command()
