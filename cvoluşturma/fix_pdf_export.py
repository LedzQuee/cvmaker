with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

old_func = text[text.find("    function executePdfExport(btn, modal) {"):text.find("        function executePrint() {")]

new_func = '''    function executePdfExport(btn, modal) {
        var originalText = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Hazirlaniyor...';
        btn.disabled = true;

        var data = CVDataManager.getData();
        var firstName = data.personalInfo.firstName || 'CV';
        var lastName  = data.personalInfo.lastName  || '';
        var fileName  = (firstName + '_' + lastName).trim().replace(/\\s+/g, '_') + '_CV.pdf';

        var content = els.previewContent.innerHTML;

        // Tum CSS'leri topla (builder.css haric)
        var cssLinks  = '';
        var cssStyles = '';
        document.querySelectorAll('link[rel="stylesheet"]').forEach(function(l) {
            if (!l.href || !l.href.includes('cv-builder.css')) cssLinks += l.outerHTML;
        });
        document.querySelectorAll('style').forEach(function(s) {
            cssStyles += s.outerHTML;
        });

        // Yeni pencerede temiz render
        var pdfWin = window.open('', '_blank', 'width=900,height=1200');
        if (!pdfWin) {
            alert('Lutfen pop-up engelleyiciye izin verin.');
            btn.innerHTML = originalText;
            btn.disabled = false;
            return;
        }

        pdfWin.document.write('<!DOCTYPE html><html lang="tr"><head>');
        pdfWin.document.write('<meta charset="utf-8">');
        pdfWin.document.write('<title>' + fileName + '</title>');
        pdfWin.document.write(cssLinks);
        pdfWin.document.write(cssStyles);
        pdfWin.document.write('<style>');
        pdfWin.document.write('@page { size: A4 portrait; margin: 0; }');
        pdfWin.document.write('* { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }');
        pdfWin.document.write('html, body { margin: 0; padding: 0; width: 210mm; background: #fff; }');
        pdfWin.document.write('.cv-tpl { width: 210mm !important; min-height: 297mm !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');
        // Yazdir butonunu goster - kullanici PDF olarak kaydedebilir
        pdfWin.document.write('.pdf-save-bar { position: fixed; top: 0; left: 0; right: 0; z-index: 9999; background: #1e3a8a; color: #fff; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; font-family: Inter, sans-serif; font-size: 14px; }');
        pdfWin.document.write('.pdf-save-bar button { background: #fff; color: #1e3a8a; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 14px; }');
        pdfWin.document.write('@media print { .pdf-save-bar { display: none !important; } body { margin-top: 0 !important; } }');
        pdfWin.document.write('body.has-bar { margin-top: 60px; }');
        pdfWin.document.write('</style>');
        pdfWin.document.write('</head><body class="has-bar">');
        pdfWin.document.write('<div class="pdf-save-bar">');
        pdfWin.document.write('<span>Kaydetmek icin: <strong>Ctrl+P</strong> → Hedef: <strong>PDF olarak kaydet</strong> → Kenar boslugu: <strong>Yok</strong></span>');
        pdfWin.document.write('<button onclick="window.print()">PDF Kaydet</button>');
        pdfWin.document.write('</div>');
        pdfWin.document.write(content);
        pdfWin.document.write('</body></html>');
        pdfWin.document.close();

        btn.innerHTML = originalText;
        btn.disabled = false;
        if (modal) { setTimeout(function(){ modal.hide(); }, 300); }
    }

    '''

if old_func:
    text = text.replace(old_func, new_func)
    print("OK: executePdfExport replaced")
else:
    print("FAIL: could not find executePdfExport")

with open("wwwroot/js/cv-builder.js", "w", encoding="utf-8") as f:
    f.write(text)
