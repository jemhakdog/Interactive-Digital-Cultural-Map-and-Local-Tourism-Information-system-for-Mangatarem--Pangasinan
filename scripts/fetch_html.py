import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://mangatarem.gov.ph/'
}

url = "https://mangatarem.gov.ph/tourism/heritage-sites/"

print(f"Fetching {url}...")
try:
    response = requests.get(url, headers=HEADERS, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        with open("instance/heritage_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Successfully saved HTML to instance/heritage_page.html")
    else:
        print("Failed to fetch page")
except Exception as e:
    print(f"Error fetching page: {e}")
