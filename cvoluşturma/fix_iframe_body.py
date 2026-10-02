with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<body style="padding:0; margin:0; background:#fff;">', '<body style="padding:0; margin:0; background:#fff; box-sizing: border-box; width: 210mm;">')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
