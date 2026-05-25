import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- HERITAGE CLUSTER SHAPES & LABELS ---")
heritage_keywords = [
    "Cultural_Inst", "LGU_Program", "Personality", "Heritage_Profile",
    "Built Details", "Movable Details", "Natural Details", "Program Details",
    "Personality Details", "Inst Details"
]

for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    cid = cell.attrib.get('id')
    style = cell.attrib.get('style', '')
    parent = cell.attrib.get('parent')
    
    clean_val = re.sub('<[^<]+?>', '', val).strip()
    clean_val = clean_val.replace('&amp;', '&').replace('\n', ' ')
    
    # Match keywords or store numbers
    matches_kw = any(kw.lower() in clean_val.lower() for kw in heritage_keywords)
    matches_num = clean_val in ["10", "11", "12", "13", "14", "15", "16", "17"]
    
    if matches_kw or matches_num:
        print(f"ID: {cid:15} | Parent: {str(parent):10} | Style: {style[:30]}... | Val: '{clean_val}'")
