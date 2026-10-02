import re
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix bindPersonalInfoEvents
text = re.sub(r'function bindPersonalInfoEvents\(\) \{[\s\S]*?\}\n\s+function bindProfileSummaryEvents', '''function bindPersonalInfoEvents() {
        document.querySelectorAll('[data-step="0"] [data-field]').forEach(function (input) {
            input.addEventListener('input', function () {
                CVDataManager.updatePersonalInfo(this.getAttribute('data-field'), this.value.trim());
                clearValidation(this);
                updatePreview();
            });
        });
    }

    function bindProfileSummaryEvents''', text)

# Fix bindProfileSummaryEvents
text = re.sub(r'function bindProfileSummaryEvents\(\) \{[\s\S]*?\}\n\s+function bindAddEntryButtons', '''function bindProfileSummaryEvents() {
        var ta = document.getElementById('profileSummary');
        if (ta) {
            ta.addEventListener('input', function () {
                CVDataManager.updateProfileSummary(this.value.trim());
                updatePreview();
            });
        }
    }

    function bindAddEntryButtons''', text)

# Fix initTemplateSelector
text = re.sub(r'function initTemplateSelector\(\) \{[\s\S]*?\}\n\s+// ==========================================\n\s+// PDF', '''function initTemplateSelector() {
        if (typeof CVTemplateManager === 'undefined') return;
        var selectEl = document.getElementById('templateSelector');
        if (!selectEl) return;

        var current = CVTemplateManager.getCurrentTemplate();
        selectEl.value = current.id;

        selectEl.addEventListener('change', function (e) {
            var selectedId = e.target.value;
            CVTemplateManager.setTemplate(selectedId);
            updatePreview();
        });
    }

    // ==========================================
    // PDF''', text)

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
