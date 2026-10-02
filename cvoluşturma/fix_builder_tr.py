# -*- coding: utf-8 -*-
with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

fixes = {
    'Kiisel': 'Kişisel',
    'Eitim': 'Eğitim',
    'letiim': 'İletişim',
    'Fotoraf': 'Fotoğrafı',
    'Adnz': 'Adınız',
    'Soyadnz': 'Soyadınız',
    'ehir, lke': 'Şehir, Ülke',
    'zeti': 'Özeti',
    'ksaca tantn': 'kısaca tanıtın',
    'cmlelik profesyonel zet': 'cümlelik profesyonel özet',
    'yazlm gelitirici, 5 yllk sektr tecrbesi': 'yazılım geliştirici, 5 yıllık sektör tecrübesi',
    'zet yazn. verenler genellikle ilk olarak bu blm okur.': 'özet yazın. İşverenler genellikle ilk olarak bu bölümü okur.',
    'gemiinizi': 'geçmişinizi',
    'balayarak': 'başlayarak',
    'I Deneyimi': 'İş Deneyimi',
    'kiisel': 'kişisel',
    'Bildiiniz': 'Bildiğiniz',
    'Sahip olduunuz': 'Sahip olduğunuz',
    'ne kan': 'Öne çıkan',
    'zel Blm': 'Özel Bölüm',
    'Gnlllk': 'Gönüllülük',
    'leri': 'İleri',
    'ablon:': 'Şablon:',
    'Trke': 'Türkçe',
    'ubuklu': 'Çubuklu',
    'ndir': 'İndir',
    'nizlemeniz burada grnecek': 'önizlemeniz burada görünecek',
    'balayn': 'başlayın',
    'Önizleme': 'Önizleme',
    'Yazdr': 'Yazdır',
    'CV\'nizi': "CV'nizi",
    'CV\'nize': "CV'nize",
    'zel': 'Özel',
    'balkl': 'başlıklı',
    'blmler': 'bölümler',
    'yazn': 'yazın',
}

for old, new in fixes.items():
    text = text.replace(old, new)

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
