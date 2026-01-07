#!/usr/bin/env python3
"""
Script to get fresh CSRF token and cookies from Artstation
"""

import requests
import re

def get_fresh_session():
    """Get fresh session with CSRF token"""
    session = requests.Session()

    # First, visit the main page to get initial cookies
    print("Visiting Artstation main page...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    response = session.get('https://www.artstation.com/', headers=headers)
    print(f"Main page status: {response.status_code}")

    # Look for CSRF token in the HTML
    csrf_token = None
    if response.status_code == 200:
        # Search for CSRF token in meta tags
        csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"Found CSRF token: {csrf_token[:20]}...")
        else:
            print("No CSRF token found in HTML")

        # Also check cookies
        for cookie in session.cookies:
            if 'csrf' in cookie.name.lower():
                csrf_token = cookie.value
                print(f"Found CSRF token in cookie: {csrf_token[:20]}...")
                break

    print("\nCurrent session cookies:")
    for cookie in session.cookies:
        print(f"  {cookie.name}: {cookie.value}")

    return session, csrf_token

def test_api_call(session, csrf_token):
    """Test the API call with fresh tokens"""
    if not csrf_token:
        print("No CSRF token available")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://www.artstation.com',
        'Referer': 'https://www.artstation.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-CSRF-Token': csrf_token,
    }

    url = "https://www.artstation.com/api/v2/search/projects.json"
    payload = {
        "query": "",
        "page": 200,
        "per_page": 50,
        "sorting": "date",
        "pro_first": "1",
        "filters": [
            {"field": "medium_ids", "method": "include", "value": ["1"]},
            {"field": "medium_ids", "method": "exclude", "value": ["2"]}
        ],
        "additional_fields": []
    }

    print(f"\nTesting API call with CSRF token: {csrf_token[:20]}...")
    response = session.post(url, json=payload, headers=headers)
    print(f"API response status: {response.status_code}")

    if response.status_code == 200:
        print("SUCCESS! API call worked with fresh token.")
        data = response.json()
        print(f"Found {len(data.get('data', []))} projects")
        return True
    else:
        print("FAILED!")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    session, csrf_token = get_fresh_session()

    if csrf_token:
        success = test_api_call(session, csrf_token)
        if success:
            print("\n" + "="*50)
            print("SUCCESS! Use this CSRF token in your scraper:")
            print(f"'X-CSRF-Token': '{csrf_token}'")
            print("="*50)
    else:
        print("Could not get CSRF token. You may need to be logged in.")

