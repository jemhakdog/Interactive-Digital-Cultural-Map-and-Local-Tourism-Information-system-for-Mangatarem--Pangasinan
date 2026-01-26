import os
import re

def find_urls():
    patterns = [r'https?://[^\s\"\'\<\>]+']
    results = set()
    
    # Directories to search
    search_dirs = ['templates', 'static', 'routes']
    
    # Exclude these patterns
    exclude_patterns = [
        'localhost', '127.0.0.1', 'static/', 'url_for', 
        'mangatarem.gov.ph', 'facebook.com', 'twitter.com', # These are likely links, not libraries
        'google-site-verification', 'canonical'
    ]
    
    for s_dir in search_dirs:
        if not os.path.exists(s_dir):
            continue
        for root, dirs, files in os.walk(s_dir):
            for file in files:
                if file.endswith(('.html', '.js', '.css', '.py')):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for p in patterns:
                                matches = re.findall(p, content)
                                for m in matches:
                                    if not any(ex in m for ex in exclude_patterns):
                                        # Clean up the URL (sometimes trailing dots or commas are caught)
                                        m = m.rstrip('.,;)]}')
                                        results.add(f'{path}: {m}')
                    except Exception as e:
                        print(f"Error reading {path}: {e}")
                        
    for r in sorted(list(results)):
        print(r)

if __name__ == "__main__":
    find_urls()
