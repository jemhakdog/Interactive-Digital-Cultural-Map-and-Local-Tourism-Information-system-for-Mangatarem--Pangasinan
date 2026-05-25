import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

if mx_root is None:
    print("Could not find root")
    sys.exit(1)

# Helper to find maximum ID to prevent collisions
def get_max_id():
    max_id = 0
    for cell in mx_root.findall('mxCell'):
        cid = cell.attrib.get('id', '')
        # extract all digits
        digits = re.findall(r'\d+', cid)
        for d in digits:
            max_id = max(max_id, int(d))
    return max_id

max_id_counter = get_max_id() + 5000

def get_new_id(prefix="erd_v3_"):
    global max_id_counter
    max_id_counter += 1
    return f"{prefix}{max_id_counter}"

# Helper to find table
def find_table(name):
    for cell in mx_root.findall('mxCell'):
        val = cell.attrib.get('value', '')
        if name in val and ('shape=table' in cell.attrib.get('style', '') or 'childLayout=tableLayout' in cell.attrib.get('style', '')):
            return cell.attrib.get('id')
    return None

# Helper to find columns/rows in a table and print/modify them
# We want to change rating and attraction_id columns in REVIEW table to be nullable
review_table_id = find_table('ATTRACTION_REVIEW')
if review_table_id:
    print(f"Modifying Attraction Review Table: {review_table_id}")
    # Rename ATTRACTION_REVIEW to REVIEW
    table_cell = mx_root.find(f".//mxCell[@id='{review_table_id}']")
    if table_cell is not None:
        table_cell.attrib['value'] = "REVIEW"
        # Increase height of table since we will add rows
        geom = table_cell.find('mxGeometry')
        if geom is not None:
            geom.attrib['height'] = "376" # Increase height to fit new rows
    
    # Locate column elements to change rating and attraction_id to nullable
    for row in mx_root.findall(f".//mxCell[@parent='{review_table_id}']"):
        row_id = row.attrib.get('id')
        cols = mx_root.findall(f".//mxCell[@parent='{row_id}']")
        if len(cols) >= 4:
            col_name = re.sub('<[^<]+?>', '', cols[1].attrib.get('value', '')).strip()
            if col_name == 'rating':
                # change 'not null' to 'nullable'
                cols[3].attrib['value'] = "nullable"
            elif col_name == 'attraction_id':
                # change 'not null' to 'nullable'
                cols[3].attrib['value'] = "nullable"

    # Add the missing rows for REVIEW table:
    # 1. establishment_id
    # 2. parent_id
    # 3. status
    # 4. updated_at
    
    review_new_rows = [
        ("(FK3)", "establishment_id", "int", "→ ESTABLISHMENT.id (nullable)"),
        ("(FK4)", "parent_id", "int", "→ REVIEW.id (nullable)"),
        ("", "status", "string", "default='pending'"),
        ("", "updated_at", "datetime", "default=now")
    ]
    
    # Let's clone visual rows from erd_table_11012_row (created_at row)
    ref_row_id = "erd_table_11012_row"
    ref_row = mx_root.find(f".//mxCell[@id='{ref_row_id}']")
    if ref_row is not None:
        y_pos = 195
        for fk, col_name, col_type, col_det in review_new_rows:
            y_pos += 34
            new_row_id = get_new_id("review_row_")
            new_row = ET.Element('mxCell')
            new_row.attrib['id'] = new_row_id
            new_row.attrib['value'] = ""
            new_row.attrib['style'] = "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;strokeColor=none;strokeWidth=0;collapsible=0;recursiveResize=0;expand=0;fontStyle=0;connectable=0;align=center;valign=middle;fontColor=none;spacing=0;spacingTop=0;spacingLeft=0;spacingBottom=0;spacingRight=0;pointerEvents=0;"
            new_row.attrib['parent'] = review_table_id
            new_row.attrib['vertex'] = "1"
            
            geom = ET.SubElement(new_row, 'mxGeometry')
            geom.attrib['y'] = str(y_pos)
            geom.attrib['width'] = "560"
            geom.attrib['height'] = "34"
            geom.attrib['as'] = "geometry"
            
            mx_root.append(new_row)
            
            # Add columns
            col_widths = [40, 150, 80, 290]
            col_vals = [fk, col_name, col_type, col_det]
            x_pos = 0
            for i in range(4):
                col_cell = ET.Element('mxCell')
                col_cell.attrib['id'] = f"{new_row_id}_col_{i}"
                col_cell.attrib['value'] = col_vals[i]
                col_cell.attrib['style'] = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;overflow=hidden;"
                col_cell.attrib['parent'] = new_row_id
                col_cell.attrib['vertex'] = "1"
                
                col_geom = ET.SubElement(col_cell, 'mxGeometry')
                col_geom.attrib['x'] = str(x_pos)
                col_geom.attrib['width'] = str(col_widths[i])
                col_geom.attrib['height'] = "34"
                col_geom.attrib['as'] = "geometry"
                
                mx_root.append(col_cell)
                x_pos += col_widths[i]

# Helper to add tables programmatically
def add_new_table(table_name, x, y, width, height, columns):
    table_id = get_new_id("erd_table_v3_")
    
    # 1. Main Table Shape
    table_cell = ET.Element('mxCell')
    table_cell.attrib['id'] = table_id
    table_cell.attrib['value'] = table_name
    table_cell.attrib['style'] = "shape=table;startSize=30;container=1;collapsible=0;childLayout=tableLayout;rowLines=1;columnLines=1;fontStyle=1;align=center;valign=middle;fontSize=14;fillColor=#f5f5f5;strokeColor=#666666;"
    table_cell.attrib['parent'] = "1"
    table_cell.attrib['vertex'] = "1"
    
    geom = ET.SubElement(table_cell, 'mxGeometry')
    geom.attrib['x'] = str(x)
    geom.attrib['y'] = str(y)
    geom.attrib['width'] = str(width)
    geom.attrib['height'] = str(height)
    geom.attrib['as'] = "geometry"
    
    mx_root.append(table_cell)
    
    # 2. Add Rows
    y_pos = 30
    row_cells = {}
    
    for fk, col_name, col_type, col_det in columns:
        row_id = get_new_id("erd_row_v3_")
        row_cells[col_name] = row_id
        
        row_cell = ET.Element('mxCell')
        row_cell.attrib['id'] = row_id
        row_cell.attrib['value'] = ""
        row_cell.attrib['style'] = "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;strokeColor=none;strokeWidth=0;collapsible=0;recursiveResize=0;expand=0;fontStyle=0;connectable=0;align=center;valign=middle;fontColor=none;spacing=0;spacingTop=0;spacingLeft=0;spacingBottom=0;spacingRight=0;pointerEvents=0;"
        row_cell.attrib['parent'] = table_id
        row_cell.attrib['vertex'] = "1"
        
        row_geom = ET.SubElement(row_cell, 'mxGeometry')
        row_geom.attrib['y'] = str(y_pos)
        row_geom.attrib['width'] = str(width)
        row_geom.attrib['height'] = "34"
        row_geom.attrib['as'] = "geometry"
        
        mx_root.append(row_cell)
        
        # Add Columns
        col_widths = [40, 150, 80, 290]
        col_vals = [fk, col_name, col_type, col_det]
        x_pos = 0
        for i in range(4):
            col_cell = ET.Element('mxCell')
            col_cell.attrib['id'] = f"{row_id}_col_{i}"
            col_cell.attrib['value'] = col_vals[i]
            col_cell.attrib['style'] = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;overflow=hidden;"
            col_cell.attrib['parent'] = row_id
            col_cell.attrib['vertex'] = "1"
            
            col_geom = ET.SubElement(col_cell, 'mxGeometry')
            col_geom.attrib['x'] = str(x_pos)
            col_geom.attrib['width'] = str(col_widths[i])
            col_geom.attrib['height'] = "34"
            col_geom.attrib['as'] = "geometry"
            
            mx_root.append(col_cell)
            x_pos += col_widths[i]
            
        y_pos += 34
        
    print(f"Successfully added table {table_name} at ({x}, {y})")
    return table_id, row_cells

# Helper to draw visual relationship edges between source column row and target table
def draw_relationship_edge(src_row_id, target_table_id, fk_label):
    edge_id = get_new_id("erd_edge_v3_")
    edge_cell = ET.Element('mxCell')
    edge_cell.attrib['id'] = edge_id
    edge_cell.attrib['value'] = fk_label
    edge_cell.attrib['style'] = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;endArrow=classic;html=1;fontSize=14;"
    edge_cell.attrib['parent'] = "1"
    edge_cell.attrib['source'] = src_row_id
    edge_cell.attrib['target'] = target_table_id
    edge_cell.attrib['edge'] = "1"
    
    geom = ET.SubElement(edge_cell, 'mxGeometry')
    geom.attrib['relative'] = "1"
    geom.attrib['as'] = "geometry"
    
    mx_root.append(edge_cell)
    return edge_id

# ----------------- 9 NEW TABLES -----------------

# 1. USER_FAVORITE
favorite_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK1)", "user_id", "int", "→ USER.id (not null)"),
    ("(FK2)", "attraction_id", "int", "→ ATTRACTION.id (nullable)"),
    ("(FK3)", "establishment_id", "int", "→ ESTABLISHMENT.id (nullable)"),
    ("(FK4)", "event_id", "int", "→ EVENT.id (nullable)"),
    ("", "status", "string", "default='favorite'"),
    ("", "created_at", "datetime", "default=now")
]
fav_table_id, fav_rows = add_new_table("USER_FAVORITE", -550, 1150, 560, 270, favorite_cols)

# 2. USER_NOTIFICATION
notif_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK)", "user_id", "int", "→ USER.id (not null)"),
    ("", "title", "string", "not null"),
    ("", "message", "text", "not null"),
    ("", "link", "string", "nullable"),
    ("", "is_read", "bool", "default=False"),
    ("", "created_at", "datetime", "default=now")
]
notif_table_id, notif_rows = add_new_table("USER_NOTIFICATION", -550, 1470, 560, 270, notif_cols)

# 3. MAP_FEEDBACK
feedback_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK)", "attraction_id", "int", "→ ATTRACTION.id (nullable)"),
    ("", "feedback_type", "string", "not null"),
    ("", "message", "text", "not null"),
    ("", "status", "string", "default='pending'"),
    ("", "created_at", "datetime", "default=now")
]
feed_table_id, feed_rows = add_new_table("MAP_FEEDBACK", 680, 600, 560, 230, feedback_cols)

# 4. BOOKABLE_ASSET
asset_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK1)", "attraction_id", "int", "→ ATTRACTION.id (nullable)"),
    ("(FK2)", "heritage_profile_id", "int", "→ HERITAGE_PROFILE.id (nullable)"),
    ("", "daily_capacity", "int", "default=50"),
    ("", "requires_approval", "bool", "default=True"),
    ("", "booking_instructions", "text", "nullable"),
    ("", "status", "string", "default='active'"),
    ("", "created_at", "datetime", "default=now")
]
asset_table_id, asset_rows = add_new_table("BOOKABLE_ASSET", 1400, 650, 560, 300, asset_cols)

# 5. BOOKING_SLOT
slot_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK)", "bookable_asset_id", "int", "→ BOOKABLE_ASSET.id (not null)"),
    ("", "date", "date", "not null"),
    ("", "total_capacity", "int", "not null"),
    ("", "booked_count", "int", "default=0")
]
slot_table_id, slot_rows = add_new_table("BOOKING_SLOT", 1400, 980, 560, 200, slot_cols)

# 6. RESERVATION
res_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK1)", "user_id", "int", "→ USER.id (not null)"),
    ("(FK2)", "booking_slot_id", "int", "→ BOOKING_SLOT.id (not null)"),
    ("", "party_size", "int", "default=1"),
    ("", "primary_contact", "string", "nullable"),
    ("", "special_requests", "text", "nullable"),
    ("", "status", "string", "default='pending'"),
    ("", "qr_code_token", "string", "not null"),
    ("", "created_at", "datetime", "default=now"),
    ("", "updated_at", "datetime", "default=now")
]
res_table_id, res_rows = add_new_table("RESERVATION", 1400, 1310, 560, 370, res_cols)

# 7. CHAT_ROOM
chatroom_cols = [
    ("PK", "id", "int", "not null"),
    ("", "type", "string", "not null"),
    ("(FK1)", "barangay_id", "int", "→ BARANGAY_INFO.id (nullable)"),
    ("(FK2)", "establishment_id", "int", "→ ESTABLISHMENT.id (nullable)"),
    ("", "created_at", "datetime", "default=now")
]
chatroom_table_id, chatroom_rows = add_new_table("CHAT_ROOM", 2150, 40, 560, 200, chatroom_cols)

# 8. CHAT_PARTICIPANT
participant_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK1)", "chat_room_id", "int", "→ CHAT_ROOM.id (not null)"),
    ("(FK2)", "user_id", "int", "→ USER.id (not null)"),
    ("", "joined_at", "datetime", "default=now"),
    ("", "last_read_at", "datetime", "default=now")
]
participant_table_id, participant_rows = add_new_table("CHAT_PARTICIPANT", 2150, 300, 560, 200, participant_cols)

# 9. CHAT_MESSAGE
message_cols = [
    ("PK", "id", "int", "not null"),
    ("(FK1)", "chat_room_id", "int", "→ CHAT_ROOM.id (not null)"),
    ("(FK2)", "sender_id", "int", "→ USER.id (not null)"),
    ("", "content", "text", "not null"),
    ("", "created_at", "datetime", "default=now"),
    ("", "is_system_msg", "bool", "default=False")
]
message_table_id, message_rows = add_new_table("CHAT_MESSAGE", 2150, 560, 560, 230, message_cols)

# ----------------- DRAW EDGES / RELATIONSHIPS -----------------

user_table_id = "erd_1001"
attraction_table_id = "erd_1037"
establishment_table_id = "erd_table_2003"
event_table_id = "erd_1108"
heritage_table_id = "erd_1390"
barangay_table_id = "erd_1220"

# USER_FAVORITE edges
draw_relationship_edge(fav_rows["user_id"], user_table_id, "user_id")
draw_relationship_edge(fav_rows["attraction_id"], attraction_table_id, "attraction_id")
draw_relationship_edge(fav_rows["establishment_id"], establishment_table_id, "establishment_id")
draw_relationship_edge(fav_rows["event_id"], event_table_id, "event_id")

# USER_NOTIFICATION edge
draw_relationship_edge(notif_rows["user_id"], user_table_id, "user_id")

# MAP_FEEDBACK edge
draw_relationship_edge(feed_rows["attraction_id"], attraction_table_id, "attraction_id")

# BOOKABLE_ASSET edges
draw_relationship_edge(asset_rows["attraction_id"], attraction_table_id, "attraction_id")
draw_relationship_edge(asset_rows["heritage_profile_id"], heritage_table_id, "heritage_profile_id")

# BOOKING_SLOT edge
draw_relationship_edge(slot_rows["bookable_asset_id"], asset_table_id, "bookable_asset_id")

# RESERVATION edges
draw_relationship_edge(res_rows["user_id"], user_table_id, "user_id")
draw_relationship_edge(res_rows["booking_slot_id"], slot_table_id, "booking_slot_id")

# CHAT_ROOM edges
draw_relationship_edge(chatroom_rows["barangay_id"], barangay_table_id, "barangay_id")
draw_relationship_edge(chatroom_rows["establishment_id"], establishment_table_id, "establishment_id")

# CHAT_PARTICIPANT edges
draw_relationship_edge(participant_rows["chat_room_id"], chatroom_table_id, "chat_room_id")
draw_relationship_edge(participant_rows["user_id"], user_table_id, "user_id")

# CHAT_MESSAGE edges
draw_relationship_edge(message_rows["chat_room_id"], chatroom_table_id, "chat_room_id")
draw_relationship_edge(message_rows["sender_id"], user_table_id, "sender_id")

# Save output
tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("Updated erd_v3.drawio successfully!")
