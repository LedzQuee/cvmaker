with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find bindEntryEvents function
match = re.search(r'function bindEntryEvents\(sectionName, container\) \{[\s\S]*?\}\s*function renderDatePicker', text)
if match:
    old_func = match.group(0)
    new_func = '''function bindEntryEvents(sectionName, container) {
        container.querySelectorAll('[data-entry-field]').forEach(function (input) {
            ['input', 'change'].forEach(function(evt) {
                input.addEventListener(evt, function () {
                    var entryId = this.closest('.entry-card').getAttribute('data-entry-id');
                    var field = this.getAttribute('data-entry-field');
                    var value = this.type === 'checkbox' ? this.checked : this.value.trim();
                    CVDataManager.updateEntry(sectionName, entryId, field, value);

                    if (field === 'current') {
                        var card = this.closest('.entry-card');
                        var endInput = card.querySelector('[data-entry-field="endDate"]');
                        if (endInput) {
                            endInput.disabled = this.checked; 
                            var dpGroup = endInput.closest('.date-picker-group') || (endInput.parentNode && endInput.parentNode.querySelector('.date-picker-group'));
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
                            }
                            if (this.checked) { endInput.value = ''; if(dpGroup) { dpGroup.querySelector('.month-select').value = ''; dpGroup.querySelector('.year-select').value = ''; } }
                        }
                    }

                    updatePreview();
                });
            });
        });
    }

    function renderDatePicker'''
    
    text = text.replace(old_func, new_func)
    
    with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed bindEntryEvents")
else:
    print("Could not find bindEntryEvents")
