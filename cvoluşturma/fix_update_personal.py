with open("wwwroot/js/cv-data.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Fix updatePersonalInfo to not require hasOwnProperty check
old = r"""    function updatePersonalInfo(field, value) {
        if (!_data) load();
        if (_data.personalInfo.hasOwnProperty(field)) {
            _data.personalInfo[field] = value;
            save();
        }
    }"""

new = """    function updatePersonalInfo(field, value) {
        if (!_data) load();
        // hasOwnProperty yerine direkt atama - yeni alanlar icin de calisir
        _data.personalInfo[field] = value;
        save();
    }"""

if old in text:
    text = text.replace(old, new)
    print("OK: updatePersonalInfo fixed")
else:
    # Try regex
    pattern = r'function updatePersonalInfo\(field, value\) \{[\s\S]*?if \(_data\.personalInfo\.hasOwnProperty\(field\)\) \{[\s\S]*?\}\s*\}'
    m = re.search(pattern, text)
    if m:
        old_found = m.group(0)
        new_func = """function updatePersonalInfo(field, value) {
        if (!_data) load();
        _data.personalInfo[field] = value;
        save();
    }"""
        text = text.replace(old_found, new_func, 1)
        print("OK: fixed via regex")
    else:
        print("FAIL: updatePersonalInfo not found as expected")

with open("wwwroot/js/cv-data.js", "w", encoding="utf-8") as f:
    f.write(text)
