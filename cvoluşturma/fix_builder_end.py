with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
# Remove the two lines we appended
with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.writelines(lines[:-2])
