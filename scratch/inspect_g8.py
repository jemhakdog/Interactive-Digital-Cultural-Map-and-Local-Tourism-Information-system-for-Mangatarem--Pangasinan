import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- INSPECT GROUP 8 & CHILDREN ---")
for cid in ['8', '9', '10']:
    cell = mx_root.find(f".//mxCell[@id='{cid}']")
    if cell is not None:
        geom = cell.find('mxGeometry')
        x, y, w, h = '0', '0', '0', '0'
        if geom is not None:
            x = geom.attrib.get('x', '0')
            y = geom.attrib.get('y', '0')
            w = geom.attrib.get('width', '0')
            h = geom.attrib.get('height', '0')
        print(f"ID: {cid:10} | Parent: {cell.attrib.get('parent'):10} | Value: '{cell.attrib.get('value')}' | style: {cell.attrib.get('style')[:40]} | X: {x}, Y: {y}, W: {w}, H: {h}")
