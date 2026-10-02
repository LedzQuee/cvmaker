with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Insert the driver's license input next to website
match = re.search(r'<div class="col-md-6">\s*<label for="website" class="form-label">Web Sitesi</label>\s*<input type="url" class="form-control" id="website" data-field="website" placeholder="www\.siteniz\.com" />\s*</div>', text)
if match:
    original = match.group(0)
    new_input = original + '''
                        <div class="col-md-6">
                            <label for="driversLicense" class="form-label">Ehliyet</label>
                            <input type="text" class="form-control" id="driversLicense" data-field="driversLicense" placeholder="Örn: B, A2" />
                        </div>'''
    text = text.replace(original, new_input)
    with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Success inserting ehliyet HTML")
else:
    print("Failed to find website input")
