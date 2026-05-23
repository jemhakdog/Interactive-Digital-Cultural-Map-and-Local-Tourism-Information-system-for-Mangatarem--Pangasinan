import re

file_path = 'd:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove UK (Unique Key) since teacher said it's not needed, we only need PK and FK.
# They are represented as value="UK"
content = re.sub(r'value="UK"', 'value=""', content)

# 2. Fix PK inconsistency: profile_id -> id
# The heritage detail tables use profile_id as their PK instead of id.
# We will replace value="profile_id" with value="id"
content = re.sub(r'value="profile_id"', 'value="id"', content)

# 3. Fix FK inconsistency: some fields are missing the _id suffix
# reviewed_by -> reviewed_by_id
content = re.sub(r'value="reviewed_by"', 'value="reviewed_by_id"', content)

# logged_by -> logged_by_id
content = re.sub(r'value="logged_by"', 'value="logged_by_id"', content)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("ERD fixes applied successfully.")
