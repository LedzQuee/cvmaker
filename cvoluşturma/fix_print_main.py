with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
old_func = r'function executePrint\(\) \{[\s\S]*?\}, 800\);\s*\}'

new_func = '''function executePrint() {
        // Native yazdırma ekranı (main window) çağırılır
        // Tüm gizleme ve hizalama işlemleri cv-templates.css içindeki @media print tarafından yönetilir
        window.print();
    }'''

text = re.sub(old_func, new_func, text, count=1)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
