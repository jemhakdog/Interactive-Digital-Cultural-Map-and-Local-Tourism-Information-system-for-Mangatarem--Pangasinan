import xml.etree.ElementTree as ET
import re
import sys

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()

# First, let's find the main mxGraphModel and root
mx_root = root.find('.//root')
if mx_root is None:
    print("Could not find root")
    sys.exit(1)

# Helper to find a table id by its name
def find_table(name):
    for cell in mx_root.findall('mxCell'):
        val = cell.attrib.get('value', '')
        # Remove any HTML tags if present, but usually the table name is plain text or wrapped
        if name in val and 'table' in cell.attrib.get('style', ''):
            return cell.attrib.get('id')
    return None

def find_row(table_id, fk_name):
    # Find rows belonging to this table
    for cell in mx_root.findall('mxCell'):
        if cell.attrib.get('parent') == table_id:
            # check the columns (children of the row) to see if they contain fk_name
            row_id = cell.attrib.get('id')
            for col in mx_root.findall(f"mxCell[@parent='{row_id}']"):
                if fk_name in col.attrib.get('value', ''):
                    return row_id
    return None

user_table_id = find_table('USER')
attraction_review_table_id = find_table('ATTRACTION_REVIEW')
visitor_log_table_id = find_table('VISITOR LOG')
review_photo_table_id = find_table('REVIEW PHOTO')
pwd_reset_table_id = find_table('PASSWORD RESET TOKEN')
audit_log_table_id = find_table('DATABASE AUDIT LOG')

print(f"USER: {user_table_id}")
print(f"ATTRACTION_REVIEW: {attraction_review_table_id}")
print(f"VISITOR LOG: {visitor_log_table_id}")
print(f"REVIEW PHOTO: {review_photo_table_id}")
print(f"PASSWORD RESET TOKEN: {pwd_reset_table_id}")
print(f"DATABASE AUDIT LOG: {audit_log_table_id}")

# Now we find the rows
edges_to_add = []

if visitor_log_table_id and user_table_id:
    row1 = find_row(visitor_log_table_id, 'logged_by_id')
    if row1: edges_to_add.append((row1, user_table_id, 'logged_by_id'))
    row2 = find_row(visitor_log_table_id, 'visitor_user_id')
    if row2: edges_to_add.append((row2, user_table_id, 'visitor_user_id'))

if review_photo_table_id and attraction_review_table_id:
    row = find_row(review_photo_table_id, 'review_id')
    if row: edges_to_add.append((row, attraction_review_table_id, 'review_id'))

if pwd_reset_table_id and user_table_id:
    row = find_row(pwd_reset_table_id, 'user_id')
    if row: edges_to_add.append((row, user_table_id, 'user_id'))

if audit_log_table_id and user_table_id:
    row = find_row(audit_log_table_id, 'user_id')
    if row: edges_to_add.append((row, user_table_id, 'user_id'))

# Find the highest edge ID to avoid collision
max_id = 0
for cell in mx_root.findall('mxCell'):
    cid = cell.attrib.get('id', '')
    if cid.startswith('erd_edge_'):
        try:
            num = int(cid.split('_')[-1])
            if num > max_id: max_id = num
        except:
            pass

print("Edges to add:")
for src, tgt, val in edges_to_add:
    print(f"Source: {src}, Target: {tgt}, Value: {val}")
    max_id += 1
    new_edge = ET.Element('mxCell')
    new_edge.attrib['id'] = f"erd_edge_{max_id}"
    new_edge.attrib['value'] = val
    new_edge.attrib['style'] = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;endArrow=classic;html=1;fontSize=14;"
    new_edge.attrib['parent'] = "1"
    new_edge.attrib['source'] = src
    new_edge.attrib['target'] = tgt
    new_edge.attrib['edge'] = "1"
    
    geom = ET.SubElement(new_edge, 'mxGeometry')
    geom.attrib['relative'] = "1"
    geom.attrib['as'] = "geometry"
    
    mx_root.append(new_edge)

tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("Updated erd_v2.drawio successfully!")
