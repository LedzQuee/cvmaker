# -*- coding: utf-8 -*-
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_opt = """        var opt = { pagebreak: { mode: 'css', avoid: '.tpl-section, .tpl-entry' }, 
            margin:       0,
            filename:     fileName,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true, logging: false },
            jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };"""

new_opt = """        var opt = {
            pagebreak: { mode: ['css', 'legacy'], avoid: ['.tpl-section', '.tpl-entry', '.bento-card', '.timeline-item', '.tpl-entry-top', '.mono-box'] },
            margin:       [8, 8, 8, 8],
            filename:     fileName,
            image:        { type: 'jpeg', quality: 1.0 },
            html2canvas:  { 
                scale: 3, 
                useCORS: true, 
                logging: false,
                letterRendering: true,
                allowTaint: true,
                backgroundColor: '#ffffff'
            },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait', compress: true }
        };"""

if old_opt in content:
    content = content.replace(old_opt, new_opt)
    print('PDF options updated')
else:
    print('WARNING: exact match not found')
    # Try simpler replace
    import re
    content = re.sub(
        r"var opt = \{ pagebreak.*?jsPDF.*?\};",
        new_opt,
        content, flags=re.DOTALL, count=1
    )
    print('Regex replace done')

# Also fix the spinner text
content = content.replace('Hazrlanyor...', 'Hazırlanıyor...')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(content)
