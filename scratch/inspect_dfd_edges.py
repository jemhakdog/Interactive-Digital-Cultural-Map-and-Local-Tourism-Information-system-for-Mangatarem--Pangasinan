import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- EDGES LINKED TO dfd_7411 (Establishment_Review_db) ---")
for cell in mx_root.findall('mxCell'):
    edge = cell.attrib.get('edge')
    if edge == "1":
        src = cell.attrib.get('source')
        tgt = cell.attrib.get('target')
        val = cell.attrib.get('value', '')
        cid = cell.attrib.get('id')
        if src == 'dfd_7411' or tgt == 'dfd_7411':
            print(f"Edge ID: {cid} | Val: '{val}' | Source: {src} | Target: {tgt}")

print("\n--- EDGES LINKED TO dfd_7414 (User_Fav_Establishment_db) ---")
for cell in mx_root.findall('mxCell'):
    edge = cell.attrib.get('edge')
    if edge == "1":
        src = cell.attrib.get('source')
        tgt = cell.attrib.get('target')
        val = cell.attrib.get('value', '')
        cid = cell.attrib.get('id')
        if src == 'dfd_7414' or tgt == 'dfd_7414':
            print(f"Edge ID: {cid} | Val: '{val}' | Source: {src} | Target: {tgt}")
