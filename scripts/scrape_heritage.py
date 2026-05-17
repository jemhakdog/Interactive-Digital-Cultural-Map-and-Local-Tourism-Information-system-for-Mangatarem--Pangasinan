#!/usr/bin/env python3
"""
Mangatarem Heritage Sites Web Scraper & Image Downloader
Parses pre-fetched heritage page HTML, extracts details and gallery images,
and concurrently downloads high-resolution assets into a local structure.
"""

import os
import re
import json
import time
import requests
import lxml.html
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constant paths
HTML_PATH = "instance/heritage_page.html"
OUTPUT_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
IMAGES_DIR = os.path.join(OUTPUT_BASE_DIR, 'scraped_images')
JSON_FILE_PATH = os.path.join(OUTPUT_BASE_DIR, 'scraped_heritage.json')

# User-Agent headers to bypass server-side bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://mangatarem.gov.ph/'
}

# Exclusion list of headings that are not actual heritage sites
EXCLUSIONS = {
    "latest news and events",
    "stay connected",
    "recent posts",
    "categories",
    "archives",
    "meta"
}


def slugify(text):
    """Converts a name to a safe folder/file-friendly name"""
    text = text.lower()
    text = text.replace('ñ', 'n')
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '_', text)
    return text.strip('_')



def clean_title(title, site_name, idx):
    """Cleans up raw image titles/filenames into elegant descriptive text"""
    if not title:
        return f"{site_name} Image {idx}"
        
    title_clean = title.strip()
    
    # If the title is just a system-generated camera tag (e.g. DSC_0357, 350117466_...)
    if (title_clean.lower().startswith('dsc_') or 
            re.match(r'^\d+_\d+_\d+_n$', title_clean) or 
            len(title_clean) > 40):
        return f"{site_name} View {idx}"
        
    # Standard replacement of underscores and hyphens with spaces
    title_clean = title_clean.replace("-", " ").replace("_", " ")
    return title_clean.title()


def download_single_image(url, save_path, retries=3):
    """Downloads a single image with retries, timeouts, and validation"""
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
        return True, "Already Exists"

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=25, stream=True)
            if response.status_code == 200:
                # Ensure the size is valid before saving
                content_length = response.headers.get('content-length')
                if content_length and int(content_length) < 100:
                    return False, f"Invalid low file size ({content_length} bytes)"

                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Validate downloaded file size
                if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
                    return True, "Downloaded"
                else:
                    return False, "File empty or too small after download"
            else:
                if attempt == retries:
                    return False, f"HTTP Error {response.status_code}"
                time.sleep(2)
        except Exception as e:
            if attempt == retries:
                return False, f"Error: {str(e)}"
            time.sleep(2)
            
    return False, "Failed after retries"


def main():
    print("==============================================================")
    print("Mangatarem Heritage Sites Scraper & Downloader")
    print("==============================================================")
    
    if not os.path.exists(HTML_PATH):
        print(f"[-] Error: Source HTML file '{HTML_PATH}' not found!")
        print("    Please run the fetch script first.")
        return

    # Create output directories if they do not exist
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    print(f"[+] Loading and parsing '{HTML_PATH}'...")
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()

    doc = lxml.html.fromstring(html_content)
    
    # Find all h2 tags
    headings = doc.xpath("//h2")
    print(f"[+] Found {len(headings)} H2 elements in the document.")

    heritage_sites = []
    download_tasks = []

    for h2 in headings:
        site_name = h2.text_content().strip()
        
        # Skip empty headers or elements in the exclusion list
        if not site_name or site_name.lower() in EXCLUSIONS:
            continue

        print(f"\n[+] Processing Site: '{site_name}'")
        slug = slugify(site_name)
        site_img_dir = os.path.join(IMAGES_DIR, slug)
        os.makedirs(site_img_dir, exist_ok=True)

        # 1. Extract Description
        # Walk through consecutive siblings until the next h2 is reached
        curr = h2.getnext()
        desc = ""
        galleries = []

        while curr is not None and curr.tag != 'h2':
            if curr.tag == 'p':
                p_text = curr.text_content().strip()
                if p_text:
                    if desc:
                        desc += "\n" + p_text
                    else:
                        desc = p_text
            # Identify Robo Gallery blocks
            elif curr.attrib.get('class') and 'robo-gallery-wrap' in curr.attrib.get('class'):
                galleries.append(curr)
            else:
                # Check for nested galleries within this block
                nested_g = curr.xpath(".//div[contains(@class, 'robo-gallery-wrap')]")
                if nested_g:
                    galleries.extend(nested_g)
            
            curr = curr.getnext()

        print(f"    Description: {len(desc)} characters found")
        print(f"    Gallery blocks found: {len(galleries)}")

        # 2. Extract Images from Galleries
        images_list = []
        img_idx = 1
        seen_urls = set()

        for gallery in galleries:
            img_containers = gallery.xpath(".//div[contains(@class, 'rbs-img')]")
            print(f"    Gallery contains {len(img_containers)} images")
            
            for container in img_containers:
                thumbs = container.xpath(".//div[contains(@class, 'rbs-img-thumbs')]")
                popups = container.xpath(".//div[contains(@class, 'rbs-img-data-popup')]")

                thumb_url = thumbs[0].attrib.get('data-thumbnail') if thumbs else None
                high_res_url = popups[0].attrib.get('data-popup') if popups else None
                raw_title = popups[0].attrib.get('title') if popups else (thumbs[0].attrib.get('title') if thumbs else None)

                # Fallback in case popup url is missing but thumbnail exists
                if not high_res_url and thumb_url:
                    high_res_url = thumb_url

                if not high_res_url:
                    continue

                # Deduplicate images based on highRes URL
                if high_res_url in seen_urls:
                    continue
                seen_urls.add(high_res_url)

                # Generate clean descriptive alt
                alt_text = clean_title(raw_title, site_name, img_idx)

                # Determine extension from the highRes URL or default to .jpg
                ext = ".jpg"
                parsed_filename = high_res_url.split('?')[0].split('/')[-1]
                if '.' in parsed_filename:
                    ext_match = re.search(r'\.[a-zA-Z0-9]+$', parsed_filename)
                    if ext_match:
                        ext = ext_match.group(0).lower()

                # Generate localized naming convention
                file_name = f"image_{img_idx}{ext}"
                save_path = os.path.join(site_img_dir, file_name)
                relative_local_path = f"data/scraped_images/{slug}/{file_name}"

                image_obj = {
                    "thumbnail": thumb_url,
                    "highRes": high_res_url,
                    "alt": alt_text,
                    "local_path": relative_local_path
                }
                
                images_list.append(image_obj)

                # Queue for concurrent downloading
                download_tasks.append({
                    "url": high_res_url,
                    "save_path": save_path,
                    "site_name": site_name,
                    "file_name": file_name
                })

                img_idx += 1


        # Populate site metadata
        site_data = {
            "name": site_name,
            "description": desc if desc else None,
            "category": "Heritage",
            "barangay": "Poblacion",
            "links": [],
            "images": images_list
        }
        
        heritage_sites.append(site_data)

    print(f"\n[+] Total Heritage Sites mapped: {len(heritage_sites)}")
    print(f"[+] Enqueuing {len(download_tasks)} high-resolution images for concurrent download...")

    # 3. Download images concurrently using ThreadPoolExecutor
    successful_downloads = 0
    skipped_downloads = 0
    failed_downloads = 0

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_task = {
            executor.submit(download_single_image, task["url"], task["save_path"]): task
            for task in download_tasks
        }

        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                success, reason = future.result()
                if success:
                    if reason == "Already Exists":
                        skipped_downloads += 1
                        print(f"  [SKIP] {task['site_name']} - {task['file_name']}: Already exists locally")
                    else:
                        successful_downloads += 1
                        print(f"  [OK] {task['site_name']} - {task['file_name']}: Downloaded successfully")
                else:
                    failed_downloads += 1
                    print(f"  [FAIL] {task['site_name']} - {task['file_name']}: Failed to download ({reason})")
            except Exception as exc:
                failed_downloads += 1
                print(f"  [ERROR] {task['site_name']} - {task['file_name']}: Generated exception: {exc}")

    # 4. Save compilation JSON data
    print(f"\n[+] Saving compiled heritage dataset to '{JSON_FILE_PATH}'...")
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(heritage_sites, f, indent=2, ensure_ascii=False)

    print("==============================================================")
    print("Scraping & Compilation Complete!")
    print(f"  - Total Heritage Sites: {len(heritage_sites)}")
    print(f"  - Total Images Mapped:  {len(download_tasks)}")
    print(f"  - Downloaded:           {successful_downloads}")
    print(f"  - Skipped (Exist):      {skipped_downloads}")
    print(f"  - Failed:               {failed_downloads}")
    print(f"  - Output Dataset:       {JSON_FILE_PATH}")
    print("==============================================================")


if __name__ == '__main__':
    main()
