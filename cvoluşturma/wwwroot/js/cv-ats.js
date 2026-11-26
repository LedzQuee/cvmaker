/* ============================================
   ATS Puanı — CV'nin işe alım sistemlerinde (ATS) ve
   yapay zeka ön elemesinde nasıl okunacağını ölçer.
   Tamamen tarayıcıda çalışır, hiçbir veri dışarı gönderilmez.
   ============================================ */
var CVAtsScorer = (function () {
    'use strict';

    var JOB_AD_KEY = 'cv_builder_job_ad';

    // Formdaki her adım için kısa ATS rehberi (adım numaraları Builder.cshtml'deki data-step ile aynı)
    var STEP_TIPS = {
        0: 'Ad, e-posta ve telefon şart. Şehir yeterli, tam adres gerekmez. LinkedIn adresi puanı artırır. Fotoğrafı ATS okumaz; yalnızca Modern ve Kurumsal şablonlarda görünür.',
        1: '2-4 cümle yaz: unvanın, deneyim süren, en güçlü 3-4 becerin ve hedefin. Başvurduğun ilandaki unvanı aynen kullan.',
        2: 'Okul, bölüm, derece ve mezuniyet tarihini yaz. Ortalaman yüksekse (3.00+) açıklamaya ekleyebilirsin.',
        3: 'Her madde = güçlü fiil + ne yaptın + sayıyla sonuç. Örnek: "Ödeme sayfasını yeniden yazarak dönüşümü %18 artırdım."',
        4: 'İlandaki yazımı birebir kullan ("JavaScript", "JS" değil). Araçların yanında yöntemleri de ekle (SQL, Scrum, REST API).',
        5: 'Seviyeyi standart biçimde yaz: A1–C2 veya Anadil.',
        6: 'Sertifikanın tam adını, veren kurumu ve tarihini yaz.',
        7: 'Kullandığın teknolojileri ve proje linkini ekle. Deneyimi az olanlar için en güçlü kanıt projelerdir.',
        8: 'Standart başlıklar kullan: Gönüllülük, Ödüller, Yayınlar, Referanslar. Hobiler çoğu ilanda gerekmez.'
    };

    var ACTION_VERBS = ['geliştirdim', 'yönettim', 'tasarladım', 'oluşturdum', 'kurdum', 'azalttım', 'artırdım',
        'sağladım', 'uyguladım', 'entegre ettim', 'optimize ettim', 'liderlik ettim', 'yürüttüm', 'hazırladım',
        'analiz ettim', 'iyileştirdim', 'otomatikleştirdim', 'koordine ettim', 'eğittim', 'planladım', 'başlattım',
        'tamamladım', 'yayınladım', 'test ettim', 'dağıttım', 'çözdüm', 'kazandırdım', 'düşürdüm', 'ölçeklendirdim',
        'developed', 'built', 'led', 'designed', 'managed', 'implemented', 'reduced', 'increased', 'improved', 'created', 'launched'];

    var STOPWORDS = ('ve veya ile için bir bu şu o da de ki mi en çok az daha gibi kadar olarak olan olup olması ' +
        'olmak ise ama fakat ancak her tüm bütün çok iyi yüksek güçlü tercihen tercih tercihen aranan aranıyor ' +
        'arıyoruz arıyor nitelik nitelikler genel gereken gerekli sahip sahibi konusunda konularında alanında ' +
        'bilgi bilgisi bilgili bilen deneyim deneyimi deneyimli tecrübe tecrübeli tecrübesi yıl yıllık en az ' +
        'pozisyon pozisyonu pozisyonda iş işi işin işler görev görevler sorumluluk sorumluluklar ekip ekibimize ' +
        'ekibine şirket şirketimiz firmamız firma bünyesinde kariyer aday adaylar başvuru başvur katılacak ' +
        'çalışacak çalışma çalışmak çalışabilen yapabilen yapacak edebilen eden etmek yapmak olacak tam zamanlı ' +
        'hybrid hibrit uzaktan ofis istanbul ankara izmir türkiye mezun mezunu üniversite üniversitelerin bölüm ' +
        'bölümlerinden lisans iletişim becerisi becerileri becerisine yetkinlik yetkinliği takım oyuncusu ' +
        'the and or for with to of in on a an is are be as at by we you our your will can must have has ' +
        'experience years year strong good knowledge skills skill ability team work working role job').split(/\s+/);
    var STOP = {};
    STOPWORDS.forEach(function (w) { if (w) STOP[w] = true; });

    function trLower(s) { return (s || '').toLocaleLowerCase('tr-TR'); }

    function stripHtml(s) {
        return (s || '').replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
    }

    function words(s) {
        var m = stripHtml(s).trim().match(/\S+/g);
        return m ? m.length : 0;
    }

    function cvText(d) {
        var parts = [];
        var pi = d.personalInfo || {};
        parts.push(pi.firstName, pi.lastName, d.profileSummary);
        (d.experience || []).forEach(function (e) { parts.push(e.position, e.company, e.description); });
        (d.education || []).forEach(function (e) { parts.push(e.school, e.degree, e.field, e.description); });
        (d.skills || []).forEach(function (s) { parts.push(s.name); });
        (d.languages || []).forEach(function (l) { parts.push(l.name); });
        (d.certifications || []).forEach(function (c) { parts.push(c.name, c.issuer); });
        (d.projects || []).forEach(function (p) { parts.push(p.name, p.technologies, p.description); });
        (d.customSections || []).forEach(function (c) { parts.push(c.title, c.content); });
        return trLower(stripHtml(parts.filter(Boolean).join(' \n ')));
    }

    function descLines(desc) {
        return stripHtml((desc || '').replace(/<\/(p|li|div)>|<br\s*\/?>/gi, '\n'))
            .split('\n').map(function (l) { return l.trim().replace(/^[-*•]\s*/, ''); }).filter(Boolean);
    }

    // İlanlarda sık geçen ama beceri olmayan kelimeler (unvan ve dolgu)
    var FILLER = ('uygulama uygulaması uygulamaları uygulamalar geliştirme geliştirmek kullanım kullanımı tasarım tasarımı ' +
        'artı sebebi sebebidir sebep yazabilen yazmak olan olanlar junior senior mid stajyer developer geliştirici ' +
        'mühendis mühendisi engineer uzman uzmanı specialist yönetimi süreç süreçleri ortam ortamında proje projeler ' +
        'projelerde benzer ilgili ilgi alan alanı minimum maksimum dahil beklenen beklenti avantaj avantajdır plus ' +
        'web yazılım yazılımı sistem sistemleri teknoloji teknolojileri araç araçları').split(/\s+/);
    FILLER.forEach(function (w) { if (w) STOP[w] = true; });

    function normTok(tok) {
        // Kesme işaretinden sonraki eki at ("React'e" -> "react"), sondaki noktalamayı temizle
        return trLower(tok.split(/['’]/)[0]).replace(/[.,;:!?)\]]+$/, '').replace(/^[(\[\-\/]+/, '');
    }

    // ---------- İlan anahtar kelimeleri ----------
    // Dönen her öğe: { label: ilandaki yazım, parts: eşleştirmede aranacak küçük harf parçalar }
    function extractKeywords(ad) {
        var src = stripHtml(ad);
        var out = [], seen = {}, used = {};

        // 1) Büyük harfle yazılmış çok kelimeli terimler: "Entity Framework", "SQL Server", "REST API"
        var phraseRe = /(?:[A-ZÇĞİÖŞÜ.][\wçğıöşüÇĞİÖŞÜ.#+]*)(?:\s+[A-ZÇĞİÖŞÜ.][\wçğıöşüÇĞİÖŞÜ.#+]*){1,2}/g;
        var m;
        while ((m = phraseRe.exec(src)) !== null) {
            var toks = m[0].split(/\s+/).map(function (t) { return { raw: t.replace(/[.,;:]+$/, ''), n: normTok(t) }; })
                .filter(function (t) { return t.n && !STOP[t.n]; });
            if (toks.length < 2) continue;
            var key = toks.map(function (t) { return t.n; }).join(' ');
            if (seen[key]) continue;
            seen[key] = true;
            toks.forEach(function (t) { used[t.n] = true; });
            out.push({ label: toks.map(function (t) { return t.raw; }).join(' '), parts: toks.map(function (t) { return t.n; }), count: 2 });
        }

        // 2) Tek kelimelik terimler, sıklığa göre
        var counts = {}, labels = {}, order = [];
        (src.match(/[A-Za-z0-9çğıöşüÇĞİÖŞÜ.#+\-\/']+/g) || []).forEach(function (raw) {
            var n = normTok(raw);
            if (!n || STOP[n] || used[n] || /^\d+$/.test(n)) return;
            var technical = /[#+.]/.test(n) || /\d/.test(n) || /^[A-Z]{2,}/.test(raw);
            if (n.length < (technical ? 2 : 3)) return;
            if (!counts[n]) { counts[n] = 0; order.push(n); labels[n] = raw.split(/['’]/)[0].replace(/[.,;:]+$/, ''); }
            counts[n]++;
        });
        order.forEach(function (n) { out.push({ label: labels[n], parts: [n], count: counts[n] }); });

        out.sort(function (a, b) { return b.count - a.count; });
        return out.slice(0, 20);
    }

    function cvHasPart(text, kw) {
        if (text.indexOf(kw) !== -1) return true;
        // Türkçe ekler: "veritabanı" ~ "veritabanları", "optimizasyon" ~ "optimizasyonu"
        if (/^[a-zçğıöşü]+$/.test(kw) && kw.length >= 6) {
            return text.indexOf(kw.slice(0, Math.max(5, kw.length - 3))) !== -1;
        }
        return false;
    }

    function cvHasKeyword(text, kw) {
        return kw.parts.every(function (p) { return cvHasPart(text, p); });
    }

    // ---------- Puanlama ----------
    function analyze(d, templateId, jobAd) {
        var checks = []; // {label, got, max, tip, step}
        function add(step, label, got, max, tip) { checks.push({ step: step, label: label, got: got, max: max, tip: got < max ? tip : '' }); }
        var pi = d.personalInfo || {};

        // İletişim (15)
        var c = 0;
        if (pi.email) c += 5;
        if (pi.phone) c += 4;
        if (pi.address) c += 3;
        if (pi.linkedin) c += 3;
        add(0, 'İletişim bilgileri', c, 15, 'E-posta, telefon, şehir ve LinkedIn adresinin hepsini ekle. ATS bunları ayrı alanlara çeker.');

        // Özet (12)
        var sw = words(d.profileSummary);
        var s = sw === 0 ? 0 : (sw >= 30 && sw <= 120 ? 12 : (sw >= 15 && sw <= 180 ? 7 : 3));
        add(1, 'Profil özeti', s, 12, sw === 0 ? 'Kısa bir özet ekle: kim olduğun, uzmanlığın ve hedef pozisyon (30-120 kelime).'
            : 'Özet ' + sw + ' kelime. İdeal aralık 30-120 kelime.');

        // Deneyim (30)
        var exps = (d.experience || []).filter(function (e) { return e.position || e.company; });
        var lines = [];
        exps.forEach(function (e) { lines = lines.concat(descLines(e.description)); });
        add(3, 'İş deneyimi girildi', exps.length ? 6 : 0, 6, 'En az bir deneyim ekle (staj, serbest çalışma ve gönüllü işler de sayılır).');
        var dated = exps.length && exps.every(function (e) { return e.startDate && (e.endDate || e.current); });
        add(3, 'Deneyim tarihleri tam', dated ? 5 : 0, 5, 'Her deneyime başlangıç ve bitiş tarihi (veya "Devam ediyor") gir. ATS süreleri hesaplar.');
        var bullets = exps.some(function (e) { return descLines(e.description).length >= 2; });
        add(3, 'Madde madde açıklama', bullets ? 5 : 0, 5, 'Deneyimleri 2-5 kısa madde halinde yaz ("- " ile başlayan satırlar).');
        // "3D", "ES6" gibi teknoloji adları sayılmasın; yüzde, miktar ve büyüklük ifadeleri sayılsın
        var METRIC = /%\s*\d|\d\s*%|\d+\s*\+|\d{2,}|\d\s*(kat|kişi|kullanıcı|müşteri|saat|gün|hafta|ay|yıl|proje|milyon|bin)|\d\s*x(?![a-zçğıöşü])/;
        var numbers = lines.filter(function (l) { return METRIC.test(trLower(l)); }).length;
        add(3, 'Ölçülebilir sonuçlar', numbers >= 2 ? 8 : (numbers === 1 ? 4 : 0), 8,
            'Sonuçları sayıyla göster: "sayfa yüklenmesini %40 hızlandırdım", "5 kişilik ekipte", "10.000+ kullanıcı".');
        var verbLines = lines.filter(function (l) {
            var low = trLower(l);
            return ACTION_VERBS.some(function (v) { return low.indexOf(v) !== -1; });
        }).length;
        // Edilgen ("geliştirildi", "çalışıldı", "sağlandı") cümleler: kimin yaptığı belli değil
        var passiveLines = lines.filter(function (l) { return /(ıldı|ildi|uldu|üldü|ndı|ndi)\.?$/.test(trLower(l)); });
        add(3, 'Etken (güçlü) fiiller', verbLines >= 2 ? 6 : (verbLines === 1 ? 3 : 0), 6,
            passiveLines.length ? 'Edilgen cümleleri etkene çevir: "geliştirildi" yerine "geliştirdim", "yapıldı" yerine "yaptım".'
                : 'Maddelere güçlü fiillerle başla: geliştirdim, yönettim, azalttım, otomatikleştirdim.');

        // Eğitim (8)
        var edus = (d.education || []).filter(function (e) { return e.school; });
        add(2, 'Eğitim bilgisi', edus.length ? 6 : 0, 6, 'Okul, bölüm ve derece bilgisini ekle.');
        add(2, 'Eğitim tarihleri', edus.length && edus.every(function (e) { return e.startDate || e.endDate; }) ? 2 : 0, 2,
            'Mezuniyet (veya beklenen mezuniyet) tarihini yaz.');

        // Yetenekler (14)
        var sk = (d.skills || []).filter(function (x) { return x.name; }).length;
        add(4, 'Yetenek sayısı', sk >= 8 ? 14 : (sk >= 5 ? 9 : (sk >= 1 ? 4 : 0)), 14,
            sk + ' yetenek var. 8-15 arası, ilandaki terimlerle aynı yazımla ekle (ör. "React", "SQL", "Docker").');

        // Diller (4)
        add(5, 'Yabancı dil', (d.languages || []).some(function (l) { return l.name; }) ? 4 : 0, 4, 'Dil bilgisini seviyesiyle (B2, C1 gibi) ekle.');

        // Ekstralar (7)
        var extra = (d.projects || []).some(function (p) { return p.name; }) || (d.certifications || []).some(function (x) { return x.name; });
        add(7, 'Proje veya sertifika', extra ? 7 : 0, 7, 'Proje veya sertifika ekle. Deneyimi az olanlar için en güçlü kanıt.');

        // Uzunluk (10)
        var total = words(cvText(d));
        add(-1, 'CV uzunluğu', total >= 200 && total <= 800 ? 10 : 5, 10,
            total < 200 ? 'CV çok kısa (' + total + ' kelime). Deneyim ve projelerini biraz daha detaylandır.'
                : 'CV uzun (' + total + ' kelime). En güncel ve ilgili bilgilerle 1-2 sayfada tut.');

        var base = checks.reduce(function (a, x) { return a + x.got; }, 0);

        // İlan eşleştirme
        var match = null;
        if (jobAd && jobAd.trim().length > 30) {
            var kws = extractKeywords(jobAd);
            var text = cvText(d);
            var found = [], missing = [];
            kws.forEach(function (k) { (cvHasKeyword(text, k) ? found : missing).push(k); });
            match = { found: found, missing: missing, percent: kws.length ? Math.round(found.length / kws.length * 100) : 0 };
        }

        var score = match ? Math.round(base * 0.6 + match.percent * 0.4) : base;
        return { score: score, base: base, checks: checks, match: match, passiveLines: passiveLines, hasPhoto: !!pi.photo };
    }

    // ---------- Arayüz ----------
    var panel, open = false, timer = null;

    function esc(t) { var d = document.createElement('div'); d.textContent = t == null ? '' : String(t); return d.innerHTML; }

    function level(score) {
        if (score >= 80) return { cls: 'good', text: 'Güçlü' };
        if (score >= 60) return { cls: 'ok', text: 'Geliştirilebilir' };
        return { cls: 'bad', text: 'Zayıf' };
    }

    function currentTemplate() {
        try { return CVTemplateManager.getCurrentTemplate().id; } catch (e) { return ''; }
    }

    function jobAd() { try { return localStorage.getItem(JOB_AD_KEY) || ''; } catch (e) { return ''; } }

    function compute() {
        var data;
        try { data = CVDataManager.getData(); } catch (e) { return null; }
        if (!data) return null;
        return analyze(data, currentTemplate(), jobAd());
    }

    function updateBadge(r) {
        var b = document.getElementById('atsScoreBadge');
        if (!b || !r) return;
        b.textContent = r.score;
        b.className = 'ats-score-badge ' + level(r.score).cls;
    }

    function renderPanel(r) {
        if (!panel || !r) return;
        var lv = level(r.score);
        var h = '';
        h += '<div class="ats-head"><div class="ats-ring ' + lv.cls + '" style="--p:' + r.score + '"><span>' + r.score + '</span></div>';
        h += '<div><div class="ats-level ' + lv.cls + '">' + lv.text + '</div>';
        h += '<div class="ats-sub">' + (r.match ? 'CV kalitesi ' + r.base + '/100 · İlan uyumu %' + r.match.percent : 'İlan eklersen uyum puanı da hesaplanır') + '</div></div></div>';

        var todo = r.checks.filter(function (c) { return c.tip; }).sort(function (a, b) { return (b.max - b.got) - (a.max - a.got); });
        if (todo.length) {
            h += '<h4>Puanını yükseltmek için</h4><ul class="ats-todo">';
            todo.forEach(function (c) {
                h += '<li><div class="ats-todo-top"><b>' + esc(c.label) + '</b><span>+' + (c.max - c.got) + '</span></div><p>' + esc(c.tip) + '</p></li>';
            });
            h += '</ul>';
        } else {
            h += '<p class="ats-done">Tüm temel kontroller tamam. Şimdi bir ilan yapıştırıp uyumu kontrol et.</p>';
        }

        h += '<h4>İş ilanıyla karşılaştır</h4>';
        h += '<p class="ats-hint">Başvuracağın ilanın metnini yapıştır. Sistemler CV\'yi ilandaki terimlerle karşılaştırarak puanlar.</p>';
        h += '<textarea id="atsJobAd" rows="6" placeholder="İlan metnini buraya yapıştır...">' + esc(jobAd()) + '</textarea>';
        if (r.match) {
            h += '<div class="ats-kw"><div class="ats-kw-title">CV\'de olmayan terimler (' + r.match.missing.length + ')</div>';
            h += r.match.missing.length ? r.match.missing.map(function (k) { return '<span class="kw miss">' + esc(k.label) + '</span>'; }).join('') : '<span class="ats-hint">Hepsi var 👍</span>';
            h += '</div><div class="ats-kw"><div class="ats-kw-title">Eşleşen terimler (' + r.match.found.length + ')</div>';
            h += r.match.found.map(function (k) { return '<span class="kw hit">' + esc(k.label) + '</span>'; }).join('') + '</div>';
            h += '<p class="ats-hint">Eksik terimleri yalnızca gerçekten biliyorsan ekle; mülakatta sorulur. Yetenekler bölümüne ve deneyim maddelerine ilandaki yazımla ekle.</p>';
        }
        h += '<p class="ats-foot">Üç şablon da ATS uyumludur. "PDF İndir" gerçek metinli PDF üretir; CV\'yi Word\'e kopyalayıp yeniden biçimlendirme, ekran görüntüsü olarak gönderme.</p>';

        var body = panel.querySelector('.ats-body');
        var ta = document.getElementById('atsJobAd');
        var hadFocus = ta && document.activeElement === ta;
        var caret = hadFocus ? ta.selectionStart : 0;
        body.innerHTML = h;
        var nta = document.getElementById('atsJobAd');
        nta.addEventListener('input', function () {
            try { localStorage.setItem(JOB_AD_KEY, nta.value); } catch (e) {}
            schedule();
        });
        if (hadFocus) { nta.focus(); nta.setSelectionRange(caret, caret); }
    }

    // Her form adımının başına o adıma özel ATS rehberi ve canlı uyarılar
    function renderCoach(r) {
        if (!r) return;
        document.querySelectorAll('.step-content[data-step]').forEach(function (stepEl) {
            var step = parseInt(stepEl.getAttribute('data-step'), 10);
            var box = stepEl.querySelector('.ats-coach');
            if (!box) {
                box = document.createElement('div');
                box.className = 'ats-coach';
                var header = stepEl.querySelector('.step-header');
                if (header && header.nextSibling) stepEl.insertBefore(box, header.nextSibling); else stepEl.appendChild(box);
            }
            var warn = r.checks.filter(function (c) { return c.step === step && c.tip; }).map(function (c) { return c.tip; });
            if (step === 3 && r.passiveLines.length) {
                warn.push('Edilgen cümleler: ' + r.passiveLines.slice(0, 3).map(function (l) {
                    return '“' + (l.length > 70 ? l.slice(0, 67) + '…' : l) + '”';
                }).join(', '));
            }
            var tplHasPhoto = false;
            try { tplHasPhoto = !!CVTemplateManager.getCurrentTemplate().photo; } catch (e) {}
            if (step === 0 && r.hasPhoto && !tplHasPhoto) {
                warn.push('Fotoğraf yükledin ama seçili şablon fotoğraf göstermez (ATS fotoğrafı zaten okumaz). Göstermek istersen Modern veya Kurumsal şablonu seç.');
            }
            var h = '<div class="ats-coach-tip"><span class="ats-coach-tag">ATS ipucu</span> ' + esc(STEP_TIPS[step] || '') + '</div>';
            if (warn.length) {
                h += '<ul class="ats-coach-warn">' + warn.map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul>';
            }
            if (box.innerHTML !== h) box.innerHTML = h;
        });
    }

    function refresh() {
        var r = compute();
        updateBadge(r);
        renderCoach(r);
        if (open) renderPanel(r);
    }

    function schedule() { clearTimeout(timer); timer = setTimeout(refresh, 500); }

    function build() {
        panel = document.createElement('aside');
        panel.className = 'ats-panel';
        panel.setAttribute('aria-label', 'ATS puanı');
        panel.innerHTML = '<div class="ats-bar"><strong>ATS Puanı</strong><button type="button" class="ats-close" aria-label="Kapat">&times;</button></div><div class="ats-body"></div>';
        document.body.appendChild(panel);
        panel.querySelector('.ats-close').addEventListener('click', toggle);
    }

    function toggle() {
        if (!panel) build();
        open = !open;
        panel.classList.toggle('open', open);
        if (open) refresh();
    }

    function init() {
        var btn = document.getElementById('btnAtsScore');
        if (btn) btn.addEventListener('click', toggle);
        // Form değiştikçe puanı güncelle (ATS panelinin kendi yazı alanı hariç)
        document.addEventListener('input', function (e) { if (e.target && e.target.id !== 'atsJobAd') schedule(); }, true);
        document.addEventListener('change', schedule, true);
        document.addEventListener('click', function (e) { if (e.target && e.target.closest && e.target.closest('button')) schedule(); }, true);
        setTimeout(refresh, 800);
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();

    function openPanel() { if (!open) toggle(); }

    return { analyze: analyze, extractKeywords: extractKeywords, refresh: refresh, score: compute, open: openPanel };
})();
