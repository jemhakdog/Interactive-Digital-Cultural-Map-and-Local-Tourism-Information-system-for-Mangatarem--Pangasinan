import xml.etree.ElementTree as ET
import html
import re

def clean_html(text):
    if not text:
        return ""
    # Unescape HTML entities
    text = html.unescape(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', ' ', text)
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_drawio_labels(file_path):
    print(f"=== Labels in {file_path} ===")
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        labels = set()
        for cell in root.findall('.//mxCell'):
            val = cell.attrib.get('value', '')
            cleaned = clean_html(val)
            if cleaned:
                labels.add(cleaned)
        for label in sorted(labels):
            print(f"  - {label}")
    except Exception as e:
        print(f"Error parsing: {e}")
    print()

parse_drawio_labels("docs/diagrams/dfd/dfd-level-1-clean_v3.drawio")
