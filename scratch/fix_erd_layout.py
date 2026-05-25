import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

if mx_root is None:
    print("Could not find ERD root")
    sys.exit(1)

# Helper to find maximum ID to prevent collisions
def get_max_id():
    max_id = 0
    for cell in mx_root.findall('mxCell'):
        cid = cell.attrib.get('id', '')
        digits = re.findall(r'\d+', cid)
        for d in digits:
            max_id = max(max_id, int(d))
    return max_id

max_id_counter = get_max_id() + 30000

def get_new_id(prefix="erd_v3_rev_"):
    global max_id_counter
    max_id_counter += 1
    return f"{prefix}{max_id_counter}"

# 1. Inject missing BUSINESS_VERIFICATION table
def add_new_table(table_name, x, y, width, height, columns):
    table_id = get_new_id("erd_table_v3_rev_")
    
    # Main Table
    table_cell = ET.Element('mxCell')
    table_cell.attrib['id'] = table_id
    table_cell.attrib['value'] = table_name
    table_cell.attrib['style'] = "shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;rowLines=1;columnLines=1;fontStyle=1;align=center;valign=middle;fontSize=14;fillColor=#f5f5f5;strokeColor=#666666;"
    table_cell.attrib['parent'] = "1"
    table_cell.attrib['vertex'] = "1"
    
    geom = ET.SubElement(table_cell, 'mxGeometry')
    geom.attrib['x'] = str(x)
    geom.attrib['y'] = str(y)
    geom.attrib['width'] = str(width)
    geom.attrib['height'] = str(height)
    geom.attrib['as'] = "geometry"
    
    mx_root.append(table_cell)
    
    # Rows
    y_pos = 30
    row_cells = {}
    
    for fk, col_name, col_type, col_det in columns:
        row_id = get_new_id("erd_row_v3_rev_")
        row_cells[col_name] = row_id
        
        row_cell = ET.Element('mxCell')
        row_cell.attrib['id'] = row_id
        row_cell.attrib['value'] = ""
        row_cell.attrib['style'] = "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;strokeColor=none;strokeWidth=0;collapsible=0;recursiveResize=0;expand=0;fontStyle=0;connectable=0;align=center;valign=middle;fontColor=none;spacing=0;spacingTop=0;spacingLeft=0;spacingBottom=0;spacingRight=0;pointerEvents=0;"
        row_cell.attrib['parent'] = table_id
        row_cell.attrib['vertex'] = "1"
        
        row_geom = ET.SubElement(row_cell, 'mxGeometry')
        row_geom.attrib['y'] = str(y_pos)
        row_geom.attrib['width'] = str(width)
        row_geom.attrib['height'] = "34"
        row_geom.attrib['as'] = "geometry"
        
        mx_root.append(row_cell)
        
        # Columns
        col_widths = [40, 150, 80, 290]
        col_vals = [fk, col_name, col_type, col_det]
        x_pos = 0
        for i in range(4):
            col_cell = ET.Element('mxCell')
            col_cell.attrib['id'] = f"{row_id}_col_{i}"
            col_cell.attrib['value'] = col_vals[i]
            col_cell.attrib['style'] = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;overflow=hidden;"
            col_cell.attrib['parent'] = row_id
            col_cell.attrib['vertex'] = "1"
            
            col_geom = ET.SubElement(col_cell, 'mxGeometry')
            col_geom.attrib['x'] = str(x_pos)
            col_geom.attrib['width'] = str(col_widths[i])
            col_geom.attrib['height'] = "34"
            col_geom.attrib['as'] = "geometry"
            
            mx_root.append(col_cell)
            x_pos += col_widths[i]
            
        y_pos += 34
        
    print(f"Successfully injected table {table_name} at ({x}, {y})")
    return table_id, row_cells

def add_relationship_edge(src_row_id, target_table_id, fk_label):
    edge_id = get_new_id("erd_edge_v3_rev_")
    edge_cell = ET.Element('mxCell')
    edge_cell.attrib['id'] = edge_id
    edge_cell.attrib['value'] = fk_label
    edge_cell.attrib['style'] = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;endArrow=classic;html=1;fontSize=14;"
    edge_cell.attrib['parent'] = "1"
    edge_cell.attrib['source'] = src_row_id
    edge_cell.attrib['target'] = target_table_id
    edge_cell.attrib['edge'] = "1"
    
    geom = ET.SubElement(edge_cell, 'mxGeometry')
    geom.attrib['relative'] = "1"
    geom.attrib['as'] = "geometry"
    
    mx_root.append(edge_cell)
    return edge_id

# Inject BUSINESS_VERIFICATION columns
verification_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK)", "user_id", "int", "→ USER.id (not null)"),
    ("", "permit_document_url", "string", "not null"),
    ("", "other_document_url", "string", "nullable"),
    ("", "status", "string", "default='pending'"),
    ("", "submitted_at", "datetime", "default=now")
]

# Place it below USER_NOTIFICATION in the USER column
verif_table_id, verif_rows = add_new_table("BUSINESS_VERIFICATION", -550, 1790, 560, 240, verification_cols)

# Wire relationship to USER
user_table_id = "erd_1001"
add_relationship_edge(verif_rows["user_id"], user_table_id, "user_id")
print("Wired relationship edge from BUSINESS_VERIFICATION.user_id to USER.")

# 2. Clean mxGeometry of ALL edges in the ERD to snap them dynamically
purged_absolute_points = 0
purged_control_arrays = 0

for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        geom = cell.find('mxGeometry')
        if geom is not None:
            # Remove absolute sourcePoint
            source_pt = geom.find("mxPoint[@as='sourcePoint']")
            if source_pt is not None:
                geom.remove(source_pt)
                purged_absolute_points += 1
            
            # Remove absolute targetPoint
            target_pt = geom.find("mxPoint[@as='targetPoint']")
            if target_pt is not None:
                geom.remove(target_pt)
                purged_absolute_points += 1
            
            # Remove custom control point array
            points_node = geom.find('Array')
            if points_node is not None:
                geom.remove(points_node)
                purged_control_arrays += 1

print(f"Purged {purged_absolute_points} absolute coordinate float overrides from ERD edges.")
print(f"Purged {purged_control_arrays} custom control point arrays from ERD edges to force dynamic snapping.")

# Save output
tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("ERD layout fix executed successfully on erd_v3.drawio!")
