"""
Generate a professional DFD Level 1 drawio XML with a Hub-and-Spoke layout.
Matches the "Gaisano" reference style:
- Left Entity: System Administrator
- Right Entity: Tourist / Public User
- Center: Main System Hub
- Columns 2 & 4: Processes & Data Stores
"""

import xml.etree.ElementTree as ET

# ─── Configuration ───
HUB_W, HUB_H = 340, 220
PROCESS_W, PROCESS_H = 180, 100
STORE_W, STORE_H = 160, 45
ENTITY_W, ENTITY_H = 100, 500  # Vertical sidebars
FONT_SIZE = 12

# ─── Colors ───
COLOR_HUB = "#FFFFFF"
COLOR_ENTITY = "#BDD7EE"
COLOR_PROCESS = "#BDD7EE"
COLOR_STORE = "#BDD7EE"

# ─── Layout Positions ───
CENTER_X, CENTER_Y = 1000, 550
HUB_X = CENTER_X - HUB_W // 2
HUB_Y = CENTER_Y - HUB_H // 2

LEFT_ENTITY_X = 50
RIGHT_ENTITY_X = 1850

COL2_X = 450   # Inside Processes (Left stack)
COL4_X = 1450  # Engagement Processes (Right stack)

# ─── Element Definitions ───
# format: (type, id_val, label, x, y)
ELEMENTS = {
    # Hub
    "HUB": ("hub", "", "Interactive Digital Cultural Map &\nTourism Information System", HUB_X, HUB_Y),

    # Sidebar Entities
    "E_ADMIN":   ("sidebar", "", "ADMIN", LEFT_ENTITY_X, CENTER_Y - 250),
    "E_TOURIST": ("sidebar", "", "TOURIST", RIGHT_ENTITY_X, CENTER_Y - 250),

    # Process Stack Left (1.0, 2.0, 5.0)
    "P1": ("process", "1.0", "User\nAuthentication", COL2_X, 100),
    "P2": ("process", "2.0", "Content\nManagement", COL2_X, 400),
    "P5": ("process", "5.0", "Admin\nApproval", COL2_X, 700),

    # Process Stack Right (3.0, 4.0, 8.0, 6.0, 7.0)
    "P3": ("process", "3.0", "Interactive\nMap Display", COL4_X, 100),
    "P4": ("process", "4.0", "Content\nDiscovery", COL4_X, 300),
    "P8": ("process", "8.0", "Review &\nFeedback", COL4_X, 500),
    "P6": ("process", "6.0", "Favorite\nManagement", COL4_X, 700),
    "P7": ("process", "7.0", "Analytics &\nReporting", COL4_X, 900),

    # External APIs (Top)
    "E_GOOGLE": ("entity", "", "Google OAuth", COL2_X + 30, 20),
    "E_MAPBOX": ("entity", "", "Mapbox API", COL4_X + 30, 20),

    # Data Stores
    # Positioned between processes and hub or directly below processes
    "D1": ("store", "1", "User_db", COL2_X + 10, 220),       # Under P1
    "D2": ("store", "2", "Attraction_db", COL2_X + 10, 520), # Under P2
    "D3": ("store", "3", "Event_db", 720, 350),             # Between COL2 and HUB
    "D5": ("store", "4", "Barangay_db", 720, 750),          # Between COL2 and HUB
    "D7": ("store", "5", "Review_db", COL4_X + 10, 620),    # Under P8
    "D8": ("store", "6", "Favorite_db", COL4_X + 10, 820),  # Under P6
    "D6": ("store", "7", "PageView_db", 1200, 400),         # Between HUB and COL4
    "D9": ("store", "8", "Reports_db", 1200, 950),          # Between HUB and COL4
}

# ─── Data Flows ───
FLOWS = [
    # ADMIN flows
    ("E_ADMIN", "P1", "Admin Credentials"),
    ("P1", "E_ADMIN", "Auth Status"),
    ("E_ADMIN", "P2", "Resident Data"), # Mapping Content as Resident
    ("P2", "E_ADMIN", "Status Update"),
    ("E_ADMIN", "P5", "Review Content"),
    ("P5", "E_ADMIN", "Approval Result"),
    ("E_ADMIN", "P7", "Reports Request"),
    ("P7", "E_ADMIN", "Report Data"),

    # HUB connections (Spokes)
    ("P1", "HUB", "User Accounts"),
    ("P2", "HUB", "Mangatarem Tourism Record"),
    ("P5", "HUB", "Approval Log"),
    ("HUB", "P3", "Map Content"),
    ("HUB", "P4", "Discovery Data"),
    ("HUB", "P8", "User Feedback"),
    ("HUB", "P6", "Engagement Logs"),
    ("HUB", "P7", "System Metrics"),

    # External APIs
    ("E_GOOGLE", "P1", "OAuth Login"),
    ("E_MAPBOX", "P3", "Tile Data"),

    # TOURIST flows
    ("E_TOURIST", "P3", "Map View Request"),
    ("P3", "E_TOURIST", "Interactive Map"),
    ("E_TOURIST", "P4", "Search Attractions"),
    ("P4", "E_TOURIST", "Search Results"),
    ("E_TOURIST", "P8", "Submit Review"),
    ("P8", "E_TOURIST", "Review Confirmation"),
    ("E_TOURIST", "P6", "Toggle Favorite"),

    # Data Store Connections (Process <-> Store)
    ("P1", "D1", "User Credentials"),
    ("D1", "P1", "Profile Data"),
    ("P2", "D2", "Attraction Entry"),
    ("D2", "P2", "Attraction Record"),
    ("P2", "D3", "Event Content"),
    ("D3", "P2", "Event Details"),
    ("P2", "D5", "Barangay Data"),
    ("P5", "D2", "Approval Status"), # Write approval back to Attraction_db
    ("P8", "D7", "New Review"),
    ("D7", "P8", "Review Feed"),
    ("P6", "D8", "Save Favorite"),
    ("D8", "P6", "Favorite List"),
    ("P7", "D6", "Activity Logs"),
    ("P7", "D9", "Report Archive"),
    ("D9", "P7", "Historical Data"),
]

# ─── ID Counter ───
_id_counter = 7000
def next_id():
    global _id_counter
    _id_counter += 1
    return f"dfd_{_id_counter}"

def build_xml():
    root = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(root, "diagram", name="Hub-and-Spoke DFD", id="DFD_HUB")
    graph = ET.SubElement(diagram, "mxGraphModel", dx="2000", dy="1500", grid="1", gridSize="10",
                          page="1", pageWidth="2400", pageHeight="1800", background="#F5F9F5")
    root_cell = ET.SubElement(graph, "root")
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    node_ids = {}

    for name, data in ELEMENTS.items():
        etype = data[0]
        id_val = data[1]
        label = data[2]
        x = data[3]
        y = data[4]
        
        nid = next_id()
        node_ids[name] = nid

        if etype == "hub":
            style = "rounded=0;whiteSpace=wrap;html=1;strokeWidth=3;fontSize=16;fontStyle=1;align=center;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;"
            node = ET.SubElement(root_cell, "mxCell", id=nid, value=label, style=style, parent="1", vertex="1")
            ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(HUB_W), height=str(HUB_H)).set("as", "geometry")

        elif etype == "sidebar":
            style = f"rounded=0;whiteSpace=wrap;html=1;fillColor={COLOR_ENTITY};strokeColor=#000000;fontStyle=1;fontColor=#000000;fontSize=14;horizontal=0;strokeWidth=2;"
            node = ET.SubElement(root_cell, "mxCell", id=nid, value=label, style=style, parent="1", vertex="1")
            ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(ENTITY_W), height=str(ENTITY_H)).set("as", "geometry")

        elif etype == "process":
            # Main container (invisible)
            container = ET.SubElement(root_cell, "mxCell", id=nid, value="", 
                                      style="group;container=1;collapsible=0;pointerEvents=0;", parent="1", vertex="1")
            ET.SubElement(container, "mxGeometry", x=str(x), y=str(y), width=str(PROCESS_W), height=str(PROCESS_H)).set("as", "geometry")
            
            # Header Bar
            header = ET.SubElement(root_cell, "mxCell", id=next_id(), value=id_val,
                                   style=f"rounded=0;whiteSpace=wrap;html=1;fillColor={COLOR_PROCESS};strokeColor=#000000;fontStyle=1;fontColor=#000000;align=center;verticalAlign=middle;strokeWidth=1.5;",
                                   parent=nid, vertex="1")
            ET.SubElement(header, "mxGeometry", width=str(PROCESS_W), height="30").set("as", "geometry")
            
            # Body Box
            body = ET.SubElement(root_cell, "mxCell", id=next_id(), value=label,
                                 style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;align=center;verticalAlign=middle;fontSize=11;strokeWidth=1.5;",
                                 parent=nid, vertex="1")
            ET.SubElement(body, "mxGeometry", y="30", width=str(PROCESS_W), height=str(PROCESS_H-30)).set("as", "geometry")

        elif etype == "store":
            # Data store group
            container = ET.SubElement(root_cell, "mxCell", id=nid, value="", style="group;", parent="1", vertex="1")
            ET.SubElement(container, "mxGeometry", x=str(x), y=str(y), width=str(STORE_W), height=str(STORE_H)).set("as", "geometry")
            
            # Sidebar indicator
            sidebar = ET.SubElement(root_cell, "mxCell", id=next_id(), value=id_val,
                                    style=f"rounded=0;whiteSpace=wrap;html=1;fillColor={COLOR_STORE};strokeColor=#000000;fontStyle=1;fontColor=#000000;align=center;strokeWidth=1.5;",
                                    parent=nid, vertex="1")
            ET.SubElement(sidebar, "mxGeometry", width="30", height=str(STORE_H)).set("as", "geometry")
            
            # Label box
            label_box = ET.SubElement(root_cell, "mxCell", id=next_id(), value=label,
                                      style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;align=center;fontSize=10;strokeWidth=1.5;",
                                      parent=nid, vertex="1")
            ET.SubElement(label_box, "mxGeometry", x="30", width=str(STORE_W-30), height=str(STORE_H)).set("as", "geometry")

        elif etype == "entity":
            style = f"rounded=0;whiteSpace=wrap;html=1;fillColor={COLOR_ENTITY};strokeColor=#000000;fontStyle=1;fontColor=#000000;fontSize=11;strokeWidth=1.5;"
            node = ET.SubElement(root_cell, "mxCell", id=nid, value=label, style=style, parent="1", vertex="1")
            ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width="120", height="40").set("as", "geometry")

    # ─── Flows ───
    hub_spoke_counts = {"left": 0, "right": 0}
    for src, tgt, label in FLOWS:
        fid = next_id()
        src_id = node_ids[src]
        tgt_id = node_ids[tgt]
        
        style = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=1.2;fontColor=#000000;fontSize=10;labelBackgroundColor=#F5F9F5;endArrow=classic;"
        
        # Smart routing offsets to avoid line overlap
        if src == "HUB" or tgt == "HUB":
            if src == "HUB":
                side = "right" if ELEMENTS[tgt][3] > CENTER_X else "left"
                style += f"exitX={'1' if side=='right' else '0'};exitY={0.2 + hub_spoke_counts[side]*0.15};"
                style += f"entryX={'0' if side=='right' else '1'};entryY=0.5;"
                hub_spoke_counts[side] += 1
            else: # tgt is HUB
                side = "right" if ELEMENTS[src][3] > CENTER_X else "left"
                style += f"exitX={'0' if side=='right' else '1'};exitY=0.5;"
                style += f"entryX={'1' if side=='right' else '0'};entryY={0.2 + hub_spoke_counts[side]*0.15};"
                hub_spoke_counts[side] += 1
        else:
            # Side-to-side logic
            src_x = ELEMENTS[src][3]
            tgt_x = ELEMENTS[tgt][3]
            if src_x < tgt_x: # Forward
                style += "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
            elif src_x > tgt_x: # Backward
                style += "exitX=0;exitY=0.5;entryX=1;entryY=0.5;"

        edge = ET.SubElement(root_cell, "mxCell", id=fid, value=label, style=style, parent="1", source=src_id, target=tgt_id, edge="1")
        ET.SubElement(edge, "mxGeometry", relative="1").set("as", "geometry")

    return root

def main():
    root = build_xml()
    # Fix the 'as' attribute issue by manual string replacement
    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    xml_str = xml_str.replace(' as_="geometry"', ' as="geometry"')
    
    output_path = "docs/diagrams/dfd-level-1-clean.drawio"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(xml_str)
    
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    main()
