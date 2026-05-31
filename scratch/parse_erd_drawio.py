import xml.etree.ElementTree as ET
import html
import re

def clean_html(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r'<[^>]*>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_erd_drawio(file_path):
    print(f"=== Tables in {file_path} ===")
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        tables = []
        for cell in root.findall('.//mxCell'):
            val = cell.attrib.get('value', '')
            style = cell.attrib.get('style', '')
            cleaned = clean_html(val)
            if 'shape=table' in style or 'swimlane' in style or 'table' in style:
                if cleaned and len(cleaned) < 50:
                    tables.append(cleaned)
        for t in sorted(list(set(tables))):
            print(f"  - {t}")
    except Exception as e:
        print(f"Error: {e}")
    print()

parse_erd_drawio("docs/diagrams/erd/erd_v1.drawio")
parse_erd_drawio("docs/diagrams/erd/erd_v2.drawio")
parse_erd_drawio("docs/diagrams/erd/erd_v3.drawio")
