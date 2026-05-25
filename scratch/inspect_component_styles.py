import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

components = ['dfd_7301', 'dfd_7302', 'dfd_7421', 'dfd_7422']

print("--- COMPONENT STYLE DETAILS ---")
for cell in mx_root.findall('mxCell'):
    cid = cell.attrib.get('id')
    if cid in components:
        print(f"ID: {cid} | Style: {cell.attrib.get('style')} | Val: '{cell.attrib.get('value')}'")
