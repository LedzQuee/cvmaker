# -*- coding: utf-8 -*-
with open('wwwroot/js/cv-templates.js', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    function descToHtml(text) {
        if (!text) return '';
        // Eer iinde HTML etiketleri varsa (eski Quill editrnden kalan),
        // nce onlar temizleyelim ki ham metin olarak ileyelim.
        text = text.replace(/<[^>]*>?/gm, '');'''

new = '''    function descToHtml(text) {
        if (!text) return '';
        // Strip any HTML tags (leftover from Quill editor)
        text = text.replace(/<br\\s*\\/?>/gi, '\\n');
        text = text.replace(/<\\/p>/gi, '\\n');
        text = text.replace(/<\\/li>/gi, '\\n');
        text = text.replace(/<\\/div>/gi, '\\n');
        text = text.replace(/<li[^>]*>/gi, '- ');
        text = text.replace(/<[^>]+>/gm, '');
        text = text.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');
        text = text.trim();'''

if old in content:
    content = content.replace(old, new)
    print('descToHtml updated')
else:
    print('WARNING: could not find old descToHtml block, trying fuzzy...')
    import re
    content = re.sub(
        r'function descToHtml\(text\) \{[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+\n[^\n]+',
        '''    function descToHtml(text) {
        if (!text) return '';
        text = text.replace(/<br\\s*\\/?>/gi, '\\n');
        text = text.replace(/<\\/p>/gi, '\\n');
        text = text.replace(/<\\/li>/gi, '\\n');
        text = text.replace(/<\\/div>/gi, '\\n');
        text = text.replace(/<li[^>]*>/gi, '- ');
        text = text.replace(/<[^>]+>/gm, '');
        text = text.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');
        text = text.trim();''',
        content, count=1
    )
    print('fuzzy replace done')

with open('wwwroot/js/cv-templates.js', 'w', encoding='utf-8') as f:
    f.write(content)
