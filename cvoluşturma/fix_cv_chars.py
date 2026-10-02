with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Fix Şirket
text = re.sub(r'<label class="form-label">.*?irket', '<label class="form-label">Şirket', text)
text = re.sub(r'placeholder=".*?irket Ad.*?"', 'placeholder="Şirket Adı"', text)

# Fix Okul / Üniversite
text = re.sub(r'<label class="form-label">Okul / .*?niversite', '<label class="form-label">Okul / Üniversite', text)
text = re.sub(r'placeholder=".*?niversite Ad.*?"', 'placeholder="Üniversite Adı"', text)

# Fix Başlangıç and Bitiş in case they broke again
text = re.sub(r'<label class="form-label">Ba.*?lang.*?</label>', '<label class="form-label">Başlangıç</label>', text)
text = re.sub(r'<label class="form-label">Biti.*?</label>', '<label class="form-label">Bitiş</label>', text)

# Fix Bölüm
text = re.sub(r'<label class="form-label">B.*?l.*?m</label>', '<label class="form-label">Bölüm</label>', text)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
