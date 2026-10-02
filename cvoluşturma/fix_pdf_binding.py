with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

old_bind = r'function bindPdfExportEvent\(\) \{[\s\S]*?function executePdfExport'
new_bind = '''function bindPdfExportEvent() {
        if (!els.btnDownloadPdf) return;

        els.btnDownloadPdf.addEventListener('click', function() {
            var _chkData = CVDataManager.getData();
            var _chkPi = (_chkData && _chkData.personalInfo) ? _chkData.personalInfo : {};
            if (!_chkPi.firstName || !_chkPi.lastName) {
                alert('PDF oluşturmak için lütfen önce Adınızı ve Soyadınızı girin (1. Adım: Kişisel Bilgiler).');
                return;
            }
            // Artık modal yok, direkt indir
            executePdfExport(els.btnDownloadPdf, null);
        });
    }

    function executePdfExport'''

text = re.sub(old_bind, new_bind, text, count=1)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
