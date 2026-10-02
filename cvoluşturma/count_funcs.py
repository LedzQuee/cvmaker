with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()
import re
print("updatePreview occurrences:", text.count('function updatePreview'))
print("init occurrences:", text.count('function init()'))
