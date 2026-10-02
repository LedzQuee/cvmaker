with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
old_iframe_styles = '''        iframe.style.position = 'fixed';
        iframe.style.right = '0';
        iframe.style.bottom = '0';
        iframe.style.width = '0';
        iframe.style.height = '0';
        iframe.style.border = 'none';'''

new_iframe_styles = '''        iframe.style.position = 'fixed';
        iframe.style.right = '0';
        iframe.style.bottom = '0';
        iframe.style.width = '210mm';
        iframe.style.height = '297mm';
        iframe.style.visibility = 'hidden';
        iframe.style.zIndex = '-1';
        iframe.style.border = 'none';'''

text = text.replace(old_iframe_styles, new_iframe_styles)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
