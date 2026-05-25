import xml.etree.ElementTree as ET
import re

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- TABLE POSITIONS ---")
for cell in mx_root.findall('mxCell'):
    style = cell.attrib.get('style', '')
    val = cell.attrib.get('value', '')
    cid = cell.attrib.get('id')
    
    if 'shape=table' in style or ('childLayout=tableLayout' in style):
        clean_val = re.sub('<[^<]+?>', '', val).strip()
        geom = cell.find('mxGeometry')
        if geom is not None:
            x = geom.attrib.get('x', '0')
            y = geom.attrib.get('y', '0')
            w = geom.attrib.get('width', '0')
            h = geom.attrib.get('height', '0')
            print(f"Table: {clean_val:25} | ID: {cid:15} | X: {x:5} | Y: {y:5} | W: {w:5} | H: {h:5}")
