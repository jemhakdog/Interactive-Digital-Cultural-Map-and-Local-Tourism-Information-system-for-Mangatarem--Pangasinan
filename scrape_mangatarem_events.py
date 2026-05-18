import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://mangatarem.gov.ph/category/events/page/{}/"
all_events = []
page = 1

print("Starting to scrape events...")

while True:
    url = "https://mangatarem.gov.ph/category/events/" if page == 1 else base_url.format(page)
    print(f"Fetching page {page}: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        print("Hit 404, stopping pagination.")
        break
    elif response.status_code != 200:
        print(f"Failed with status code: {response.status_code}")
        break
        
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    
    if not articles:
        print("No articles found on this page, stopping.")
        break
        
    for article in articles:
        event = {}
        
        # Title and Link
        title_tag = article.find(['h1', 'h2', 'h3', 'h4'])
        if title_tag:
            event['title'] = title_tag.text.strip()
            a_tag = title_tag.find('a')
            if a_tag:
                event['link'] = a_tag.get('href')
            else:
                event['link'] = None
        else:
            event['title'] = None
            event['link'] = None
            
        # Date
        date_tag = article.find(class_='entry-date') or article.find('time')
        event['date'] = date_tag.text.strip() if date_tag else None
        
        # Image
        img_tag = article.find('img')
        event['image_url'] = img_tag.get('src') if img_tag else None
        
        # Excerpt
        excerpt_tag = article.find(class_='entry-content') or article.find(class_='entry-summary')
        event['excerpt'] = excerpt_tag.text.strip() if excerpt_tag else None
        
        all_events.append(event)
        
    print(f"Extracted {len(articles)} events from page {page}")
    page += 1
    time.sleep(1) # Be polite

output_file = 'data/scraped_events.json'
import os
os.makedirs('data', exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_events, f, ensure_ascii=False, indent=4)

print(f"Successfully scraped {len(all_events)} events and saved to {output_file}")
