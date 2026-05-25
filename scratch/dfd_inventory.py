import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- EXHAUSTIVE DFD TEXT INVENTORY ---")
for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    cid = cell.attrib.get('id')
    parent = cell.attrib.get('parent')
    style = cell.attrib.get('style', '')
    edge = cell.attrib.get('edge', '0')
    
    clean_val = re.sub('<[^<]+?>', '', val).strip()
    clean_val = clean_val.replace('&amp;', '&').replace('\n', ' ')
    
    if clean_val and len(clean_val) < 150:
        print(f"ID: {cid:15} | Parent: {str(parent):10} | Edge: {str(edge):5} | Val: '{clean_val}'")
