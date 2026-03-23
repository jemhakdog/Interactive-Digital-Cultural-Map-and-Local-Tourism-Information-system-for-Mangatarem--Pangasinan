import xml.etree.ElementTree as ET
import sys

def update_flowchart(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Find the <root> element which contains all mxCells
    print("Finding root element...")
    mx_graph_model = root.find(".//mxGraphModel")
    if mx_graph_model is not None:
        graph_root = mx_graph_model.find(".//root")
    else:
        graph_root = root.find(".//root")
        
    if graph_root is None:
        print("Error: Could not find <root> element in XML")
        return

    # Layer 1 cell (usually id="1")
    layer_1 = graph_root.find(".//mxCell[@id='1']")
    if layer_1 is None:
        print("Warning: Could not find layer with id='1'. Creating one.")
        layer_1 = ET.SubElement(graph_root, 'mxCell', {'id': '1', 'parent': '0'})

    # IDs we manage
    managed_ids = ['manual_collect', 'manual_digitize', 'edge_manual_1', 'edge_manual_2', 'edge_manual_3']
    
    # 1. CLEANUP: Remove managed items from EVERYWHERE (root and nested inside layer 1)
    # Check root children
    for mid in managed_ids:
        # Check direct children of root
        found_in_root = graph_root.findall(f"./mxCell[@id='{mid}']")
        for f in found_in_root:
            print(f"Removing old {mid} from root")
            graph_root.remove(f)
            
        # Check nested children inside layer 1 (the bug I introduced)
        found_in_layer = layer_1.findall(f"./mxCell[@id='{mid}']")
        for f in found_in_layer:
            print(f"Removing old nested {mid} from layer 1")
            layer_1.remove(f)
    
    print("Adding new elements to root...")
    # 2. ADD NEW ITEMS to ROOT (not to layer_1)
    # Key change: Append to graph_root, but set parent='1'
    
    # 1. Manual Collection (Bottleneck)
    manual_collect = ET.SubElement(graph_root, 'mxCell', {
        'id': 'manual_collect',
        'value': 'Manual Field Surveys<br/>(Forms 01A-07)',
        'style': 'whiteSpace=wrap;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1',
        'vertex': '1',
        'parent': '1'
    })
    ET.SubElement(manual_collect, 'mxGeometry', {
        'x': '480', 'y': '930', 'width': '180', 'height': '60', 'as': 'geometry'
    })

    # 2. Manual Digitization (Bottleneck)
    manual_digitize = ET.SubElement(graph_root, 'mxCell', {
        'id': 'manual_digitize',
        'value': 'Manual Encoding<br/>(Word/Excel)',
        'style': 'whiteSpace=wrap;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1',
        'vertex': '1',
        'parent': '1'
    })
    ET.SubElement(manual_digitize, 'mxGeometry', {
        'x': '480', 'y': '1030', 'width': '180', 'height': '60', 'as': 'geometry'
    })

    # 3. Connection: Barangay Dashboard -> Manual Collect
    edge1 = ET.SubElement(graph_root, 'mxCell', {
        'id': 'edge_manual_1',
        'edge': '1',
        'parent': '1',
        'source': 'duccTRtAYDFomMVnRmlh-9',
        'target': 'manual_collect',
        'style': 'curved=1;startArrow=none;endArrow=block;exitX=1;exitY=0.5;entryX=0;entryY=0.5;rounded=0;'
    })
    ET.SubElement(edge1, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    # 4. Connection: Manual Collect -> Manual Digitize
    edge2 = ET.SubElement(graph_root, 'mxCell', {
        'id': 'edge_manual_2',
        'edge': '1',
        'parent': '1',
        'source': 'manual_collect',
        'target': 'manual_digitize',
        'style': 'curved=1;startArrow=none;endArrow=block;exitX=0.5;exitY=1;entryX=0.5;entryY=0;rounded=0;'
    })
    ET.SubElement(edge2, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    # 5. Connection: Manual Digitize -> Create New Attraction/Event
    edge3 = ET.SubElement(graph_root, 'mxCell', {
        'id': 'edge_manual_3',
        'edge': '1',
        'parent': '1',
        'source': 'manual_digitize',
        'target': 'duccTRtAYDFomMVnRmlh-10',
        'style': 'curved=1;startArrow=none;endArrow=block;exitX=0;exitY=0.5;entryX=1;entryY=0.5;rounded=0;'
    })
    ET.SubElement(edge3, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    # Remove specific edge as requested ("Click Login" from "Is User Logged In?")
    edge_click_login = graph_root.find(".//mxCell[@id='duccTRtAYDFomMVnRmlh-26']")
    if edge_click_login is not None:
        print("Removing 'Click Login' (duccTRtAYDFomMVnRmlh-26)")
        graph_root.remove(edge_click_login)

    # Remove "Role: Guest/User" (duccTRtAYDFomMVnRmlh-28) from "Check User Role"
    edge_guest_user = graph_root.find(".//mxCell[@id='duccTRtAYDFomMVnRmlh-28']")
    if edge_guest_user is not None:
        print("Removing 'Role: Guest/User' (duccTRtAYDFomMVnRmlh-28)")
        graph_root.remove(edge_guest_user)

    # Change "Check User Role" (duccTRtAYDFomMVnRmlh-5) to "Is Admin?"
    check_role = graph_root.find(".//mxCell[@id='duccTRtAYDFomMVnRmlh-5']")
    if check_role is not None:
        print("Updating 'Check User Role' to 'Is Admin?'")
        check_role.set('value', 'Is Admin?')

    # Update "Role: Admin" (duccTRtAYDFomMVnRmlh-30) to "Yes"
    edge_admin = graph_root.find(".//mxCell[@id='duccTRtAYDFomMVnRmlh-30']")
    if edge_admin is not None:
        print("Updating 'Role: Admin' to 'Yes'")
        edge_admin.set('value', 'Yes')
        
    # Update "Role: Barangay Rep" (duccTRtAYDFomMVnRmlh-29) to "No"
    # Note: This implies "Not Admin" -> "Barangay Rep" (simplified flow)
    edge_bgry = graph_root.find(".//mxCell[@id='duccTRtAYDFomMVnRmlh-29']")
    if edge_bgry is not None:
        print("Updating 'Role: Barangay Rep' to 'No'")
        edge_bgry.set('value', 'No')

    tree.write(file_path, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    import os
    target_file = 'docs/diagrams/flowchart.drawio'
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    
    if not os.path.exists(target_file):
        print(f"Error: File '{target_file}' not found.")
        sys.exit(1)
        
    print(f"Updating flowchart: {target_file}")
    update_flowchart(target_file)
    print("Update complete.")
