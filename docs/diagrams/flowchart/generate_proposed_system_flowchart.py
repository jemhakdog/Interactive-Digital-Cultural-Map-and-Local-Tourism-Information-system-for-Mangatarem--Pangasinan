import xml.etree.ElementTree as ET
import os

# Configuration
PAGE_WIDTH = 2000
PAGE_HEIGHT = 1500
COL_WIDTH = 300
ROW_HEIGHT = 150
START_X = 100
START_Y = 100

# Colors
COLOR_START = "#D5E8D4"  # Green
COLOR_PROCESS = "#FFFFFF" # White
COLOR_DECISION = "#FFE6CC" # Orange
COLOR_END = "#F8CECC"    # Red
COLOR_DB = "#DAE8FC"     # Blue

# (id, label, type, cx, cy, w, h)
NODES = [
    # Start
    ("START", "Start", "start", 400, 100, 80, 40),
    ("ACCESS_SYS", "Access GoMangatarem\nPortal", "process", 400, 200, 160, 60),
    ("LOGIN", "Login / Register", "process", 400, 300, 160, 60),
    
    ("DEC_ROLE", "User Role?", "decision", 400, 450, 120, 80),
    
    # Paths
    # Tourist (Left)
    ("T_DASH", "Tourist Dashboard", "process", 150, 550, 160, 60),
    ("T_MAP", "Explore Interactive\nCultural Map", "process", 50, 650, 160, 60),
    ("T_SEARCH", "Search Attractions\n& Heritage", "process", 250, 650, 160, 60),
    ("T_INTERACT", "Leave Reviews,\nRatings & Favorites", "process", 150, 750, 160, 60),
    
    # Business Owner (Mid-Left)
    ("B_DASH", "Business Dashboard", "process", 400, 550, 160, 60),
    ("B_MANAGE", "Manage Establishments\n(Rooms/Menus)", "process", 400, 650, 160, 60),
    ("B_UPDATE", "Update Availability\n& Pricing", "process", 400, 750, 160, 60),

    # Contributor (Mid-Right)
    ("C_DASH", "Contributor/Barangay\nDashboard", "process", 650, 550, 160, 60),
    ("C_SUBMIT", "Submit Cultural\nHeritage Profiles", "process", 650, 650, 160, 60),
    ("C_EVENTS", "Manage Local\nEvents", "process", 650, 750, 160, 60),
    
    # Admin (Right)
    ("A_DASH", "Admin Dashboard", "process", 900, 550, 160, 60),
    ("A_VERIFY", "Verify & Approve\nSubmissions", "process", 900, 650, 160, 60),
    ("A_USERS", "Manage Users &\nRoles", "process", 900, 750, 160, 60),
    ("A_ANALYTICS", "View System\nAnalytics", "process", 900, 850, 160, 60),

    # System/DB Actions
    ("SYS_DB", "System Database\n(Supabase / PostGIS)", "db", 525, 950, 160, 80),
    
    # End
    ("LOGOUT", "Logout", "process", 400, 1100, 120, 60),
    ("END", "End", "end", 400, 1200, 80, 40)
]

# (src, tgt, label)
EDGES = [
    ("START", "ACCESS_SYS", ""),
    ("ACCESS_SYS", "LOGIN", ""),
    ("LOGIN", "DEC_ROLE", ""),
    
    # Tourist
    ("DEC_ROLE", "T_DASH", "Tourist"),
    ("T_DASH", "T_MAP", ""),
    ("T_DASH", "T_SEARCH", ""),
    ("T_MAP", "T_INTERACT", ""),
    ("T_SEARCH", "T_INTERACT", ""),
    ("T_INTERACT", "SYS_DB", "Save Data"),
    ("T_INTERACT", "LOGOUT", ""),
    
    # Business
    ("DEC_ROLE", "B_DASH", "Business Owner"),
    ("B_DASH", "B_MANAGE", ""),
    ("B_MANAGE", "B_UPDATE", ""),
    ("B_UPDATE", "SYS_DB", "Save Data"),
    ("B_UPDATE", "LOGOUT", ""),
    
    # Contributor
    ("DEC_ROLE", "C_DASH", "Contributor"),
    ("C_DASH", "C_SUBMIT", ""),
    ("C_DASH", "C_EVENTS", ""),
    ("C_SUBMIT", "SYS_DB", "Pending Data"),
    ("C_EVENTS", "SYS_DB", "Save Data"),
    ("C_SUBMIT", "LOGOUT", ""),
    ("C_EVENTS", "LOGOUT", ""),
    
    # Admin
    ("DEC_ROLE", "A_DASH", "Admin"),
    ("A_DASH", "A_VERIFY", ""),
    ("A_DASH", "A_USERS", ""),
    ("A_DASH", "A_ANALYTICS", ""),
    ("A_VERIFY", "SYS_DB", "Update Status"),
    ("A_USERS", "SYS_DB", "Update Data"),
    ("SYS_DB", "A_ANALYTICS", "Fetch Data"),
    ("A_VERIFY", "LOGOUT", ""),
    ("A_USERS", "LOGOUT", ""),
    ("A_ANALYTICS", "LOGOUT", ""),
    
    ("LOGOUT", "END", "")
]

def create_flowchart():
    root = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(root, "diagram", name="Proposed System Flowchart")
    graph = ET.SubElement(diagram, "mxGraphModel", dx="0", dy="0", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(PAGE_WIDTH), pageHeight=str(PAGE_HEIGHT), background="#FFFFFF")
    root_cell = ET.SubElement(graph, "root")
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    # Draw Nodes
    for nid, label, ntype, cx, cy, w, h in NODES:
        x = cx - w // 2
        y = cy - h // 2
        style = ""
        if ntype == "start":
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor={COLOR_START};strokeColor=#82B366;"
        elif ntype == "end":
            style = f"ellipse;whiteSpace=wrap;html=1;fillColor={COLOR_END};strokeColor=#B85450;"
        elif ntype == "process":
            style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={COLOR_PROCESS};strokeColor=#000000;arcSize=10;"
        elif ntype == "decision":
            style = f"rhombus;whiteSpace=wrap;html=1;fillColor={COLOR_DECISION};strokeColor=#D6B656;"
        elif ntype == "db":
            style = f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor={COLOR_DB};strokeColor=#6c8ebf;"

        node = ET.SubElement(root_cell, "mxCell", id=nid, value=label, style=style, parent="1", vertex="1")
        ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h)).set("as", "geometry")

    # Draw Edges
    for src, tgt, label in EDGES:
        # Avoid edge overlap where possible
        edge_style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;"
        
        edge = ET.SubElement(root_cell, "mxCell", id=f"edge_{src}_{tgt}", value=label, 
                             style=edge_style, 
                             parent="1", source=src, target=tgt, edge="1")
        ET.SubElement(edge, "mxGeometry", relative="1").set("as", "geometry")

    return root

def main():
    root = create_flowchart()
    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    output_path = r"d:\porjects\capstone_system\docs\diagrams\flowchart\proposed_system_flowchart.drawio"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    main()
