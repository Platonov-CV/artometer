import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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
    # Setup browser for scraping
    print("Setting up browser...")
    page, browser, playwright = setup_browser()
    print("Browser setup complete!")

    # Load URLs from CSV file

    # Create directory for images if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

    # List to store like counts
    like_counts = []

    # Counter for image naming
    image_counter = 0

    # Load URLs from CSV file
    csv_path = "../2 processing artstation artwork analysis dataset/artstation_main_data.csv"
    print(f"Loading URLs from CSV: {csv_path}")

    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from CSV")

        # Get URLs from the 'URL' column
        if 'URL' not in df.columns:
            print("ERROR: 'URL' column not found in CSV")
            return

        urls = df['URL'].dropna().tolist()
        print(f"Found {len(urls)} URLs to process")

    except FileNotFoundError:
        print(f"ERROR: CSV file not found at {csv_path}")
        return
    except Exception as e:
        print(f"ERROR loading CSV: {e}")
        return

    # Process each URL from the CSV
    for i, project_url in enumerate(urls):
        print(f"Processing item {i+1}/{len(urls)}: {project_url}")

        try:
            # Visit the project page with browser
            page.goto(project_url, wait_until='domcontentloaded', timeout=30000)

            # Wait for content to load
            time.sleep(2)

            # Get page source and parse
            soup = BeautifulSoup(page.content(), 'html.parser')

            # Check if this is a video project - skip if so
            video_div = soup.find('div', class_='asset-embedded video-clip')
            if video_div:
                print("    Skipping video project")
                continue

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
                print("    No image found, skipping")
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
                print(f"    Successfully processed item {i+1}")

        except Exception as e:
            print(f"    Error processing item {i+1}: {e}")

        # Add a small delay to be respectful to the server
        time.sleep(1)

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

