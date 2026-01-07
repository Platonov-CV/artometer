#!/usr/bin/env python3
"""
Update the scraper script with tokens from a working curl command
"""

import re

def update_scraper_from_curl():
    print("Paste your working curl command from browser dev tools:")
    print("(End with empty line)")
    print()

    # Read curl command
    lines = []
    while True:
        try:
            line = input().strip()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break

    curl_command = " ".join(lines)
    print(f"Processing curl command ({len(curl_command)} chars)...")
    print(f"First 200 chars: {curl_command[:200]}...")

    # Extract Cookie header (handle Windows ^ escapes and different quote styles)
    cookie_match = re.search(r"-H\s+\^?['\"]?Cookie:\s*([^'^\"]+)\^?['\"]?", curl_command)
    cookie_header = None
    if cookie_match:
        cookie_header = cookie_match.group(1).strip()
        print("Found Cookie header ✓")
        print(f"Cookie length: {len(cookie_header)}")
    else:
        # Try alternative patterns
        cookie_match = re.search(r'-H\s+\^?"Cookie:\s*([^"]+)\^?"', curl_command)
        if cookie_match:
            cookie_header = cookie_match.group(1).strip()
            print("Found Cookie header ✓ (alt pattern)")
            print(f"Cookie length: {len(cookie_header)}")

    # Extract X-CSRF-Token header (handle case variations and Windows escapes)
    csrf_match = re.search(r"-H\s+\^?['\"]?X-CSRF-TOKEN:\s*([^'^\"]+)\^?['\"]?", curl_command, re.IGNORECASE)
    csrf_token = None
    if csrf_match:
        csrf_token = csrf_match.group(1).strip()
        print("Found X-CSRF-TOKEN header ✓")
        print(f"Token: {csrf_token[:30]}...")
    else:
        # Try alternative patterns
        csrf_match = re.search(r'-H\s+\^?"X-CSRF-TOKEN:\s*([^"]+)\^?"', curl_command, re.IGNORECASE)
        if csrf_match:
            csrf_token = csrf_match.group(1).strip()
            print("Found X-CSRF-TOKEN header ✓ (alt pattern)")
            print(f"Token: {csrf_token[:30]}...")

    if not cookie_header or not csrf_token:
        print("ERROR: Could not find both Cookie and X-CSRF-Token headers in curl command")
        return

    # Read current scraper
    try:
        with open('artstation_scraper.py', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("ERROR: artstation_scraper.py not found")
        return

    # Update Cookie header
    old_cookie_pattern = r"'Cookie':\s*'[^']*'"
    new_cookie_line = f"'Cookie': '{cookie_header}'"
    content = re.sub(old_cookie_pattern, new_cookie_line, content, flags=re.MULTILINE)

    # Update X-CSRF-Token header
    old_csrf_pattern = r"'X-CSRF-Token':\s*'[^']*'"
    new_csrf_line = f"'X-CSRF-Token': '{csrf_token}'"
    content = re.sub(old_csrf_pattern, new_csrf_line, content, flags=re.MULTILINE)

    # Write back
    with open('artstation_scraper.py', 'w') as f:
        f.write(content)

    print("\n✅ Successfully updated artstation_scraper.py with fresh tokens!")
    print(f"Cookie: {cookie_header[:50]}...")
    print(f"X-CSRF-Token: {csrf_token[:30]}...")

    print("\n🎯 Ready to test! Run:")
    print("python artstation_scraper.py")

if __name__ == "__main__":
    update_scraper_from_curl()
