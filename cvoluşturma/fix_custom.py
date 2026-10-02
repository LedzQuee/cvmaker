# -*- coding: utf-8 -*-

# ---- 1. cv-data.js: add customSections support ----
with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# Add customSections to default data
old_default = """            personalInfo: {
                  firstName: '',
                  lastName: '',
                  email: '',
                  phone: '',
                  address: '',
                  linkedin: '',
                  website: '',
                  photoUrl: ''"""
new_default = """            personalInfo: {
                  firstName: '',
                  lastName: '',
                  email: '',
                  phone: '',
                  address: '',
                  linkedin: '',
                  website: '',
                  photoUrl: ''"""
# Also need to add customSections array
if 'customSections' not in data_js:
    # Find where education, experience etc are in getDefaultData
    old_section_end = "            projects: [],"
    if old_section_end in data_js:
        data_js = data_js.replace(old_section_end, old_section_end + "\n            customSections: [],")
        print('customSections added to defaultData')
    else:
        # Try alternative
        old_section_end2 = "            projects: []"
        if old_section_end2 in data_js:
            data_js = data_js.replace(old_section_end2, old_section_end2 + ",\n            customSections: []")
            print('customSections added to defaultData (alt)')
        else:
            print('WARNING: projects array end not found')

# Add getEmptyCustomSection factory
old_empty_project_end = """    function getEmptyProject() {
          return {
              id: generateId(),
              name: '',
              description: '',
              technologies: '',"""
if 'getEmptyCustomSection' not in data_js:
    data_js = data_js.replace(
        "    // Entry factories",
        """    function getEmptyCustomSection() {
        return {
            id: generateId(),
            title: 'Özel Bölüm',
            content: ''
        };
    }

    // Entry factories"""
    )
    print('getEmptyCustomSection added')

# Expose it
if 'getEmptyCustomSection' in data_js and 'getEmptyCustomSection:' not in data_js:
    data_js = data_js.replace(
        "        getEmptyProject: getEmptyProject",
        "        getEmptyProject: getEmptyProject,\n        getEmptyCustomSection: getEmptyCustomSection"
    )
    print('getEmptyCustomSection exposed')

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)
print('cv-data.js saved')
