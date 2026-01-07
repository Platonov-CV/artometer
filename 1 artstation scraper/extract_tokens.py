#!/usr/bin/env python3
"""
Artstation Token Extractor
Run this script and paste your curl command from browser dev tools
"""

import re
import urllib.parse

def extract_from_curl():
    print("Paste your curl command from browser dev tools (Ctrl+V then Enter):")
    print("(Look for the search/projects.json request)")
    print()

    # Read multi-line curl command
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    curl_command = "\n".join(lines)
    print(f"\nExtracted from curl command:\n{'='*50}\n")

    # Extract cookies
    cookie_match = re.search(r"'Cookie:\s*([^']+)'", curl_command)
    if cookie_match:
        cookies = cookie_match.group(1)
        print(f"Cookie header:")
        print(f"'{cookies}'")
        print()

    # Extract X-CSRF-Token
    csrf_match = re.search(r"'X-CSRF-Token:\s*([^']+)'", curl_command)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"X-CSRF-Token header:")
        print(f"'{csrf_token}'")
        print()

    # Extract individual important cookies
    if cookie_match:
        cookies = cookie_match.group(1)
        print("Individual cookies (update these in your script):")
        cookie_pairs = cookies.split('; ')
        important_cookies = ['_ArtStation_session', 'ArtStationSessionCookie', 'PRIVATE-CSRF-TOKEN', '__cf_bm', 'visitor-uuid']
        for cookie_pair in cookie_pairs:
            if '=' in cookie_pair:
                name, value = cookie_pair.split('=', 1)
                if name in important_cookies:
                    print(f"  {name}: '{value}'")

if __name__ == "__main__":
    extract_from_curl()

