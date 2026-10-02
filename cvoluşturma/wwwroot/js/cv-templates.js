/* ============================================
   CV Templates — 8 YENİ PREMIUM ŞABLON
   ============================================ */

var CVTemplateManager = (function () {
    'use strict';

    var STORAGE_KEY = 'cv_builder_template';
    var currentTemplateId = 'nordic';

        function renderPhoto(pi) {
        if (pi.photo) {
            // XSS Koruma: Sadece guvenli URL formatlarini kabul et
            var photo = pi.photo;
            var isDataUrl = typeof photo === "string" && photo.indexOf("data:image/") === 0 && photo.indexOf(";base64,") > 0;
            var isHttpUrl = typeof photo === "string" && (photo.indexOf("http://") === 0 || photo.indexOf("https://") === 0);
            if (!isDataUrl && !isHttpUrl) return "";
            return "<div class=\"tpl-photo\" style=\"flex-shrink:0;\"><img src=\"" + photo + "\" alt=\"Profil\" style=\"width:120px;height:120px;border-radius:50%;object-fit:cover;border:3px solid #eee;\"/></div>";
        }
        return "";
    }
    function esc(text) {
        if (!text) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }

        function descToHtml(text) {
        if (!text) return '';
        // Guvenlik: Once DOMPurify ile temizle (XSS korumasi)
        if (typeof DOMPurify !== "undefined") {
            text = DOMPurify.sanitize(text, { ALLOWED_TAGS: ["br", "p", "ul", "li", "b", "strong", "em", "div"], ALLOWED_ATTR: [] });
        }
        // Strip any HTML tags (leftover from Quill editor)
        text = text.replace(/<br\s*\/?>/gi, '\n');
        text = text.replace(/<\/p>/gi, '\n');
        text = text.replace(/<\/li>/gi, '\n');
        text = text.replace(/<\/div>/gi, '\n');
        text = text.replace(/<li[^>]*>/gi, '- ');
        text = text.replace(/<[^>]+>/gm, '');
        text = text.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ');
        text = text.trim();
        
        var lines = text.split('\n');
        var html = '', inList = false;
        for (var i = 0; i < lines.length; i++) {
            var line = lines[i].trim();
            if (!line) continue;
            if (line.indexOf('- ') === 0 || line.indexOf('* ') === 0) {
                if (!inList) { html += '<ul>'; inList = true; }
                html += '<li>' + esc(line.substring(2)) + '</li>';
            } else {
                if (inList) { html += '</ul>'; inList = false; }
                html += '<p>' + esc(line) + '</p>';
            }
        }
        if (inList) html += '</ul>';
        return html;
    }

    function formatMonth(dateStr) {
        if (!dateStr) return '';
        var parts = dateStr.split('-');
        if (parts.length < 2) return esc(dateStr);
        var months = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'];
        var mIndex = parseInt(parts[1], 10) - 1;
        var month = (mIndex >= 0 && mIndex < 12) ? months[mIndex] : parts[1];
        return month + ' ' + parts[0];
    }

    function dateRange(start, end, isCurrent) {
        if (!start && !end && !isCurrent) return '';
        var s = start ? formatMonth(start) : '';
        var e = isCurrent ? 'Devam Ediyor' : (end ? formatMonth(end) : '');
        if (s && e) return s + ' - ' + e;
        if (s) return s;
        if (e) return e;
        return '';
    }

    function fullName(pi) {
        return ((pi.firstName || '') + ' ' + (pi.lastName || '')).trim();
    }

    function contactLine(pi) {
        var parts = [];
        if (pi.email) parts.push(esc(pi.email));
        if (pi.phone) parts.push(esc(pi.phone));
        if (pi.address) parts.push(esc(pi.address));
        if (pi.driversLicense) parts.push('Ehliyet: ' + esc(pi.driversLicense));
        return parts.join(' • ');
    }

    function linkLine(pi) {
        var parts = [];
        if (pi.linkedin) parts.push(esc(pi.linkedin));
        if (pi.website) parts.push(esc(pi.website));
        return parts.join(' • ');
    }

        function skillLabel(lvl) {
        if (!lvl) return '';
        var l = lvl.toLowerCase();
        if (l === 'beginner' || l === 'başlangıç' || l.includes('ba')) return 'Başlangıç';
        if (l === 'intermediate' || l === 'orta') return 'Orta';
        if (l === 'advanced' || l === 'i̇leri' || l === 'ileri') return 'İleri';
        if (l === 'expert' || l === 'uzman') return 'Uzman';
        return lvl;
    }

    function langLabel(lvl) {
        if (!lvl) return '';
        if (lvl === 'beginner') return 'A1';
        if (lvl === 'elementary') return 'A2';
        if (lvl === 'intermediate') return 'B1';
        if (lvl === 'upper_intermediate') return 'B2';
        if (lvl === 'advanced') return 'C1';
        if (lvl === 'native') return 'C2 / Anadil';
        return lvl;
    }

    function hasEntries(arr) { return arr && arr.length > 0 && arr.some(function(e) { return e.name || e.school || e.company || e.position; }); }

    function renderNordic(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-nordic">';
        var name = fullName(pi);
        if (name) {
            h += '<div class="tpl-header" style="display:flex; align-items:center; gap:30px;">';
            h += renderPhoto(pi);
            h += '<div class="tpl-header-content"><h1>' + esc(name) + '</h1>';
            var cl = contactLine(pi); if (cl) h += '<p class="tpl-contact">' + cl + '</p>';
            var ll = linkLine(pi); if (ll) h += '<p class="tpl-links">' + ll + '</p>';
            h += '</div></div>';
        }
        if (data.profileSummary) h += '<div class="tpl-section"><h2>Hakkımda</h2><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div>';
        
        if (hasEntries(data.experience)) {
            h += '<div class="tpl-section"><h2>Deneyim</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            }); h += '</div>';
        }
        
        if (hasEntries(data.education)) {
            h += '<div class="tpl-section"><h2>Eğitim</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                h += '<div class="tpl-company">' + esc(e.school) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + esc(e.description) + '</div>';
                h += '</div>';
            }); h += '</div>';
        }
        
        h += renderSkillsInline(data, 'Nordic'); h += renderLangsInline(data, 'Nordic'); h += renderCustomSections(data, 'Nordic'); 
        h += renderCertsBlock(data, 'Nordic'); h += renderProjectsBlock(data, 'Nordic');
        h += '</div>'; return h;
    }

    function renderBento(data) {
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
        h += renderCertsBlock(data, 'BentoCard'); h += renderCustomSections(data, 'BentoCard');
        h += renderProjectsBlock(data, 'BentoCard');
        h += '</div>';
        
        h += '</div></div>'; return h;
    }


    function renderSidebar(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-sidebar">';
        var name = fullName(pi);
        h += '<div class="sidebar-left">';
        if (pi.photo) h += '<div class="sidebar-photo">' + renderPhoto(pi) + '</div>';
        if (name) h += '<div class="sidebar-name">' + esc(name) + '</div>';
        if (pi.email || pi.phone) {
            h += '<div class="sidebar-section"><div class="sidebar-section-title">İletişim</div>';
            if (pi.email) h += '<div class="sidebar-item">&#9993; ' + esc(pi.email) + '</div>';
            if (pi.phone) h += '<div class="sidebar-item">&#9742; ' + esc(pi.phone) + '</div>';
            if (pi.address) h += '<div class="sidebar-item">&#9679; ' + esc(pi.address) + '</div>';
            if (pi.linkedin) h += '<div class="sidebar-item">in: ' + esc(pi.linkedin) + '</div>';
            h += '</div>';
        }
        if (hasEntries(data.skills)) {
            h += '<div class="sidebar-section"><div class="sidebar-section-title">Yetenekler</div>';
            data.skills.forEach(function(s) {
                if (!s.name) return;
                h += '<div class="sidebar-skill">';
                h += '<span>' + esc(s.name) + '</span>';
                var lvl = (s.level || '').toLowerCase();
                var pct = 0;
                if (lvl === 'expert' || lvl === 'uzman') pct = 95;
                else if (lvl === 'advanced' || lvl === 'ileri' || lvl.includes('iler')) pct = 80;
                else if (lvl === 'intermediate' || lvl === 'orta') pct = 60;
                else if (lvl === 'beginner' || lvl === 'başlangıç' || lvl.includes('ba')) pct = 25;
                if (pct > 0) h += '<div class="sidebar-skill-bar"><div class="sidebar-skill-fill" style="width:' + pct + '%"></div></div>';
                h += '</div>';
            });
            h += '</div>';
        }
        if (hasEntries(data.languages)) {
            h += '<div class="sidebar-section"><div class="sidebar-section-title">Diller</div>';
            data.languages.forEach(function(l) { if(l.name) h += '<div class="sidebar-item"><b>' + esc(l.name) + '</b> — ' + langLabel(l.level) + '</div>'; });
            h += '</div>';
        }
        h += '</div>';
        h += '<div class="sidebar-right">';
        if (data.profileSummary) h += '<div class="sidebar-main-section"><h2>Hakkımda</h2><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="sidebar-main-section"><h2>İş Deneyimi</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            });
            h += '</div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="sidebar-main-section"><h2>Eğitim</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div><div class="tpl-company">' + esc(e.school) + '</div></div>';
            });
            h += '</div>';
        }
        h += renderCertsBlock(data, 'Sidebar');
        h += renderProjectsBlock(data, 'Sidebar');
        h += renderCustomSections(data, 'Sidebar');
        h += '</div></div>'; return h;
    }

    function renderClassic(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-classic">';
        var name = fullName(pi);
        h += '<div class="classic-header">';
        if (name) h += '<h1>' + esc(name) + '</h1>';
        var cl = contactLine(pi); if (cl) h += '<p class="classic-contact">' + cl + '</p>';
        h += '</div>';
        h += '<hr class="classic-divider">';
        if (data.profileSummary) h += '<div class="classic-section"><h2>HAKKIMDA</h2><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="classic-section"><h2>İŞ DENEYİMİ</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            });
            h += '</div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="classic-section"><h2>EĞİTİM</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div><div class="tpl-company">' + esc(e.school) + '</div></div>';
            });
            h += '</div>';
        }
        if (hasEntries(data.skills)) {
            h += '<div class="classic-section"><h2>YETENEKLER</h2><p class="classic-skills">';
            h += data.skills.filter(function(s){ return s.name; }).map(function(s){ return esc(s.name) + (s.level ? ' (' + skillLabel(s.level) + ')' : ''); }).join(' &bull; ');
            h += '</p></div>';
        }
        if (hasEntries(data.languages)) {
            h += '<div class="classic-section"><h2>DİLLER</h2><p class="classic-skills">';
            h += data.languages.filter(function(l){ return l.name; }).map(function(l){ return esc(l.name) + ' (' + langLabel(l.level) + ')'; }).join(' &bull; ');
            h += '</p></div>';
        }
        h += renderCertsBlock(data, 'Classic');
        h += renderCustomSections(data, 'Classic');
        h += '</div>'; return h;
    }

    function renderTimeline(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-timeline">';
        var name = fullName(pi);
        if (name) {
            h += '<div class="tpl-header" style="display:flex; align-items:center; gap:30px;">';
            h += renderPhoto(pi);
            h += '<div class="tpl-header-content"><h1>' + esc(name) + '</h1>';
            var cl = contactLine(pi); if (cl) h += '<p>' + cl + '</p>';
            var ll = linkLine(pi); if (ll) h += '<p class="tpl-links">' + ll + '</p>';
            h += '</div></div>';
        }
        if (data.profileSummary) h += '<div class="tpl-section"><h2>Profil</h2><div class="tpl-content"><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="tpl-section"><h2>Deneyim</h2><div class="timeline-container">';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-date">' + dateRange(e.startDate, e.endDate, e.current) + '</div>';
                h += '<div class="timeline-content"><h3>' + esc(e.position) + '</h3>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div></div>';
            }); h += '</div></div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="tpl-section"><h2>Eğitim</h2><div class="timeline-container">';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-date">' + dateRange(e.startDate, e.endDate, e.current) + '</div>';
                h += '<div class="timeline-content"><h3>' + esc(t) + '</h3>';
                h += '<div class="tpl-company">' + esc(e.school) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + esc(e.description) + '</div>';
                h += '</div></div>';
            }); h += '</div></div>';
        }
        h += renderSkillsInline(data, 'Timeline'); h += renderLangsInline(data, 'Timeline'); h += renderCustomSections(data, 'Timeline'); h += renderCertsBlock(data, 'Timeline'); h += renderProjectsBlock(data, 'Timeline');
        h += '</div>'; return h;
    }

    function renderEditorial(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-editorial">';
        var name = fullName(pi);
        if (name) {
            h += '<div class="tpl-header" style="display:flex; align-items:center; gap:30px;">';
            h += renderPhoto(pi);
            h += '<div class="tpl-header-content"><h1>' + esc(name) + '</h1>';
            var cl = contactLine(pi); if (cl) h += '<p>' + cl + '</p>';
            var ll = linkLine(pi); if (ll) h += '<p class="tpl-links">' + ll + '</p>';
            h += '</div></div>';
        }
        h += '<div class="ed-grid">';
        h += '<div class="ed-col-main">';
        if (data.profileSummary) h += '<div class="tpl-section"><div class="ed-lead">' + descToHtml(data.profileSummary) + '</div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="tpl-section"><h2>Deneyim Geçmişi</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="ed-entry-header"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            }); h += '</div>';
        }
        h += '</div>';
        h += '<div class="ed-col-side">';
        if (hasEntries(data.education)) {
            h += '<div class="tpl-section"><h2>Eğitim</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><h3>' + esc(t) + '</h3><div class="tpl-company">' + esc(e.school) + '</div><div class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</div></div>';
            }); h += '</div>';
        }
        h += renderSkillsInline(data, 'Editorial'); h += renderLangsInline(data, 'Editorial'); h += renderProjectsBlock(data, 'Editorial');
        h += '</div></div></div>'; return h;
    }

    function renderMonochrome(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-monochrome">';
        var name = fullName(pi);
        if (name) {
            h += '<div class="tpl-header" style="display:flex; align-items:center; gap:30px;">';
            h += renderPhoto(pi);
            h += '<div class="tpl-header-content"><h1>' + esc(name) + '</h1>';
            var cl = contactLine(pi); if (cl) h += '<div class="mono-badge">' + cl + '</div>';
            var ll = linkLine(pi); if (ll) h += '<div class="mono-badge mono-link">' + ll + '</div>';
            h += '</div></div>';
        }
        if (data.profileSummary) h += '<div class="tpl-section mono-box"><h2>Profil</h2><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="tpl-section mono-box"><h2>Deneyim</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            }); h += '</div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="tpl-section mono-box"><h2>Eğitim</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                h += '<div class="tpl-company">' + esc(e.school) + '</div></div>';
            }); h += '</div>';
        }
        h += '<div class="mono-grid">';
        h += renderSkillsInline(data, 'Mono'); h += renderLangsInline(data, 'Mono'); h += renderCustomSections(data, 'Mono');
        h += '</div></div>'; return h;
    }

    function renderArchitect(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-architect">';
        var name = fullName(pi);
        if (name) {
            h += '<div class="tpl-header" style="display:flex; align-items:center; gap:30px;">';
            h += renderPhoto(pi);
            h += '<div class="tpl-header-content"><h1>' + esc(name) + '</h1>';
            var cl = contactLine(pi); if (cl) h += '<p>' + cl + '</p>';
            var ll = linkLine(pi); if (ll) h += '<p class="tpl-links">' + ll + '</p>';
            h += '</div></div>';
        }
        if (data.profileSummary) h += '<div class="tpl-section"><div class="arch-left"><h2>Profil</h2></div><div class="arch-right"><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="tpl-section"><div class="arch-left"><h2>Deneyim</h2></div><div class="arch-right">';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="arch-entry-header"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            }); h += '</div></div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="tpl-section"><div class="arch-left"><h2>Eğitim</h2></div><div class="arch-right">';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="arch-entry-header"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                h += '<div class="tpl-company">' + esc(e.school) + '</div></div>';
            }); h += '</div></div>';
        }
        if (hasEntries(data.skills)) {
            h += '<div class="tpl-section"><div class="arch-left"><h2>Yetenekler</h2></div><div class="arch-right"><div class="arch-tags">';
            data.skills.forEach(function(s) { if(s.name) h += '<span class="arch-tag">' + esc(s.name) + '</span>'; });
            h += '</div></div></div>';
        }
        h += '</div>'; return h;
    }

    function renderStudio(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-studio">';
        var name = fullName(pi);
        if (name) {
            h += '<div class="tpl-header" style="display:flex; align-items:center; gap:40px;">';
            h += renderPhoto(pi);
            h += '<div class="tpl-header-content"><h1>' + esc(name) + '<span class="studio-dot">.</span></h1>';
            var cl = contactLine(pi); if (cl) h += '<p>' + cl + '</p>';
            var ll = linkLine(pi); if (ll) h += '<p class="tpl-links">' + ll + '</p>';
            h += '</div></div>';
        }
        if (data.profileSummary) h += '<div class="tpl-section"><h2 class="studio-title">Hakkımda</h2><div class="studio-lead">' + descToHtml(data.profileSummary) + '</div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="tpl-section"><h2 class="studio-title">Deneyim</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="studio-entry-top"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            }); h += '</div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="tpl-section"><h2 class="studio-title">Eğitim</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="studio-entry-top"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                h += '<div class="tpl-company">' + esc(e.school) + '</div></div>';
            }); h += '</div>';
        }
        h += renderSkillsInline(data, 'Studio'); h += renderLangsInline(data, 'Studio');
        h += '</div>'; return h;
    }

    function renderFloating(data) {
        var pi = data.personalInfo, h = '<div class="cv-tpl cv-tpl-floating">';
        var name = fullName(pi);
        h += '<div class="float-bg"></div>';
        if (name || pi.email || pi.phone) {
            h += '<div class="float-header-card" style="display:flex; align-items:center; gap:30px;">';
            h += renderPhoto(pi);
            h += '<div class="tpl-header-content">';
            if (name) h += '<h1>' + esc(name) + '</h1>';
            var cl = contactLine(pi); if (cl) h += '<p>' + cl + '</p>';
            var ll = linkLine(pi); if (ll) h += '<p class="tpl-links">' + ll + '</p>';
            h += '</div></div>';
        }
        h += '<div class="float-content">';
        if (data.profileSummary) h += '<div class="tpl-section"><h2>Profil</h2><div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div></div>';
        if (hasEntries(data.experience)) {
            h += '<div class="tpl-section"><h2>Kariyer Geçmişi</h2>';
            data.experience.forEach(function(e) {
                if (!e.position && !e.company) return;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(e.position) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                if (e.company) h += '<div class="tpl-company">' + esc(e.company) + '</div>';
                if (e.description) h += '<div class="tpl-desc">' + descToHtml(e.description) + '</div>';
                h += '</div>';
            }); h += '</div>';
        }
        if (hasEntries(data.education)) {
            h += '<div class="tpl-section"><h2>Eğitim Bilgileri</h2>';
            data.education.forEach(function(e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(t) + '</h3><span class="tpl-date">' + dateRange(e.startDate, e.endDate, e.current) + '</span></div>';
                h += '<div class="tpl-company">' + esc(e.school) + '</div></div>';
            }); h += '</div>';
        }
        h += renderSkillsInline(data, 'Floating');
        h += '</div></div>'; return h;
    }

        function renderSkillsInline(data, mode) {
        if (!hasEntries(data.skills)) return '';
        if (mode === 'BentoCard') {
            var h = '<div class="bento-card tpl-section"><h2>Yetenekler</h2><div class="bento-tags">';
            data.skills.forEach(function(s){ if(s.name) h += '<span class="bento-tag">' + esc(s.name) + ' (' + skillLabel(s.level) + ')</span>'; });
            h += '</div></div>';
            return h;
        }
        var h = '<div class="tpl-section' + (mode==='Mono'?' mono-box':'') + '"><h2>Yetenekler</h2><p>';
        var items = data.skills.filter(function(s){ return s.name; }).map(function(s){ return esc(s.name) + (s.level ? ' (' + skillLabel(s.level) + ')' : ''); });
        h += items.join(' &bull; ') + '</p></div>';
        return h;
    }

        function renderLangsInline(data, mode) {
        if (!hasEntries(data.languages)) return '';
        if (mode === 'BentoCard') {
            var h = '<div class="bento-card tpl-section"><h2>Diller</h2><div class="bento-tags">';
            data.languages.forEach(function(l){ if(l.name) h += '<span class="bento-tag">' + esc(l.name) + ' (' + langLabel(l.level) + ')</span>'; });
            h += '</div></div>';
            return h;
        }
        var h = '<div class="tpl-section' + (mode==='Mono'?' mono-box':'') + '"><h2>Diller</h2><p>';
        var items = data.languages.filter(function(l){ return l.name; }).map(function(l){ return esc(l.name) + ' (' + langLabel(l.level) + ')'; });
        h += items.join(' &bull; ') + '</p></div>';
        return h;
    }


    function renderCustomSections(data, mode) {
        if (!data.customSections || data.customSections.length === 0) return '';
        var h = '';
        data.customSections.forEach(function(sec) {
            if (!sec.title && !sec.content) return;
            var cls = mode === 'Mono' ? 'tpl-section mono-box' :
                      mode === 'BentoCard' ? 'bento-card tpl-section' : 'tpl-section';
            h += '<div class="' + cls + '"><h2>' + esc(sec.title || 'Özel Bölüm') + '</h2>';
            if (sec.content) h += '<div class="tpl-desc">' + descToHtml(sec.content) + '</div>';
            h += '</div>';
        });
        return h;
    }

    function renderCertsBlock(data, mode) {
        if (!hasEntries(data.certifications)) return '';
        var h = '<div class="tpl-section' + (mode === 'BentoCard' ? ' bento-card' : '') + '"><h2>Sertifikalar</h2>';
        data.certifications.forEach(function(c) {
            if (!c.name) return;
            h += '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + esc(c.name) + '</h3>';
            if (c.date) h += '<span class="tpl-date">' + formatMonth(c.date) + '</span>';
            h += '</div>';
            if (c.issuer) h += '<div class="tpl-company">' + esc(c.issuer) + '</div>';
            h += '</div>';
        });
        h += '</div>'; return h;
    }

    function renderProjectsBlock(data, mode) {
        if (!hasEntries(data.projects)) return '';
        var h = '<div class="tpl-section' + (mode==='BentoCard'?' bento-card':'') + '"><h2>Projeler</h2>';
        data.projects.forEach(function(p) {
            if (!p.name) return;
            h += '<div class="tpl-entry"><h3>' + esc(p.name) + '</h3>';
            if (p.technologies) h += '<div class="tpl-tech">' + esc(p.technologies) + '</div>';
            if (p.description) h += '<div class="tpl-desc"><p>' + esc(p.description) + '</p></div>';
            if (p.url) h += '<div class="tpl-links">' + esc(p.url) + '</div>';
            h += '</div>';
        });
        h += '</div>'; return h;
    }

    var templates = [
        { id: 'sidebar', name: 'Kenar Çubuklu', desc: 'Renkli sol panel, beceri barları', render: renderSidebar, color: '#6366F1' },
          { id: 'classic', name: 'Klasik Türkçe', desc: 'Düz, güçlü tipografi', render: renderClassic, color: '#64748B' },
          { id: 'nordic', name: 'Nordic', desc: 'Ultra sade, geniş boşluklar', render: renderNordic, color: '#9CA3AF' },
        { id: 'bento', name: 'Bento Grid', desc: 'Modern UI kart tasarımı', render: renderBento, color: '#6366F1' },
        { id: 'editorial', name: 'Editorial', desc: 'Serif font, dergi düzeni', render: renderEditorial, color: '#111827' },
        { id: 'timeline', name: 'Timeline', desc: 'Dikey akış çizgisi', render: renderTimeline, color: '#10B981' },
        { id: 'monochrome', name: 'Monokrom', desc: 'Keskin neo-brutalism', render: renderMonochrome, color: '#000000' },
        { id: 'architect', name: 'Architect', desc: '2 Sütunlu Grid', render: renderArchitect, color: '#0F172A' },
        { id: 'studio', name: 'Studio', desc: 'Büyük tipografi, ajans stili', render: renderStudio, color: '#F43F5E' },
        { id: 'floating', name: 'Floating', desc: 'Gölge detaylı başlık kartı', render: renderFloating, color: '#3B82F6' }
    ];

    function loadSavedTemplate() {
        try {
            var saved = localStorage.getItem(STORAGE_KEY);
            if (saved && templates.filter(function(t){ return t.id === saved; }).length > 0) {
                currentTemplateId = saved;
            }
        } catch(e) {}
    }

    function setTemplate(id) {
        if (templates.filter(function(t){ return t.id === id; }).length > 0) {
            currentTemplateId = id;
            try { localStorage.setItem(STORAGE_KEY, id); } catch(e) {}
        }
    }

    function getCurrentTemplate() {
        var found = templates.filter(function(t){ return t.id === currentTemplateId; });
        return found.length > 0 ? found[0] : templates[0];
    }

    function getTemplates() { return templates; }
    function render(data) { var tpl = getCurrentTemplate(); return tpl.render(data); }

    loadSavedTemplate();

    return { setTemplate: setTemplate, getCurrentTemplate: getCurrentTemplate, getTemplates: getTemplates, render: render, loadSavedTemplate: loadSavedTemplate };
})();












