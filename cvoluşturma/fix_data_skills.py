with open("wwwroot/js/cv-data.js", "r", encoding="utf-8") as f:
    text = f.read()

# Update getEmptySkill and getEmptyLanguage to default to empty string
text = text.replace(
    "function getEmptySkill() {\n        return { id: generateId(), name: '', level: 'Orta' };\n    }",
    "function getEmptySkill() {\n        return { id: generateId(), name: '', level: '' };\n    }"
)

text = text.replace(
    "function getEmptyLanguage() {\n        return { id: generateId(), name: '', level: 'B2' };\n    }",
    "function getEmptyLanguage() {\n        return { id: generateId(), name: '', level: '' };\n    }"
)

with open("wwwroot/js/cv-data.js", "w", encoding="utf-8") as f:
    f.write(text)

print("OK: cv-data updated")
