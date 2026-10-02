with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'setVal\(\'website\', pi\.website\);', text)
if match:
    original = match.group(0)
    text = text.replace(original, "setVal('website', pi.website);\n        setVal('driversLicense', pi.driversLicense);")
    with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Success updating JS")
else:
    print("Failed to find website setVal")
