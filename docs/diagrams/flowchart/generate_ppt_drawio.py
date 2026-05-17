import xml.etree.ElementTree as ET
import os

# Configuration
PAGE_WIDTH = 1600
PAGE_HEIGHT = 1200

# Colors
COLOR_VISITOR = "#e0f7fa"
STROKE_VISITOR = "#006064"

COLOR_CONTRIB = "#f1f8e9"
STROKE_CONTRIB = "#33691e"

COLOR_ADMIN = "#fff3e0"
STROKE_ADMIN = "#e65100"

COLOR_DB = "#ede7f6"
STROKE_DB = "#4527a0"

COLOR_DECISION = "#fff9c4"
STROKE_DECISION = "#fbc02d"

# (id, label, type, cx, cy, w, h, color, stroke)
NODES = [
    # Visitor
    ("V1", "Access Web Portal", "process", 200, 100, 180, 60, COLOR_VISITOR, STROKE_VISITOR),
    ("V2", "Search & Filter Categories", "process", 200, 250, 180, 60, COLOR_VISITOR, STROKE_VISITOR),
    ("V3", "Explore Interactive Map", "process", 200, 400, 180, 60, COLOR_VISITOR, STROKE_VISITOR),
    ("V4", "View Attraction Details", "process", 200, 550, 180, 60, COLOR_VISITOR, STROKE_VISITOR),
    ("V5", "Leave Review / Navigate", "process", 200, 700, 180, 60, COLOR_VISITOR, STROKE_VISITOR),
    
    # Contributor
    ("C1", "Secure Login\n(Contributor)", "process", 600, 100, 180, 60, COLOR_CONTRIB, STROKE_CONTRIB),
    ("C2", "Access Barangay\nDashboard", "process", 600, 250, 180, 60, COLOR_CONTRIB, STROKE_CONTRIB),
    ("C3", "Digitally Fill Heritage\nForms 01-07", "process", 600, 400, 180, 60, COLOR_CONTRIB, STROKE_CONTRIB),
    ("C4", "Upload Photos & Videos", "process", 600, 550, 180, 60, COLOR_CONTRIB, STROKE_CONTRIB),
    ("C5", "Submit Asset for Review", "process", 600, 700, 180, 60, COLOR_CONTRIB, STROKE_CONTRIB),
    
    # Admin
    ("A1", "Secure Login\n(Admin)", "process", 1000, 100, 180, 60, COLOR_ADMIN, STROKE_ADMIN),
    ("A2", "Access Admin Dashboard", "process", 1000, 250, 180, 60, COLOR_ADMIN, STROKE_ADMIN),
    ("A3", "Review Pending\nSubmissions", "process", 1000, 400, 180, 60, COLOR_ADMIN, STROKE_ADMIN),
    ("A4", "Meets Standards?", "decision", 1000, 550, 180, 80, COLOR_DECISION, STROKE_DECISION),
    ("A5", "Approve & Publish", "process", 1000, 700, 180, 60, COLOR_ADMIN, STROKE_ADMIN),
    ("A6", "Reject &\nSend Feedback", "process", 1250, 550, 180, 60, COLOR_ADMIN, STROKE_ADMIN),
    
    # Database
    ("DB1", "Supabase PostgreSQL &\nMapbox Vector Tiles", "db", 600, 900, 220, 80, COLOR_DB, STROKE_DB)
]

# (src, tgt, label)
EDGES = [
    # Visitor
    ("V1", "V2", ""),
    ("V2", "V3", ""),
    ("V3", "V4", ""),
    ("V4", "V5", ""),
    
    # Contributor
    ("C1", "C2", ""),
    ("C2", "C3", ""),
    ("C3", "C4", ""),
    ("C4", "C5", ""),
    
    # Admin
    ("A1", "A2", ""),
    ("A2", "A3", ""),
    ("A3", "A4", ""),
    ("A4", "A5", "Yes"),
    ("A4", "A6", "No"),
    
    # Cross-Lane
    ("A6", "C2", "Return to Dash"),
    ("C5", "A3", "Pending"),
    ("A5", "DB1", "Saves to"),
    ("DB1", "V3", "Feeds live data to"),
    ("V5", "DB1", "Saves Review"),
    ("C5", "DB1", "Saves Pending")
]

def create_flowchart():
    root = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(root, "diagram", name="Proposed System Flowchart")
    graph = ET.SubElement(diagram, "mxGraphModel", dx="0", dy="0", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(PAGE_WIDTH), pageHeight=str(PAGE_HEIGHT), background="#FFFFFF")
    root_cell = ET.SubElement(graph, "root")
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    # Draw Nodes
    for nid, label, ntype, cx, cy, w, h, bg_color, stroke_color in NODES:
        x = cx - w // 2
        y = cy - h // 2
        style = ""
        if ntype == "process":
            style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={bg_color};strokeColor={stroke_color};strokeWidth=2;arcSize=10;fontColor=#111111;"
        elif ntype == "decision":
            style = f"rhombus;whiteSpace=wrap;html=1;fillColor={bg_color};strokeColor={stroke_color};strokeWidth=2;fontColor=#111111;"
        elif ntype == "db":
            style = f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor={bg_color};strokeColor={stroke_color};strokeWidth=2;fontColor=#111111;"

        node = ET.SubElement(root_cell, "mxCell", id=nid, value=label, style=style, parent="1", vertex="1")
        ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h)).set("as", "geometry")

    # Draw Edges
    for src, tgt, label in EDGES:
        edge_style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#111111;strokeWidth=2;fontColor=#111111;labelBackgroundColor=none;"
        
        # Apply specific routing ports to avoid visual intersection/overlaps
        if src == "A5" and tgt == "DB1":
            edge_style += "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
        elif src == "V5" and tgt == "DB1":
            edge_style += "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
        elif src == "C5" and tgt == "DB1":
            edge_style += "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
        elif src == "C5" and tgt == "A3":
            edge_style += "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
        elif src == "A6" and tgt == "C2":
            edge_style += "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
        elif src == "DB1" and tgt == "V3":
            edge_style += "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
            
        edge = ET.SubElement(root_cell, "mxCell", id=f"edge_{src}_{tgt}", value=label, 
                             style=edge_style, 
                             parent="1", source=src, target=tgt, edge="1")
        ET.SubElement(edge, "mxGeometry", relative="1").set("as", "geometry")

    # Add Lane Titles
    ET.SubElement(root_cell, "mxCell", id="TITLE_V", value="<b>Public Visitor Workflow</b>", style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontColor=#111111;", parent="1", vertex="1").append(ET.Element("mxGeometry", x="100", y="40", width="200", height="30", **{"as": "geometry"}))
    ET.SubElement(root_cell, "mxCell", id="TITLE_C", value="<b>Barangay Representative Workflow</b>", style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontColor=#111111;", parent="1", vertex="1").append(ET.Element("mxGeometry", x="500", y="40", width="200", height="30", **{"as": "geometry"}))
    ET.SubElement(root_cell, "mxCell", id="TITLE_A", value="<b>Tourism Office Admin Workflow</b>", style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontColor=#111111;", parent="1", vertex="1").append(ET.Element("mxGeometry", x="900", y="40", width="200", height="30", **{"as": "geometry"}))

    return root

def main():
    root = create_flowchart()
    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    output_path = r"d:\porjects\capstone_system\docs\diagrams\flowchart\proposed_system_flowchart_ppt.drawio"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    main()
