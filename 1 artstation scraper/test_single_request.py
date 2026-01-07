import requests
import json

def test_single_request():
    # Create a session and set cookies directly
    session = requests.Session()

    # Set cookies individually on the session
    cookies = {
        '__stripe_mid': 'd6d25e5e-09a4-45aa-8d2b-467d70b92af1e1de21',
        'visitor-uuid': '3324bf9b-4498-435b-a1b1-9fa6ef7ad34e',
        'G_ENABLED_IDPS': 'google',
        'ArtStationSessionCookie': 'IjU3MmY4ZWFhLTdhY2YtNGU2Ny1hNTVlLTIzMDhhYjFiOTNlZSI%3D--003739a825137034af5cf8e5610044c0227ed13a989afb8ec0b8bff636267ee2',
        'PRIVATE-CSRF-TOKEN': 'xST9ZkHulL06kKpeUX%2F4xzxrDLcOqIiyDOfKS%2FlY1Z0%3D',
        'G_AUTHUSER_H': '0',
        '__cf_bm': 'Wb7CQvSYUZxTBYIJh8ORFVTmmQyGm6py0xswUcBABH4-1767808517-1.0.1.1-G97pyO0Jecy7jdncsl1Ol_14ZVjZ85sKCMNzM4kVpoU4CiZ4_wnqEJf.vgnlHfyI4Fil39iYn6srLF3jPayjdEb2SuGebpkAyD6h1ufKR_QovlpESl.2XrdshBFFNQ.H',
        '__stripe_sid': '3fde4a93-fbcf-49bd-9754-5ce323d6326da3e528'
    }

    for name, value in cookies.items():
        session.cookies.set(name, value, domain='www.artstation.com')

    # Headers that match your working browser request
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
        'X-CSRF-Token': '6z4gvkeJ1/TU57fa6Xn2wUaOtI0bwxSvEfR8tR1usZHclsIdGel0/tPwyXO9QFiFOhNdw069KinNxd3C12Gi2w==',
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

    print("Testing single request...")
    try:
        response = session.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            print("SUCCESS! Request worked.")
            data = response.json()
            print(f"Found {len(data.get('data', []))} projects")
        else:
            print("FAILED!")
            print(f"Response body: {response.text}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_single_request()
