import xml.etree.ElementTree as ET
import os

def generate_v2():
    v1_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v1.drawio"
    v2_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v2.drawio"
    
    if not os.path.exists(v1_path):
        print(f"Error: {v1_path} does not exist!")
        return
        
    print(f"Reading {v1_path}...")
    tree = ET.parse(v1_path)
    root = tree.getroot()
    
    # Locate the mxGraphModel's root cell container
    root_cell = None
    for element in root.iter('root'):
        root_cell = element
        break
        
    if root_cell is None:
        print("Error: Could not find <root> cell element in Draw.io file!")
        return

    # Styling constants exactly matching ERD v1 styles
    TABLE_STYLE = "shape=table;startSize=25;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=1;fontStyle=1;align=center;resizeLast=1;fontSize=18;"
    ROW_STYLE = "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;right=0;bottom=0;"
    CELL_KEY_STYLE = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=2;overflow=hidden;fontSize=16;fontStyle=5;"
    CELL_VAL_STYLE = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=2;overflow=hidden;fontSize=16;"
    
    # Simple straight/orthogonal connector style
    EDGE_STYLE = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;endArrow=classic;html=1;fontSize=14;"

    new_tables = [
        # Column 1 (x = -550): User-related helpers (width 560, matching USER)
        {
            "id": "erd_table_2000",
            "name": "PASSWORD_RESET_TOKEN",
            "x": -550, "y": 1150, "w": 560, "col_w": [50, 200, 100, 210],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK)", "user_id", "int", "→ USER.id"),
                ("", "token", "string", "not null"),
                ("", "expires_at", "datetime", "not null"),
                ("", "used", "bool", "default=False"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        {
            "id": "erd_table_2001",
            "name": "NEWSLETTER_SUBSCRIBER",
            "x": -550, "y": 1450, "w": 560, "col_w": [50, 200, 100, 210],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("UK", "email", "string", "not null"),
                ("", "is_active", "bool", "default=True"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        {
            "id": "erd_table_2002",
            "name": "DATABASE_AUDIT_LOG",
            "x": -550, "y": 1680, "w": 560, "col_w": [50, 200, 100, 210],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK)", "user_id", "int", "→ USER.id"),
                ("", "action", "string", "not null"),
                ("", "table_name", "string", "not null"),
                ("", "record_id", "int", "nullable"),
                ("", "ip_address", "string", "nullable"),
                ("", "user_agent", "string", "nullable"),
                ("", "query_summary", "string", "nullable"),
                ("", "status", "string", "default='success'"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        # Column 2 (x = 40): Business/Establishment portal suite (width 500, perfectly fitting margin)
        {
            "id": "erd_table_2003",
            "name": "ESTABLISHMENT",
            "x": 40, "y": 810, "w": 500, "col_w": [50, 180, 90, 180],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK1)", "owner_id", "int", "→ USER.id"),
                ("UK", "name", "string", "not null"),
                ("", "type", "string", "not null"),
                ("", "description", "text", "nullable"),
                ("", "address", "string", "nullable"),
                ("", "latitude", "float", "not null"),
                ("", "longitude", "float", "not null"),
                ("(FK2)", "barangay_id", "int", "→ BARANGAY_INFO.id"),
                ("", "contact_number", "string", "nullable"),
                ("", "email", "string", "nullable"),
                ("", "website", "string", "nullable"),
                ("", "operating_hours", "json", "nullable"),
                ("", "price_range", "string", "nullable"),
                ("", "amenities", "json", "nullable"),
                ("", "cover_image_url", "string", "nullable"),
                ("", "logo_url", "string", "nullable"),
                ("", "status", "string", "default='pending'"),
                ("", "is_featured", "bool", "default=False"),
                ("", "rating_avg", "float", "default=0"),
                ("", "review_count", "int", "default=0"),
                ("", "created_at", "datetime", "default=now"),
                ("", "geom", "geometry", "Point, 4326"),
            ]
        },
        {
            "id": "erd_table_2004",
            "name": "ESTABLISHMENT_ROOM",
            "x": 40, "y": 1690, "w": 500, "col_w": [50, 180, 90, 180],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK)", "establishment_id", "int", "→ ESTABLISHMENT.id"),
                ("UK", "name", "string", "not null"),
                ("", "description", "text", "nullable"),
                ("", "price_per_night", "float", "nullable"),
                ("", "capacity", "int", "default=2"),
                ("", "amenities", "json", "nullable"),
                ("", "image_urls", "json", "nullable"),
                ("", "is_available", "bool", "default=True"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        {
            "id": "erd_table_2005",
            "name": "ESTABLISHMENT_MENU_ITEM",
            "x": 40, "y": 2130, "w": 500, "col_w": [50, 180, 90, 180],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK)", "establishment_id", "int", "→ ESTABLISHMENT.id"),
                ("UK", "name", "string", "not null"),
                ("", "description", "text", "nullable"),
                ("", "price", "float", "nullable"),
                ("", "category", "string", "nullable"),
                ("", "image_url", "string", "nullable"),
                ("", "is_available", "bool", "default=True"),
                ("", "is_bestseller", "bool", "default=False"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        {
            "id": "erd_table_2006",
            "name": "ESTABLISHMENT_REVIEW",
            "x": 40, "y": 2570, "w": 500, "col_w": [50, 180, 90, 180],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK1)", "user_id", "int", "→ USER.id"),
                ("(FK2)", "establishment_id", "int", "→ ESTABLISHMENT.id"),
                ("", "rating", "int", "not null"),
                ("", "comment", "text", "nullable"),
                ("", "status", "string", "default='pending'"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        {
            "id": "erd_table_2007",
            "name": "USER_FAVORITE_ESTABLISHMENT",
            "x": 40, "y": 2900, "w": 500, "col_w": [50, 180, 90, 180],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK1)", "user_id", "int", "→ USER.id"),
                ("(FK2)", "establishment_id", "int", "→ ESTABLISHMENT.id"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        {
            "id": "erd_table_2008",
            "name": "VISITOR_LOG",
            "x": 40, "y": 3120, "w": 500, "col_w": [50, 180, 90, 180],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("", "target_type", "string", "not null"),
                ("", "target_id", "int", "not null"),
                ("", "visitor_count", "int", "default=1"),
                ("", "visitor_name", "string", "nullable"),
                ("", "visitor_age", "int", "nullable"),
                ("", "visitor_address", "string", "nullable"),
                ("", "is_system_user", "bool", "default=False"),
                ("", "visit_date", "date", "default=today"),
                ("(FK1)", "logged_by", "int", "→ USER.id"),
                ("(FK2)", "visitor_user_id", "int", "→ USER.id"),
                ("", "notes", "text", "nullable"),
                ("", "created_at", "datetime", "default=now"),
            ]
        },
        # Column 3 (x = 2090): Review Attachments (width 560, matching ATTRACTION_REVIEW)
        {
            "id": "erd_table_2009",
            "name": "REVIEW_PHOTO",
            "x": 2090, "y": 650, "w": 560, "col_w": [50, 200, 100, 210],
            "columns": [
                ("PK", "id", "int", "not null"),
                ("(FK)", "review_id", "int", "→ ATTRACTION_REVIEW.id"),
                ("", "url", "string", "not null"),
                ("", "created_at", "datetime", "default=now"),
            ]
        }
    ]

    new_cells = []

    for t in new_tables:
        row_count = len(t["columns"])
        total_height = 25 + row_count * 34
        
        # 1. Add Main Table Cell
        table_cell = ET.Element("mxCell", id=t["id"], value=t["name"], style=TABLE_STYLE, parent="1", vertex="1")
        ET.SubElement(table_cell, "mxGeometry", x=str(t["x"]), y=str(t["y"]), width=str(t["w"]), height=str(total_height), **{"as": "geometry"})
        new_cells.append(table_cell)
        
        # 2. Add Row Cells and Column subdivisions
        for row_idx, cols in enumerate(t["columns"]):
            row_id = f"{t['id']}_row_{row_idx}"
            row_offset = 25 + row_idx * 34
            
            # Row Container
            row_cell = ET.Element("mxCell", id=row_id, value="", style=ROW_STYLE, parent=t["id"], vertex="1")
            ET.SubElement(row_cell, "mxGeometry", y=str(row_offset), width=str(t["w"]), height="34", **{"as": "geometry"})
            new_cells.append(row_cell)
            
            # Columns
            col_x_accum = 0
            for col_idx, val in enumerate(cols):
                col_id = f"{row_id}_col_{col_idx}"
                col_w = t["col_w"][col_idx]
                
                # Determine font style (PK/FK and column name get fontStyle=5 if PK/FK row)
                is_key_row = cols[0] in ("PK", "UK", "(FK)", "(FK1)", "(FK2)")
                col_style = CELL_VAL_STYLE
                if col_idx in (0, 1) and is_key_row:
                    col_style = CELL_KEY_STYLE
                    
                col_cell = ET.Element("mxCell", id=col_id, value=val, style=col_style, parent=row_id, vertex="1")
                
                # Layout geometry details
                geom_args = {"as": "geometry"}
                if col_x_accum > 0:
                    geom_args["x"] = str(col_x_accum)
                ET.SubElement(col_cell, "mxGeometry", width=str(col_w), height="34", **{"as": "geometry"})
                new_cells.append(col_cell)
                
                col_x_accum += col_w

    # Phase 3: Add Clean Connectors without overlapping or cutting through other tables
    # Connectors using vertical clean alignment or short steps
    connectors = [
        # 1. PASSWORD_RESET_TOKEN to USER (direct clean vertical route upward)
        {
            "id": "erd_edge_3000",
            "source": "erd_table_2000_row_1",  # FK user_id row
            "target": "erd_1001",              # USER table
            "label": "user_id"
        },
        # 2. DATABASE_AUDIT_LOG to USER (clean vertical route upward)
        {
            "id": "erd_edge_3001",
            "source": "erd_table_2002_row_1",  # FK user_id row
            "target": "erd_1001",              # USER table
            "label": "user_id"
        },
        # 3. ESTABLISHMENT to USER (horizontal connection)
        {
            "id": "erd_edge_3002",
            "source": "erd_table_2003_row_1",  # FK owner_id row
            "target": "erd_1001",              # USER table
            "label": "owner_id"
        },
        # 4. ESTABLISHMENT_ROOM to ESTABLISHMENT (vertical within column)
        {
            "id": "erd_edge_3003",
            "source": "erd_table_2004_row_1",  # FK establishment_id row
            "target": "erd_table_2003",         # ESTABLISHMENT table
            "label": "establishment_id"
        },
        # 5. ESTABLISHMENT_MENU_ITEM to ESTABLISHMENT (vertical within column)
        {
            "id": "erd_edge_3004",
            "source": "erd_table_2005_row_1",  # FK establishment_id row
            "target": "erd_table_2003",         # ESTABLISHMENT table
            "label": "establishment_id"
        },
        # 6. ESTABLISHMENT_REVIEW to ESTABLISHMENT (vertical within column)
        {
            "id": "erd_edge_3005",
            "source": "erd_table_2006_row_2",  # FK establishment_id row
            "target": "erd_table_2003",         # ESTABLISHMENT table
            "label": "establishment_id"
        },
        # 7. USER_FAVORITE_ESTABLISHMENT to ESTABLISHMENT (vertical within column)
        {
            "id": "erd_edge_3006",
            "source": "erd_table_2007_row_2",  # FK establishment_id row
            "target": "erd_table_2003",         # ESTABLISHMENT table
            "label": "establishment_id"
        },
        # 8. REVIEW_PHOTO to ATTRACTION_REVIEW (vertical within column)
        {
            "id": "erd_edge_3007",
            "source": "erd_table_2009_row_1",  # FK review_id row
            "target": "erd_1344",              # ATTRACTION_REVIEW table
            "label": "review_id"
        }
    ]

    for conn in connectors:
        edge = ET.Element("mxCell", id=conn["id"], value=conn["label"], style=EDGE_STYLE, parent="1", source=conn["source"], target=conn["target"], edge="1")
        ET.SubElement(edge, "mxGeometry", relative="1", **{"as": "geometry"})
        new_cells.append(edge)

    # Inject all new elements into root_cell
    for cell in new_cells:
        root_cell.append(cell)
        
    print(f"Writing updated v2 drawio to {v2_path}...")
    tree.write(v2_path, encoding="utf-8", xml_declaration=True)
    print("ERD v2 drawio file successfully written!")

if __name__ == '__main__':
    generate_v2()
