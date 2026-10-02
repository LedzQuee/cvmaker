# -*- coding: utf-8 -*-
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Make updatePreview also auto-save
old_updatepreview_call = "            updatePreview();\n                updatePreview();"

# Find the updatePreview function and add auto-save
old_up = "    function updatePreview() {"
new_up = """    var _autoSaveTimer = null;
    function autoSave() {
        if (_autoSaveTimer) clearTimeout(_autoSaveTimer);
        _autoSaveTimer = setTimeout(function() {
            try { CVDataManager.save(); } catch(e) {}
        }, 400);
    }

    function updatePreview() {"""

if old_up in content and 'function autoSave()' not in content:
    content = content.replace(old_up, new_up)
    print('autoSave added before updatePreview')

# Add autoSave() call inside updatePreview
old_up_body = """    function updatePreview() {
        // Update template label regardless of data presence"""
new_up_body = """    function updatePreview() {
        autoSave();
        // Update template label regardless of data presence"""

if old_up_body in content:
    content = content.replace(old_up_body, new_up_body)
    print('autoSave() call added inside updatePreview')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(content)
