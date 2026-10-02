import re
with open('wwwroot/js/cv-templates.js', 'r', encoding='utf-8') as f:
    text = f.read()

# For classic template
classic_contact = '''var contact = [];
        if (p.phone) contact.push(esc(p.phone));
        if (p.email) contact.push(esc(p.email));
        if (p.address) contact.push(esc(p.address));
        if (p.linkedin) contact.push(esc(p.linkedin));
        if (p.website) contact.push(esc(p.website));
        if (p.driversLicense) contact.push('Ehliyet: ' + esc(p.driversLicense));'''

text = re.sub(r'var contact = \[\];\s*if \(p\.phone\) contact\.push\(esc\(p\.phone\)\);\s*if \(p\.email\) contact\.push\(esc\(p\.email\)\);\s*if \(p\.address\) contact\.push\(esc\(p\.address\)\);\s*if \(p\.linkedin\) contact\.push\(esc\(p\.linkedin\)\);\s*if \(p\.website\) contact\.push\(esc\(p\.website\)\);', classic_contact, text)

# For sidebar template
sidebar_contact = '''var contactHtml = '';
        if (p.phone) contactHtml += '<div class="sidebar-item">' + esc(p.phone) + '</div>';
        if (p.email) contactHtml += '<div class="sidebar-item">' + esc(p.email) + '</div>';
        if (p.address) contactHtml += '<div class="sidebar-item">' + esc(p.address) + '</div>';
        if (p.linkedin) contactHtml += '<div class="sidebar-item">' + esc(p.linkedin) + '</div>';
        if (p.website) contactHtml += '<div class="sidebar-item">' + esc(p.website) + '</div>';
        if (p.driversLicense) contactHtml += '<div class="sidebar-item">Ehliyet: ' + esc(p.driversLicense) + '</div>';'''

text = re.sub(r'var contactHtml = \'\';\s*if \(p\.phone\) contactHtml \+= \'<div class="sidebar-item">\' \+ esc\(p\.phone\) \+ \'</div>\';\s*if \(p\.email\) contactHtml \+= \'<div class="sidebar-item">\' \+ esc\(p\.email\) \+ \'</div>\';\s*if \(p\.address\) contactHtml \+= \'<div class="sidebar-item">\' \+ esc\(p\.address\) \+ \'</div>\';\s*if \(p\.linkedin\) contactHtml \+= \'<div class="sidebar-item">\' \+ esc\(p\.linkedin\) \+ \'</div>\';\s*if \(p\.website\) contactHtml \+= \'<div class="sidebar-item">\' \+ esc\(p\.website\) \+ \'</div>\';', sidebar_contact, text)

# For base (nordic/default) template
base_contact = '''var contactHtml = '<div class="tpl-contact">';
        if (p.phone) contactHtml += '<span>' + esc(p.phone) + '</span>';
        if (p.email) contactHtml += '<span>' + esc(p.email) + '</span>';
        if (p.address) contactHtml += '<span>' + esc(p.address) + '</span>';
        if (p.linkedin) contactHtml += '<span>' + esc(p.linkedin) + '</span>';
        if (p.website) contactHtml += '<span>' + esc(p.website) + '</span>';
        if (p.driversLicense) contactHtml += '<span>Ehliyet: ' + esc(p.driversLicense) + '</span>';'''

text = re.sub(r'var contactHtml = \'<div class="tpl-contact">\';\s*if \(p\.phone\) contactHtml \+= \'<span>\' \+ esc\(p\.phone\) \+ \'</span>\';\s*if \(p\.email\) contactHtml \+= \'<span>\' \+ esc\(p\.email\) \+ \'</span>\';\s*if \(p\.address\) contactHtml \+= \'<span>\' \+ esc\(p\.address\) \+ \'</span>\';\s*if \(p\.linkedin\) contactHtml \+= \'<span>\' \+ esc\(p\.linkedin\) \+ \'</span>\';\s*if \(p\.website\) contactHtml \+= \'<span>\' \+ esc\(p\.website\) \+ \'</span>\';', base_contact, text)


# For Bento Grid template
bento_contact = '''var bentoContact = '';
        if (p.phone) bentoContact += '<div class="contact-item">' + esc(p.phone) + '</div>';
        if (p.email) bentoContact += '<div class="contact-item">' + esc(p.email) + '</div>';
        if (p.address) bentoContact += '<div class="contact-item">' + esc(p.address) + '</div>';
        if (p.linkedin) bentoContact += '<div class="contact-item">' + esc(p.linkedin) + '</div>';
        if (p.website) bentoContact += '<div class="contact-item">' + esc(p.website) + '</div>';
        if (p.driversLicense) bentoContact += '<div class="contact-item">Ehliyet: ' + esc(p.driversLicense) + '</div>';'''

text = re.sub(r'var bentoContact = \'\';\s*if \(p\.phone\) bentoContact \+= \'<div class="contact-item">\' \+ esc\(p\.phone\) \+ \'</div>\';\s*if \(p\.email\) bentoContact \+= \'<div class="contact-item">\' \+ esc\(p\.email\) \+ \'</div>\';\s*if \(p\.address\) bentoContact \+= \'<div class="contact-item">\' \+ esc\(p\.address\) \+ \'</div>\';\s*if \(p\.linkedin\) bentoContact \+= \'<div class="contact-item">\' \+ esc\(p\.linkedin\) \+ \'</div>\';\s*if \(p\.website\) bentoContact \+= \'<div class="contact-item">\' \+ esc\(p\.website\) \+ \'</div>\';', bento_contact, text)

with open('wwwroot/js/cv-templates.js', 'w', encoding='utf-8') as f:
    f.write(text)
