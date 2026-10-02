with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find the end of init function, or right after loadFormData()
insert_code = '''
        // URL'den gelen şablon parametresini kontrol et
        const urlParams = new URLSearchParams(window.location.search);
        const templateParam = urlParams.get('template');
        if (templateParam && typeof CVTemplateManager !== 'undefined') {
            CVTemplateManager.setTemplate(templateParam);
            var selectEl = document.getElementById('templateSelector');
            if (selectEl) selectEl.value = templateParam;
        }

        renderAllDynamicSections();'''

text = text.replace('        renderAllDynamicSections();', insert_code)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
