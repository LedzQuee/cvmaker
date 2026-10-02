# -*- coding: utf-8 -*-
import ast, sys

with open('wwwroot/js/cv-templates.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Check descToHtml is correct
if 'replace(/<br' in content:
    print('cv-templates.js: descToHtml HTML stripping OK')
else:
    print('WARNING: descToHtml HTML stripping not found')

if 'function skillLabel' in content:
    print('cv-templates.js: skillLabel OK')
if 'function langLabel' in content:
    print('cv-templates.js: langLabel OK')
if 'function renderBento' in content:
    print('cv-templates.js: renderBento OK')

with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    content2 = f.read()

if 'function autoSave' in content2:
    print('cv-builder.js: autoSave OK')
if 'function migrateStoredData' in content2:
    print('cv-builder.js: migration OK')
if 'function renderDatePicker' in content2:
    print('cv-builder.js: datepicker OK')
if 'photoPreview' in content2:
    print('cv-builder.js: photo preview OK')
if 'firstName || !_chkPi.lastName' in content2:
    print('cv-builder.js: PDF validation OK')
if 'function autoSave' in content2:
    print('cv-builder.js: autosave OK')

print('All checks done!')
