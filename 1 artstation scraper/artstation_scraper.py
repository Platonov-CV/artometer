import requests
import json
import os
import urllib.request
from urllib.parse import urlparse
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Playwright

def download_image(page, url, filename):
    """Download image from URL using browser session and save with given filename"""
    try:
        # Use the browser page to download with proper cookies
        response = page.request.get(url)
        if response.status == 200:
            with open(filename, 'wb') as f:
                f.write(response.body())
            print(f"Downloaded: {filename}")
            return True
        else:
            print(f"Failed to download {url}: HTTP {response.status}")
            return False
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def setup_browser():
    """Setup Playwright browser with cookies for Artstation"""
    print("  Setting up Playwright browser...")

    playwright = sync_playwright().start()

    # Create browser context with cookies
    browser = playwright.chromium.launch(headless=False)  # Set to False for debugging
    context = browser.new_context()

    print("  Setting up cookies...")
    # Set cookies
    cookies = [
        {'name': '__stripe_mid', 'value': 'd6d25e5e-09a4-45aa-8d2b-467d70b92af1e1de21', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': 'visitor-uuid', 'value': '3324bf9b-4498-435b-a1b1-9fa6ef7ad34e', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': 'G_ENABLED_IDPS', 'value': 'google', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': 'ArtStationSessionCookie', 'value': 'IjU3MmY4ZWFhLTdhY2YtNGU2Ny1hNTVlLTIzMDhhYjFiOTNlZSI%3D--003739a825137034af5cf8e5610044c0227ed13a989afb8ec0b8bff636267ee2', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': 'PRIVATE-CSRF-TOKEN', 'value': 'xST9ZkHulL06kKpeUX%2F4xzxrDLcOqIiyDOfKS%2FlY1Z0%3D', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': 'G_AUTHUSER_H', 'value': '0', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': '__stripe_sid', 'value': '3fde4a93-fbcf-49bd-9754-5ce323d6326da3e528', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': '_ArtStation_session', 'value': 'dUJMK256dEI2S2k2N1VnRHNZQytjVjFZdGg1ZHBWSVZPMGlnTExHK3RSaUlZRnpXb1dkeVhCYVJvVytYNVpKcno3Zzd0VkgzLzdINUEzdmNXeFVCY2c9PS0tcExyaUVVNy8zUjVZTDN6UDBHTnFCdz09--df958e23cb350f30dbd517403cc696841340c260', 'domain': 'www.artstation.com', 'path': '/'},
        {'name': '__cf_bm', 'value': 'q24q3aOjB6zSS440boSi0ulmfTx1UVDqxPwHjsTIim0-1767810374-1.0.1.1-1d4czxPRaWrPvsKoRj7qxY5A6hiN46H82an5rn2abaVUuSE66nXsOUxNQILBIFvRQ.M3yQ37hJdmHIEeY1fvYe5srzDgOwEk7P.fTlPh.TjeEBcSq1lGnmpaOKT95PLV', 'domain': 'www.artstation.com', 'path': '/'}
    ]

    # Add cookies
    context.add_cookies(cookies)
    print("  Cookies added successfully")

    print("  Creating new page...")
    page = context.new_page()

    # Test the page
    print(f"  Initial page URL: {page.url}")

    print("  Browser setup complete!")
    return page, browser, playwright

def main():
    # Create a session for API calls
    session = requests.Session()

    # Set the exact Cookie header from your curl command
    session.headers.update({
        'Cookie': '__stripe_mid=d6d25e5e-09a4-45aa-8d2b-467d70b92af1e1de21; visitor-uuid=3324bf9b-4498-435b-a1b1-9fa6ef7ad34e; G_ENABLED_IDPS=google; ArtStationSessionCookie=IjU3MmY4ZWFhLTdhY2YtNGU2Ny1hNTVlLTIzMDhhYjFiOTNlZSI%3D--003739a825137034af5cf8e5610044c0227ed13a989afb8ec0b8bff636267ee2; PRIVATE-CSRF-TOKEN=xST9ZkHulL06kKpeUX%2F4xzxrDLcOqIiyDOfKS%2FlY1Z0%3D; G_AUTHUSER_H=0; __stripe_sid=3fde4a93-fbcf-49bd-9754-5ce323d6326da3e528; _ArtStation_session=dUJMK256dEI2S2k2N1VnRHNZQytjVjFZdGg1ZHBWSVZPMGlnTExHK3RSaUlZRnpXb1dkeVhCYVJvVytYNVpKcno3Zzd0VkgzLzdINUEzdmNXeFVCY2c9PS0tcExyaUVVNy8zUjVZTDN6UDBHTnFCdz09--df958e23cb350f30dbd517403cc696841340c260; __cf_bm=q24q3aOjB6zSS440boSi0ulmfTx1UVDqxPwHjsTIim0-1767810374-1.0.1.1-1d4czxPRaWrPvsKoRj7qxY5A6hiN46H82an5rn2abaVUuSE66nXsOUxNQILBIFvRQ.M3yQ37hJdmHIEeY1fvYe5srzDgOwEk7P.fTlPh.TjeEBcSq1lGnmpaOKT95PLV'
    })

    # Setup browser for scraping
    print("Setting up browser...")
    page, browser, playwright = setup_browser()
    print("Browser setup complete!")

    # Headers that match your working browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'X-CSRF-TOKEN': 'R75qAOCOTIKpng7XF7dBNO515IkLo4jkTY/ih0vztkR0Yro5F35rp3kvYj393RhPxj4BwNgrS98IRMWu1WGerg==',
        'PUBLIC-CSRF-TOKEN': 'h1Vj/VSYamkiJZYBqPTc6vyhAGi1rxFAxtUU5XgX701CcZ6bFXb+1Bi1PF/5iyQtwMoM37sHmfLKMt6ugU860A==',
        'Content-Type': 'application/json',
        'Origin': 'https://www.artstation.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.artstation.com/search?sort_by=date&medium_ids_include=1&medium_ids_exclude=2',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }

    # First visit main page to establish session
    print("Establishing session with Artstation...")
    try:
        main_response = session.get('https://www.artstation.com/', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        print(f"Main page status: {main_response.status_code}")
        time.sleep(1)
    except Exception as e:
        print(f"Error visiting main page: {e}")

    # API endpoint
    url = "https://www.artstation.com/api/v2/search/projects.json"

    # Base payload
    base_payload = {
        "query": "",
        "per_page": 50,
        "sorting": "date",
        "pro_first": "1",
        "filters": [
            {"field": "medium_ids", "method": "include", "value": ["1"]},
            {"field": "medium_ids", "method": "exclude", "value": ["2"]},
            {"field": "tags", "method": "exclude", "value": ["References", "animated", "character reference"]},
            {"field": "asset_types", "method": "exclude", "value": ["video", "video_clip"]}
        ],
        "additional_fields": []
    }

    # Create directory for images if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # List to store like counts
    like_counts = []

    # Counter for image naming
    image_counter = 0

    # Test API first
    print("Testing API call...")
    payload = base_payload.copy()
    payload["page"] = 200

    response = session.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("API working!")
        data = response.json()
        projects = data.get('data', [])
        print(f"Found {len(projects)} projects on page 200")
    else:
        print(f"API failed: {response.status_code}")
        return

    # Go from page 200 backwards to 100
    for page_num in range(200, 199, -1):
        print(f"Processing page {page_num}...")

        # Update payload with current page
        payload = base_payload.copy()
        payload["page"] = page_num

        try:
            # Make POST request using session
            response = session.post(url, json=payload, headers=headers)

            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            # Get projects from response
            projects = data.get('data', [])

            print(f"Found {len(projects)} projects on page {page_num}")

            for project in projects:
                project_id = project.get('id')
                project_url = project.get('url')

                try:
                    # Visit the project page with browser
                    page.goto(project_url, wait_until='domcontentloaded', timeout=30000)

                    # Wait for content to load
                    time.sleep(2)

                    # Get page source and parse
                    soup = BeautifulSoup(page.content(), 'html.parser')

                    # Find the first artwork image in the asset-image container
                    asset_image_div = soup.find('div', class_='asset-image')
                    image_url = None

                    if asset_image_div:
                        # Find the img tag within the asset-image div
                        img_tag = asset_image_div.find('img')
                        if img_tag and img_tag.get('src'):
                            image_url = img_tag['src']
                            # Make sure it's a full URL
                            if not image_url.startswith('http'):
                                if image_url.startswith('//'):
                                    image_url = 'https:' + image_url
                                elif image_url.startswith('/'):
                                    image_url = 'https://www.artstation.com' + image_url

                    if not image_url:
                        continue  # Skip if no image found

                    # Find likes count from show-likes-button component or fa-thumbs-up icon
                    like_count = 0

                    # First try to find the show-likes-button component
                    likes_button = soup.find('show-likes-button')
                    if likes_button:
                        like_div = likes_button.find('div', class_='btn-wrapper')
                        if like_div:
                            like_button = like_div.find('button', class_='btn btn-reset')
                            if like_button:
                                like_span = like_button.find('span', class_='link-fake')
                                if like_span and like_span.next_sibling:
                                    try:
                                        like_count = int(like_span.next_sibling.strip())
                                    except (ValueError, AttributeError):
                                        pass

                    # If that didn't work, try finding by fa-thumbs-up icon
                    if like_count == 0:
                        thumbs_up_icon = soup.find('i', class_='fa-thumbs-up')
                        if thumbs_up_icon:
                            # Navigate up to find the parent btn-wrapper
                            btn_wrapper = thumbs_up_icon.find_parent('div', class_='btn-wrapper')
                            if btn_wrapper:
                                like_button = btn_wrapper.find('button', class_='btn btn-reset')
                                if like_button:
                                    like_span = like_button.find('span', class_='link-fake')
                                    if like_span and like_span.next_sibling:
                                        try:
                                            like_count = int(like_span.next_sibling.strip())
                                        except (ValueError, AttributeError):
                                            pass

                    # Download the image
                    filename = f"images/{image_counter}.png"
                    if download_image(page, image_url, filename):
                        like_counts.append(str(like_count))
                        image_counter += 1

                except Exception as e:
                    print(f"    Error processing project {project_id}: {e}")

                # Add a small delay to be respectful to the server
                time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error on page {page}: {e}")
            continue

    # Write like counts to txt file
    with open('like_counts.txt', 'w') as f:
        f.write('\n'.join(like_counts))

    print(f"Downloaded {image_counter} images")
    print("Like counts saved to like_counts.txt")

    # Close browser
    browser.close()
    playwright.stop()

if __name__ == "__main__":
    main()

