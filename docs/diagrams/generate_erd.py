"""
Generate a clean ERD drawio XML with a 3-column left-to-right layout.
Column 1: USER (Auth)
Column 2: Content entities (ATTRACTION, EVENT, GALLERY_ITEM, BARANGAY_INFO)
Column 3: Engagement entities (FAVORITE, REVIEW, PAGE_VIEW, EVENT_INTEREST)

All tables include fields from models.py including reviewed_by/reviewed_at.
"""

import xml.etree.ElementTree as ET

# ─── Configuration ───
TABLE_WIDTH = 540
ROW_HEIGHT = 40
HEADER_HEIGHT = 45  # First row (PK row) is taller
TABLE_START_SIZE = 25  # Title bar height
FONT_SIZE = 18

# Column widths inside each row (4 cells: type, field, key, extra)
COL1_W = 70   # type column
COL2_W = 231  # field name column
COL3_W = 39   # key column
COL4_W = 200  # extra column

# ─── Table Definitions (from models.py) ───
TABLES = {
    "USER": {
        "fields": [
            ("int",    "id",            "PK", ""),
            ("string", "username",      "UK", ""),
            ("string", "email",         "UK", ""),
            ("string", "password_hash", "",   ""),
            ("string", "role",          "",   "default='user'"),
            ("string", "barangay",      "",   "nullable"),
            ("bool",   "is_approved",   "",   "default=False"),
        ]
    },
    "ATTRACTION": {
        "fields": [
            ("int",      "id",          "PK", ""),
            ("string",   "name",        "",   "not null"),
            ("text",     "description", "",   "not null"),
            ("string",   "category",    "",   "not null"),
            ("string",   "barangay",    "",   "nullable"),
            ("float",    "lat",         "",   "not null"),
            ("float",    "lng",         "",   "not null"),
            ("string",   "image_url",   "",   "nullable"),
            ("string",   "status",      "",   "default='pending'"),
            ("int",      "user_id",     "FK", "→ user.id"),
            ("int",      "reviewed_by", "FK", "→ user.id"),
            ("datetime", "reviewed_at", "",   "nullable"),
            ("datetime", "created_at",  "",   "default=now"),
        ]
    },
    "EVENT": {
        "fields": [
            ("int",      "id",          "PK", ""),
            ("string",   "title",       "",   "not null"),
            ("text",     "description", "",   "not null"),
            ("datetime", "date",        "",   "not null"),
            ("string",   "location",    "",   "not null"),
            ("string",   "barangay",    "",   "nullable"),
            ("string",   "image_url",   "",   "nullable"),
            ("int",      "user_id",     "FK", "→ user.id"),
            ("string",   "status",      "",   "default='pending'"),
            ("string",   "category",    "",   "not null"),
            ("int",      "reviewed_by", "FK", "→ user.id"),
            ("datetime", "reviewed_at", "",   "nullable"),
            ("datetime", "created_at",  "",   "default=now"),
        ]
    },
    "GALLERY_ITEM": {
        "fields": [
            ("int",      "id",          "PK", ""),
            ("string",   "type",        "",   "not null"),
            ("string",   "url",         "",   "not null"),
            ("string",   "caption",     "",   "nullable"),
            ("int",      "user_id",     "FK", "→ user.id"),
            ("string",   "status",      "",   "default='pending'"),
            ("int",      "reviewed_by", "FK", "→ user.id"),
            ("datetime", "reviewed_at", "",   "nullable"),
            ("datetime", "uploaded_at", "",   "default=now"),
        ]
    },
    "BARANGAY_INFO": {
        "fields": [
            ("int",      "id",              "PK", ""),
            ("string",   "barangay_name",   "UK", "not null"),
            ("text",     "history",         "",   "nullable"),
            ("text",     "cultural_assets", "",   "nullable"),
            ("text",     "traditions",      "",   "nullable"),
            ("text",     "local_practices", "",   "nullable"),
            ("text",     "unique_features", "",   "nullable"),
            ("int",      "user_id",         "FK", "→ user.id"),
            ("datetime", "updated_at",      "",   "default=now"),
        ]
    },
    "PAGE_VIEW": {
        "fields": [
            ("int",      "id",        "PK", ""),
            ("string",   "view_type", "",   "not null"),
            ("int",      "item_id",   "",   "nullable"),
            ("string",   "page_name", "",   "nullable"),
            ("datetime", "timestamp", "",   "default=now"),
            ("int",      "user_id",   "",   "nullable"),
        ]
    },
    "FAVORITE": {
        "fields": [
            ("int",      "id",            "PK", ""),
            ("int",      "user_id",       "FK", "→ user.id"),
            ("int",      "attraction_id", "FK", "→ attraction.id"),
            ("datetime", "created_at",    "",   "default=now"),
        ]
    },
    "EVENT_INTEREST": {
        "fields": [
            ("int",      "id",         "PK", ""),
            ("int",      "user_id",    "FK", "→ user.id"),
            ("int",      "event_id",   "FK", "→ event.id"),
            ("string",   "status",     "",   "default='interested'"),
            ("datetime", "created_at", "",   "default=now"),
        ]
    },
    "REVIEW": {
        "fields": [
            ("int",      "id",            "PK", ""),
            ("int",      "user_id",       "FK", "→ user.id"),
            ("int",      "attraction_id", "FK", "→ attraction.id"),
            ("int",      "rating",        "",   "not null"),
            ("text",     "comment",       "",   "nullable"),
            ("string",   "status",        "",   "default='pending'"),
            ("int",      "reviewed_by",   "FK", "→ user.id"),
            ("datetime", "reviewed_at",   "",   "nullable"),
            ("datetime", "created_at",    "",   "default=now"),
        ]
    },
}


def calc_table_height(fields):
    """Calculate table height based on number of fields."""
    return TABLE_START_SIZE + HEADER_HEIGHT + ROW_HEIGHT * (len(fields) - 1)


# ─── Layout Positions (3-column left-to-right) ───
# Column 1: USER (centered vertically)
# Column 2: Content tables (stacked)
# Column 3: Engagement tables (stacked, aligned near parents)

COL1_X = 40
COL2_X = 700
COL3_X = 1400
VERTICAL_GAP = 80

# Calculate heights to determine vertical positions
heights = {name: calc_table_height(t["fields"]) for name, t in TABLES.items()}

# Column 2 positions (stacked vertically)
col2_tables = ["ATTRACTION", "EVENT", "GALLERY_ITEM", "BARANGAY_INFO"]
col2_y = {}
y = 40
for name in col2_tables:
    col2_y[name] = y
    y += heights[name] + VERTICAL_GAP

# Column 3 positions (aligned near their Column 2 parents)
col3_tables = ["FAVORITE", "REVIEW", "PAGE_VIEW", "EVENT_INTEREST"]
col3_y = {}
# FAVORITE and REVIEW near ATTRACTION
col3_y["FAVORITE"] = col2_y["ATTRACTION"]
col3_y["REVIEW"] = col3_y["FAVORITE"] + heights["FAVORITE"] + VERTICAL_GAP
# PAGE_VIEW between ATTRACTION and EVENT areas
col3_y["PAGE_VIEW"] = col3_y["REVIEW"] + heights["REVIEW"] + VERTICAL_GAP
# EVENT_INTEREST near EVENT
col3_y["EVENT_INTEREST"] = col3_y["PAGE_VIEW"] + heights["PAGE_VIEW"] + VERTICAL_GAP

# USER in Column 1 (centered vertically relative to full diagram)
total_col2_height = sum(heights[n] for n in col2_tables) + VERTICAL_GAP * (len(col2_tables) - 1)
user_y = 40 + (total_col2_height - heights["USER"]) // 2

POSITIONS = {
    "USER": (COL1_X, user_y),
}
for name in col2_tables:
    POSITIONS[name] = (COL2_X, col2_y[name])
for name in col3_tables:
    POSITIONS[name] = (COL3_X, col3_y[name])


# ─── Relationships ───
RELATIONSHIPS = [
    # (source_table, target_table, label, start_card, end_card)
    ("USER", "ATTRACTION",     "creates",  "ERmandOne", "ERzeroToMany"),
    ("USER", "EVENT",          "creates",  "ERmandOne", "ERzeroToMany"),
    ("USER", "GALLERY_ITEM",   "uploads",  "ERmandOne", "ERzeroToMany"),
    ("USER", "BARANGAY_INFO",  "manages",  "ERmandOne", "ERzeroToMany"),
    ("USER", "FAVORITE",       "has",      "ERmandOne", "ERzeroToMany"),
    ("USER", "REVIEW",         "writes",   "ERmandOne", "ERzeroToMany"),
    ("ATTRACTION", "FAVORITE", "for",      "ERmandOne", "ERzeroToMany"),
    ("ATTRACTION", "REVIEW",   "receives", "ERmandOne", "ERzeroToMany"),
    ("ATTRACTION", "PAGE_VIEW","tracks",   "ERmandOne", "ERzeroToMany"),
    ("EVENT", "PAGE_VIEW",     "tracks",   "ERmandOne", "ERzeroToMany"),
    ("EVENT", "EVENT_INTEREST","receives", "ERmandOne", "ERzeroToMany"),
]

# ─── ID Counter ───
_id_counter = 1000

def next_id():
    global _id_counter
    _id_counter += 1
    return f"erd_{_id_counter}"


def build_xml():
    """Build the complete drawio XML."""

    root = ET.Element("mxfile", host="65bd71144e")
    diagram = ET.SubElement(root, "diagram", name="Page-1", id="ERD_CLEAN")
    graph = ET.SubElement(diagram, "mxGraphModel",
                          dx="2800", dy="1800", grid="1", gridSize="10",
                          guides="1", tooltips="1", connect="1", arrows="1",
                          fold="1", page="1", pageScale="1",
                          pageWidth="2400", pageHeight="2200",
                          math="0", shadow="0")
    root_cell = ET.SubElement(graph, "root")
    ET.SubElement(root_cell, "mxCell", id="0")
    ET.SubElement(root_cell, "mxCell", id="1", parent="0")

    table_ids = {}      # table_name -> container mxCell id
    table_row_ids = {}   # table_name -> dict of row_index -> row mxCell id

    # ─── Create Tables ───
    for table_name, table_def in TABLES.items():
        fields = table_def["fields"]
        x, y = POSITIONS[table_name]
        h = calc_table_height(fields)

        # Table container
        tid = next_id()
        table_ids[table_name] = tid
        table_row_ids[table_name] = {}

        tbl = ET.SubElement(root_cell, "mxCell",
            id=tid, value=table_name,
            style=(
                "shape=table;startSize=25;container=1;collapsible=0;"
                "childLayout=tableLayout;fixedRows=1;rowLines=1;"
                "fontStyle=1;align=center;resizeLast=1;fontSize=18;"
            ),
            parent="1", vertex="1")
        geo = ET.SubElement(tbl, "mxGeometry",
            x=str(x), y=str(y), width=str(TABLE_WIDTH), height=str(h))
        geo.set("as", "geometry")

        # ─── Rows ───
        row_y = TABLE_START_SIZE
        for i, (dtype, fname, key, extra) in enumerate(fields):
            is_first = (i == 0)
            rh = HEADER_HEIGHT if is_first else ROW_HEIGHT

            row_id = next_id()
            table_row_ids[table_name][i] = row_id

            row = ET.SubElement(root_cell, "mxCell",
                id=row_id,
                style=(
                    "shape=tableRow;horizontal=0;startSize=0;"
                    "swimlaneHead=0;swimlaneBody=0;fillColor=none;"
                    "collapsible=0;dropTarget=0;"
                    "points=[[0,0.5],[1,0.5]];"
                    "portConstraint=eastwest;"
                    "top=0;left=0;right=0;bottom=0;"
                ),
                parent=tid, vertex="1")
            geo = ET.SubElement(row, "mxGeometry",
                y=str(row_y), width=str(TABLE_WIDTH), height=str(rh))
            geo.set("as", "geometry")

            # Cell 1: data type
            c1 = ET.SubElement(root_cell, "mxCell",
                id=next_id(), value=dtype,
                style=(
                    "shape=partialRectangle;connectable=0;fillColor=none;"
                    "top=0;left=0;bottom=0;right=0;align=left;"
                    f"spacingLeft=2;overflow=hidden;fontSize={FONT_SIZE};"
                ),
                parent=row_id, vertex="1")
            g1 = ET.SubElement(c1, "mxGeometry",
                width=str(COL1_W), height=str(rh))
            g1.set("as", "geometry")
            a1 = ET.SubElement(g1, "mxRectangle",
                width=str(COL1_W), height=str(rh))
            a1.set("as", "alternateBounds")

            # Cell 2: field name
            c2 = ET.SubElement(root_cell, "mxCell",
                id=next_id(), value=fname,
                style=(
                    "shape=partialRectangle;connectable=0;fillColor=none;"
                    "top=0;left=0;bottom=0;right=0;align=left;"
                    f"spacingLeft=2;overflow=hidden;fontSize={FONT_SIZE};"
                ),
                parent=row_id, vertex="1")
            g2 = ET.SubElement(c2, "mxGeometry",
                x=str(COL1_W), width=str(COL2_W), height=str(rh))
            g2.set("as", "geometry")
            a2 = ET.SubElement(g2, "mxRectangle",
                width=str(COL2_W), height=str(rh))
            a2.set("as", "alternateBounds")

            # Cell 3: key
            c3 = ET.SubElement(root_cell, "mxCell",
                id=next_id(), value=key,
                style=(
                    "shape=partialRectangle;connectable=0;fillColor=none;"
                    "top=0;left=0;bottom=0;right=0;align=left;"
                    f"spacingLeft=2;overflow=hidden;fontSize={FONT_SIZE};"
                ),
                parent=row_id, vertex="1")
            g3 = ET.SubElement(c3, "mxGeometry",
                x=str(COL1_W + COL2_W), width=str(COL3_W), height=str(rh))
            g3.set("as", "geometry")
            a3 = ET.SubElement(g3, "mxRectangle",
                width=str(COL3_W), height=str(rh))
            a3.set("as", "alternateBounds")

            # Cell 4: extra info
            c4 = ET.SubElement(root_cell, "mxCell",
                id=next_id(), value=extra,
                style=(
                    "shape=partialRectangle;connectable=0;fillColor=none;"
                    "top=0;left=0;bottom=0;right=0;align=left;"
                    f"spacingLeft=2;overflow=hidden;fontSize={FONT_SIZE};"
                ),
                parent=row_id, vertex="1")
            g4 = ET.SubElement(c4, "mxGeometry",
                x=str(COL1_W + COL2_W + COL3_W),
                width=str(TABLE_WIDTH - COL1_W - COL2_W - COL3_W),
                height=str(rh))
            g4.set("as", "geometry")
            a4 = ET.SubElement(g4, "mxRectangle",
                width=str(TABLE_WIDTH - COL1_W - COL2_W - COL3_W),
                height=str(rh))
            a4.set("as", "alternateBounds")

            row_y += rh

    # ─── Create Relationships ───
    for src_table, tgt_table, label, start_card, end_card in RELATIONSHIPS:
        edge_id = next_id()
        src_id = table_ids[src_table]
        tgt_id = table_ids[tgt_table]

        style = (
            f"edgeStyle=orthogonalEdgeStyle;rounded=1;"
            f"startArrow={start_card};startSize=10;"
            f"endArrow={end_card};endSize=10;"
            f"fontSize=14;"
        )

        edge = ET.SubElement(root_cell, "mxCell",
            id=edge_id, value=label, style=style,
            parent="1", source=src_id, target=tgt_id, edge="1")
        geo = ET.SubElement(edge, "mxGeometry")
        geo.set("relative", "1")
        geo.set("as", "geometry")

    return root


def main():
    root = build_xml()
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")

    output_path = "erd.drawio"
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)
    print(f"Generated: {output_path}")

    # Print layout summary
    print("\n=== Layout Summary ===")
    for name in TABLES:
        x, y = POSITIONS[name]
        h = calc_table_height(TABLES[name]["fields"])
        col = "Col1" if x == COL1_X else ("Col2" if x == COL2_X else "Col3")
        print(f"  {name:20s} → {col} ({x:4d}, {y:4d}) h={h}")


if __name__ == "__main__":
    main()
