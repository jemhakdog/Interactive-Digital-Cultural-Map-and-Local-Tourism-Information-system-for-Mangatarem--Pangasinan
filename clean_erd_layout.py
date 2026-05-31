import xml.etree.ElementTree as ET
import os

def clean_erd_drawio():
    file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    tree = ET.parse(file_path)
    root = tree.getroot()
    mx_root = root.find('.//root')
    
    if mx_root is None:
        print("Error: Could not find mxGraphModel root.")
        return

    edge_count = 0
    cleaned_points = 0
    
    # Elegant, premium design style for ERD relation lines (dark slate, rounded, clean orthogonal)
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

    for cell in mx_root.findall('mxCell'):
        # Check if cell is an edge
        if cell.attrib.get('edge') == '1':
            edge_count += 1
            # 1. Update style to the clean, premium style
            # If the edge has a label value (e.g. FK name), preserve it
            cell.attrib['style'] = premium_edge_style
            
            # 2. Find mxGeometry and strip manual routing/bend points
            geom = cell.find('mxGeometry')
            if geom is not None:
                # Remove any custom path points (Array/mxPoint elements) that force line overlays or internal crossing
                points_arr = geom.find('Array')
                if points_arr is not None:
                    geom.remove(points_arr)
                    cleaned_points += 1
                    
                for pt in list(geom.findall('mxPoint')):
                    # Keep only 'as="sourcePoint"' or 'as="targetPoint"' if they are structural,
                    # remove others which represent manual bend overrides.
                    if pt.attrib.get('as') not in ['sourcePoint', 'targetPoint']:
                        geom.remove(pt)
                        cleaned_points += 1

    print(f"Total edges found: {edge_count}")
    print(f"Total manual points/bends stripped: {cleaned_points}")
    
    # Save the updated drawio file
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    print("Successfully cleaned up erd_v2.drawio!")

if __name__ == '__main__':
    clean_erd_drawio()
