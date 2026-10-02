with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'.{0,15}_chkData.{0,15}', text)
print("chkData matches:", matches)

matches2 = re.findall(r'.{0,15}currentStep ===.{0,15}', text)
print("currentStep matches:", matches2)
