import json
import os

log_path = r'C:\Users\jem\.gemini\antigravity\brain\f16e497e-2b4e-4c96-826b-30e151f5b9b4\.system_generated\logs\overview.txt'

with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    last_model_turn = json.loads(lines[23]) # line 24 is index 23
with open(r'd:\porjects\capstone_system\scratch\extracted_plan.md', 'w', encoding='utf-8') as out:
    out.write(last_model_turn['content'])

