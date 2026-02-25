import xml.etree.ElementTree as ET
import os

def create_flowchart(file_path):
    # Create the root element
    mxfile = ET.Element('mxfile', {
        'host': 'app.diagrams.net',
        'agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'version': '24.7.5'
    })
    
    # --- PAGE 1: ORGANIZATION WORKFLOW ---
    diagram_org = ET.SubElement(mxfile, 'diagram', {
        'id': 'OrgWorkflow',
        'name': 'Organization Workflow (Existing)'
    })
    
    mxGraphModel_org = ET.SubElement(diagram_org, 'mxGraphModel', {
        'dx': '1422',
        'dy': '762',
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '850',
        'pageHeight': '1100',
        'math': '0',
        'shadow': '0'
    })
    
    root_org = ET.SubElement(mxGraphModel_org, 'root')
    ET.SubElement(root_org, 'mxCell', {'id': '0'})
    ET.SubElement(root_org, 'mxCell', {'id': '1', 'parent': '0'})
    
    # Styles
    style_start = "rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1"
    style_bottleneck = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1"
    style_manual = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#ffe6cc;strokeColor=#d79b00;"
    style_storage = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;"
    style_decision = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    style_end = "rounded=1;whiteSpace=wrap;html=1;arcSize=50;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1"
    style_edge = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"

    # Org Content
    start = ET.SubElement(root_org, 'mxCell', {'id': 'org_start', 'value': 'Start: Need for Cultural Data', 'style': style_start, 'vertex': '1', 'parent': '1'})
    ET.SubElement(start, 'mxGeometry', {'x': '340', 'y': '40', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    step1 = ET.SubElement(root_org, 'mxCell', {'id': 'org_step1', 'value': 'Manual Field Survey\n(Forms 01A-07)', 'style': style_bottleneck, 'vertex': '1', 'parent': '1'})
    ET.SubElement(step1, 'mxGeometry', {'x': '340', 'y': '140', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    step2 = ET.SubElement(root_org, 'mxCell', {'id': 'org_step2', 'value': 'Manual Encoding\n(Word/Excel)', 'style': style_bottleneck, 'vertex': '1', 'parent': '1'})
    ET.SubElement(step2, 'mxGeometry', {'x': '340', 'y': '240', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    step3 = ET.SubElement(root_org, 'mxCell', {'id': 'org_step3', 'value': 'Physical/Email Submission\nto Tourism Office', 'style': style_manual, 'vertex': '1', 'parent': '1'})
    ET.SubElement(step3, 'mxGeometry', {'x': '340', 'y': '340', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    decision = ET.SubElement(root_org, 'mxCell', {'id': 'org_decision', 'value': 'Manual Review by\nTourism Officer', 'style': style_decision, 'vertex': '1', 'parent': '1'})
    ET.SubElement(decision, 'mxGeometry', {'x': '360', 'y': '440', 'width': '140', 'height': '140', 'as': 'geometry'})
    
    step4 = ET.SubElement(root_org, 'mxCell', {'id': 'org_step4', 'value': 'Physical Filing /\nLocal File Storage', 'style': style_storage, 'vertex': '1', 'parent': '1'})
    ET.SubElement(step4, 'mxGeometry', {'x': '360', 'y': '620', 'width': '140', 'height': '80', 'as': 'geometry'})

    step5 = ET.SubElement(root_org, 'mxCell', {'id': 'org_step5', 'value': 'Manual Retrieval\n(Walk-in/Request)', 'style': style_manual, 'vertex': '1', 'parent': '1'})
    ET.SubElement(step5, 'mxGeometry', {'x': '340', 'y': '740', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    end = ET.SubElement(root_org, 'mxCell', {'id': 'org_end', 'value': 'Information Provided\n(Paper/Soft Copy)', 'style': style_end, 'vertex': '1', 'parent': '1'})
    ET.SubElement(end, 'mxGeometry', {'x': '340', 'y': '840', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    # Org Edges
    edges_org = [
        ('org_start', 'org_step1', ''),
        ('org_step1', 'org_step2', ''),
        ('org_step2', 'org_step3', ''),
        ('org_step3', 'org_decision', ''),
        ('org_decision', 'org_step4', 'Approved'),
        ('org_decision', 'org_step3', 'Return for Correction'),
        ('org_step4', 'org_step5', ''),
        ('org_step5', 'org_end', '')
    ]
    
    for i, (src, tgt, val) in enumerate(edges_org):
        style = style_edge
        if val == 'Return for Correction':
             style += "entryX=1;entryY=0.5;exitX=1;exitY=0.5;"
        edge = ET.SubElement(root_org, 'mxCell', {'id': f'org_edge{i}', 'value': val, 'style': style, 'edge': '1', 'parent': '1', 'source': src, 'target': tgt})
        ET.SubElement(edge, 'mxGeometry', {'relative': '1', 'as': 'geometry'})


    # --- PAGE 2: TOURIST WORKFLOW ---
    diagram_tourist = ET.SubElement(mxfile, 'diagram', {
        'id': 'TouristWorkflow',
        'name': 'Tourist/Public User Workflow (Existing)'
    })
    
    mxGraphModel_tourist = ET.SubElement(diagram_tourist, 'mxGraphModel', {
        'dx': '1422',
        'dy': '762',
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '850',
        'pageHeight': '1100',
        'math': '0',
        'shadow': '0'
    })
    
    root_tourist = ET.SubElement(mxGraphModel_tourist, 'root')
    ET.SubElement(root_tourist, 'mxCell', {'id': '0'})
    ET.SubElement(root_tourist, 'mxCell', {'id': '1', 'parent': '0'})

    # Tourist Content
    t_start = ET.SubElement(root_tourist, 'mxCell', {'id': 't_start', 'value': 'Start: Tourist Arrives\nin Mangatarem', 'style': style_start, 'vertex': '1', 'parent': '1'})
    ET.SubElement(t_start, 'mxGeometry', {'x': '340', 'y': '40', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    t_step1 = ET.SubElement(root_tourist, 'mxCell', {'id': 't_step1', 'value': 'Visit Municipal Tourism Office\n(Physical Visit)', 'style': style_manual, 'vertex': '1', 'parent': '1'})
    ET.SubElement(t_step1, 'mxGeometry', {'x': '340', 'y': '140', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    t_step2 = ET.SubElement(root_tourist, 'mxCell', {'id': 't_step2', 'value': 'Request Information/\nBrochures', 'style': style_manual, 'vertex': '1', 'parent': '1'})
    ET.SubElement(t_step2, 'mxGeometry', {'x': '340', 'y': '240', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    t_step3 = ET.SubElement(root_tourist, 'mxCell', {'id': 't_step3', 'value': 'Receive Paper Map /\nVerbal Directions', 'style': style_storage, 'vertex': '1', 'parent': '1'})
    ET.SubElement(t_step3, 'mxGeometry', {'x': '340', 'y': '340', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    t_step4 = ET.SubElement(root_tourist, 'mxCell', {'id': 't_step4', 'value': 'Manual Navigation to Site\n(No GPS/Digital Map)', 'style': style_bottleneck, 'vertex': '1', 'parent': '1'})
    ET.SubElement(t_step4, 'mxGeometry', {'x': '340', 'y': '440', 'width': '180', 'height': '60', 'as': 'geometry'})
    
    t_end = ET.SubElement(root_tourist, 'mxCell', {'id': 't_end', 'value': 'Visit Attraction\n(Risk: Closed/Hard to Find)', 'style': style_end, 'vertex': '1', 'parent': '1'})
    ET.SubElement(t_end, 'mxGeometry', {'x': '340', 'y': '540', 'width': '180', 'height': '60', 'as': 'geometry'})

    # Tourist Edges
    edges_tourist = [
        ('t_start', 't_step1', ''),
        ('t_step1', 't_step2', ''),
        ('t_step2', 't_step3', ''),
        ('t_step3', 't_step4', ''),
        ('t_step4', 't_end', '')
    ]
    
    for i, (src, tgt, val) in enumerate(edges_tourist):
        edge = ET.SubElement(root_tourist, 'mxCell', {'id': f't_edge{i}', 'value': val, 'style': style_edge, 'edge': '1', 'parent': '1', 'source': src, 'target': tgt})
        ET.SubElement(edge, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

    # Write to file
    tree = ET.ElementTree(mxfile)
    with open(file_path, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    print(f"Flowchart generated at: {file_path}")

if __name__ == "__main__":
    target_dir = os.path.join("docs", "diagrams")
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "existing_workflow.drawio")
    create_flowchart(target_file)
