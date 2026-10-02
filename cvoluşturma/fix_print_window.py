with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
old_func = r'function executePrint\(\) \{[\s\S]*?window\.print\(\);\s*\}'

new_func = '''function executePrint() {
        var content = els.previewContent.innerHTML;
        var printWindow = window.open('', '_blank', 'width=1000,height=900');
        if (!printWindow) {
            alert("Lütfen yazdırma penceresi için pop-up engelleyiciye izin verin.");
            return;
        }
        
        printWindow.document.write('<html><head><title>CV Yazdır - NovaCV</title>');
        
        // Ana sayfadaki CSS'leri al
        var styles = document.querySelectorAll('link[rel="stylesheet"], style');
        styles.forEach(function(s) { 
            // cv-builder.css'i alma, sadece template ve bootstrap kalsın
            if (!s.href || !s.href.includes('cv-builder.css')) {
                printWindow.document.write(s.outerHTML); 
            }
        });
        
        // Özel Print CSS'i
        printWindow.document.write('<style>');
        printWindow.document.write('@page { size: A4 portrait; margin: 0; }');
        printWindow.document.write('html, body { margin: 0; padding: 0; width: 210mm; background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }');
        printWindow.document.write('.cv-tpl { width: 210mm !important; min-height: 297mm !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');
        printWindow.document.write('</style>');
        
        printWindow.document.write('</head><body>');
        printWindow.document.write(content);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        
        setTimeout(function() {
            printWindow.focus();
            printWindow.print();
            // printWindow.close(); // Kullanıcı isterse sekmeyi kendi kapatır, bazen erken kapanırsa yazdırma iptal oluyor
        }, 800);
    }'''

text = re.sub(old_func, new_func, text, count=1)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
