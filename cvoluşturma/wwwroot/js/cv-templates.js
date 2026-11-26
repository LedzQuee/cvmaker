/* ============================================
   CV Şablonları — 3 ATS uyumlu şablon
   Üçü de aynı tek sütunlu, düz metin yapısını kullanır; yalnızca
   görünüm (CSS) farklıdır. Böylece işe alım sistemleri (ATS) ve
   yapay zeka ön elemesi her şablonu aynı doğrulukla okur:
   - Tek sütun, yukarıdan aşağı okuma sırası
   - Standart bölüm adları (Özet, İş Deneyimi, Eğitim, Yetenekler...)
   - İletişim bilgileri gövdede düz metin (başlık/alt bilgi alanında değil)
   - Tablo, sütun, ikon, beceri çubuğu yok
   ============================================ */

var CVTemplateManager = (function () {
    'use strict';

    var STORAGE_KEY = 'cv_builder_template';
    var DEFAULT_ID = 'ats';
    var currentTemplateId = DEFAULT_ID;

    // Eski (kaldırılan) şablonlardan yenilerine geçiş
    var LEGACY = {
        nordic: 'modern', timeline: 'modern', studio: 'modern', floating: 'modern',
        bento: 'modern', sidebar: 'modern', architect: 'modern',
        editorial: 'classic', monochrome: 'ats'
    };

    // ---------- Yardımcılar ----------
    function esc(text) {
        if (!text) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }
    function escAttr(text) {
        return esc(text).replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    // Kullanıcının yazdığı linki güvenli bir http(s) adresine çevir; değilse boş dön
    function safeUrl(url) {
        if (!url || typeof url !== 'string') return '';
        var u = url.trim();
        if (/^https?:\/\//i.test(u)) return u;
        if (/^[a-z0-9.-]+\.[a-z]{2,}(\/|$)/i.test(u)) return 'https://' + u;
        return '';
    }
    function linkHtml(url) {
        var safe = safeUrl(url);
        if (!safe) return esc(url);
        return '<a href="' + escAttr(safe) + '">' + esc(url) + '</a>';
    }

    function trLower(s) { return (s || '').toLocaleLowerCase('tr-TR'); }

    function renderPhoto(pi) {
        var photo = pi.photo;
        if (!photo || typeof photo !== 'string') return '';
        var isDataUrl = /^data:image\/(png|jpe?g|gif|webp);base64,[A-Za-z0-9+\/=]+$/.test(photo);
        var isHttpUrl = /^https?:\/\//i.test(photo);
        if (!isDataUrl && !isHttpUrl) return '';
        return '<img class="tpl-photo" src="' + escAttr(photo) + '" alt="Profil fotoğrafı" />';
    }

    function descToHtml(text) {
        if (!text) return '';
        if (typeof DOMPurify !== 'undefined') {
            text = DOMPurify.sanitize(text, { ALLOWED_TAGS: ['br', 'p', 'ul', 'li', 'b', 'strong', 'em', 'div'], ALLOWED_ATTR: [] });
        }
        // Quill editöründen gelen HTML'i düz satırlara çevir
        text = text.replace(/<br\s*\/?>/gi, '\n')
            .replace(/<\/p>/gi, '\n').replace(/<\/li>/gi, '\n').replace(/<\/div>/gi, '\n')
            .replace(/<li[^>]*>/gi, '- ')
            .replace(/<[^>]+>/gm, '')
            .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ')
            .trim();

        var lines = text.split('\n');
        var html = '', inList = false;
        for (var i = 0; i < lines.length; i++) {
            var line = lines[i].trim();
            if (!line) continue;
            if (/^[-*•]\s/.test(line)) {
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
        var parts = String(dateStr).split('-');
        if (parts.length < 2) return esc(dateStr);
        var months = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'];
        var mIndex = parseInt(parts[1], 10) - 1;
        var month = (mIndex >= 0 && mIndex < 12) ? months[mIndex] : parts[1];
        return month + ' ' + parts[0];
    }

    function dateRange(start, end, isCurrent) {
        var s = start ? formatMonth(start) : '';
        var e = isCurrent ? 'Devam Ediyor' : (end ? formatMonth(end) : '');
        if (s && e) return s + ' – ' + e;
        return s || e || '';
    }

    function fullName(pi) {
        return ((pi.firstName || '') + ' ' + (pi.lastName || '')).trim();
    }

    function skillLabel(lvl) {
        if (!lvl) return '';
        var l = trLower(lvl);
        if (l === 'beginner' || l === 'başlangıç') return 'Başlangıç';
        if (l === 'intermediate' || l === 'orta') return 'Orta';
        if (l === 'advanced' || l === 'ileri') return 'İleri';
        if (l === 'expert' || l === 'uzman') return 'Uzman';
        return lvl;
    }

    function langLabel(lvl) {
        if (!lvl) return '';
        var map = { beginner: 'A1', elementary: 'A2', intermediate: 'B1', upper_intermediate: 'B2', advanced: 'C1', native: 'Anadil' };
        return map[lvl] || lvl;
    }

    function hasEntries(arr) {
        return arr && arr.length > 0 && arr.some(function (e) { return e.name || e.school || e.company || e.position || e.title; });
    }

    function section(title, body) {
        if (!body) return '';
        return '<section class="tpl-section"><h2>' + title + '</h2>' + body + '</section>';
    }

    function entry(title, date, sub, desc) {
        var h = '<div class="tpl-entry"><div class="tpl-entry-top"><h3>' + title + '</h3>';
        if (date) h += '<span class="tpl-date">' + date + '</span>';
        h += '</div>';
        if (sub) h += '<div class="tpl-company">' + sub + '</div>';
        if (desc) h += '<div class="tpl-desc">' + desc + '</div>';
        return h + '</div>';
    }

    // ---------- Ortak, ATS uyumlu düzen ----------
    function renderLinear(data, cfg) {
        var pi = data.personalInfo || {};
        var h = '<div class="cv-tpl ' + cfg.cls + '">';

        // Başlık: ad + iletişim düz metin olarak (ATS bu alanları ayrıştırır)
        var photo = cfg.photo ? renderPhoto(pi) : '';
        h += '<header class="tpl-header' + (photo ? ' has-photo' : '') + '"><div class="tpl-header-text">';
        var name = fullName(pi);
        if (name) h += '<h1>' + esc(name) + '</h1>';
        var contact = [];
        if (pi.email) contact.push(esc(pi.email));
        if (pi.phone) contact.push(esc(pi.phone));
        if (pi.address) contact.push(esc(pi.address));
        if (contact.length) h += '<p class="tpl-contact">' + contact.join(' | ') + '</p>';
        var links = [];
        if (pi.linkedin) links.push(linkHtml(pi.linkedin));
        if (pi.website) links.push(linkHtml(pi.website));
        if (pi.driversLicense) links.push('Ehliyet: ' + esc(pi.driversLicense));
        if (links.length) h += '<p class="tpl-contact">' + links.join(' | ') + '</p>';
        h += '</div>' + photo + '</header>';

        // Özet
        if (data.profileSummary) h += section('Özet', '<div class="tpl-desc">' + descToHtml(data.profileSummary) + '</div>');

        // İş Deneyimi (en kritik bölüm, özetten hemen sonra)
        if (hasEntries(data.experience)) {
            var exp = '';
            data.experience.forEach(function (e) {
                if (!e.position && !e.company) return;
                exp += entry(esc(e.position || e.company), dateRange(e.startDate, e.endDate, e.current),
                    e.position ? esc(e.company) : '', descToHtml(e.description));
            });
            h += section('İş Deneyimi', exp);
        }

        // Eğitim
        if (hasEntries(data.education)) {
            var edu = '';
            data.education.forEach(function (e) {
                if (!e.school) return;
                var t = e.degree || ''; if (e.field) t += (t ? ', ' : '') + e.field;
                edu += entry(esc(e.school), dateRange(e.startDate, e.endDate, e.current), esc(t), descToHtml(e.description));
            });
            h += section('Eğitim', edu);
        }

        // Yetenekler: virgülle ayrılmış düz liste (ATS anahtar kelime eşleşmesi için en iyi biçim)
        if (hasEntries(data.skills)) {
            var sk = data.skills.filter(function (s) { return s.name; })
                .map(function (s) { return esc(s.name) + (s.level ? ' (' + skillLabel(s.level) + ')' : ''); });
            h += section('Yetenekler', '<p>' + sk.join(', ') + '</p>');
        }

        // Diller
        if (hasEntries(data.languages)) {
            var lg = data.languages.filter(function (l) { return l.name; })
                .map(function (l) { return esc(l.name) + (l.level ? ' (' + esc(langLabel(l.level)) + ')' : ''); });
            h += section('Diller', '<p>' + lg.join(', ') + '</p>');
        }

        // Sertifikalar
        if (hasEntries(data.certifications)) {
            var ce = '';
            data.certifications.forEach(function (c) {
                if (!c.name) return;
                ce += entry(esc(c.name), formatMonth(c.date), esc(c.issuer), '');
            });
            h += section('Sertifikalar', ce);
        }

        // Projeler
        if (hasEntries(data.projects)) {
            var pr = '';
            data.projects.forEach(function (p) {
                if (!p.name) return;
                var sub = [];
                if (p.technologies) sub.push(esc(p.technologies));
                if (p.url) sub.push(linkHtml(p.url));
                pr += entry(esc(p.name), esc(p.date), sub.join(' | '), descToHtml(p.description));
            });
            h += section('Projeler', pr);
        }

        // Özel bölümler
        (data.customSections || []).forEach(function (sec) {
            if (!sec.title && !sec.content) return;
            h += section(esc(sec.title || 'Ek Bilgiler'), '<div class="tpl-desc">' + descToHtml(sec.content) + '</div>');
        });

        return h + '</div>';
    }

    var templates = [
        { id: 'ats', name: 'Standart', desc: 'En sade ve en güvenli. Her sektöre uyar.', color: '#0F766E',
          render: function (d) { return renderLinear(d, { cls: 'cv-tpl-ats', photo: false }); } },
        { id: 'classic', name: 'Klasik', desc: 'Serif yazı, ortalı başlık. Kurumsal, finans, hukuk.', color: '#1F2937',
          render: function (d) { return renderLinear(d, { cls: 'cv-tpl-classic', photo: false }); } },
        { id: 'modern', name: 'Modern', desc: 'Güçlü başlık, renk vurgusu, isteğe bağlı fotoğraf.', color: '#1D4ED8', photo: true,
          render: function (d) { return renderLinear(d, { cls: 'cv-tpl-modern', photo: true }); } },
        { id: 'executive', name: 'Kurumsal', desc: 'Koyu başlık bandı, isteğe bağlı fotoğraf. Yönetici ve kurumsal başvurular.', color: '#1E293B', photo: true,
          render: function (d) { return renderLinear(d, { cls: 'cv-tpl-executive', photo: true }); } },
        { id: 'elegant', name: 'Zarif', desc: 'Serif başlıklar, bordo vurgu. Eğitim, sağlık, akademi.', color: '#7F1D1D',
          render: function (d) { return renderLinear(d, { cls: 'cv-tpl-elegant', photo: false }); } },
        { id: 'tech', name: 'Teknik', desc: 'Yeşil vurgulu bölüm çizgileri. Yazılım ve mühendislik.', color: '#047857',
          render: function (d) { return renderLinear(d, { cls: 'cv-tpl-tech', photo: false }); } },
        { id: 'compact', name: 'Kompakt', desc: 'Dar boşluklar, küçük yazı. Çok bilgiyi tek sayfaya sığdırır.', color: '#475569',
          render: function (d) { return renderLinear(d, { cls: 'cv-tpl-compact', photo: false }); } }
    ];

    function resolveId(id) {
        if (!id) return null;
        if (LEGACY[id]) id = LEGACY[id];
        return templates.some(function (t) { return t.id === id; }) ? id : null;
    }

    function loadSavedTemplate() {
        try {
            var id = resolveId(localStorage.getItem(STORAGE_KEY));
            if (id) currentTemplateId = id;
        } catch (e) {}
    }

    function setTemplate(id) {
        id = resolveId(id);
        if (!id) return;
        currentTemplateId = id;
        try { localStorage.setItem(STORAGE_KEY, id); } catch (e) {}
    }

    function getCurrentTemplate() {
        var found = templates.filter(function (t) { return t.id === currentTemplateId; });
        return found.length ? found[0] : templates[0];
    }

    function getTemplates() { return templates; }
    function render(data) { return getCurrentTemplate().render(data); }

    loadSavedTemplate();

    return { setTemplate: setTemplate, getCurrentTemplate: getCurrentTemplate, getTemplates: getTemplates, render: render, loadSavedTemplate: loadSavedTemplate };
})();
