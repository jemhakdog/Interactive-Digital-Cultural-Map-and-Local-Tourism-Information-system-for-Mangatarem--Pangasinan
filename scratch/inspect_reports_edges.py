import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

reports_ids = ['dfd_7078', 'dfd_7079', 'dfd_7080']

print("--- EDGES LINKED TO REPORTS_DB ---")
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        src = cell.attrib.get('source')
        tgt = cell.attrib.get('target')
        val = cell.attrib.get('value', '')
        cid = cell.attrib.get('id')
        
        if src in reports_ids or tgt in reports_ids:
            print(f"Edge ID: {cid:15} | Val: '{val:25}' | Src: {src} | Tgt: {tgt}")
