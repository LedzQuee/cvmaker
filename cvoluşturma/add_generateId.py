with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = text.replace('function load() {', '''function generateId() {
        return Math.random().toString(36).substr(2, 9);
    }

    function load() {''')

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
