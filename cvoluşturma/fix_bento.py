import re

with open('wwwroot/js/cv-templates.js', 'r', encoding='utf-8') as f:
    content = f.read()

new_bento = '''    function renderBento(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-bento">';
        var name = fullName(pi);
        if (name || pi.email || pi.phone) {
            h += '<div class="bento-card bento-header" style="display:flex; align-items:center; justify-content:flex-start; gap:30px; text-align:left;">';
            var photo = renderPhoto(pi);
            if (photo) h += photo;
            h += '<div class="tpl-header-content" style="flex:1;">';
            if (name) h += '<h1>' + esc(name) + '</h1>';
            var cl = contactLine(pi); if (cl) h += '<p>' + cl + '</p>';
            var ll = linkLine(pi); if (ll) h += '<p class="tpl-links">' + ll + '</p>';
            h += '</div></div>';
        }
        h += '<div class="bento-grid">';
        
        // MAIN COL
        h += '<div class="bento-col-main">';
        if (data.profileSummary) h += '<div class="bento-card tpl-section"><h2>Profil</h2><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div>';
        
        if (hasEntries(data.experience)) {
            h += '<div class="bento-card tpl-section"><h2>Deneyim</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            }); h += '</div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="bento-card tpl-section"><h2>Eğitim</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                h += '<div class="tpl-company">' + esc(e.school) + '</div></div>';
            }); h += '</div>';
        }
        h += '</div>';

        // SIDE COL
        h += '<div class="bento-col-side">';
        h += renderSkillsInline(data, 'BentoCard');
        h += renderLangsInline(data, 'BentoCard');
        h += renderCertsBlock(data, 'BentoCard');
        h += renderProjectsBlock(data, 'BentoCard');
        h += '</div>';
        
        h += '</div></div>'; return h;
    }'''

content = re.sub(r'(?s)\s+function renderBento\(data\) \{.*?(?=\n\s+function renderTimeline)', '\n\n' + new_bento, content)

with open('wwwroot/js/cv-templates.js', 'w', encoding='utf-8') as f:
    f.write(content)
