import xml.etree.ElementTree as ET
import os

def verify_v2():
    v2_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v2.drawio"
    
    if not os.path.exists(v2_path):
        print(f"FAIL: File {v2_path} does not exist!")
        return False
        
    try:
        tree = ET.parse(v2_path)
        root = tree.getroot()
    except Exception as e:
        print(f"FAIL: XML parse error on {v2_path}: {e}")
        return False
        
    print("SUCCESS: File is well-formed XML.")

    # 1. Assert all 10 new tables are present
    expected_tables = {
        "erd_table_2000": "PASSWORD_RESET_TOKEN",
        "erd_table_2001": "NEWSLETTER_SUBSCRIBER",
        "erd_table_2002": "DATABASE_AUDIT_LOG",
        "erd_table_2003": "ESTABLISHMENT",
        "erd_table_2004": "ESTABLISHMENT_ROOM",
        "erd_table_2005": "ESTABLISHMENT_MENU_ITEM",
        "erd_table_2006": "ESTABLISHMENT_REVIEW",
        "erd_table_2007": "USER_FAVORITE_ESTABLISHMENT",
        "erd_table_2008": "VISITOR_LOG",
        "erd_table_2009": "REVIEW_PHOTO"
    }

    found_tables = {}
    bounding_boxes = []

    for cell in root.iter('mxCell'):
        cid = cell.get('id')
        if cid in expected_tables:
            val = cell.get('value')
            geom = cell.find('mxGeometry')
            if geom is not None:
                x = float(geom.get('x', 0))
                y = float(geom.get('y', 0))
                w = float(geom.get('width', 0))
                h = float(geom.get('height', 0))
                found_tables[cid] = {
                    "name": val,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                }
                bounding_boxes.append((val, x, y, w, h))

    # Output verification details
    print(f"\n--- Injected Tables Found: {len(found_tables)}/10 ---")
    for cid, data in found_tables.items():
        print(f"ID: {cid} | Name: {data['name']} | Coords: x={data['x']}, y={data['y']}, w={data['w']}, h={data['h']}")

    missing = set(expected_tables.keys()) - set(found_tables.keys())
    if missing:
        print(f"FAIL: Missing {len(missing)} tables: {missing}")
        return False
    else:
        print("SUCCESS: All 10 tables were programmatically injected successfully.")

    # 2. Check for bounding box coordinate overlaps (intersection test)
    # Check new tables against each other
    overlap_detected = False
    for i in range(len(bounding_boxes)):
        name1, x1, y1, w1, h1 = bounding_boxes[i]
        for j in range(i + 1, len(bounding_boxes)):
            name2, x2, y2, w2, h2 = bounding_boxes[j]
            
            # Simple 2D bounding box intersection test
            # If overlap occurs horizontally AND vertically
            x_overlap = (x1 < x2 + w2) and (x1 + w1 > x2)
            y_overlap = (y1 < y2 + h2) and (y1 + h1 > y2)
            
            if x_overlap and y_overlap:
                print(f"WARNING: Overlap detected between '{name1}' and '{name2}'!")
                overlap_detected = True

    if not overlap_detected:
        print("SUCCESS: 2D Collision test passed. Zero coordinate intersections between new tables!")
    else:
        print("FAIL: Coordination collisions detected.")
        return False
        
    return True

if __name__ == '__main__':
    verify_v2()
