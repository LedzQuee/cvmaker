with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'function updatePreview\(\) \{[\s\S]*?\n    \}', text)
if match:
    original = match.group(0)
    body = original[original.find('{')+1:original.rfind('}')]
    new_func = f'''function updatePreview() {{
        try {{
            {body}
        }} catch (err) {{
            console.error(err);
            alert("Önizleme Hatası: " + err.message);
        }}
    }}'''
    text = text.replace(original, new_func)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
