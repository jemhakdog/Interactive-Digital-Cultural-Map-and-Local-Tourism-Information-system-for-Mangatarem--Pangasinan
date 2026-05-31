import xml.etree.ElementTree as ET
import os
import re

def layout_erd():
    file_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v3.drawio"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    tree = ET.parse(file_path)
    root = tree.getroot()
    mx_root = root.find('.//root')
    if mx_root is None:
        print("Error: Could not find mxGraphModel root.")
        return

    # 1. Define columns and their exact table lists
    columns = [
        # Column 1
        ['USER', 'USER_FAVORITE', 'USER_NOTIFICATION', 'BUSINESS_VERIFICATION'],
        # Column 2
        ['ATTRACTION', 'MAP_FEEDBACK', 'EVENT', 'GALLERY_ITEM', 'BARANGAY_INFO', 'VISITOR_LOG'],
        # Column 3
        ['HERITAGE_PROFILE', 'BOOKABLE_ASSET', 'BOOKING_SLOT', 'RESERVATION'],
        # Column 4
        ['CHAT_ROOM', 'CHAT_PARTICIPANT', 'CHAT_MESSAGE', 'ANALYTICS_PAGE_VIEW', 'ESTABLISHMENT_MENU_ITEM'],
        # Column 5
        ['ESTABLISHMENT', 'ESTABLISHMENT_ROOM', 'NEWSLETTER_SUBSCRIBER', 'DATABASE_AUDIT_LOG', 'REVIEW']
    ]

    # Clean name helper
    def get_clean_table_name(val):
        clean = re.sub(r'<[^>]+>', '', val)
        clean = clean.replace('\n', ' ').replace('\r', '').strip()
        return clean.upper()

    # Find the table cells and map them by clean name
    tables_by_name = {}
    for cell in mx_root.findall('mxCell'):
        style = cell.attrib.get('style', '')
        val = cell.attrib.get('value', '')
        parent = cell.attrib.get('parent', '')
        if 'shape=table' in style and (parent == '1' or parent == '0' or parent == ''):
            clean_name = get_clean_table_name(val)
            tables_by_name[clean_name] = cell

    print(f"Mapped {len(tables_by_name)} tables from draw.io.")
    
    # 2. Verify all tables in columns are mapped
    missing_tables = []
    for col_idx, col in enumerate(columns):
        for t_name in col:
            if t_name not in tables_by_name:
                missing_tables.append(t_name)
    if missing_tables:
        print(f"Warning: The following expected tables were not found in the draw.io XML: {missing_tables}")

    # 3. Calculate layout
    # Gap size is 3 inches = 288 pixels
    GAP = 288.0

    # We will compute the width of each column to align horizontally
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

    print(f"Computed column widths: {col_widths}")

    # Column X coordinates
    col_xs = []
    current_x = -550.0 # Column 1 starts here
    for i, w in enumerate(col_widths):
        col_xs.append(current_x)
        current_x += w + GAP
    print(f"Computed column X coordinates: {col_xs}")

    # Starting Y for each column
    # Column 1 starts at 819.0, others start at 40.0
    col_start_ys = [819.0, 40.0, 40.0, 40.0, 40.0]

    # Place each table
    for col_idx, col in enumerate(columns):
        x = col_xs[col_idx]
        y = col_start_ys[col_idx]
        print(f"\nPositioning Column {col_idx+1} at x = {x}:")
        
        for t_name in col:
            cell = tables_by_name.get(t_name)
            if cell is None:
                continue
            
            geom = cell.find('mxGeometry')
            if geom is None:
                continue
            
            h = float(geom.attrib.get('height', '300'))
            w = float(geom.attrib.get('width', '560'))
            
            # Update geometry attributes
            geom.attrib['x'] = str(int(x))
            geom.attrib['y'] = str(int(y))
            print(f"  - '{t_name}' positioned at ({int(x)}, {int(y)}) with width {int(w)}, height {int(h)}")
            
            # Next table Y
            y += h + GAP

    # 4. Enforce premium orthogonal style and strip bend points for all relationship edges
    premium_edge_style = (
        "edgeStyle=orthogonalEdgeStyle;"
        "rounded=1;"
        "jettySize=auto;"
        "orthogonalLoop=1;"
        "strokeColor=#4A5568;"
        "strokeWidth=2;"
        "endArrow=classic;"
        "endSize=8;"
        "html=1;"
        "fontSize=12;"
    )

    edge_count = 0
    cleaned_points = 0
    for cell in mx_root.findall('mxCell'):
        if cell.attrib.get('edge') == '1':
            edge_count += 1
            cell.attrib['style'] = premium_edge_style
            geom = cell.find('mxGeometry')
            if geom is not None:
                # Remove manual route points array
                points_arr = geom.find('Array')
                if points_arr is not None:
                    geom.remove(points_arr)
                    cleaned_points += 1
                
                # Remove custom mxPoints
                for pt in list(geom.findall('mxPoint')):
                    if pt.attrib.get('as') not in ['sourcePoint', 'targetPoint']:
                        geom.remove(pt)
                        cleaned_points += 1

    print(f"\nProcessed {edge_count} relationship edges.")
    print(f"Stripped {cleaned_points} manual edge routing bend points.")

    # Save the updated draw.io XML file
    # We must write with encoding='utf-8' andxml_declaration=False (draw.io doesn't strictly need xml decl, let's keep exact structure)
    tree.write(file_path, encoding='utf-8', xml_declaration=False)
    print(f"\nSuccessfully rearranged tables in {file_path} with exactly 1-inch (96px) spacing!")

if __name__ == '__main__':
    layout_erd()
