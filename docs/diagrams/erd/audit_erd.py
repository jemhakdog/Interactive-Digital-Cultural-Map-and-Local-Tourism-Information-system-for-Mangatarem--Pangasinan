"""Audit: Compare generate_erd.py fields vs actual models."""
import ast
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# --- Extract fields from generate_erd.py ---
from generate_erd import TABLES as ERD_TABLES

erd_fields = {}
for name, tdef in ERD_TABLES.items():
    erd_fields[name] = [f[1] for f in tdef["fields"]]

# --- Extract fields from actual models ---
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

model_files = {
    "User": os.path.join(ROOT, "models.py"),
    "Attraction": os.path.join(ROOT, "models.py"),
    "Event": os.path.join(ROOT, "models.py"),
    "GalleryItem": os.path.join(ROOT, "models.py"),
    "BarangayInfo": os.path.join(ROOT, "models.py"),
    "AnalyticsPageView": os.path.join(ROOT, "models.py"),
    "Favorite": os.path.join(ROOT, "models.py"),
    "EventInterest": os.path.join(ROOT, "models.py"),
    "Review": os.path.join(ROOT, "models.py"),
    "NaturalHeritage": os.path.join(ROOT, "heritage_models", "natural_heritage.py"),
    "IntangibleHeritage": os.path.join(ROOT, "heritage_models", "intangible_heritage.py"),
    "CulturalInstitution": os.path.join(ROOT, "heritage_models", "cultural_institution.py"),
    "LGUCultureProgram": os.path.join(ROOT, "heritage_models", "lgu_culture_program.py"),
    "PersonalityProfile": os.path.join(ROOT, "heritage_models", "personality_profile.py"),
}

# Map class names to ERD table names
class_to_table = {
    "User": "USER",
    "Attraction": "ATTRACTION",
    "Event": "EVENT",
    "GalleryItem": "GALLERY_ITEM",
    "BarangayInfo": "BARANGAY_INFO",
    "AnalyticsPageView": "ANALYTICS_PAGE_VIEW",
    "Favorite": "FAVORITE",
    "EventInterest": "EVENT_INTEREST",
    "Review": "REVIEW",
    "NaturalHeritage": "NATURAL_HERITAGE",
    "IntangibleHeritage": "INTANGIBLE_HERITAGE",
    "CulturalInstitution": "CULTURAL_INSTITUTION",
    "LGUCultureProgram": "LGU_CULTURE_PROGRAM",
    "PersonalityProfile": "PERSONALITY_PROFILE",
}

def extract_fields_from_file(filepath, classname):
    with open(filepath, 'r') as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == classname:
            fields = []
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and target.id != '__tablename__':
                            fields.append(target.id)
            return fields
    return []

print("=" * 80)
print(f"{'TABLE':<25} {'ERD Fields':<12} {'Model Fields':<14} {'Status'}")
print("=" * 80)

all_ok = True
for classname, filepath in model_files.items():
    table = class_to_table[classname]
    model_f = extract_fields_from_file(filepath, classname)
    erd_f = erd_fields.get(table, [])
    
    erd_set = set(erd_f)
    model_set = set(model_f)
    
    extra_in_erd = erd_set - model_set
    missing_in_erd = model_set - erd_set
    
    status = "OK" if not extra_in_erd and not missing_in_erd else "MISMATCH"
    if status == "MISMATCH":
        all_ok = False
    
    print(f"{table:<25} {len(erd_f):<12} {len(model_f):<14} {status}")
    if extra_in_erd:
        for f in sorted(extra_in_erd):
            print(f"  [ERD EXTRA]   {f}")
    if missing_in_erd:
        for f in sorted(missing_in_erd):
            print(f"  [MODEL ONLY]  {f}")

print("=" * 80)
if all_ok:
    print("RESULT: All ERD tables match their models perfectly.")
else:
    print("RESULT: Mismatches found! ERD needs updating.")
