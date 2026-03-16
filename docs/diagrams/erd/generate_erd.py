"""
Generate a clean ERD drawio XML with a Top-Down layout.
Fixes visual glitches (diagonal lines) and updates names to plural with Form IDs.
"""

import xml.etree.ElementTree as ET
from collections import defaultdict

# ─── Configuration ───
TABLE_WIDTH = 320
ROW_HEIGHT = 30
HEADER_HEIGHT = 34
TABLE_START_SIZE = 25
FONT_SIZE = 14

# Column widths
COL1_W = 40   # PK/FK
COL2_W = 180  # Name
COL3_W = 100  # Type

# Spacing
HORIZONTAL_GAP = 60
VERTICAL_GAP = 120  # Increased for cleaner routing

# ─── Table Definitions ───
TABLES = {
    "USERS": {
        "form_id": "",
        "fields": [
            ("int",    "id",            "PK", ""),
            ("string", "username",      "UK", ""),
            ("string", "email",         "UK", ""),
            ("string", "password_hash", "",   ""),
            ("string", "role",          "",   ""),
            ("string", "barangay",      "",   ""),
            ("bool",   "is_approved",   "",   ""),
        ]
    },
    "ATTRACTIONS": {
        "form_id": "",
        "fields": [
            ("int",      "id",                      "PK", ""),
            ("string",   "name",                    "",   ""),
            ("text",     "description",             "",   ""),
            ("string",   "category",                "",   ""),
            ("string",   "barangay",                "",   ""),
            ("float",    "lat",                     "",   ""),
            ("float",    "lng",                     "",   ""),
            ("string",   "image_url",               "",   ""),
            ("string",   "status",                  "",   ""),
            ("int",      "user_id",                 "FK", ""),
            ("int",      "reviewed_by",             "FK", ""),
            ("datetime", "reviewed_at",             "",   ""),
            ("datetime", "created_at",              "",   ""),
            ("int",      "heritage_profile_id",     "FK", ""),
        ]
    },
    "EVENTS": {
        "form_id": "",
        "fields": [
            ("int",      "id",          "PK", ""),
            ("string",   "title",       "",   ""),
            ("text",     "description", "",   ""),
            ("datetime", "date",        "",   ""),
            ("string",   "location",    "",   ""),
            ("string",   "barangay",    "",   ""),
            ("string",   "image_url",   "",   ""),
            ("int",      "user_id",     "FK", ""),
            ("string",   "status",      "",   ""),
            ("string",   "category",    "",   ""),
            ("int",      "reviewed_by", "FK", ""),
            ("datetime", "reviewed_at", "",   ""),
            ("datetime", "created_at",  "",   ""),
        ]
    },
    "GALLERY_ITEMS": {
        "form_id": "",
        "fields": [
            ("int",      "id",          "PK", ""),
            ("string",   "type",        "",   ""),
            ("string",   "url",         "",   ""),
            ("string",   "caption",     "",   ""),
            ("int",      "user_id",     "FK", ""),
            ("string",   "status",      "",   ""),
            ("int",      "reviewed_by", "FK", ""),
            ("datetime", "reviewed_at", "",   ""),
            ("datetime", "uploaded_at", "",   ""),
        ]
    },
    "BARANGAY_INFOS": {
        "form_id": "",
        "fields": [
            ("int",      "id",              "PK", ""),
            ("string",   "barangay_name",   "UK", ""),
            ("text",     "history",         "",   ""),
            ("text",     "cultural_assets", "",   ""),
            ("text",     "traditions",      "",   ""),
            ("text",     "local_practices", "",   ""),
            ("text",     "unique_features", "",   ""),
            ("int",      "user_id",         "FK", ""),
            ("datetime", "updated_at",      "",   ""),
        ]
    },
    "PAGE_VIEWS": {
        "form_id": "",
        "fields": [
            ("int",      "id",        "PK", ""),
            ("string",   "view_type", "",   ""),
            ("int",      "item_id",   "",   ""),
            ("string",   "page_name", "",   ""),
            ("datetime", "timestamp", "",   ""),
            ("int",      "user_id",   "",   ""),
        ]
    },
    "FAVORITES": {
        "form_id": "",
        "fields": [
            ("int",      "id",            "PK", ""),
            ("int",      "user_id",       "FK", ""),
            ("int",      "attraction_id", "FK", ""),
            ("datetime", "created_at",    "",   ""),
        ]
    },
    "EVENT_INTERESTS": {
        "form_id": "",
        "fields": [
            ("int",      "id",         "PK", ""),
            ("int",      "user_id",    "FK", ""),
            ("int",      "event_id",   "FK", ""),
            ("string",   "status",     "",   ""),
            ("datetime", "created_at", "",   ""),
        ]
    },
    "REVIEWS": {
        "form_id": "",
        "fields": [
            ("int",      "id",            "PK", ""),
            ("int",      "user_id",       "FK", ""),
            ("int",      "attraction_id", "FK", ""),
            ("int",      "rating",        "",   ""),
            ("text",     "comment",       "",   ""),
            ("string",   "status",        "",   ""),
            ("int",      "reviewed_by",   "FK", ""),
            ("datetime", "reviewed_at",   "",   ""),
            ("datetime", "created_at",    "",   ""),
        ]
    },
    "HERITAGE_PROFILES": {
        "form_id": "",
        "fields": [
            ("int",    "id",            "PK", ""),
            ("string", "asset_type",    "",   ""),
            ("string", "mapper_name",   "",   ""),
            ("date",   "date_profiled", "",   ""),
            ("string", "status",        "",   ""),
            ("int",    "user_id",       "FK", ""),
            ("int",    "reviewed_by",   "FK", ""),
            ("datetime", "reviewed_at", "",   ""),
            ("datetime", "created_at",  "",   ""),
            ("json",   "key_informants", "",  ""),
            ("text",   "reference_sources", "", ""),
            ("text",   "significance",  "",   ""),
            ("text",   "constraints_threats", "", ""),
            ("text",   "conservation_measures", "", ""),
            ("string", "common_photo_url", "", ""),
        ]
    },
    "BUILT_HERITAGE_DETAILS": {
        "form_id": "Form 2017-B",
        "fields": [
            ("int",    "profile_id",  "PK, FK", ""),
            ("string", "building_type", "", ""),
            ("int",    "year_constructed", "", ""),
            ("string", "ownership_type", "", ""),
            ("text",   "physical_description", "", ""),
            ("text",   "history_structure", "", ""),
            ("string", "occupation_status", "", ""),
            ("bool",   "is_altered", "", ""),
            ("bool",   "is_original_site", "", ""),
            ("json",   "movable_heritage_list", "", ""),
        ]
    },
    "MOVABLE_HERITAGE_DETAILS": {
        "form_id": "Form 2017-A",
        "fields": [
            ("int",    "profile_id", "PK, FK", ""),
            ("string", "object_type", "", ""),
            ("string", "place_found", "", ""),
            ("date",   "date_found", "", ""),
            ("string", "estimated_age", "", ""),
            ("string", "materials", "", ""),
            ("string", "dimensions", "", ""),
            ("text",   "comparative_criteria", "", ""),
        ]
    },
    "NATURAL_HERITAGE_DETAILS": {
        "form_id": "Form 01A",
        "fields": [
            ("int",   "profile_id", "PK, FK", ""),
            ("string", "subcategory", "", ""),
            ("float",  "area_hectares", "", ""),
            ("string", "ownership", "", ""),
            ("string", "protection_status", "", ""),
        ]
    },
    "INTANGIBLE_HERITAGE_DETAILS": {
        "form_id": "Form 2017-C",
        "fields": [
            ("int",    "profile_id", "PK, FK", ""),
            ("string", "heritage_type", "", ""),
            ("text",   "geographical_range", "", ""),
            ("json",   "related_domains", "", ""),
            ("text",   "culture_bearers", "", ""),
            ("text",   "transmission_mode", "", ""),
            ("json",   "objects_used", "", ""),
            ("json",   "safeguarding_measures", "", ""),
        ]
    },
    "PERSONALITY_DETAILS": {
        "form_id": "Form 03",
        "fields": [
            ("int",    "profile_id", "PK, FK", ""),
            ("date",   "date_of_birth", "", ""),
            ("date",   "date_of_death", "", ""),
            ("string", "birth_place", "", ""),
            ("string", "prominence_field", "", ""),
            ("text",   "biography", "", ""),
            ("json",   "works_achievements", "", ""),
        ]
    },
    "INSTITUTION_DETAILS": {
        "form_id": "Form 04",
        "fields": [
            ("int",    "profile_id", "PK, FK", ""),
            ("string", "institution_type", "", ""),
            ("text",   "mandate_description", "", ""),
            ("text",   "milestones", "", ""),
            ("text",   "condition_status", "", ""),
        ]
    },
    "LGU_PROGRAM_DETAILS": {
        "form_id": "Form 05",
        "fields": [
            ("int",    "profile_id", "PK, FK", ""),
            ("text",   "vision_statement", "", ""),
            ("text",   "mission_statement", "", ""),
            ("date",   "adoption_date", "", ""),
            ("json",   "chief_executives", "", ""),
            ("json",   "culture_projects", "", ""),
        ]
    },
}

def calc_table_height(fields):
    return TABLE_START_SIZE + HEADER_HEIGHT + ROW_HEIGHT * len(fields)

LAYOUT_ROWS = [
    ["USERS"],
    ["HERITAGE_PROFILES", "ATTRACTIONS", "EVENTS", "GALLERY_ITEMS", "BARANGAY_INFOS"],
    ["BUILT_HERITAGE_DETAILS", "NATURAL_HERITAGE_DETAILS", "INTANGIBLE_HERITAGE_DETAILS", "MOVABLE_HERITAGE_DETAILS"],
    ["PERSONALITY_DETAILS", "INSTITUTION_DETAILS", "LGU_PROGRAM_DETAILS"],
    ["REVIEWS", "FAVORITES", "EVENT_INTERESTS", "ANALYTICS_PAGE_VIEW"],
]

POSITIONS = {}
def calculate_positions():
    current_y = 60
    canvas_center = 1300
    for row in LAYOUT_ROWS:
        row_width = len(row) * TABLE_WIDTH + (len(row) - 1) * HORIZONTAL_GAP
        start_x = canvas_center - (row_width // 2)
        max_h = 0
        for i, table_name in enumerate(row):
            x = start_x + i * (TABLE_WIDTH + HORIZONTAL_GAP)
            POSITIONS[table_name] = (x, current_y)
            h = calc_table_height(TABLES[table_name]["fields"])
            max_h = max(max_h, h)
        current_y += max_h + VERTICAL_GAP

calculate_positions()

RELATIONSHIPS = [
    ("USERS", "ATTRACTIONS",            "creates",  "ERmandOne", "ERzeroToMany"),
    ("USERS", "EVENTS",                 "creates",  "ERmandOne", "ERzeroToMany"),
    ("USERS", "GALLERY_ITEMS",          "uploads",  "ERmandOne", "ERzeroToMany"),
    ("USERS", "BARANGAY_INFOS",         "manages",  "ERmandOne", "ERzeroToMany"),
    ("USERS", "FAVORITES",              "has",      "ERmandOne", "ERzeroToMany"),
    ("USERS", "REVIEWS",                "writes",   "ERmandOne", "ERzeroToMany"),
    ("ATTRACTIONS", "FAVORITES",        "receives", "ERmandOne", "ERzeroToMany"),
    ("ATTRACTIONS", "REVIEWS",          "receives", "ERmandOne", "ERzeroToMany"),
    ("ATTRACTIONS", "ANALYTICS_PAGE_VIEW",       "tracks",   "ERmandOne", "ERzeroToMany"),
    ("EVENTS", "ANALYTICS_PAGE_VIEW",            "tracks",   "ERmandOne", "ERzeroToMany"),
    ("EVENTS", "EVENT_INTERESTS",       "receives", "ERmandOne", "ERzeroToMany"),
    ("USERS", "HERITAGE_PROFILES",      "profiles", "ERmandOne", "ERzeroToMany"),
    ("ATTRACTIONS", "HERITAGE_PROFILES", "linked",   "ERmandOne", "ERmandOne"),
    ("HERITAGE_PROFILES", "BUILT_HERITAGE_DETAILS",      "details", "ERmandOne", "ERmandOne"),
    ("HERITAGE_PROFILES", "MOVABLE_HERITAGE_DETAILS",    "details", "ERmandOne", "ERmandOne"),
    ("HERITAGE_PROFILES", "NATURAL_HERITAGE_DETAILS",    "details", "ERmandOne", "ERmandOne"),
    ("HERITAGE_PROFILES", "INTANGIBLE_HERITAGE_DETAILS", "details", "ERmandOne", "ERmandOne"),
    ("HERITAGE_PROFILES", "PERSONALITY_DETAILS",         "details", "ERmandOne", "ERmandOne"),
    ("HERITAGE_PROFILES", "INSTITUTION_DETAILS",         "details", "ERmandOne", "ERmandOne"),
    ("HERITAGE_PROFILES", "LGU_PROGRAM_DETAILS",         "details", "ERmandOne", "ERmandOne"),
    ("USERS", "EVENT_INTERESTS",        "marks",    "ERmandOne", "ERzeroToMany"),
]

_counter = 1000
def next_id():
    global _counter
    _counter += 1
    return f"e{_counter}"

def build_xml():
    root = ET.Element("mxfile", host="Electron", agent="5.0 (Windows NT 10.0; Win64; x64)")
    diagram = ET.SubElement(root, "diagram", id="ERD", name="Page-1")
    model = ET.SubElement(diagram, "mxGraphModel", dx="2000", dy="2000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="2600", pageHeight="3000")
    root_cell = ET.SubElement(model, "root")
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    table_ids = {}
    for name, tdef in TABLES.items():
        x, y = POSITIONS[name]
        h = calc_table_height(tdef["fields"])
        tid = next_id()
        table_ids[name] = tid
        
        header_val = name
        if tdef["form_id"]:
            header_val = f"{name} ({tdef['form_id']})"

        # Table Container
        tbl = ET.SubElement(root_cell, "mxCell", id=tid, value=header_val, parent="1", vertex="1",
            style="shape=table;startSize=25;container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;rowLines=1;fontStyle=1;align=center;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=18;")
        ET.SubElement(tbl, "mxGeometry", x=str(x), y=str(y), width=str(TABLE_WIDTH), height=str(h)).set("as", "geometry")

        ry = TABLE_START_SIZE
        for i, (dtype, fname, key, _) in enumerate(tdef["fields"]):
            is_pk = "PK" in key
            is_fk = "FK" in key
            font_style = 1 if is_pk else 0
            row_id = next_id()
            
            # Row
            row = ET.SubElement(root_cell, "mxCell", id=row_id, parent=tid, vertex="1",
                style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;top=0;left=0;right=0;bottom=0;")
            ET.SubElement(row, "mxGeometry", y=str(ry), width=str(TABLE_WIDTH), height=str(ROW_HEIGHT)).set("as", "geometry")

            # Cells
            c1 = ET.SubElement(root_cell, "mxCell", id=next_id(), value=key, parent=row_id, vertex="1",
                style=f"connectable=0;fillColor=none;align=left;spacingLeft=4;fontSize={FONT_SIZE};fontStyle={font_style};")
            ET.SubElement(c1, "mxGeometry", width=str(COL1_W), height=str(ROW_HEIGHT)).set("as", "geometry")

            c2 = ET.SubElement(root_cell, "mxCell", id=next_id(), value=fname, parent=row_id, vertex="1",
                style=f"connectable=0;fillColor=none;align=left;spacingLeft=4;fontSize={FONT_SIZE};fontStyle={font_style};")
            ET.SubElement(c2, "mxGeometry", x=str(COL1_W), width=str(COL2_W), height=str(ROW_HEIGHT)).set("as", "geometry")

            c3 = ET.SubElement(root_cell, "mxCell", id=next_id(), value=dtype, parent=row_id, vertex="1",
                style=f"connectable=0;fillColor=none;align=left;spacingLeft=4;fontSize={FONT_SIZE};")
            ET.SubElement(c3, "mxGeometry", x=str(COL1_W+COL2_W), width=str(COL3_W), height=str(ROW_HEIGHT)).set("as", "geometry")
            
            ry += ROW_HEIGHT

    # Edges
    for src, tgt, label, startA, endA in RELATIONSHIPS:
        eid = next_id()
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;startArrow={startA};startSize=8;endArrow={endA};endSize=8;strokeWidth=1.5;fontSize=11;"
        edge = ET.SubElement(root_cell, "mxCell", id=eid, value=label, parent="1", source=table_ids[src], target=table_ids[tgt], edge="1", style=style)
        geo = ET.SubElement(edge, "mxGeometry", relative="1")
        geo.set("as", "geometry")

    return root

if __name__ == "__main__":
    root = build_xml()
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")
    out = "docs/diagrams/erd_v2.drawio"
    tree.write(out, encoding="UTF-8", xml_declaration=True)
    print(f"Generated: {out}")
