with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Modal icons
text = text.replace('&#128229; PDF Olarak İndir', 'PDF Olarak İndir')
text = text.replace('&#128438; Yazdır', 'Yazdır')

# Fix Şşablon and Ççubuklu
text = text.replace('Şşablon', 'Şablon')
text = text.replace('Ççubuklu', 'Çubuklu')

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
