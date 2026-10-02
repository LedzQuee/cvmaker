with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('ŞŞ', 'Ş').replace('şş', 'ş')
text = text.replace('ÇÇ', 'Ç').replace('çç', 'ç')
text = text.replace('ÖÖ', 'Ö').replace('öö', 'ö')
text = text.replace('ÜÜ', 'Ü').replace('üü', 'ü')
text = text.replace('İİ', 'İ').replace('ıı', 'ı')
text = text.replace('ĞĞ', 'Ğ').replace('ğğ', 'ğ')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)

with open('wwwroot/js/cv-templates.js', 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace('ŞŞ', 'Ş').replace('şş', 'ş')
text2 = text2.replace('ÇÇ', 'Ç').replace('çç', 'ç')
text2 = text2.replace('ÖÖ', 'Ö').replace('öö', 'ö')
text2 = text2.replace('ÜÜ', 'Ü').replace('üü', 'ü')
text2 = text2.replace('İİ', 'İ').replace('ıı', 'ı')
text2 = text2.replace('ĞĞ', 'Ğ').replace('ğğ', 'ğ')

with open('wwwroot/js/cv-templates.js', 'w', encoding='utf-8') as f:
    f.write(text2)

with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text3 = f.read()

text3 = text3.replace('ŞŞ', 'Ş').replace('şş', 'ş')
text3 = text3.replace('ÇÇ', 'Ç').replace('çç', 'ç')
text3 = text3.replace('ÖÖ', 'Ö').replace('öö', 'ö')
text3 = text3.replace('ÜÜ', 'Ü').replace('üü', 'ü')
text3 = text3.replace('İİ', 'İ').replace('ıı', 'ı')
text3 = text3.replace('ĞĞ', 'Ğ').replace('ğğ', 'ğ')

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text3)
