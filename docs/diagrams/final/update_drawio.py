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

    content = re.sub(r'"FAVORITE"', '"USER_FAVORITE_ATTRACTION"', content)
    content = re.sub(r'>FAVORITE<', '>USER_FAVORITE_ATTRACTION<', content)
    
    content = re.sub(r'"REVIEW"', '"ATTRACTION_REVIEW"', content)
    content = re.sub(r'>REVIEW<', '>ATTRACTION_REVIEW<', content)
    
    content = re.sub(r'"EVENT_INTEREST"', '"USER_EVENT_INTEREST"', content)
    content = re.sub(r'>EVENT_INTEREST<', '>USER_EVENT_INTEREST<', content)

    content = re.sub(r'value="favorite"', 'value="user_favorite_attraction"', content)
    content = re.sub(r'value="review"', 'value="attraction_review"', content)
    content = re.sub(r'value="event_interest"', 'value="user_event_interest"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated diagrams successfully')
