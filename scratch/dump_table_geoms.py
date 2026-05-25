import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

table_ids = ['erd_1001', 'erd_1037', 'erd_table_6009', 'erd_table_2009']
for cell in mx_root.findall('mxCell'):
    cid = cell.attrib.get('id')
    if cid in table_ids:
        print(f"Table Found: ID={cid}, Name={cell.attrib.get('value')}")
        geom = cell.find('mxGeometry')
        if geom is not None:
            print(f"  Geometry: {geom.attrib}")
