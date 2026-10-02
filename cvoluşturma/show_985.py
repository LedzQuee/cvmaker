import sys
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

for i, line in enumerate(text.split('\n')):
    if 980 < i+1 < 1000:
        clean = line.strip().encode('ascii', 'ignore').decode('ascii')
        print(f'Line {i+1}: {clean}')
