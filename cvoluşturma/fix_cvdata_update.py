with open("wwwroot/js/cv-data.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Fix updateEntry to remove hasOwnProperty
old_func = """    function updateEntry(sectionName, entryId, field, value) {
        if (!_data) load();
        const section = _data[sectionName];
        if (Array.isArray(section)) {
            const entry = section.find(e => e.id === entryId);
            if (entry && entry.hasOwnProperty(field)) {
                entry[field] = value;
                save();
                return true;
            }
        }
        return false;
    }"""

new_func = """    function updateEntry(sectionName, entryId, field, value) {
        if (!_data) load();
        const section = _data[sectionName];
        if (Array.isArray(section)) {
            const entry = section.find(e => e.id === entryId);
            if (entry) {
                entry[field] = value;
                save();
                return true;
            }
        }
        return false;
    }"""

if old_func in text:
    text = text.replace(old_func, new_func)
    print("OK: updateEntry fixed exactly")
else:
    # Try regex
    pattern = r"function updateEntry\(sectionName, entryId, field, value\) \{[\s\S]*?if \(entry && entry\.hasOwnProperty\(field\)\) \{[\s\S]*?return false;\s*\}"
    m = re.search(pattern, text)
    if m:
        text = text.replace(m.group(0), new_func)
        print("OK: updateEntry fixed via regex")
    else:
        print("FAIL: updateEntry not found")

# Fix arrayFields in validateSchema
old_array = 'var arrayFields = ["experience", "education", "skills", "languages", "certificates", "customSections"];'
new_array = 'var arrayFields = ["experience", "education", "skills", "languages", "certifications", "projects", "customSections"];'

if old_array in text:
    text = text.replace(old_array, new_array)
    print("OK: arrayFields fixed")
else:
    print("FAIL: arrayFields not found")

with open("wwwroot/js/cv-data.js", "w", encoding="utf-8") as f:
    f.write(text)
