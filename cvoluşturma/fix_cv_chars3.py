with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('bindAdıdEntryButtons', 'bindAddEntryButtons')
text = text.replace('Adıım', 'Adım')
text = text.replace('Adıd', 'Add')
text = text.replace('Adıres', 'Adres')
text = text.replace('Adıı', 'Adı')
text = text.replace('Adı+', 'Ad+')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
