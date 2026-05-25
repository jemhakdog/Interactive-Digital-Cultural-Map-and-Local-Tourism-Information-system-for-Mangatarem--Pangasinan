import xml.etree.ElementTree as ET
import re

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- TABLES FOUND IN erd_v2.drawio ---")
tables = []
for cell in mx_root.findall('mxCell'):
    style = cell.attrib.get('style', '')
    val = cell.attrib.get('value', '')
    cid = cell.attrib.get('id')
    
    # Check if it looks like a table or contains a table-like header
    if 'shape=table' in style or 'swimlane' in style or ('childLayout=tableLayout' in style):
        clean_val = re.sub('<[^<]+?>', '', val).strip()
        tables.append((cid, clean_val, style))
        print(f"ID: {cid} | Name: {clean_val}")

print("\n--- ALL UNIQUE mxCell VALUES CONTAINS 'shape=table' OR TYPICAL HEADERS ---")
# Let's also print cells that have parent=1 and represent custom shapes/swimlanes
for cell in mx_root.findall("mxCell[@parent='1']"):
    val = cell.attrib.get('value', '')
    if val and not val.startswith('<'):
        clean_val = re.sub('<[^<]+?>', '', val).strip()
        if clean_val and len(clean_val) < 50:
            print(f"Parent=1 | ID: {cell.attrib.get('id')} | Val: {clean_val}")
