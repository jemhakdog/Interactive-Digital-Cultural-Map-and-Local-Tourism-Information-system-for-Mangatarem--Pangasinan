import sys
import xml.etree.ElementTree as ET

file_path = 'docs/diagrams/final/dfd-level-1-clean_v1.drawio'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

try:
    tree = ET.fromstring(content)
    root = tree.find('.//root')
    
    if root is None:
        print("Could not find <root> in XML.")
        sys.exit(1)
        
    labels = ["Natural_Heritage", "Intangible_Heritage", "Cultural_Inst", "LGU_Program", "Personality", "Built_Heritage", "Movable_Heritage", "Heritage Profile", "Heritage Management"]
    
    node_mapping = {}
    edges = []
    
    for cell in root.findall('.//mxCell'):
        value = cell.get('value', '')
        cell_id = cell.get('id', '')
        source = cell.get('source', '')
        target = cell.get('target', '')
        
        # Check if it's an edge
        if cell.get('edge') == '1':
            edges.append(cell)
            continue
            
        # Check if it's a node we care about
        for label in labels:
            if label in value:
                node_mapping[cell_id] = label
                print(f"Found Node: {label} (ID: {cell_id}) -> {value[:30]}...")
                
    print(f"\nTotal Edges: {len(edges)}")
    for edge in edges:
        s = edge.get('source')
        t = edge.get('target')
        if s in node_mapping and t in node_mapping:
            print(f"Edge {edge.get('id')}: {node_mapping[s]} -> {node_mapping[t]} | value='{edge.get('value')}' | style='{edge.get('style')}'")

except ET.ParseError as e:
    print(f"Error parsing XML: {e}")
