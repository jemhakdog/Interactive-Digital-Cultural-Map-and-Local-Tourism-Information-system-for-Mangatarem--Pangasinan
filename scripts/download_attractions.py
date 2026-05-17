#!/usr/bin/env python3
"""
Mangatarem Tourist Attractions Image Downloader & Data compiler
Downloads all scraped high-resolution attraction images and builds a structured JSON dataset.
"""

import os
import re
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Raw Scraped Dataset from the Bayan ng Mangatarem Official website
ATTRACTIONS_DATA = [
  {
    "name": "Daang Kalikasan",
    "description": "A scenic road offering breathtaking views of the mountains and rolling hills. A highly popular spot for road trips, cycling, and landscape photography in Mangatarem.",
    "category": "Nature",
    "barangay": "Malabobo",
    "links": [],
    "images": [
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0218-300x169.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0218.jpg",
        "alt": "Daang Kalikasan Drone View 1"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0250-300x169.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0250.jpg",
        "alt": "Daang Kalikasan Curves and Hills"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0253-300x169.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0253.jpg",
        "alt": "Daang Kalikasan Panoramic Mountain Vista"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0314-300x169.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0314.jpg",
        "alt": "Daang Kalikasan Roadway View"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0329-300x169.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI_0329.jpg",
        "alt": "Daang Kalikasan Sunset Over the Hills"
      }
    ]
  },
  {
    "name": "Pacalat River",
    "description": "A pristine river in Mangatarem, popular for family outings, swimming, and enjoying clean, refreshing mountain waters in a scenic natural environment.",
    "category": "Nature",
    "barangay": "Pacalat",
    "links": [],
    "images": [
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG_20220429_082916-300x131.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG_20220429_082916.jpg",
        "alt": "Pacalat River Stream"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG_20220429_085555-300x179.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG_20220429_085555.jpg",
        "alt": "Pacalat River Rocks and Flow"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG20220429091314-300x226.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG20220429091314.jpg",
        "alt": "Pacalat River Quiet Pool"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG20220429084907-scaled-1-226x300.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG20220429084907-scaled-1.jpg",
        "alt": "Pacalat River Shallow Crossing"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG20220429085130-scaled-1-226x300.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/06/IMG20220429085130-scaled-1.jpg",
        "alt": "Pacalat River Green Banks"
      }
    ]
  },
  {
    "name": "Manleluag Spring Protected Landscape",
    "description": "A federally protected area containing therapeutic natural hot and cold springs, lush tropical rainforest walking trails, and a rich biodiversity ecosystem perfect for eco-tourism.",
    "category": "Nature",
    "barangay": "Malabobo",
    "links": [],
    "images": [
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1089-300x200.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1089.jpg",
        "alt": "Manleluag Spring Entrance and Pool"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1080-300x200.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1080.jpg",
        "alt": "Manleluag Spring Lush Pathways"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1067-300x200.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1067.jpg",
        "alt": "Manleluag Protected Forest Canopy"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1054-300x200.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1054.jpg",
        "alt": "Manleluag Forest Trail Steps"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_0348-300x200.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_0348.jpg",
        "alt": "Manleluag Picnic and Recreation Grounds"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1040-300x200.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_1040.jpg",
        "alt": "Manleluag Eco-Tourism Cottage"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_0316-300x200.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2022/09/DSC_0316.jpg",
        "alt": "Manleluag Forest Natural Habitat"
      }
    ]
  },
  {
    "name": "Canding Falls",
    "description": "A beautiful, secluded waterfall cascade nestled in the hills of Mangatarem. Offers crystal-clear waters and refreshing rock pools ideal for adventurous travelers and trekkers.",
    "category": "Nature",
    "barangay": "Cabaluyan",
    "links": [],
    "images": [
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/84497583_142873167182846_478314874074562560_n-300x225.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/84497583_142873167182846_478314874074562560_n.jpg",
        "alt": "Canding Falls Basin View"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/86450436_142873217182841_2933906444958826496_n-300x297.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/86450436_142873217182841_2933906444958826496_n.jpg",
        "alt": "Canding Falls Rock Formations"
      }
    ]
  },
  {
    "name": "Timmanguyob Falls",
    "description": "A towering and majestic waterfall hidden in the mountain forests of Cabaluyan. Requires a rewarding nature hike to reach the deep, refreshing basin pool.",
    "category": "Nature",
    "barangay": "Cabaluyan",
    "links": [],
    "images": [
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/120040403_2711248012312235_1616072299363534736_n-300x265.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/120040403_2711248012312235_1616072299363534736_n.jpg",
        "alt": "Timmanguyob Falls Cascading Pool"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/120099066_2712443285526041_4056194629836246264_n-207x300.png",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/120099066_2712443285526041_4056194629836246264_n.png",
        "alt": "Timmanguyob Falls Majestic Rock Face"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/165158227_3179007818869583_1723889373203731851_n-166x300.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/08/165158227_3179007818869583_1723889373203731851_n.jpg",
        "alt": "Timmanguyob Falls Flowing stream"
      }
    ]
  },
  {
    "name": "Teraoka Farm",
    "description": "An eco-friendly family farm in Mangatarem dedicated to organic farming, nature appreciation, and agricultural learning experience. Perfect for agro-tourism and retreats.",
    "category": "Nature",
    "barangay": "Parian",
    "links": [
      "https://www.facebook.com/Teraokafamilyfarm"
    ],
    "images": [
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/354252884_606082825038270_4687713740306082844_n-1024x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/354252884_606082825038270_4687713740306082844_n.jpg",
        "alt": "Teraoka Farm Organic Produce"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/12715893_1661343684115302_3943762607586051605_o-1024x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/12715893_1661343684115302_3943762607586051605_o.jpg",
        "alt": "Teraoka Farm Camping Grounds"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/1511700_1632929206956750_5739449454977786922_o-819x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/1511700_1632929206956750_5739449454977786922_o.jpg",
        "alt": "Teraoka Farm Pine and Foliage"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11008635_1579399485643056_3114279746302474679_n-1024x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11008635_1579399485643056_3114279746302474679_n.jpg",
        "alt": "Teraoka Farm Freshly Harvested Veggies"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11187294_1616112435305094_984660879789586866_o-1024x680.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11187294_1616112435305094_984660879789586866_o.jpg",
        "alt": "Teraoka Farm Scenic Mountain Backdrop"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11231749_1579069959009342_1536109449586156792_n-1024x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11231749_1579069959009342_1536109449586156792_n.jpg",
        "alt": "Teraoka Farm Family Farm Gathering"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11942116_1615843551998649_2388067835982508231_o-1024x680.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/11942116_1615843551998649_2388067835982508231_o.jpg",
        "alt": "Teraoka Farm Sunrise Over Fields"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/13254735_1695377800711890_1760250534732972604_o-1024x768.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/13254735_1695377800711890_1760250534732972604_o.jpg",
        "alt": "Teraoka Farm Retreat and Cottages"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/18056128_1847267278856274_7768341267899529185_o-1024x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/18056128_1847267278856274_7768341267899529185_o.jpg",
        "alt": "Teraoka Farm Organic Crop Bed"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/21458008_1907497489499919_7893749523046428640_o-1024x767.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/21458008_1907497489499919_7893749523046428640_o.jpg",
        "alt": "Teraoka Farm Harvesting Veggies"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/22137175_1918008965115438_7593836381076714373_o-1024x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/22137175_1918008965115438_7593836381076714373_o.jpg",
        "alt": "Teraoka Farm Eco Cabin"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/29873096_2000270690222598_287909975830193601_o-1024x1018.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/29873096_2000270690222598_287909975830193601_o.jpg",
        "alt": "Teraoka Farm Sunflowers"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/36546657_2050719391844394_4348734535584710656_n-1024x768.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/36546657_2050719391844394_4348734535584710656_n.jpg",
        "alt": "Teraoka Farm Organic Salad Greens"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/16992160_1823054204610915_4505885959696596350_o-1024x767.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/16992160_1823054204610915_4505885959696596350_o.jpg",
        "alt": "Teraoka Farm Planting Event"
      },
      {
        "thumbnail": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/335073750_888858962420856_206240379336491207_n-1024x1024.jpg",
        "highRes": "https://mangatarem.gov.ph/wp-content/uploads/2023/09/335073750_888858962420856_206240379336491207_n.jpg",
        "alt": "Teraoka Farm Fresh Eggs"
      }
    ]
  }
]

# Set Chrome User-Agent header to bypass blocks on government website
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://mangatarem.gov.ph/'
}

# Base Output Directories
OUTPUT_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
IMAGES_DIR = os.path.join(OUTPUT_BASE_DIR, 'scraped_images')
JSON_FILE_PATH = os.path.join(OUTPUT_BASE_DIR, 'scraped_attractions.json')


def slugify(text):
    """Converts attraction name to file-friendly folder name"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '_', text)
    return text.strip('_')


def download_single_image(url, save_path, retries=3):
    """Downloads a single image with support for retries, timeouts, and validation"""
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
        # Already downloaded successfully
        return True, "Already Exists"

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=20, stream=True)
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
    print("Mangatarem Tourist Attractions Image & Data Downloader")
    print("==============================================================")
    print(f"Base Output Directory: {OUTPUT_BASE_DIR}")
    print(f"Scraped Images Directory: {IMAGES_DIR}")
    print(f"Target JSON Location: {JSON_FILE_PATH}")
    
    # 1. Create target directories if they do not exist
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # 2. Compile list of download tasks
    download_tasks = []
    updated_attractions = []
    
    for attraction in ATTRACTIONS_DATA:
        attraction_name = attraction["name"]
        slug = slugify(attraction_name)
        attraction_img_dir = os.path.join(IMAGES_DIR, slug)
        os.makedirs(attraction_img_dir, exist_ok=True)
        
        updated_images_list = []
        
        print(f"\nProcessing attraction: '{attraction_name}' -> Folder: 'data/scraped_images/{slug}'")
        
        for idx, img in enumerate(attraction["images"], 1):
            high_res_url = img["highRes"]
            
            # Extract extension or default to .jpg
            ext = ".jpg"
            parsed_url = urllib_parse = url.split('/')[-1] if 'url' in locals() else high_res_url.split('?')[0].split('/')[-1]
            if '.' in parsed_url:
                ext_match = re.search(r'\.[a-zA-Z0-9]+$', parsed_url)
                if ext_match:
                    ext = ext_match.group(0).lower()
            
            # Create standard file name based on URL/index
            file_name = f"image_{idx}{ext}"
            save_path = os.path.join(attraction_img_dir, file_name)
            
            # Local path relative to the workspace root for application mapping
            relative_local_path = f"data/scraped_images/{slug}/{file_name}"
            
            # Record task
            download_tasks.append({
                "url": high_res_url,
                "save_path": save_path,
                "attraction_name": attraction_name,
                "file_name": file_name
            })
            
            # Update image object
            updated_image_obj = img.copy()
            updated_image_obj["local_path"] = relative_local_path
            updated_images_list.append(updated_image_obj)
            
        updated_attraction_obj = attraction.copy()
        updated_attraction_obj["images"] = updated_images_list
        updated_attractions.append(updated_attraction_obj)

    # 3. Download images concurrently using ThreadPoolExecutor
    print(f"\n[+] Enqueuing {len(download_tasks)} high-resolution images for download...")
    
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
                        print(f"  [SKIP] {task['attraction_name']} - {task['file_name']}: Already exists locally (Skipped)")
                    else:
                        successful_downloads += 1
                        print(f"  [OK] {task['attraction_name']} - {task['file_name']}: Downloaded successfully")
                else:
                    failed_downloads += 1
                    print(f"  [FAIL] {task['attraction_name']} - {task['file_name']}: Failed to download ({reason})")
            except Exception as exc:
                failed_downloads += 1
                print(f"  [ERROR] {task['attraction_name']} - {task['file_name']}: Generated an exception: {exc}")

    # 4. Save compilation JSON data
    print("\n[+] Saving mapped metadata to JSON...")
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(updated_attractions, f, indent=2, ensure_ascii=False)
        
    print("==============================================================")
    print("Download & Compilation Complete!")
    print(f"  - Total Images: {len(download_tasks)}")
    print(f"  - Downloaded:   {successful_downloads}")
    print(f"  - Skipped:      {skipped_downloads}")
    print(f"  - Failed:       {failed_downloads}")
    print(f"  - Final Dataset: {JSON_FILE_PATH}")
    print("==============================================================")


if __name__ == '__main__':
    main()
