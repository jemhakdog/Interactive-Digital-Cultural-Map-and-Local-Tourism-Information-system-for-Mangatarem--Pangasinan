import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- DFD DATA STORES AND COORDINATES ---")
for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    cid = cell.attrib.get('id')
    style = cell.attrib.get('style', '')
    
    if val and 'partialRectangle' in style:
        clean_val = re.sub('<[^<]+?>', '', val).strip()
        geom = cell.find('mxGeometry')
        if geom is not None and cell.attrib.get('parent') == '1':
            x = geom.attrib.get('x', '0')
            y = geom.attrib.get('y', '0')
            w = geom.attrib.get('width', '0')
            h = geom.attrib.get('height', '0')
            print(f"Store Name: {clean_val:25} | ID: {cid:12} | X: {x:5} | Y: {y:5} | W: {w:5} | H: {h:5}")
