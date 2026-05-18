from bs4 import BeautifulSoup

with open('events.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

articles = soup.find_all('article')
print(f"Found {len(articles)} articles.")

for i, article in enumerate(articles[:2]):
    print(f"\n--- Article {i+1} ---")
    print(f"Classes: {article.get('class')}")
    
    # Try to find title
    title_tag = article.find(['h1', 'h2', 'h3', 'h4'])
    if title_tag:
        print(f"Title: {title_tag.text.strip()}")
        a_tag = title_tag.find('a')
        if a_tag:
            print(f"Link: {a_tag.get('href')}")
    
    # Try to find date
    date_tag = article.find(class_='entry-date') or article.find('time')
    if date_tag:
        print(f"Date: {date_tag.text.strip()}")
        
    # Try to find image
    img_tag = article.find('img')
    if img_tag:
        print(f"Image: {img_tag.get('src')}")
        
    # Content snippet
    content_tag = article.find(class_='entry-content') or article.find(class_='entry-summary')
    if content_tag:
        print(f"Content length: {len(content_tag.text.strip())}")

# Also look for pagination
nav = soup.find('nav', class_='navigation') or soup.find(class_='pagination')
if nav:
    print("\nFound pagination!")
    links = nav.find_all('a')
    for link in links:
        print(link.get('href'))
