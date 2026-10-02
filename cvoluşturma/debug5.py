with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

# #7 is inside bindDynamicEntryEvents - show larger context
idx = 17101
print(repr(text[idx-400:idx+200]))
