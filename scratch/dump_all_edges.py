import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

count = 0
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == '1':
        src = cell.attrib.get('source', '')
        tgt = cell.attrib.get('target', '')
        val = cell.attrib.get('value', '')
        
        # skip our newly added ar/fix edges to see original ones
        if 'ar_fix' in cell.attrib.get('id', ''):
            continue
            
        print(f"Edge ID={cell.attrib.get('id')}, Value={repr(val)}")
        print(f"  Source: {src}")
        print(f"  Target: {tgt}")
        print(f"  Style: {cell.attrib.get('style', '')}")
        geom = cell.find('mxGeometry')
        if geom is not None:
            print(f"  Geometry: {geom.attrib}")
            for pt in geom.findall('mxPoint'):
                print(f"    Point: {pt.attrib}")
        count += 1
        if count >= 10:
            break
