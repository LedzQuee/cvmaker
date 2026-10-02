with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Revert the position: fixed hack
old_setup = r"var originalTransform = element\.style\.transform;[\s\S]*?window\.scrollTo\(0, 0\);"
new_setup = '''var originalTransform = element.style.transform;
        element.style.transform = 'none';'''

text = re.sub(old_setup, new_setup, text, count=1)

old_restore = r"element\.style\.transform = originalTransform;\s*element\.style\.position = originalPosition;[\s\S]*?btn\.disabled = false;"
new_restore = '''element.style.transform = originalTransform;
            btn.innerHTML = originalText;
            btn.disabled = false;'''

text = re.sub(old_restore, new_restore, text, count=1)

# Change save() to output('bloburl') and window.open
old_save = r"html2pdf\(\)\.set\(opt\)\.from\(element\)\.save\(\)\.then\(function\(\) \{"
new_save = '''html2pdf().set(opt).from(element).output('bloburl').then(function(pdfUrl) {
            window.open(pdfUrl, '_blank');'''

text = text.replace(old_save, new_save)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
