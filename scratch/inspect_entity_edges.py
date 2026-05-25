import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

entities = {
    'dfd_7003': 'TOURIST',
    'dfd_7002': 'ADMIN',
    'dfd_7501': 'BUSINESS OWNER',
    'dfd_7502': 'HERITAGE GUARDIAN (GUARD)'
}

print("--- EDGES LINKED TO EXTERNAL ENTITIES ---")
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        src = cell.attrib.get('source')
        tgt = cell.attrib.get('target')
        val = cell.attrib.get('value', '')
        cid = cell.attrib.get('id')
        
        if src in entities or tgt in entities:
            src_name = entities.get(src, src)
            tgt_name = entities.get(tgt, tgt)
            print(f"Edge ID: {cid:15} | Val: '{val:25}' | Src: {str(src_name):30} | Tgt: {str(tgt_name):30}")
