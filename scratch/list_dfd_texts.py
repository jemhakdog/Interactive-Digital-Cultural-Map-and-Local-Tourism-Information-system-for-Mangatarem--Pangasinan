import xml.etree.ElementTree as ET
import re

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- ALL TEXT VALUES IN DFD V2 ---")
for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    if val:
        clean_val = re.sub('<[^<]+?>', '', val).strip()
        clean_val = clean_val.replace('&amp;', '&').replace('\n', ' ')
        cid = cell.attrib.get('id')
        if len(clean_val) > 0 and len(clean_val) < 100:
            print(f"ID: {cid} | Text: {clean_val}")
