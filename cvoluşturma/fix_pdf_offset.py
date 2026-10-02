with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

old_setup = r"var originalTransform = element\.style\.transform;\s*element\.style\.transform = 'none';"
new_setup = '''var originalTransform = element.style.transform;
        var originalPosition = element.style.position;
        var originalLeft = element.style.left;
        var originalTop = element.style.top;
        var originalMargin = element.style.margin;
        var originalZIndex = element.style.zIndex;

        // Take it completely out of flow and pin it to top-left to avoid html2canvas offset bugs
        element.style.transform = 'none';
        element.style.position = 'fixed';
        element.style.left = '0';
        element.style.top = '0';
        element.style.margin = '0';
        element.style.zIndex = '9999';
        
        // Ensure scroll is at top so html2canvas doesn't shift
        window.scrollTo(0, 0);'''

text = re.sub(old_setup, new_setup, text, count=1)

old_restore = r"element\.style\.transform = originalTransform;\s*btn\.innerHTML = originalText;\s*btn\.disabled = false;"
new_restore = '''element.style.transform = originalTransform;
            element.style.position = originalPosition;
            element.style.left = originalLeft;
            element.style.top = originalTop;
            element.style.margin = originalMargin;
            element.style.zIndex = originalZIndex;
            btn.innerHTML = originalText;
            btn.disabled = false;'''

text = re.sub(old_restore, new_restore, text, count=1)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
