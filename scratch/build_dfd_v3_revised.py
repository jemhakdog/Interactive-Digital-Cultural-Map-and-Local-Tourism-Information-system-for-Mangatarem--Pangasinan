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
    print("Could not find DFD XML root")
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

max_id_counter = get_max_id() + 20000

def get_new_id(prefix="dfd_v3_rev_"):
    global max_id_counter
    max_id_counter += 1
    return f"{prefix}{max_id_counter}"

# 1. Eliminate central system hub (dfd_7001)
hub_cell = mx_root.find(".//mxCell[@id='dfd_7001']")
if hub_cell is not None:
    mx_root.remove(hub_cell)
    print("Eliminated central System Hub bubble (dfd_7001).")

# 2. Reroute all edges linked to central system hub dfd_7001
# User_db = dfd_7035, Attraction_db = dfd_7038, Heritage_Profile = dfd_7047
# Review_db = dfd_7071, Favorite_db = dfd_7074, PageView_db = dfd_7076
# Audit_Log_db = dfd_7420, Visitor_Log_db = dfd_7417, Gallery_db = dfd_7427
# Establishment_db = dfd_7402, Newsletter_db = dfd_7423
# Visitor Logging Body = dfd_7305

hub_reroutings = {
    'dfd_7091': ('dfd_7004', 'dfd_7035'),  # User Accounts: 1.0 Auth -> User_db
    'dfd_7092': ('dfd_7009', 'dfd_7038'),  # mangatarem Tourism Record: 2.0 Content -> Attraction_db
    'dfd_7093': ('dfd_7012', 'dfd_7047'),  # Heritage Records: 9.0 Heritage -> Heritage_Profile
    'dfd_7094': ('dfd_7013', 'dfd_7420'),  # Approval Log: 5.0 Approval -> Audit_Log_db
    'dfd_7095': ('dfd_7038', 'dfd_7016'),  # Map Content: Attraction_db -> 3.0 Map Display (process body dfd_7016 / dfd_7018)
    'dfd_7096': ('dfd_7038', 'dfd_7019'),  # Discovery Data: Attraction_db -> 4.0 Content Discovery
    'dfd_7097': ('dfd_7071', 'dfd_7022'),  # User Feedback: Review_db -> 8.0 Review Process (body dfd_7022 / dfd_7024)
    'dfd_7098': ('dfd_7074', 'dfd_7025'),  # Engagement Logs: Favorite_db -> 6.0 Favorites Process
    'dfd_7099': ('dfd_7076', 'dfd_7028'),  # System Metrics: PageView_db -> 7.0 Analytics Process
    'dfd_edge_7514': ('dfd_7302', 'dfd_7402'),  # Establishment Records: 10.0 Biz Mgmt body dfd_7302 -> Establishment_db
    'dfd_edge_7515': ('dfd_7311', 'dfd_7427'),  # Gallery Records: 13.0 Gallery -> Gallery_db
    'dfd_edge_7516': ('dfd_7305', 'dfd_7417'),  # Log Summary: 11.0 Visitor Log body dfd_7305 -> Visitor_Log_db
    'dfd_edge_7517': ('dfd_7308', 'dfd_7423')   # Subscriber Metrics: 12.0 Newsletter body dfd_7308 -> Newsletter_db
}

for edge_id, (src, tgt) in hub_reroutings.items():
    edge_cell = mx_root.find(f".//mxCell[@id='{edge_id}']")
    if edge_cell is not None:
        edge_cell.attrib['source'] = src
        edge_cell.attrib['target'] = tgt
        print(f"Rerouted Edge {edge_id} ('{edge_cell.attrib.get('value')}') to connect {src} directly to {tgt}.")

# 3. Reroute and wire external entity float edges
# ADMIN = dfd_7002, TOURIST = dfd_7003
# 9.0 Heritage Mgmt Body = dfd_7012
# 8.0 Review Body = dfd_7024
# 7.0 Analytics Body = dfd_7028
# 3.0 Map Display Body = dfd_7018
# 4.0 Discovery Body = dfd_7019

entity_reroutings = {
    'dfd_7085': ('dfd_7002', 'dfd_7012'), # Heritage Data: ADMIN -> 9.0 Heritage
    'dfd_7087': ('dfd_7002', 'dfd_7024'), # Review Content: ADMIN -> 8.0 Review
    'dfd_7089': ('dfd_7002', 'dfd_7028'), # Reports Request: ADMIN -> 7.0 Analytics
    'dfd_7102': ('dfd_7003', 'dfd_7018'), # Map View Request: TOURIST -> 3.0 Map Display
    'dfd_7104': ('dfd_7003', 'dfd_7019'), # Search Attractions: TOURIST -> 4.0 Discovery
    'dfd_7105': ('dfd_7019', 'dfd_7003'), # Search Results: 4.0 Discovery -> TOURIST
    'dfd_7106': ('dfd_7003', 'dfd_7022')  # Submit Review: TOURIST -> 8.0 Review Body
}

for edge_id, (src, tgt) in entity_reroutings.items():
    edge_cell = mx_root.find(f".//mxCell[@id='{edge_id}']")
    if edge_cell is not None:
        edge_cell.attrib['source'] = src
        edge_cell.attrib['target'] = tgt
        # make sure it is marked as edge
        edge_cell.attrib['edge'] = "1"
        print(f"Connected External Entity Edge {edge_id} ('{edge_cell.attrib.get('value')}') from {src} to {tgt}.")

# 4. Delete obsolete Heritage Cluster datastore shapes recursively
obsolete_heritage_datastores = [
    'dfd_7048', # 16 container
    'dfd_7051', # 17 container
    'dfd_7054', # 10 container
    'dfd_7057', # 11 container
    'dfd_7060', # 12 container
    'dfd_7063', # 13 container
    'dfd_7066', # 14 container
    '8'         # duplicate 15 group
]

# Find all children cells of these obsolete parents
children_to_delete = []
for cell in mx_root.findall('mxCell'):
    parent_id = cell.attrib.get('parent')
    if parent_id in obsolete_heritage_datastores:
        children_to_delete.append(cell.attrib.get('id'))

# Combine containers and children
all_to_delete = obsolete_heritage_datastores + children_to_delete

deleted_heritage_count = 0
for cid in all_to_delete:
    cell = mx_root.find(f".//mxCell[@id='{cid}']")
    if cell is not None:
        mx_root.remove(cell)
        deleted_heritage_count += 1

print(f"Deleted {deleted_heritage_count} heritage datastore containers and labels.")

# 5. Reroute heritage detail flow edges directly to D15 Heritage_Profile label (dfd_7047)
# Admin Approval body is dfd_7015
heritage_edge_reroutings = {
    'dfd_7118': 'dfd_7047', # Built Details
    'dfd_7119': 'dfd_7047', # Movable Details
    'dfd_7120': 'dfd_7047', # Natural Details
    'dfd_7122': 'dfd_7047', # Inst Details
    'dfd_7123': 'dfd_7047', # Program Details
    'dfd_7124': 'dfd_7047', # Personality Details
    'dfd_7126': 'dfd_7047'  # Profile Approval
}

for edge_id, tgt in heritage_edge_reroutings.items():
    edge_cell = mx_root.find(f".//mxCell[@id='{edge_id}']")
    if edge_cell is not None:
        edge_cell.attrib['target'] = tgt
        if edge_id == 'dfd_7126':
            # Wire source to Admin Approval body
            edge_cell.attrib['source'] = 'dfd_7015'
        print(f"Rerouted Heritage Edge {edge_id} to unified Heritage_Profile datastore ({tgt}).")

# 6. Renumber duplicate process IDs
# Newsletter Subscription = dfd_7307 -> 13.0
# Media Gallery = dfd_7310 -> 12.0
# Booking = dfd_proc_h_15518 -> 14.0
# Chat = dfd_proc_h_15523 -> 15.0

process_renumberings = {
    'dfd_7307': '13.0',
    'dfd_7310': '12.0',
    'dfd_proc_h_15518': '14.0',
    'dfd_proc_h_15523': '15.0'
}

for proc_id, new_val in process_renumberings.items():
    proc_cell = mx_root.find(f".//mxCell[@id='{proc_id}']")
    if proc_cell is not None:
        proc_cell.attrib['value'] = new_val
        print(f"Renumbered Process ID {proc_id} to '{new_val}'.")

# 7. Remove obsolete Reports_db (dfd_7078 group and children dfd_7079, dfd_7080)
reports_cells = ['dfd_7078', 'dfd_7079', 'dfd_7080']
deleted_reports_count = 0
for cid in reports_cells:
    cell = mx_root.find(f".//mxCell[@id='{cid}']")
    if cell is not None:
        mx_root.remove(cell)
        deleted_reports_count += 1

# Delete old reports edges dfd_7132 and dfd_7133
for edge_id in ['dfd_7132', 'dfd_7133']:
    cell = mx_root.find(f".//mxCell[@id='{edge_id}']")
    if cell is not None:
        mx_root.remove(cell)

print(f"Removed obsolete Reports_db (deleted {deleted_reports_count} cells) and its archive/historical edges.")

# 8. Inject D30 Map_Feedback_db and D31 Business_Verification_db
def inject_store(num_val, store_name, x, y):
    group_id = get_new_id("dfd_store_g_rev_")
    num_id = get_new_id("dfd_store_n_rev_")
    lbl_id = get_new_id("dfd_store_l_rev_")
    
    # Group
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
    
    # Number label
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
    
    # Database label
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
    print(f"Injected Datastore D{num_val}: {store_name} at ({x}, {y})")
    return lbl_id

def inject_edge(src_id, tgt_id, val):
    edge_id = get_new_id("dfd_edge_rev_")
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

# Inject D30 Map_Feedback_db and flow
feedback_db_lbl = inject_store("30", "Map_Feedback_db", 1460, 780)
inject_edge("dfd_7024", feedback_db_lbl, "Save Feedback") # Review Process body (dfd_7024) -> Feedback DB

# Inject D31 Business_Verification_db and flows
verif_db_lbl = inject_store("31", "Business_Verification_db", 730, 1790)
inject_edge("dfd_7302", verif_db_lbl, "Save Permit") # Establishment Mgmt body (dfd_7302) -> Verification DB
inject_edge(verif_db_lbl, "dfd_7015", "Verification Data") # Verification DB -> Admin Approval body (dfd_7015)

# Inject direct Analytics Pull flows
# PageView_db = dfd_7076, Audit_Log_db = dfd_7420, Analytics Process body = dfd_7028
inject_edge("dfd_7076", "dfd_7028", "Page Metrics")
inject_edge("dfd_7420", "dfd_7028", "Audit Logs")

# Save output
tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("Updated dfd-level-1-clean_v3.drawio successfully with Level 1 structural and database corrections!")
