import xml.etree.ElementTree as ET
import sys
import uuid

def create_diagram_xml():
    """Generates the XML structure for the new DRD page."""
    # Define nodes for the sequential process map
    nodes = [
        {"id": "p1", "value": "Manual Field Survey<br/>(Word Forms / Paper)", "x": 40, "y": 40, "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1"},
        {"id": "p2", "value": "System Digitization<br/>(Barangay/Admin Entry)", "x": 280, "y": 40, "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1"},
        {"id": "p3", "value": "Admin Validation<br/>(Tourism Office Review)", "x": 520, "y": 40, "style": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1"},
        {"id": "p4", "value": "Relational Database Sync<br/>(Supabase Storage)", "x": 760, "y": 40, "style": "shape=datastore;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1"},
        {"id": "p5", "value": "Georeferencing & Processing<br/>(GIS Mapping)", "x": 1000, "y": 40, "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1"},
        {"id": "p6", "value": "Public Interactive Map<br/>(Digital Discovery)", "x": 1240, "y": 40, "style": "ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1"},
    ]

    # Define edges (sequential flow)
    edges = [
        {"id": "e1", "source": "p1", "target": "p2"},
        {"id": "e2", "source": "p2", "target": "p3"},
        {"id": "e3", "source": "p3", "target": "p4", "label": "Approved"},
        {"id": "e4", "source": "p4", "target": "p5"},
        {"id": "e5", "source": "p5", "target": "p6"},
        {"id": "e6", "source": "p3", "target": "p2", "label": "Revisions Needed", "style": "edgeStyle=orthogonalEdgeStyle;curved=1;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=1;"},
    ]

    # Create MX structure
    mx_model = ET.Element('mxGraphModel', {
        'dx': '1422', 'dy': '794', 'grid': '1', 'gridSize': '10', 
        'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1', 
        'fold': '1', 'page': '1', 'pageScale': '1', 'pageWidth': '1500', 
        'pageHeight': '500', 'math': '0', 'shadow': '0'
    })
    root = ET.SubElement(mx_model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})

    # Add Nodes
    for node in nodes:
        cell = ET.SubElement(root, 'mxCell', {
            'id': node['id'],
            'value': node['value'],
            'style': node['style'],
            'vertex': '1',
            'parent': '1'
        })
        ET.SubElement(cell, 'mxGeometry', {
            'x': str(node['x']), 'y': str(node['y']), 
            'width': '180' if node['id'] != 'p3' else '200', 
            'height': '80' if node['id'] != 'p3' else '120', 
            'as': 'geometry'
        })

    # Add Edges
    for edge in edges:
        style = edge.get('style', 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;')
        cell = ET.SubElement(root, 'mxCell', {
            'id': edge['id'],
            'value': edge.get('label', ''),
            'style': style,
            'edge': '1',
            'parent': '1',
            'source': edge['source'],
            'target': edge['target']
        })
        ET.SubElement(cell, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    return ET.tostring(mx_model, encoding='unicode')

def inject_page(file_path):
    try:
        tree = ET.parse(file_path)
        mxfile = tree.getroot()
        
        # Create new diagram element
        new_diagram = ET.Element('diagram', {
            'name': 'Overall Sequential Process Map',
            'id': f'DRD_{uuid.uuid4().hex[:8]}'
        })
        # Parse the XML string and append as child
        mx_model = ET.fromstring(create_diagram_xml())
        new_diagram.append(mx_model)
        
        # Append to mxfile
        mxfile.append(new_diagram)
        
        # Save
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        print(f"Successfully added 'Overall Sequential Process Map' page to {file_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import os
    
    # Default path relative to the script's root (assuming run from project root)
    default_path = os.path.join("docs", "diagrams", "erd_v1.drawio")
    
    # Use command line argument if provided, else use default
    target_path = sys.argv[1] if len(sys.argv) > 1 else default_path
    
    if not os.path.exists(target_path):
        print(f"Error: File not found at {target_path}")
        sys.exit(1)
        
    inject_page(target_path)
