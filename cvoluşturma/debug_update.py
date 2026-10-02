with open("wwwroot/js/cv-data.js", "r", encoding="utf-8") as f:
    text = f.read()

# Check the full updateEntry function
idx = text.find("function updateEntry")
print(repr(text[idx:idx+400]))
