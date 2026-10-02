# -*- coding: utf-8 -*-
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_v = """            if (!CVDataManager.hasData()) {
                alert('L\u00fctfen \u00f6nce CV bilgilerinizi doldurun.');
                  return;
              }
              if (exportModal) {"""

new_v = """            var _chkData = CVDataManager.getData();
              var _chkPi = (_chkData && _chkData.personalInfo) ? _chkData.personalInfo : {};
              if (!_chkPi.firstName || !_chkPi.lastName) {
                  alert('PDF oluşturmak için lütfen önce Adınızı ve Soyadınızı girin (1. Adım: Kişisel Bilgiler).');
                  return;
              }
              if (exportModal) {"""

if old_v in content:
    content = content.replace(old_v, new_v)
    print('Validation fix applied')
else:
    # Try alternate
    import re
    content = re.sub(
        r"if \(!CVDataManager\.hasData\(\)\) \{\s*alert\('L[^']*doldurun\.'\);\s*return;\s*\}\s*if \(exportModal\) \{",
        new_v,
        content, count=1
    )
    print('Regex validation fix applied')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(content)
