import xml.etree.ElementTree as ET
import os

# ─── Configuration ───
PAGE_WIDTH = 2400
PAGE_HEIGHT = 1600
COL_WIDTH = 500
GUTTER = 40
START_X = 80
START_Y = 100

# ─── Colors ───
COLOR_COL1 = "#E1D5E7"   # User: Purple
COLOR_COL2 = "#DAE8FC"   # Tourism: Blue
COLOR_COL3 = "#D5E8D4"   # Heritage: Green
COLOR_COL4 = "#FFE6CC"   # Interaction: Orange
COLOR_PROCESS = "#FFFFFF"
COLOR_STORE = "#F5F5F5"
COLOR_ENTITY = "#FFFFFF"

# ─── Layout Calculations ───
X_COL1 = START_X
X_COL2 = START_X + COL_WIDTH + GUTTER
X_COL3 = START_X + (COL_WIDTH + GUTTER) * 2
X_COL4 = START_X + (COL_WIDTH + GUTTER) * 3

# Center points for nodes within columns
CX_COL1 = X_COL1 + COL_WIDTH // 2
CX_COL2 = X_COL2 + COL_WIDTH // 2
CX_COL3 = X_COL3 + COL_WIDTH // 2
CX_COL4 = X_COL4 + COL_WIDTH // 2

def create_dfd():
    root = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(root, "diagram", name="Defense DFD")
    model = ET.SubElement(diagram, "mxGraphModel", dx="0", dy="0", grid="1", gridSize="10", 
                          guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", 
                          pageScale="1", pageWidth=str(PAGE_WIDTH), pageHeight=str(PAGE_HEIGHT), 
                          background="#FFFFFF")
    root_cell = ET.SubElement(model, "root")
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    # 1. Draw Columns (Swimlanes/Backgrounds)
    columns = [
        ("COL1", "1. User Entity (The Actor)", X_COL1, COLOR_COL1),
        ("COL2", "2. Tourism Content (The Public Face)", X_COL2, COLOR_COL2),
        ("COL3", "3. Heritage Framework (The Cultural Core)", X_COL3, COLOR_COL3),
        ("COL4", "4. Interaction & Engagement (The User Voice)", X_COL4, COLOR_COL4)
    ]
    
    for cid, label, x, color in columns:
        col = ET.SubElement(root_cell, "mxCell", id=cid, value=label, 
                            style=f"rounded=0;whiteSpace=wrap;html=1;fillColor={color};strokeColor=none;align=center;verticalAlign=top;fontStyle=1;fontSize=14;opacity=50;", 
                            parent="1", vertex="1")
        ET.SubElement(col, "mxGeometry", x=str(x), y="50", width=str(COL_WIDTH), height=str(PAGE_HEIGHT-100)).set("as", "geometry")

    # 2. Draw Nodes
    nodes = []

    # -- Col 1: User --
    nodes.append(("E_USER", "User Entity", "entity", CX_COL1, 200, 140, 60))
    nodes.append(("P_AUTH", "1.0 Auth & Access", "process", CX_COL1, 350, 160, 80))
    nodes.append(("D_USER", "User DB", "store", CX_COL1, 500, 140, 50))
    
    # -- Col 2: Tourism --
    nodes.append(("P_TOURISM", "2.0 Manage Tourism", "process", CX_COL2, 200, 160, 80))
    nodes.append(("D_ATTR", "Attraction DB", "store", CX_COL2, 350, 140, 50))
    nodes.append(("D_EVENT", "Event DB", "store", CX_COL2, 450, 140, 50))
    nodes.append(("D_BRGY", "Barangay DB", "store", CX_COL2, 550, 140, 50))

    # -- Col 3: Heritage --
    nodes.append(("P_HERITAGE", "3.0 Heritage Mgmt", "process", CX_COL3, 200, 160, 80))
    nodes.append(("D_PROFILE", "Heritage Profile", "store", CX_COL3, 350, 140, 50))
    nodes.append(("P_VERIFY", "3.1 Verify & Approve", "process", CX_COL3, 650, 160, 80))
    # Sub-stores
    nodes.append(("D_BUILT", "Built", "store", CX_COL3 - 100, 480, 90, 40))
    nodes.append(("D_NATURAL", "Natural", "store", CX_COL3 + 100, 480, 90, 40))
    nodes.append(("D_MOVABLE", "Movable", "store", CX_COL3 - 100, 550, 90, 40))
    nodes.append(("D_INTANGIBLE", "Intangible", "store", CX_COL3 + 100, 550, 90, 40))

    # -- Col 4: Interaction --
    nodes.append(("P_INTERACT", "4.0 User Interaction", "process", CX_COL4, 200, 160, 80))
    nodes.append(("D_REVIEW", "Review DB", "store", CX_COL4, 350, 140, 50))
    nodes.append(("D_FAVE", "Favorite DB", "store", CX_COL4, 450, 140, 50))
    nodes.append(("D_VIEWS", "PageView DB", "store", CX_COL4, 550, 140, 50))
    nodes.append(("P_ANALYTICS", "5.0 Analytics", "process", CX_COL4, 700, 160, 80))

    for nid, label, ntype, cx, cy, w, h in nodes:
        x = cx - w // 2
        y = cy - h // 2
        style = ""
        if ntype == "entity":
            style = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;"
        elif ntype == "process":
            style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;arcSize=20;"
        elif ntype == "store":
            style = "shape=partialRectangle;whiteSpace=wrap;html=1;left=0;right=0;fillColor=#F5F5F5;strokeColor=#000000;strokeWidth=1.5;"
        
        node = ET.SubElement(root_cell, "mxCell", id=nid, value=label, style=style, parent="1", vertex="1")
        ET.SubElement(node, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h)).set("as", "geometry")

    # 3. Draw Flows
    flows = [
        # Auth Loop
        ("E_USER", "P_AUTH"), ("P_AUTH", "D_USER"),
        # User -> Content
        ("E_USER", "P_TOURISM"), ("P_TOURISM", "D_ATTR"), ("P_TOURISM", "D_EVENT"), ("P_TOURISM", "D_BRGY"),
        # User -> Heritage
        ("E_USER", "P_HERITAGE"), ("P_HERITAGE", "D_PROFILE"),
        ("D_PROFILE", "D_BUILT"), ("D_PROFILE", "D_NATURAL"), ("D_PROFILE", "D_MOVABLE"), ("D_PROFILE", "D_INTANGIBLE"),
        # Verification
        ("P_HERITAGE", "P_VERIFY"), ("P_VERIFY", "D_PROFILE"),
        # User -> Interaction
        ("E_USER", "P_INTERACT"), ("P_INTERACT", "D_REVIEW"), ("P_INTERACT", "D_FAVE"), ("P_INTERACT", "D_VIEWS"),
        # Analytics
        ("D_REVIEW", "P_ANALYTICS"), ("D_VIEWS", "P_ANALYTICS")
    ]

    for src, tgt in flows:
        edge = ET.SubElement(root_cell, "mxCell", id=f"edge_{src}_{tgt}", value="", 
                             style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;exitX=0.5;exitY=1;strokeColor=#000000;strokeWidth=1.5;", 
                             parent="1", source=src, target=tgt, edge="1")
        ET.SubElement(edge, "mxGeometry", relative="1").set("as", "geometry")

    return root

if __name__ == "__main__":
    r = create_dfd()
    tree = ET.ElementTree(r)
    # Correct output path
    out_path = r"d:\porjects\Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan\docs\diagrams\defense_dfd.drawio"
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"Generated {out_path}")
