with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace init function body with a try-catch
import re
# Find function init() {
init_match = re.search(r'function init\(\) \{[\s\S]*?\n    \}', text)
if init_match:
    original_init = init_match.group(0)
    # wrap the body
    body = original_init[original_init.find('{')+1:original_init.rfind('}')]
    new_init = f'''function init() {{
        try {{
            {body}
        }} catch (err) {{
            console.error(err);
            alert("Init Hatası: " + err.message + "\\nSatır: " + (err.lineNumber || err.line || "?"));
            isInitialized = true; // Try to force it to allow some interaction
        }}
    }}'''
    text = text.replace(original_init, new_init)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
