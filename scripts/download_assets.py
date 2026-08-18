import os
import urllib.request
import re

assets = {
    "vendor/sweetalert2/sweetalert2.all.min.js": "https://cdn.jsdelivr.net/npm/sweetalert2@11",
    "vendor/leaflet/leaflet.css": "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
    "vendor/leaflet/leaflet.js": "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
    "vendor/leaflet-1.7.1/leaflet.css": "https://unpkg.com/leaflet@1.7.1/dist/leaflet.css",
    "vendor/leaflet-1.7.1/leaflet.js": "https://unpkg.com/leaflet@1.7.1/dist/leaflet.js",
    "vendor/aos/aos.css": "https://unpkg.com/aos@next/dist/aos.css",
    "vendor/aos/aos.js": "https://unpkg.com/aos@next/dist/aos.js",
    "vendor/chartjs/chart.min.js": "https://cdn.jsdelivr.net/npm/chart.js",
    "vendor/google/gsi_client.js": "https://accounts.google.com/gsi/client",
    "vendor/leaflet-markercluster/MarkerCluster.Default.css": "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css",
    "vendor/leaflet-markercluster/MarkerCluster.css": "https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css",
    "vendor/leaflet-markercluster/leaflet.markercluster.js": "https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js",
    "vendor/tailwindcss/tailwind.min.js": "https://cdn.tailwindcss.com",
    "img/textures/felt.png": "https://www.transparenttextures.com/patterns/felt.png",
    "img/textures/natural-paper.png": "https://www.transparenttextures.com/patterns/natural-paper.png"
}

google_fonts = [
    "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&family=Lora:ital,wght@0,400..700;1,400..700&display=swap",
    "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Montserrat:wght@300;400;600;700&display=swap",
    "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@600;700&display=swap"
]

def download_file(url, dest):
    print(f"Downloading {url} to {dest}...")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read()
            with open(dest, 'wb') as out_file:
                out_file.write(content)
            return content
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def download_google_fonts(urls, base_dir):
    css_content = b""
    font_count = 0
    font_dir = os.path.join(base_dir, "fonts")
    os.makedirs(font_dir, exist_ok=True)

    for i, url in enumerate(urls):
        content = download_file(url, os.path.join(base_dir, f"vendor/google/fonts_{i}.css"))
        if content:
            # Parse CSS for font URLs
            content_str = content.decode('utf-8', errors='ignore')
            font_urls = re.findall(r'url\((https://fonts\.gstatic\.com/[^\)]+)\)', content_str)
            
            for f_url in font_urls:
                font_filename = f_url.split('/')[-1]
                local_font_path = f"../../fonts/{font_filename}"
                download_file(f_url, os.path.join(font_dir, font_filename))
                content_str = content_str.replace(f_url, local_font_path)
                font_count += 1
            
            css_content += content_str.encode('utf-8')
    
    with open(os.path.join(base_dir, "vendor/google/fonts.css"), "wb") as f:
        f.write(css_content)
    print(f"Downloaded {len(urls)} font CSS files and {font_count} font files.")

def main():
    base_static = "static"
    for path, url in assets.items():
        download_file(url, os.path.join(base_static, path))
    
    download_google_fonts(google_fonts, base_static)
    
    print("Download complete.")

if __name__ == "__main__":
    main()
