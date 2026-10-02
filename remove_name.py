# -*- coding: utf-8 -*-
import os

file_path = os.path.join('cvoluşturma', 'wwwroot', 'js', 'cv-data.js')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("firstName: 'Burak'", "firstName: 'Kullanıcı'")
content = content.replace("lastName: 'Koçak'", "lastName: 'Adı'")
content = content.replace("lastName: 'KoÃ§ak'", "lastName: 'Adı'")  # Handle encoding just in case
content = content.replace("website: 'https://github.com/LedzQuee'", "website: 'https://github.com/ornek-profil'")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Name and github removed')
