import sys
import os
import json
import shutil
import re

# Add root directory to path to import app and models
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from app import create_app
from extensions import db
from modules.attractions.models import Attraction
from modules.barangay.models import BarangayInfo
from modules.auth.models import User
from modules.gallery.models import GalleryItem

COORDINATES_MAPPING = {
    "Municipal Hall": (15.7898, 120.2920),
    "Dr. Jose Rizal Monument": (15.7892, 120.2926),
    "Old Convent": (15.7903, 120.2915),
    "Saint Raymund de Peñafort Parish Church": (15.7901, 120.2917),
    "Corleto Residence": (15.7885, 120.2940),
    "Don Ramon Ventenilla Residence": (15.7878, 120.2932),
    "Aviles Residence": (15.7882, 120.2950),
    "Teraoka Farm": (15.7950, 120.2850),
    "Manleluag Spring Protected Landscape": (15.6667, 120.2833),
}

def clean_name(name):
    if not name:
        return ""
    n = name.lower().strip()
    n = re.sub(r'[^\w\s]', '', n)
    n = n.replace("saint", "st")
    n = n.replace("church", "")
    n = n.replace("parish", "")
    n = n.replace("de", "of")
    n = n.replace("peñafort", "penafort")
    n = n.replace("peafort", "penafort")
    n = n.replace("ñ", "n")
    return " ".join(n.split())

def is_match(name1, name2):
    c1 = clean_name(name1)
    c2 = clean_name(name2)
    return c1 == c2 or c1 in c2 or c2 in c1

def copy_image_assets():
    src_dir = os.path.join(root_dir, "data", "scraped_images")
    dest_dir = os.path.join(root_dir, "static", "img", "attractions")
    
    if not os.path.exists(src_dir):
        print(f"[WARN] Source directory {src_dir} does not exist. Skipping image relocation.")
        return
        
    os.makedirs(dest_dir, exist_ok=True)
    
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        if os.path.isdir(item_path):
            dest_item_path = os.path.join(dest_dir, item)
            try:
                shutil.copytree(item_path, dest_item_path, dirs_exist_ok=True)
                print(f"[INFO] Copied media folder '{item}' to static/img/attractions/")
            except Exception as e:
                print(f"[WARN] Failed to copy media folder '{item}' due to OS lock: {e}. Skipping copy.")

def get_or_create_steward(barangay_name, barangay_id):
    clean_brgy = clean_name(barangay_name).replace(" ", "_")
    username = f"{clean_brgy}_steward"
    email = f"{clean_brgy}_steward@gomangatarem.gov.ph"
    
    steward = User.query.filter_by(username=username).first()
    if not steward:
        steward = User(
            username=username,
            email=email,
            role="contributor",
            is_approved=True,
            barangay_id=barangay_id
        )
        steward.set_password("StewardPass123!")
        db.session.add(steward)
        db.session.flush()
        print(f"[INFO] Created Barangay Steward User: {username} for {barangay_name}")
    return steward

def sync_dataset(dataset_path, default_category="Historical"):
    if not os.path.exists(dataset_path):
        print(f"[WARN] Dataset path {dataset_path} does not exist. Skipping.")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        name = item.get("name")
        description = item.get("description")
        scraped_category = item.get("category", default_category)
        barangay_name = item.get("barangay", "Poblacion")
        images = item.get("images", [])

        # Format category: map "Heritage" to "Historical" for map UI filter integration
        category = "Historical" if scraped_category == "Heritage" else scraped_category

        # Determine primary image URL
        primary_image_url = None
        if images:
            local_path = images[0].get("local_path")
            if local_path:
                primary_image_url = "/" + local_path.replace("data/scraped_images/", "static/img/attractions/").replace("\\", "/")
            else:
                primary_image_url = images[0].get("highRes")

        # Sanitize description: cannot be Null in DB model
        if not description:
            description = "A registered local cultural heritage site in Mangatarem, Pangasinan."

        # Fetch or create Barangay
        brgy = BarangayInfo.query.filter_by(name=barangay_name).first()
        if not brgy:
            brgy = BarangayInfo(
                name=barangay_name,
                mission=f"Mission of {barangay_name}",
                vision=f"Vision of {barangay_name}",
                history=f"History of {barangay_name}"
            )
            db.session.add(brgy)
            db.session.flush()
            print(f"[INFO] Created missing Barangay: {barangay_name}")

        # Fetch or create Steward User for decentralized CBIS model
        steward = get_or_create_steward(barangay_name, brgy.id)

        # Check for existing matching attractions in DB
        all_db_attractions = Attraction.query.all()
        matched_attractions = [a for a in all_db_attractions if is_match(name, a.name)]

        # Extract coordinates from JSON if available, falling back to mapping/defaults
        json_lat = item.get("latitude")
        json_lng = item.get("longitude")
        osm_alternatives = item.get("osm_alternatives", [])
        if json_lat is not None and json_lng is not None:
            lat, lng = float(json_lat), float(json_lng)
        else:
            lat, lng = COORDINATES_MAPPING.get(name, (15.7900, 120.2910))

        attraction_record = None
        if matched_attractions:
            for existing in matched_attractions:
                # Update existing record
                print(f"[INFO] Match Found! Updating existing attraction: ID {existing.id} | {existing.name}")
                
                # Correct encoding on Saint Raymund if needed
                if "peafort" in existing.name.lower():
                    existing.name = "St. Raymund of Peñafort Parish"

                existing.description = description
                if primary_image_url:
                    existing.image_url = primary_image_url
                existing.status = "approved"  # Make sure it is approved so it renders on map v1
                existing.user_id = steward.id
                existing.osm_alternatives = osm_alternatives
                
                # Update coordinates
                existing.latitude = lat
                existing.longitude = lng
                attraction_record = existing
        else:
            # Create new record
            new_attr = Attraction(
                name=name,
                description=description,
                category=category,
                latitude=lat,
                longitude=lng,
                image_url=primary_image_url,
                barangay_id=brgy.id,
                user_id=steward.id,
                status="approved",
                is_featured=True,
                osm_alternatives=osm_alternatives
            )
            db.session.add(new_attr)
            print(f"[INFO] Created new approved attraction: {name} at ({lat}, {lng})")
            attraction_record = new_attr

        # Synchronize multiple images into GalleryItem linked to the Barangay Steward
        if images:
            for idx, img_obj in enumerate(images):
                local_path = img_obj.get("local_path")
                alt = img_obj.get("alt", f"{name} Image {idx + 1}")
                
                if local_path:
                    img_url = "/" + local_path.replace("data/scraped_images/", "static/img/attractions/").replace("\\", "/")
                else:
                    img_url = img_obj.get("highRes")
                    
                if not img_url:
                    continue
                    
                # Create GalleryItem if not exists
                existing_item = GalleryItem.query.filter_by(url=img_url).first()
                if not existing_item:
                    new_item = GalleryItem(
                        type="photo",
                        url=img_url,
                        caption=alt,
                        user_id=steward.id,
                        status="approved"
                    )
                    db.session.add(new_item)
                    print(f"[INFO] Associated Gallery Image: {alt} -> {img_url}")

    db.session.commit()
    print(f"[SUCCESS] Committed all updates from {os.path.basename(dataset_path)} to database.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("[START] Starting programmatic copy of image assets...")
        copy_image_assets()
        
        print("\n[START] Ingesting scraped heritage dataset with GalleryItems...")
        sync_dataset(os.path.join(root_dir, "data", "scraped_heritage.json"), default_category="Historical")
        
        print("\n[START] Ingesting scraped attractions dataset with GalleryItems...")
        sync_dataset(os.path.join(root_dir, "data", "scraped_attractions.json"), default_category="Nature")
        
        print("\n[FINISHED] Synchronization complete with multiple images integrated!")
