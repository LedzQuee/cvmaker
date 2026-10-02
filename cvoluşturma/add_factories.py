with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

factories = '''    function generateId() {
        return Math.random().toString(36).substr(2, 9);
    }

    function getEmptyEducation() {
        return { id: generateId(), school: '', degree: '', field: '', startDate: '', endDate: '', description: '' };
    }

    function getEmptyExperience() {
        return { id: generateId(), company: '', position: '', startDate: '', endDate: '', current: false, description: '' };
    }

    function getEmptySkill() {
        return { id: generateId(), name: '', level: 'Orta' };
    }

    function getEmptyLanguage() {
        return { id: generateId(), name: '', level: 'B2' };
    }

    function getEmptyCertification() {
        return { id: generateId(), name: '', issuer: '', date: '' };
    }

    function getEmptyProject() {
        return { id: generateId(), name: '', role: '', date: '', description: '' };
    }'''

text = text.replace('    function generateId() {\n        return Math.random().toString(36).substr(2, 9);\n    }', factories)

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
