"""
Generate a System Flowchart for the ERD Defense Script.
Flow: Left to Right (Columns 1 -> 4)
"""

import xml.etree.ElementTree as ET
import os

# ─── Configuration ───
PAGE_WIDTH = 2000
PAGE_HEIGHT = 1200
COL_WIDTH = 400
GUTTER = 50
START_X = 100
START_Y = 100

# ─── Colors ───
COLOR_START = "#D5E8D4"  # Green
COLOR_PROCESS = "#FFFFFF"
COLOR_DECISION = "#FFE6CC" # Orange
COLOR_END = "#F8CECC"    # Red

# ─── Nodes ───
# (id, label, type, x, y, w, h)
NODES = [
    # Col 1: Auth
    ("START", "Start", "start", START_X + 200, 100, 80, 40),
    ("LOGIN", "Login / Register", "process", START_X + 200, 200, 140, 60),
    ("DEC_ROLE", "User Role?", "decision", START_X + 200, 350, 120, 80),

    # Col 2: Tourist Path
    ("VIEW_MAP", "View Interactive Map", "process", START_X + COL_WIDTH + 200, 200, 160, 60),
    ("SEARCH_ATTR", "Search Attractions", "process", START_X + COL_WIDTH + 200, 350, 160, 60),
    
    # Col 3: Contributor/Admin Path
    ("SUBMIT_HERITAGE", "Submit Heritage\nProfile", "process", START_X + COL_WIDTH * 2 + 200, 350, 160, 60),
    ("VERIFY_DATA", "Verify & Approve", "process", START_X + COL_WIDTH * 2 + 200, 500, 160, 60),

    # Col 4: Participation
    ("T_INTERACT", "Rate / Comment /\nAdd to Favorites", "process", START_X + COL_WIDTH * 3 + 200, 275, 160, 60),
    ("END_TOURIST", "End (Tourist)", "end", START_X + COL_WIDTH * 3 + 200, 400, 100, 40),
    
    ("END_CONTRIB", "End (Contributor)", "end", START_X + COL_WIDTH * 3 + 200, 500, 120, 40),
]

# ─── Edges ───
# (src, tgt, label)
EDGES = [
    ("START", "LOGIN", ""),
    ("LOGIN", "DEC_ROLE", ""),
    
    # Tourist Flow
    ("DEC_ROLE", "VIEW_MAP", "Tourist"),
    ("DEC_ROLE", "SEARCH_ATTR", "Tourist"), # Alternative path
    ("VIEW_MAP", "T_INTERACT", ""),
    ("SEARCH_ATTR", "T_INTERACT", ""),
    ("T_INTERACT", "END_TOURIST", ""),

    # Contributor Flow
    ("DEC_ROLE", "SUBMIT_HERITAGE", "Contributor"),
    ("SUBMIT_HERITAGE", "VERIFY_DATA", "Admin Review"),
    ("VERIFY_DATA", "END_CONTRIB", "Published"),
]

def create_flowchart():
    root = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(root, "diagram", name="Defense Flowchart")
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

        node = ET.SubElement(root_cell, "mxCell", id=nid, value=label, style=style, parent="1", vertex="1")
        ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h)).set("as", "geometry")

    # Draw Edges
    for src, tgt, label in EDGES:
        edge = ET.SubElement(root_cell, "mxCell", id=f"edge_{src}_{tgt}", value=label, 
                             style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;", 
                             parent="1", source=src, target=tgt, edge="1")
        ET.SubElement(edge, "mxGeometry", relative="1").set("as", "geometry")

    return root

def main():
    root = create_flowchart()
    xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
    output_path = r"d:\porjects\Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan\docs\diagrams\defense_flowchart.drawio"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    main()
