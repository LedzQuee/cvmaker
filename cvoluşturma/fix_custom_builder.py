# -*- coding: utf-8 -*-
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add customSections to sectionConfig
old_projects_config = """        projects: {
              container: 'projectEntries',
              factory: function () { return CVDataManager.getEmptyProject(); },
              label: 'Proje',
              renderForm: renderProjectForm
          }
      };"""
new_projects_config = """        projects: {
              container: 'projectEntries',
              factory: function () { return CVDataManager.getEmptyProject(); },
              label: 'Proje',
              renderForm: renderProjectForm
          },
          customSections: {
              container: 'customSectionEntries',
              factory: function () { return CVDataManager.getEmptyCustomSection(); },
              label: 'Özel Bölüm',
              renderForm: renderCustomSectionForm
          }
      };"""

if old_projects_config in js:
    js = js.replace(old_projects_config, new_projects_config)
    print('customSections sectionConfig added')
else:
    print('WARNING: projects config end not found')
    import re
    js = re.sub(
        r"(projects: \{[^}]+renderForm: renderProjectForm\s*\})\s*\};",
        r"""\1,
          customSections: {
              container: 'customSectionEntries',
              factory: function () { return CVDataManager.getEmptyCustomSection(); },
              label: 'Özel Bölüm',
              renderForm: renderCustomSectionForm
          }
      };""",
        js, count=1
    )
    print('Regex replace done')

# 2. Add renderCustomSectionForm function
custom_form = '''
    function renderCustomSectionForm(entry) {
        return '<div class="row g-3">' +
            '<div class="col-12">' +
                '<label class="form-label">Bölüm Başlığı <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="title" value="' + esc(entry.title || '') + '" placeholder="Gönüllülük, Hobiler, Referanslar..." />' +
            '</div>' +
            '<div class="col-12">' +
                '<label class="form-label">İçerik</label>' +
                '<textarea class="form-control" data-entry-field="content" rows="4" placeholder="Bu bölüme ait bilgileri buraya yazın...">' + esc(entry.content || '') + '</textarea>' +
                '<div class="form-text mt-1">Her satırı - ile başlatırsanız madde listesi olarak görünür.</div>' +
            '</div>' +
        '</div>';
    }
'''

if 'function renderCustomSectionForm' not in js:
    js = js.replace('    function renderSkillForm', custom_form + '\n    function renderSkillForm')
    print('renderCustomSectionForm added')

# 3. Update TOTAL_STEPS to 9
js = js.replace('const TOTAL_STEPS = 8;', 'const TOTAL_STEPS = 9;')
js = js.replace("'1 / 8'", "'1 / 9'")
print('TOTAL_STEPS updated to 9')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('cv-builder.js saved')
