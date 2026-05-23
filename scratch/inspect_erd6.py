import re

with open('d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's print all values of shape=partialRectangle that could be fields
cells = re.findall(r'<mxCell [^>]*value="([^"]*)"[^>]*style="shape=partialRectangle;[^>]*>', content)
# Now let's group them in fours (which is typically how they are defined: key, name, type, extra)
for i in range(0, len(cells) - 3, 4):
    c1, c2, c3, c4 = cells[i], cells[i+1], cells[i+2], cells[i+3]
    if c1 in ['PK', 'UK', 'FK'] or 'FK' in c1 or 'PK' in c1:
        print(f"{c1} | {c2} | {c3} | {c4.replace(chr(8594), '->')}")

