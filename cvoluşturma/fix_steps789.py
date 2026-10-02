# -*- coding: utf-8 -*-
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ---- ADIM 7: Better validation before PDF ----
old_validate = "            if (!CVDataManager.hasData()) {\n                  alert('L\u00fctfen \u00f6nce CV bilgilerinizi doldurun.');"
new_validate = """            var _data = CVDataManager.getData();
              var _pi = _data.personalInfo || {};
              if (!_pi.firstName || !_pi.lastName) {
                  alert('PDF oluşturmak için lütfen önce Adınızı ve Soyadınızı girin (1. Adım: Kişisel Bilgiler).');
                  return;
              }
              if (false && !CVDataManager.hasData()) {
                  alert('Lütfen önce CV bilgilerinizi doldurun.');"""

if old_validate in content:
    content = content.replace(old_validate, new_validate)
    print('Validation improved')
else:
    print('Validation target not found - skipping')

# ---- ADIM 8: Save template to localStorage ----
old_set_template = "    function setTemplate(id) {\n        if (templates.filter(function(t){ return t.id === id; }).length > 0) {\n            currentTemplateId = id;\n            try { localStorage.setItem(STORAGE_KEY, id); } catch(e) {}\n        }\n    }"
# Already saves to localStorage in cv-templates.js, check it's correct
if 'localStorage.setItem(STORAGE_KEY, id)' in content:
    print('Template localStorage save already present in cv-builder.js (or cv-templates.js)')
else:
    print('Template save not found in cv-builder.js')

# ---- ADIM 9: Fix checkbox disabling selects ----
old_checkbox = "endInput.disabled = this.checked; var group = endInput.closest('.date-picker-group'); if(group) { group.querySelector('.month-select').disabled = this.checked; group.querySelector('.year-select').disabled = this.checked; }"
new_checkbox = """endInput.disabled = this.checked; 
                        var dpGroup = endInput.closest('.date-picker-group') || (endInput.parentNode && endInput.parentNode.querySelector('.date-picker-group'));
                        // Also find the group by searching parent card
                        if (!dpGroup) {
                            var parentCard = this.closest('.entry-card');
                            if (parentCard) {
                                var hiddenEnd = parentCard.querySelector('[data-entry-field="endDate"]');
                                if (hiddenEnd) dpGroup = hiddenEnd.parentNode;
                            }
                        }
                        if(dpGroup) { 
                            var mSel = dpGroup.querySelector('.month-select');
                            var ySel = dpGroup.querySelector('.year-select');
                            if (mSel) mSel.disabled = this.checked;
                            if (ySel) ySel.disabled = this.checked;
                        }"""

if old_checkbox in content:
    content = content.replace(old_checkbox, new_checkbox)
    print('Checkbox disable fix applied')
else:
    print('Checkbox target not found - trying alternate search')
    import re
    m = re.search(r'endInput\.disabled = this\.checked;.*?group\.querySelector.*?disabled = this\.checked;', content, re.DOTALL)
    if m:
        print('Found at:', m.start(), '-', m.end())
        print('Match:', content[m.start():m.end()][:100])
    else:
        print('No match at all')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(content)
