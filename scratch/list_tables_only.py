import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- UNIQUE ERD TABLES AND COORDINATES ---")
for cell in mx_root.findall('mxCell'):
    style = cell.attrib.get('style', '')
    val = cell.attrib.get('value', '')
    cid = cell.attrib.get('id')
    parent = cell.attrib.get('parent')
    
    # Unique table checks
    if ('shape=table' in style or ('childLayout=tableLayout' in style)) and parent == '1':
        clean_val = re.sub('<[^<]+?>', '', val).strip()
        geom = cell.find('mxGeometry')
        if geom is not None:
            x = geom.attrib.get('x', '0')
            y = geom.attrib.get('y', '0')
            w = geom.attrib.get('width', '0')
            h = geom.attrib.get('height', '0')
            print(f"Table Name: {clean_val:25} | ID: {cid:20} | X: {x:6} | Y: {y:6} | W: {w:6} | H: {h:6}")
