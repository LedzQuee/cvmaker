with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
old_event = r"var eventType = input\.type === 'checkbox' \? 'change' : 'input';\s*input\.addEventListener\(eventType, function \(\) \{"
new_event = '''['input', 'change'].forEach(function(evt) {
                input.addEventListener(evt, function () {'''

text = re.sub(old_event, new_event, text)

# We must close the forEach loop. The original ends with:
#                updatePreview();
#            });
#        });
old_end = r"updatePreview\(\);\s*\}\);"
new_end = "updatePreview();\n                });\n            });"

text = re.sub(old_end, new_end, text)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
