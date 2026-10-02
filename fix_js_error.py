# -*- coding: utf-8 -*-
import os

file_path = os.path.join('cvoluşturma', 'wwwroot', 'js', 'cv-data.js')
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for the unclosed string line
for i in range(len(lines)):
    if '- ASP.NET Core ve MVC' in lines[i] and not lines[i].rstrip().endswith("}"):
        # It means the string breaks to the next line.
        # We need to merge lines[i] and lines[i+1] with \n
        lines[i] = lines[i].rstrip() + r'\n' + lines[i+1].lstrip()
        lines[i+1] = "" # empty out the next line

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Fixed newline issue in cv-data.js')
