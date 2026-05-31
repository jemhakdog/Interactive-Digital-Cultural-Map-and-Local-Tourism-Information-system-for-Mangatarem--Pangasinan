import xml.etree.ElementTree as ET
import os

def add_newsletter_line():
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

    # Find NEWSLETTER_SUBSCRIBER table shape
    subscriber_table = None
    for cell in mx_root.findall('mxCell'):
        val = cell.attrib.get('value', '')
        if 'NEWSLETTER_SUBSCRIBER' in val and 'shape=table' in cell.attrib.get('style', ''):
            subscriber_table = cell
            break

    if subscriber_table is None:
        print("Error: NEWSLETTER_SUBSCRIBER table not found.")
        return

    table_id = subscriber_table.attrib['id']
    print(f"Found NEWSLETTER_SUBSCRIBER table with ID: {table_id}")

    # Increase table height to fit the new row (current height is 161, we make it 195)
    geom = subscriber_table.find('mxGeometry')
    if geom is not None:
        geom.attrib['height'] = '195'
        print("Updated table geometry height to 195.")

    # Create the user_id row elements for NEWSLETTER_SUBSCRIBER
    # ID: erd_table_2001_row_4
    row_id = f"{table_id}_row_4"
    
    # Check if row already exists
    exists = any(cell.attrib.get('id') == row_id for cell in mx_root.findall('mxCell'))
    if not exists:
        # Create row container
        row = ET.Element('mxCell')
        row.attrib['id'] = row_id
        row.attrib['parent'] = table_id
        row.attrib['style'] = "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;right=0;bottom=0;"
        row.attrib['value'] = ""
        row.attrib['vertex'] = "1"
        row_geom = ET.SubElement(row, 'mxGeometry')
        row_geom.attrib['height'] = '34'
        row_geom.attrib['width'] = '560'
        row_geom.attrib['y'] = '161'
        row_geom.attrib['as'] = 'geometry'
        mx_root.append(row)

        # Col 0: FK label
        col0 = ET.Element('mxCell')
        col0.attrib['id'] = f"{row_id}_col_0"
        col0.attrib['parent'] = row_id
        col0.attrib['style'] = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=2;overflow=hidden;fontSize=16;fontStyle=5;"
        col0.attrib['value'] = "(FK)"
        col0.attrib['vertex'] = "1"
        c0_geom = ET.SubElement(col0, 'mxGeometry')
        c0_geom.attrib['height'] = '34'
        c0_geom.attrib['width'] = '50'
        c0_geom.attrib['as'] = 'geometry'
        mx_root.append(col0)

        # Col 1: user_id field
        col1 = ET.Element('mxCell')
        col1.attrib['id'] = f"{row_id}_col_1"
        col1.attrib['parent'] = row_id
        col1.attrib['style'] = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=2;overflow=hidden;fontSize=16;fontStyle=5;"
        col1.attrib['value'] = "user_id"
        col1.attrib['vertex'] = "1"
        c1_geom = ET.SubElement(col1, 'mxGeometry')
        c1_geom.attrib['height'] = '34'
        c1_geom.attrib['width'] = '200'
        c1_geom.attrib['x'] = '50'
        c1_geom.attrib['as'] = 'geometry'
        mx_root.append(col1)

        # Col 2: int type
        col2 = ET.Element('mxCell')
        col2.attrib['id'] = f"{row_id}_col_2"
        col2.attrib['parent'] = row_id
        col2.attrib['style'] = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=2;overflow=hidden;fontSize=16;"
        col2.attrib['value'] = "int"
        col2.attrib['vertex'] = "1"
        c2_geom = ET.SubElement(col2, 'mxGeometry')
        c2_geom.attrib['height'] = '34'
        c2_geom.attrib['width'] = '100'
        c2_geom.attrib['x'] = '250'
        c2_geom.attrib['as'] = 'geometry'
        mx_root.append(col2)

        # Col 3: -> USER.id description
        col3 = ET.Element('mxCell')
        col3.attrib['id'] = f"{row_id}_col_3"
        col3.attrib['parent'] = row_id
        col3.attrib['style'] = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=2;overflow=hidden;fontSize=16;"
        col3.attrib['value'] = "→ USER.id"
        col3.attrib['vertex'] = "1"
        c3_geom = ET.SubElement(col3, 'mxGeometry')
        c3_geom.attrib['height'] = '34'
        c3_geom.attrib['width'] = '210'
        c3_geom.attrib['x'] = '350'
        c3_geom.attrib['as'] = 'geometry'
        mx_root.append(col3)

        print("Added user_id column row to NEWSLETTER_SUBSCRIBER table shape.")
    else:
        print("user_id column row already exists in NEWSLETTER_SUBSCRIBER table shape.")

    # Add the edge from NEWSLETTER_SUBSCRIBER to USER (erd_1001)
    edge_id = "erd_edge_newsletter_to_user"
    edge_exists = any(cell.attrib.get('id') == edge_id for cell in mx_root.findall('mxCell'))
    
    if not edge_exists:
        edge = ET.Element('mxCell')
        edge.attrib['id'] = edge_id
        edge.attrib['edge'] = '1'
        edge.attrib['parent'] = '1'
        edge.attrib['source'] = table_id
        edge.attrib['target'] = 'erd_1001' # USER table ID
        # Premium orthogonal style with rounded corners
        edge.attrib['style'] = (
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
            "exitX=0.25;"
            "exitY=0;"
            "exitDx=0;"
            "exitDy=0;"
        )
        edge.attrib['value'] = "user_id"
        
        edge_geom = ET.SubElement(edge, 'mxGeometry')
        edge_geom.attrib['relative'] = '1'
        edge_geom.attrib['as'] = 'geometry'
        
        mx_root.append(edge)
        print("Added relationship edge from NEWSLETTER_SUBSCRIBER to USER.")
    else:
        print("Relationship edge already exists.")

    tree.write(file_path, encoding='utf-8', xml_declaration=False)
    print("Successfully updated draw.io file!")

if __name__ == '__main__':
    add_newsletter_line()
