with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    'Ã§': 'ç', 'Ã‡': 'Ç',
    'Ä±': 'ı', 'Ä°': 'İ',
    'ÅŸ': 'ş', 'Åž': 'Ş',
    'Ã¶': 'ö', 'Ã–': 'Ö',
    'Ã¼': 'ü', 'Ãœ': 'Ü',
    'ÄŸ': 'ğ', 'Äž': 'Ğ',
    '?': 'Ş',
    '': 'ı'  # Be careful with this wildcard-like replace!
}

for old, new in replacements.items():
    if old != '':
        text = text.replace(old, new)

# Targeted replaces for any remaining broken chars
text = text.replace('Balang', 'Başlangıç')
text = text.replace('Biti', 'Bitiş')
text = text.replace('Blm', 'Bölüm')
text = text.replace('irket', 'Şirket')
text = text.replace('niversite', 'Üniversite')
text = text.replace('Ad', 'Adı')
text = text.replace('Halen alyorum', 'Halen çalışıyorum')
text = text.replace('Aklama', 'Açıklama')
text = text.replace('Derece / nvan', 'Derece / Ünvan')
text = text.replace('nvan', 'Ünvan')
text = text.replace('Devam ediyor', 'Devam ediyor')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
