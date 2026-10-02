# -*- coding: utf-8 -*-
import re

def fix_turkish(content):
    fixes = {
        # Broken Turkish chars in ASCII/latin1 encoded strings
        'irket Ad': 'Şirket Adı',
        'niversite Ad': 'Üniversite Adı',
        'Bilgisayar Mhendislii': 'Bilgisayar Mühendisliği',
        'Bilgisayar M\u00fchendisl': 'Bilgisayar Mühendisliği',
        'Yazlm Gelitirici': 'Yazılım Geliştirici',
        'Yazlm Geli\u015ftirici': 'Yazılım Geliştirici',
        'ngilizce, Almanca': 'İngilizce, Almanca',
        'Ba\u015flang\u0131\u00e7': 'Başlangıç',
        'Biti\u015f': 'Bitiş',
        'Se\u00e7in': 'Seçin',
        '\u00d6n Lisans': 'Ön Lisans',
        'Y\u00fcksek Lisans': 'Yüksek Lisans',
        'Di\u011fer': 'Diğer',
        'A\u00e7klama': 'Açıklama',
        'Do\u011frulama URL': 'Doğrulama URL',
        'projenin amac': 'projenin amacı',
        'katklarnz': 'katkılarınız',
        'ba\u015farlarnz': 'başarılarınız',
        'Sorumluluklarnz': 'Sorumluluklarınız',
        'placeholder=\\"niversite Ad\\"': 'placeholder=\\"Üniversite Adı\\"',
        'placeholder=\\"irket Ad\\"': 'placeholder=\\"Şirket Adı\\"',
        'placeholder=\\"Yazlm Geli\u015ftirici\\"': 'placeholder=\\"Yazılım Geliştirici\\"',
        'placeholder=\\"ngilizce': 'placeholder=\\"İngilizce',
    }
    for old, new in fixes.items():
        content = content.replace(old, new)
    return content

files = [
    'wwwroot/js/cv-builder.js',
    'wwwroot/js/cv-templates.js',
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        fixed = fix_turkish(content)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
        print(f'Fixed: {f}')
    except Exception as e:
        print(f'Error {f}: {e}')
