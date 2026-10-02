with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

# Find the block after entry-field events end
idx = text.find("updatePreview();\n")
print(f"idx={idx}")
print(repr(text[idx:idx+300]))
