with open("wwwroot/js/cv-templates.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Fix renderCertsBlock to support BentoCard
old_block = """    function renderCertsBlock(data, mode) {
        if (!hasEntries(data.certifications)) return '';
        if (mode === 'BentoCard') return ''; 
        var h = '<div class="tpl-section"><h2>Sertifikalar</h2>';"""

new_block = """    function renderCertsBlock(data, mode) {
        if (!hasEntries(data.certifications)) return '';
        var h = '<div class="tpl-section' + (mode === 'BentoCard' ? ' bento-card' : '') + '"><h2>Sertifikalar</h2>';"""

if old_block in text:
    text = text.replace(old_block, new_block)
    print("OK: renderCertsBlock fixed")
else:
    print("FAIL: renderCertsBlock not found exactly. Trying regex...")
    
with open("wwwroot/js/cv-templates.js", "w", encoding="utf-8") as f:
    f.write(text)
