import re

with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Restore ternary operators
text = re.sub(r'\bŞ\b', '?', text) # This might not match because Ş is a word character!
# Let's be more specific: match space + Ş + space, or ) + space + Ş + space
text = text.replace(' Ş ', ' ? ')
text = text.replace(') Ş ', ') ? ')
text = text.replace('] Ş ', '] ? ')
text = text.replace('\' Ş ', '\' ? ')
text = text.replace('" Ş ', '" ? ')

# Also restore the regex replace I broke: /<br\s*\/Ş>/gi
text = text.replace('/<br\\s*\\/Ş>/gi', '/<br\\s*\\/?>/gi')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
