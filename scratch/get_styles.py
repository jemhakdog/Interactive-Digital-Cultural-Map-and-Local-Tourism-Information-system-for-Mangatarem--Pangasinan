import xml.etree.ElementTree as ET
import os

def print_styles():
    erd_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v1.drawio"
    if not os.path.exists(erd_path):
        return
        
    tree = ET.parse(erd_path)
    root = tree.getroot()
    
    # Let's find erd_1083 and all cells that have parent='erd_1083'
    row_cell = None
    sub_cells = []
    
    for cell in root.iter('mxCell'):
        cid = cell.get('id')
        parent = cell.get('parent')
        if cid == 'erd_1083':
            row_cell = cell
        elif parent == 'erd_1083':
            sub_cells.append(cell)
            
    if row_cell is not None:
        print(f"Row ID: {row_cell.get('id')}")
        print(f"  Style: {row_cell.get('style')}")
        geom = row_cell.find('mxGeometry')
        if geom is not None:
            print(f"  Geometry: x={geom.get('x')}, y={geom.get('y')}, w={geom.get('width')}, h={geom.get('height')}")
            
    for sc in sub_cells:
        print(f"Subcell ID: {sc.get('id')}")
        print(f"  Value: {sc.get('value')}")
        print(f"  Style: {sc.get('style')}")
        geom = sc.find('mxGeometry')
        if geom is not None:
            print(f"  Geometry: x={geom.get('x')}, y={geom.get('y')}, w={geom.get('width')}, h={geom.get('height')}")
        print()

if __name__ == '__main__':
    print_styles()
