with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

bad_func = '''        function getEmptyCustomSection() {
        return {
            id: generateId(),
            title: 'Özel Bölüm',
            content: ''
        };
    }'''
bad_func_alt = '''        function getEmptyCustomSection() {
        return {
            id: generateId(),
            title: '-zel BlǬm',
            content: ''
        };
    }'''
    
# Remove it from inside return block
import re
text = re.sub(r'        function getEmptyCustomSection\(\) \{\s*return \{\s*id: generateId\(\),\s*title: [^\n]+,\s*content: \'\'\s*\};\s*\}', '', text)

# Put it before "return {"
text = text.replace('    // Public API\n    return {', '''
    function getEmptyCustomSection() {
        return {
            id: generateId(),
            title: 'Özel Bölüm',
            content: ''
        };
    }

    // Public API
    return {''')

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
