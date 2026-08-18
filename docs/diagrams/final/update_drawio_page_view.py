import os
import re

files_to_update = [
    'docs/diagrams/final/erd_v1.drawio',
    'docs/diagrams/final/dfd-level-0.drawio',
    'docs/diagrams/final/dfd-level-1-clean_v1.drawio',
    'docs/diagrams/final/dfd-level-1-clean.drawio'
]

for file_path in files_to_update:
    if not os.path.exists(file_path):
        continue
        
    print(f'Updating {file_path}')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Uppercase headers
    content = re.sub(r'>PAGE_VIEW<', '>ANALYTICS_PAGE_VIEW<', content)
    content = re.sub(r'"PAGE_VIEW"', '"ANALYTICS_PAGE_VIEW"', content)
    
    # Just in case there's any lowercase instances
    content = re.sub(r'value="page_view"', 'value="analytics_page_view"', content)
    content = re.sub(r'>page_view<', '>analytics_page_view<', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated diagrams successfully')
