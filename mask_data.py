# -*- coding: utf-8 -*-
import re
import os

file_path = os.path.join('cvoluşturma', 'wwwroot', 'js', 'cv-data.js')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the real phone, email and linkedin with placeholders
content = content.replace('b.kocak.dev@gmail.com', 'kullanici@ornek.com')
content = content.replace('0545 514 44 96', '+90 555 000 00 00')
content = content.replace('https://www.linkedin.com/in/burak-koçak-8664ba280/', 'https://linkedin.com/in/kullanici-adi')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Data masked locally')
