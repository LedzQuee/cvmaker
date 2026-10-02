with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

print_css = '''
/* ==============================
   PRINT STYLES (Yazdır Modu)
   ============================== */
@media print {
    @page {
        margin: 0 !important;
        size: A4 portrait;
    }
    
    body * {
        visibility: hidden;
    }
    
    #previewContent, #previewContent * {
        visibility: visible;
    }
    
    #previewContent {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        margin: 0;
        padding: 0;
        background-color: white;
    }
    
    .cv-tpl {
        width: 210mm !important;
        min-height: 297mm !important;
        height: auto !important;
        margin: 0 !important;
        box-shadow: none !important;
        page-break-after: avoid;
    }
    
    /* Ensure sidebar stretches in print */
    .cv-tpl-sidebar .sidebar-left {
        bottom: 0;
    }
    
    /* Prevent awkward page breaks */
    .tpl-section, .tpl-entry, .bento-card, .sidebar-section {
        page-break-inside: avoid;
        break-inside: avoid;
    }
    
    /* Force background graphics */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
}
'''

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text + "\n" + print_css)
