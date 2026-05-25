import xml.etree.ElementTree as ET
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

# 1. Consolidate 6 heritage detail edges into one single edge dfd_7118
edge_7118 = mx_root.find(".//mxCell[@id='dfd_7118']")
if edge_7118 is not None:
    edge_7118.attrib['value'] = "Heritage Details (Built, Movable, Natural, Intangible, Inst, Program, Personality)"
    edge_7118.attrib['source'] = "dfd_7012"
    edge_7118.attrib['target'] = "dfd_7047"
    print("Updated edge dfd_7118 to consolidate all heritage details.")

# Remove other redundant detail edges
redundant_edges = ['dfd_7119', 'dfd_7120', 'dfd_7122', 'dfd_7123', 'dfd_7124']
deleted_edges_count = 0
for eid in redundant_edges:
    cell = mx_root.find(f".//mxCell[@id='{eid}']")
    if cell is not None:
        mx_root.remove(cell)
        deleted_edges_count += 1
print(f"Deleted {deleted_edges_count} redundant heritage detail edges to clear layout jumble.")

# 2. Re-wire and fix other edges that were floating or disconnected
rewire_map = {
    'dfd_7116': ('dfd_7012', 'dfd_7047'), # Heritage Profile Entry: 9.0 body -> D15 label
    'dfd_7117': ('dfd_7047', 'dfd_7012'), # Profile Record: D15 label -> 9.0 body
    'dfd_7126': ('dfd_7015', 'dfd_7047'), # Profile Approval: 5.0 Admin Approval -> D15 label
    'dfd_7110': ('dfd_7003', 'dfd_7006'), # Profile Data: TOURIST -> 1.0 User Auth body
    'dfd_7111': ('dfd_7003', 'dfd_7009'), # Attraction Entry: TOURIST -> 2.0 Content Mgmt body
    'dfd_7112': ('dfd_7009', 'dfd_7038'), # Attraction Record: 2.0 Content Mgmt -> D2 Attraction_db
    'dfd_7114': ('dfd_7041', 'dfd_7019'), # Event Details: D3 Event_db -> 4.0 Content Discovery body
    'dfd_7128': ('dfd_7071', 'dfd_7022'), # Review Feed: D5 Review_db -> 8.0 Review Process body
    'dfd_edge_7516': ('dfd_7305', 'dfd_7417'), # Log Summary: 11.0 Visitor Log body -> D23 Visitor_Log_db
    'dfd_7083': ('dfd_7002', 'dfd_7009'), # Resident Data: ADMIN -> 2.0 Content Mgmt body
    'dfd_7085': ('dfd_7002', 'dfd_7012'), # Heritage Data: ADMIN -> 9.0 Heritage Mgmt
    'dfd_7086': ('dfd_7012', 'dfd_7002'), # Heritage Status: 9.0 Heritage -> ADMIN
    'dfd_7087': ('dfd_7002', 'dfd_7024'), # Review Content: ADMIN -> 8.0 Review Process body
    'dfd_7088': ('dfd_7015', 'dfd_7002'), # Approval Result: 5.0 Admin Approval -> ADMIN
    'dfd_7089': ('dfd_7002', 'dfd_7028'), # Reports Request: ADMIN -> 7.0 Analytics & Reporting body
    'dfd_7100': ('dfd_7006', 'dfd_7031'), # OAuth Login: 1.0 User Auth body -> Google OAuth
    'dfd_7102': ('dfd_7003', 'dfd_7018'), # Map View Request: TOURIST -> 3.0 Interactive Map Display body
    'dfd_7104': ('dfd_7003', 'dfd_7019'), # Search Attractions: TOURIST -> 4.0 Content Discovery body
    'dfd_7105': ('dfd_7019', 'dfd_7003'), # Search Results: 4.0 Content Discovery body -> TOURIST
    'dfd_7106': ('dfd_7003', 'dfd_7022')  # Submit Review: TOURIST -> 8.0 Review Process body
}

for edge_id, (src, tgt) in rewire_map.items():
    cell = mx_root.find(f".//mxCell[@id='{edge_id}']")
    if cell is not None:
        cell.attrib['source'] = src
        cell.attrib['target'] = tgt
        cell.attrib['edge'] = "1"
        print(f"Rewired edge {edge_id} ('{cell.attrib.get('value')}') strictly from {src} to {tgt}.")

# 3. Clean mxGeometry of all edges to snap them dynamically
# Specifically, we remove absolute sourcePoint, targetPoint, and intermediate points
# for ALL edges in the diagram to force them to snap cleanly to boxes
purged_absolute_points = 0
purged_control_arrays = 0

for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        geom = cell.find('mxGeometry')
        if geom is not None:
            # 1. Remove absolute sourcePoint
            source_pt = geom.find("mxPoint[@as='sourcePoint']")
            if source_pt is not None:
                geom.remove(source_pt)
                purged_absolute_points += 1
            
            # 2. Remove absolute targetPoint
            target_pt = geom.find("mxPoint[@as='targetPoint']")
            if target_pt is not None:
                geom.remove(target_pt)
                purged_absolute_points += 1
            
            # 3. Remove custom control point array
            points_node = geom.find('Array')
            if points_node is not None:
                geom.remove(points_node)
                purged_control_arrays += 1

print(f"Purged {purged_absolute_points} absolute coordinate float overrides from edges.")
print(f"Purged {purged_control_arrays} custom control point arrays from edges to force dynamic snapping.")

# Save output
tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("Line fix executed successfully on dfd-level-1-clean_v3.drawio!")
