import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

store_ids = {
    'dfd_7034': 'D1: User_db',
    'dfd_7037': 'D2: Attraction_db',
    'dfd_7040': 'D3: Event_db',
    'dfd_7043': 'D4: Barangay_db',
    'dfd_7070': 'D5: Review_db',
    'dfd_7073': 'D6: Favorite_db',
    'dfd_7076': 'D7: PageView_db',
    'dfd_7079': 'D8: Reports_db',
    'dfd_7401': 'D18: Establishment_db',
    'dfd_7404': 'D19: Establishment_Room_db',
    'dfd_7407': 'D20: Establishment_Menu_db',
    'dfd_7410': 'D21: Establishment_Review_db',
    'dfd_7413': 'D22: User_Fav_Establishment_db',
    'dfd_7416': 'D23: Visitor_Log_db',
    'dfd_7422': 'D24: Newsletter_db',
    'dfd_7426': 'D25: Gallery_db',
    'dfd_7419': 'D26: Audit_Log_db'
}

print("--- DATA STORE CONTAINER POSITIONS ---")
for cell in mx_root.findall('mxCell'):
    cid = cell.attrib.get('id')
    if cid in store_ids:
        geom = cell.find('mxGeometry')
        if geom is not None:
            x = geom.attrib.get('x', '0')
            y = geom.attrib.get('y', '0')
            w = geom.attrib.get('width', '0')
            h = geom.attrib.get('height', '0')
            print(f"{store_ids[cid]:30} | ID: {cid} | X: {x:5} | Y: {y:5} | W: {w:5} | H: {h:5}")
