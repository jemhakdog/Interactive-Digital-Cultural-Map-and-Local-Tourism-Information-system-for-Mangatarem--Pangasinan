import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

if mx_root is None:
    print("Could not find DFD root")
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

max_id_counter = get_max_id() + 8000

def get_new_id(prefix="dfd_v3_"):
    global max_id_counter
    max_id_counter += 1
    return f"{prefix}{max_id_counter}"

# 1. Reroute old review/favorite edges
# dfd_edge_7508 goes to dfd_7071 (Review_db label)
# dfd_edge_7509 goes to dfd_7074 (Favorite_db label)
edge_7508 = mx_root.find(".//mxCell[@id='dfd_edge_7508']")
if edge_7508 is not None:
    edge_7508.attrib['target'] = "dfd_7071"
    print("Rerouted edge dfd_edge_7508 (Save Est Review) to unified Review_db (dfd_7071)")

edge_7509 = mx_root.find(".//mxCell[@id='dfd_edge_7509']")
if edge_7509 is not None:
    edge_7509.attrib['target'] = "dfd_7074"
    print("Rerouted edge dfd_edge_7509 (Save Fav Est) to unified Favorite_db (dfd_7074)")

# 2. Delete old Review and Favorite datastore containers and their children
to_delete_ids = [
    'dfd_7409', 'dfd_7410', 'dfd_7411', # Establishment_Review_db container, number, label
    'dfd_7412', 'dfd_7413', 'dfd_7414'  # User_Fav_Establishment_db container, number, label
]

deleted_count = 0
for cid in to_delete_ids:
    cell = mx_root.find(f".//mxCell[@id='{cid}']")
    if cell is not None:
        mx_root.remove(cell)
        deleted_count += 1

print(f"Deleted {deleted_count} elements associated with consolidated establishment review/favorite datastores.")

# 3. Helpers to inject new processes & datastores
def add_dfd_process(num_val, body_val, x, y):
    header_id = get_new_id("dfd_proc_h_")
    body_id = get_new_id("dfd_proc_b_")
    
    # Header cell (number row, e.g. "12.0")
    header_cell = ET.Element('mxCell')
    header_cell.attrib['id'] = header_id
    header_cell.attrib['value'] = num_val
    header_cell.attrib['style'] = "rounded=1;whiteSpace=wrap;html=1;fillColor=#BDD7EE;strokeColor=#000000;fontStyle=1;fontColor=#000000;align=center;verticalAlign=middle;strokeWidth=1.5;fontSize=13;"
    header_cell.attrib['parent'] = "1"
    header_cell.attrib['vertex'] = "1"
    
    h_geom = ET.SubElement(header_cell, 'mxGeometry')
    h_geom.attrib['x'] = str(x)
    h_geom.attrib['y'] = str(y)
    h_geom.attrib['width'] = "180"
    h_geom.attrib['height'] = "25"
    h_geom.attrib['as'] = "geometry"
    
    # Body cell (process description, e.g. "Booking Management")
    body_cell = ET.Element('mxCell')
    body_cell.attrib['id'] = body_id
    body_cell.attrib['value'] = body_val
    body_cell.attrib['style'] = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;align=center;verticalAlign=middle;fontSize=13;strokeWidth=1.5;"
    body_cell.attrib['parent'] = "1"
    body_cell.attrib['vertex'] = "1"
    
    b_geom = ET.SubElement(body_cell, 'mxGeometry')
    b_geom.attrib['x'] = str(x)
    b_geom.attrib['y'] = str(y + 25)
    b_geom.attrib['width'] = "180"
    b_geom.attrib['height'] = "127"
    b_geom.attrib['as'] = "geometry"
    
    mx_root.append(header_cell)
    mx_root.append(body_cell)
    print(f"Added Process {num_val} ({body_val}) at ({x}, {y})")
    return header_id, body_id

def add_dfd_datastore(num_val, store_name, x, y):
    group_id = get_new_id("dfd_store_g_")
    num_id = get_new_id("dfd_store_n_")
    lbl_id = get_new_id("dfd_store_l_")
    
    # Outer Group
    group_cell = ET.Element('mxCell')
    group_cell.attrib['id'] = group_id
    group_cell.attrib['value'] = ""
    group_cell.attrib['style'] = "group;fontSize=13;"
    group_cell.attrib['parent'] = "1"
    group_cell.attrib['vertex'] = "1"
    
    g_geom = ET.SubElement(group_cell, 'mxGeometry')
    g_geom.attrib['x'] = str(x)
    g_geom.attrib['y'] = str(y)
    g_geom.attrib['width'] = "160"
    g_geom.attrib['height'] = "45"
    g_geom.attrib['as'] = "geometry"
    
    # Number Label ("27")
    num_cell = ET.Element('mxCell')
    num_cell.attrib['id'] = num_id
    num_cell.attrib['value'] = num_val
    num_cell.attrib['style'] = "rounded=0;whiteSpace=wrap;html=1;fillColor=#BDD7EE;strokeColor=#000000;fontStyle=1;fontColor=#000000;align=center;strokeWidth=1.5;fontSize=13;"
    num_cell.attrib['parent'] = group_id
    num_cell.attrib['vertex'] = "1"
    
    n_geom = ET.SubElement(num_cell, 'mxGeometry')
    n_geom.attrib['width'] = "30"
    n_geom.attrib['height'] = "45"
    n_geom.attrib['as'] = "geometry"
    
    # Store Name Label ("Booking_db")
    lbl_cell = ET.Element('mxCell')
    lbl_cell.attrib['id'] = lbl_id
    lbl_cell.attrib['value'] = store_name
    lbl_cell.attrib['style'] = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;align=center;strokeWidth=1.5;fontSize=13;"
    lbl_cell.attrib['parent'] = group_id
    lbl_cell.attrib['vertex'] = "1"
    
    l_geom = ET.SubElement(lbl_cell, 'mxGeometry')
    l_geom.attrib['x'] = "30"
    l_geom.attrib['width'] = "130"
    l_geom.attrib['height'] = "45"
    l_geom.attrib['as'] = "geometry"
    
    mx_root.append(group_cell)
    mx_root.append(num_cell)
    mx_root.append(lbl_cell)
    print(f"Added Datastore D{num_val}: {store_name} at ({x}, {y})")
    return group_id, lbl_id

def add_dfd_edge(src_id, tgt_id, val):
    edge_id = get_new_id("dfd_edge_v3_")
    edge_cell = ET.Element('mxCell')
    edge_cell.attrib['id'] = edge_id
    edge_cell.attrib['value'] = val
    edge_cell.attrib['style'] = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=1.5;endArrow=classic;html=1;fontSize=12;"
    edge_cell.attrib['parent'] = "1"
    edge_cell.attrib['source'] = src_id
    edge_cell.attrib['target'] = tgt_id
    edge_cell.attrib['edge'] = "1"
    
    geom = ET.SubElement(edge_cell, 'mxGeometry')
    geom.attrib['relative'] = "1"
    geom.attrib['as'] = "geometry"
    
    mx_root.append(edge_cell)
    return edge_id

# 4. Inject V3 DFD components
# A. Process 12.0: Booking & Reservations Management
proc12_h, proc12_b = add_dfd_process("12.0", "Booking & Reservations Management", 950, 1200)

# B. Datastore 27: Booking_db
store27_g, store27_l = add_dfd_datastore("27", "Booking_db", 950, 1050)

# C. Process 13.0: Chat Messaging Network
proc13_h, proc13_b = add_dfd_process("13.0", "Chat Messaging Network", 280, 1200)

# D. Datastore 28: Chat_db
store28_g, store28_l = add_dfd_datastore("28", "Chat_db", 280, 1050)

# E. Datastore 29: Notification_db
store29_g, store29_l = add_dfd_datastore("29", "Notification_db", -120, 1390)

# 5. Draw DFD relationship edges / flows
add_dfd_edge(proc12_b, store27_l, "Save Booking")
add_dfd_edge(proc13_b, store28_l, "Send Message")
add_dfd_edge(proc12_b, store29_l, "Notify User")

# Flow from Process 10.0 (Establishment Management body is dfd_7302) to Booking_db
add_dfd_edge("dfd_7302", store27_l, "Initialize Slots")

# Save output
tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("Updated dfd-level-1-clean_v3.drawio successfully!")
