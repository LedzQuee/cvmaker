with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[-30:]):
    print(f"{len(lines)-30+i+1}: {line.rstrip()}")
