import xml.etree.ElementTree as ET
import os
import re
import sys

def verify_erd_layout():
    file_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v3.drawio"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)

    tree = ET.parse(file_path)
    root = tree.getroot()
    mx_root = root.find('.//root')
    if mx_root is None:
        print("Error: Could not find mxGraphModel root.")
        sys.exit(1)

    columns = [
        ['USER', 'USER_FAVORITE', 'USER_NOTIFICATION', 'BUSINESS_VERIFICATION'],
        ['ATTRACTION', 'MAP_FEEDBACK', 'EVENT', 'GALLERY_ITEM', 'BARANGAY_INFO', 'VISITOR_LOG'],
        ['HERITAGE_PROFILE', 'BOOKABLE_ASSET', 'BOOKING_SLOT', 'RESERVATION'],
        ['CHAT_ROOM', 'CHAT_PARTICIPANT', 'CHAT_MESSAGE', 'ANALYTICS_PAGE_VIEW', 'ESTABLISHMENT_MENU_ITEM'],
        ['ESTABLISHMENT', 'ESTABLISHMENT_ROOM', 'NEWSLETTER_SUBSCRIBER', 'DATABASE_AUDIT_LOG', 'REVIEW']
    ]

    def get_clean_table_name(val):
        clean = re.sub(r'<[^>]+>', '', val)
        clean = clean.replace('\n', ' ').replace('\r', '').strip()
        return clean.upper()

    tables_by_name = {}
    for cell in mx_root.findall('mxCell'):
        style = cell.attrib.get('style', '')
        val = cell.attrib.get('value', '')
        parent = cell.attrib.get('parent', '')
        if 'shape=table' in style and (parent == '1' or parent == '0' or parent == ''):
            clean_name = get_clean_table_name(val)
            tables_by_name[clean_name] = cell

    errors = []

    # Verify each column X coordinate alignment and vertical gap
    expected_gap = 288.0
    
    col_widths = []
    for col in columns:
        max_w = 0.0
        for t_name in col:
            cell = tables_by_name.get(t_name)
            if cell is not None:
                geom = cell.find('mxGeometry')
                if geom is not None:
                    w = float(geom.attrib.get('width', '560'))
                    if w > max_w:
                        max_w = w
        col_widths.append(max_w if max_w > 0 else 560.0)

    expected_xs = []
    current_x = -550.0
    for w in col_widths:
        expected_xs.append(current_x)
        current_x += w + expected_gap

    for col_idx, col in enumerate(columns):
        expected_x = expected_xs[col_idx]
        prev_bottom = None
        prev_name = None
        
        for t_name in col:
            cell = tables_by_name.get(t_name)
            if cell is None:
                errors.append(f"Expected table '{t_name}' not found in the diagram.")
                continue
            
            geom = cell.find('mxGeometry')
            if geom is None:
                errors.append(f"Table '{t_name}' has no mxGeometry.")
                continue
            
            x = float(geom.attrib.get('x', '0'))
            y = float(geom.attrib.get('y', '0'))
            w = float(geom.attrib.get('width', '0'))
            h = float(geom.attrib.get('height', '0'))
            
            # Check X alignment
            if abs(x - expected_x) > 0.001:
                errors.append(f"Table '{t_name}' in column {col_idx+1} has X coordinate {x}, expected {expected_x}.")
            
            # Check vertical gap
            if prev_bottom is not None:
                actual_gap = y - prev_bottom
                if abs(actual_gap - expected_gap) > 0.001:
                    errors.append(f"Vertical gap between '{prev_name}' and '{t_name}' is {actual_gap}px, expected {expected_gap}px.")
            
            prev_bottom = y + h
            prev_name = t_name

    # Verify horizontal gap between columns
    for i in range(len(columns) - 1):
        # Max right edge of column i
        max_right = -9999.0
        for t_name in columns[i]:
            cell = tables_by_name.get(t_name)
            if cell is not None:
                geom = cell.find('mxGeometry')
                if geom is not None:
                    x = float(geom.attrib.get('x', '0'))
                    w = float(geom.attrib.get('width', '0'))
                    right = x + w
                    if right > max_right:
                        max_right = right
        
        # Left edge of column i+1
        col_next_x = expected_xs[i+1]
        horizontal_gap = col_next_x - max_right
        if abs(horizontal_gap - expected_gap) > 0.001:
            errors.append(f"Horizontal gap between Column {i+1} and Column {i+2} is {horizontal_gap}px, expected {expected_gap}px.")

    if errors:
        print("VERIFICATION FAILED:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("VERIFICATION SUCCESSFUL: All tables are perfectly aligned with exactly 3-inch (288px) spacing on all sides!")
        sys.exit(0)

if __name__ == '__main__':
    verify_erd_layout()
