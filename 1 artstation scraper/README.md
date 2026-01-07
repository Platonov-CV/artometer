# Artstation Scraper

This script downloads images and like counts from Artstation projects using their API.

## Features

- Downloads first image from each project
- Names images sequentially (0.png, 1.png, 2.png...)
- Saves like counts to a text file in the same order
- Processes pages 200 down to 100 (backwards)

## Authentication Issue

Artstation requires CSRF token authentication for API access. The current implementation attempts to extract this token automatically, but Artstation has implemented strong anti-bot measures that may block automated access.

### Potential Solutions

1. **Browser Session Cookies**: You can manually extract cookies from a logged-in browser session and add them to the script.

2. **Manual CSRF Token**: If you can access the Artstation website in a browser, you can inspect the page source to find the CSRF token and manually add it to the script.

3. **API Key**: Artstation may offer official API access with proper authentication.

## Usage

```bash
python artstation_scraper.py
```

## Output

- `images/` directory containing downloaded images (0.png, 1.png, etc.)
- `like_counts.txt` containing like counts in the same order as images

## Requirements

- Python 3.x
- requests library (`pip install requests`)

## Current Status

The script is functionally complete but requires proper authentication to work with Artstation's API. The 412 "Invalid CSRF Token" error indicates that Artstation's security measures are blocking automated access.



