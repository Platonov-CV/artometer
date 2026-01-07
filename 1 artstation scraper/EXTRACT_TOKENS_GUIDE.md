# How to Extract Working Tokens from Your Browser

Since Artstation blocks automated requests, we need to copy the **exact working request** from your browser.

## Step-by-Step Instructions

### 1. Open Browser Dev Tools
- Press `F12` or `Ctrl+Shift+I`
- Go to the **Network** tab

### 2. Make a Search Request
- Go to https://www.artstation.com/
- Perform a search or scroll to trigger the API call
- Look for the request to `search/projects.json` in the Network tab

### 3. Copy the Request as cURL
- Right-click the `search/projects.json` request
- Select **"Copy" → "Copy as cURL"**

### 4. Paste the cURL Command
The curl command will look like this:
```bash
curl 'https://www.artstation.com/api/v2/search/projects.json' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Accept-Encoding: gzip, deflate, br' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: [LONG COOKIE STRING]' \
  -H 'Origin: https://www.artstation.com' \
  -H 'Referer: https://www.artstation.com/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0...' \
  -H 'X-CSRF-Token: [YOUR CSRF TOKEN]' \
  --data-raw '{"query":"","page":200,"per_page":50,"sorting":"date","pro_first":"1","filters":[{"field":"medium_ids","method":"include","value":["1"]},{"field":"medium_ids","method":"exclude","value":["2"]}],"additional_fields":[]}' \
  --compressed
```

### 5. Extract Key Values

From the cURL command, you need:

**Cookie Header**: The entire value after `-H 'Cookie: `
```
__stripe_mid=...; visitor-uuid=...; ArtStationSessionCookie=...; etc.
```

**X-CSRF-Token Header**: The value after `-H 'X-CSRF-Token: `
```
X-CSRF-Token: [YOUR_TOKEN_HERE]
```

### 6. Update Your Script

Replace these lines in `artstation_scraper.py`:

```python
# Replace the entire Cookie string
'Cookie': '[PASTE_YOUR_COOKIE_STRING_HERE]',

# Replace the X-CSRF-Token
'X-CSRF-Token': '[PASTE_YOUR_CSRF_TOKEN_HERE]',
```

## Important Notes

- **Use a fresh cURL command** each time (tokens expire)
- **Make sure you're logged in** to Artstation in your browser
- **Copy the exact request** that works for you
- **Don't share your cookies publicly** - they contain session data

## If Still Not Working

If you still get 412 errors after updating with fresh tokens:

1. Try copying the request from a different browser (Chrome/Firefox/Edge)
2. Make sure your browser session is fresh (re-login if needed)
3. Try a different page number in the test first (like page 1 instead of 200)

## Quick Test

After updating the tokens, test with just one page:
```python
for page in range(200, 199, -1):  # Test single page
```
