with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Remove the entire @media print block we just added
text = re.sub(r'/\* ==============================\n   PRINT STYLES \(Yazdır Modu\)\n   ============================== \*/\n@media print \{[\s\S]*?\}\n', '', text)

# Add a much safer print block
safe_print_css = '''
/* ==============================
   PRINT STYLES (Yazdır Modu)
   ============================== */
@media print {
    @page {
        margin: 0 !important;
        size: A4 portrait;
    }
    
    /* Sadece önizleme alanını göster, sol menüyü gizle */
    .builder-form-panel, .builder-nav, .mobile-panel-toggle, .preview-header, header {
        display: none !important;
    }
    
    .builder-layout {
        display: block !important;
    }
    
    .builder-preview-panel {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
    }
    
    #previewContent {
        width: 210mm !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .cv-tpl {
        width: 100% !important;
        height: 100% !important;
        min-height: 297mm !important;
        margin: 0 !important;
        padding: 0;
        box-shadow: none !important;
    }
    
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
}
'''

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text + "\n" + safe_print_css)
