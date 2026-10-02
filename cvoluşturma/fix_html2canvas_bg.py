with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
insert_code = '''
            // Arkaplan rengi ve esneme sorunlarını çözmek için
            element.style.backgroundColor = '#ffffff';
            
            // html2canvas flexbox stretch bug fix
            var sidebarLeft = element.querySelector('.sidebar-left');
            if (sidebarLeft) {
                sidebarLeft.style.minHeight = element.offsetHeight + 'px';
            }
            
            var bentoCards = element.querySelectorAll('.bento-card');
            bentoCards.forEach(function(c) {
                c.style.backgroundColor = window.getComputedStyle(c).backgroundColor;
            });
'''

text = text.replace("            // zellikle background rengi ekle (Siyah arkaplan hatalarna kar)\n            element.style.backgroundColor = '#ffffff';", insert_code)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
