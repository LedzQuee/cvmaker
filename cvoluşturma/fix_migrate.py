# -*- coding: utf-8 -*-
# Add localStorage migration to cv-builder.js
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    content = f.read()

migration_code = '''
    // === localStorage Migration: strip HTML tags from old Quill data ===
    function migrateStoredData(data) {
        function stripHtml(text) {
            if (!text || typeof text !== 'string') return text;
            return text
                .replace(/<br\\s*\\/?>/gi, ' ')
                .replace(/<\\/p>/gi, ' ')
                .replace(/<\\/li>/gi, ' ')
                .replace(/<[^>]+>/g, '')
                .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ')
                .trim();
        }
        if (data.profileSummary) data.profileSummary = stripHtml(data.profileSummary);
        if (data.experience) data.experience.forEach(function(e) { e.description = stripHtml(e.description); });
        if (data.education) data.education.forEach(function(e) { e.description = stripHtml(e.description); });
        if (data.projects) data.projects.forEach(function(p) { p.description = stripHtml(p.description); });
        return data;
    }
'''

# Find the load function and inject migration there
old_load_pattern = "CVDataManager.load();"
new_load = "CVDataManager.load(); try { var _d = CVDataManager.getData(); migrateStoredData(_d); CVDataManager.save(); } catch(e) {}"

if migration_code.strip()[:40] not in content:
    # Inject before init function
    content = content.replace('    let isInitialized = false;', migration_code + '\n    let isInitialized = false;')
    print('Migration code injected')
else:
    print('Migration code already exists')

# Update the load call to also run migration  
if old_load_pattern in content and new_load not in content:
    content = content.replace(old_load_pattern, new_load)
    print('Load updated with migration call')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(content)
