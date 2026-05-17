import xml.etree.ElementTree as ET

tree = ET.parse('docs/diagrams/system-architecture.drawio')
root = tree.getroot()

model_root = root.find('.//root')

ids_to_remove = [
    'label-admin', 'icon-staff1', 'icon-staff2', 'icon-staff3', 'icon-clipboard', 
    'label-staff', 'arrow-admin-device', 'arrow-staff-device', 'arrow-guard-device',
    '2', 'icon-admin', 'icon-key',
    '4', 'icon-guard-actor', 'icon-guard-badge', 'label-guard'
]

for cell in list(model_root):
    if cell.get('id') in ids_to_remove:
        model_root.remove(cell)

users = [
    {
        'id_prefix': 'admin',
        'color': '#6495ED', 'stroke': '#4169E1',
        'emoji': '🔑', 'label': 'System Admin',
        'y': 100, 'target': 'icon-laptop'
    },
    {
        'id_prefix': 'brgy',
        'color': '#98FB98', 'stroke': '#2E8B57',
        'emoji': '📋', 'label': 'Barangay Rep.',
        'y': 230, 'target': 'icon-laptop'
    },
    {
        'id_prefix': 'biz',
        'color': '#FFA07A', 'stroke': '#FF4500',
        'emoji': '🏪', 'label': 'Business Owner',
        'y': 360, 'target': 'icon-laptop'
    },
    {
        'id_prefix': 'tourist',
        'color': '#DDA0DD', 'stroke': '#8B008B',
        'emoji': '📷', 'label': 'Tourist / Visitor',
        'y': 490, 'target': 'icon-pc'
    },
    {
        'id_prefix': 'guard',
        'color': '#FFD700', 'stroke': '#DAA520',
        'emoji': '🛡️', 'label': 'Security / Guard\n(Logbook)',
        'y': 620, 'target': 'icon-pc'
    }
]

for u in users:
    prefix = u['id_prefix']
    grp = ET.SubElement(model_root, "mxCell", id=f"group-{prefix}", value="", style="group", parent="1", vertex="1", connectable="0")
    ET.SubElement(grp, "mxGeometry", x="60", y=str(u['y']), width="120", height="90").set("as", "geometry")
    
    act = ET.SubElement(model_root, "mxCell", id=f"icon-{prefix}-actor", value="", style=f"shape=actor;whiteSpace=wrap;html=1;fillColor={u['color']};strokeColor={u['stroke']};", parent=f"group-{prefix}", vertex="1")
    ET.SubElement(act, "mxGeometry", x="40", y="0", width="40", height="60").set("as", "geometry")
    
    bdg = ET.SubElement(model_root, "mxCell", id=f"icon-{prefix}-badge", value=u['emoji'], style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=20;", parent=f"group-{prefix}", vertex="1")
    ET.SubElement(bdg, "mxGeometry", x="70", y="20", width="30", height="30").set("as", "geometry")
    
    lbl = ET.SubElement(model_root, "mxCell", id=f"label-{prefix}", value=u['label'], style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontStyle=1;", parent=f"group-{prefix}", vertex="1")
    ET.SubElement(lbl, "mxGeometry", x="0", y="70", width="120", height="30").set("as", "geometry")
    
    arr = ET.SubElement(model_root, "mxCell", id=f"arrow-{prefix}", value="", style="endArrow=classic;html=1;strokeWidth=3;strokeColor=#6B8E23;exitX=1;exitY=0.5;exitDx=0;exitDy=0;", parent="1", source=f"group-{prefix}", target=u['target'], edge="1")
    ET.SubElement(arr, "mxGeometry", width="50", height="50", relative="1").set("as", "geometry")

tree.write('docs/diagrams/system-architecture.drawio', encoding='utf-8', xml_declaration=True)
print("Updated successfully.")
