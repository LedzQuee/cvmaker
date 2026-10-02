/* ============================================
   CV Builder â€” Ana Orkestrasyon Modülü
   Adım yönetimi, dinamik form bölümleri, doğrulama, önizleme
   ============================================ */

const CVBuilder = (function () {
    'use strict';

    // --- Sabitler ---
    const TOTAL_STEPS = 9;
    const STEP_NAMES = [
        'Kişisel Bilgiler', 'Profil Özeti', 'Eğitim', 'İş Deneyimi',
        'Yetenekler', 'Diller', 'Sertifikalar', 'Projeler'
    ];

        const SKILL_LEVELS = [
        { value: 'Başlangıç', label: 'Başlangıç' },
        { value: 'Orta', label: 'Orta' },
        { value: 'İleri', label: 'İleri' },
        { value: 'Uzman', label: 'Uzman' }
    ];

    const LANGUAGE_LEVELS = [
        { value: 'A1', label: 'A1 (Başlangıç)' },
        { value: 'A2', label: 'A2 (Temel)' },
        { value: 'B1', label: 'B1 (Orta)' },
        { value: 'B2', label: 'B2 (İyi)' },
        { value: 'C1', label: 'C1 (İleri)' },
        { value: 'C2', label: 'C2 (Anadil / Akıcı)' },
        { value: 'Anadil', label: 'Anadil' }
    ];

    // --- Durum ---
    let currentStep = 0;

    // === localStorage Migration: strip HTML tags from old Quill data ===
    function migrateStoredData(data) {
        function stripHtml(text) {
            if (!text || typeof text !== 'string') return text;
            return text
                .replace(/<br\s*\/?>/gi, ' ')
                .replace(/<\/p>/gi, ' ')
                .replace(/<\/li>/gi, ' ')
                .replace(/<[^>]+>/g, '')
                .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ')
                .trim();
        }
        if (data.profileSummary) data.profileSummary = stripHtml(data.profileSummary);
        if (data.experience) data.experience.forEach(function(e) { e.description = stripHtml(e.description); });
        if (data.education) data.education.forEach(function(e) { e.description = stripHtml(e.description); });
        if (data.projects) data.projects.forEach(function(p) { p.description = stripHtml(p.description); });
        return data;
    }

    let isInitialized = false;

    // --- DOM Referanslar ---
    let els = {};

    // ==========================================
    // BAÅLATMA
    // ==========================================

    function init() {
        try {
            
        if (isInitialized) return;

        els = {
            stepper: document.getElementById('stepper'),
            stepContents: document.querySelectorAll('.step-content'),
            stepperItems: document.querySelectorAll('.stepper-item'),
            btnPrev: document.getElementById('btnPrev'),
            btnNext: document.getElementById('btnNext'),
            stepIndicator: document.getElementById('stepIndicator'),
            previewContent: document.getElementById('previewContent'),
            previewPlaceholder: document.getElementById('previewPlaceholder'),
            mobileToggle: document.getElementById('mobileToggle'),
            mobileToggleLabel: document.getElementById('mobileToggleLabel'),
            formPanel: document.getElementById('formPanel'),
            previewPanel: document.getElementById('previewPanel'),
            btnDownloadPdf: document.getElementById('btnDownloadPdf')
        };

        CVDataManager.load(); try { var _d = CVDataManager.getData(); migrateStoredData(_d); CVDataManager.save(); } catch(e) {}

        bindNavigationEvents();
        bindStepperEvents();
        bindPersonalInfoEvents();
        bindProfileSummaryEvents();
        bindAddEntryButtons();
        bindMobileToggle();
        initTemplateSelector();
        bindPdfExportEvent();

        loadFormData();

        // URL'den gelen şablon parametresini kontrol et
        const urlParams = new URLSearchParams(window.location.search);
        const templateParam = urlParams.get('template');
        if (templateParam && typeof CVTemplateManager !== 'undefined') {
            CVTemplateManager.setTemplate(templateParam);
            var selectEl = document.getElementById('templateSelector');
            if (selectEl) selectEl.value = templateParam;
        }

        renderAllDynamicSections();
        updatePreview();

        isInitialized = true;
    
        } catch (err) {
            console.error(err);
            alert("Init Hatası: " + err.message + "\nSatır: " + (err.lineNumber || err.line || "?"));
            isInitialized = true; // Try to force it to allow some interaction
        }
    }

    // ==========================================
    // ADM YÖNETİMİ
    // ==========================================

    function goToStep(step) {
        if (step < 0 || step >= TOTAL_STEPS) return;
        els.stepContents[currentStep].classList.remove('active');
        els.stepperItems[currentStep].classList.remove('active');
        if (step > currentStep) {
            els.stepperItems[currentStep].classList.add('completed');
        }
        currentStep = step;
        els.stepContents[currentStep].classList.add('active');
        els.stepperItems[currentStep].classList.remove('completed');
        els.stepperItems[currentStep].classList.add('active');
        updateNavigation();
        els.formPanel.scrollTop = 0;
    }

    function updateNavigation() {
        els.btnPrev.disabled = currentStep === 0;
        els.btnNext.innerHTML = currentStep === TOTAL_STEPS - 1 ? 'Tamamla' : 'İleri &rarr;';
        els.stepIndicator.textContent = (currentStep + 1) + ' / ' + TOTAL_STEPS;
    }

    function bindNavigationEvents() {
        els.btnPrev.addEventListener('click', function () {
            if (currentStep > 0) goToStep(currentStep - 1);
        });
        els.btnNext.addEventListener('click', function () {
            if (currentStep === 0 && !validatePersonalInfo()) return;
            if (currentStep < TOTAL_STEPS - 1) goToStep(currentStep + 1);
            else { var btnPdf = document.getElementById('btnDownloadPdf'); if (btnPdf) btnPdf.click(); }
        });
    }

    function bindStepperEvents() {
        els.stepperItems.forEach(function (item) {
            item.addEventListener('click', function () {
                goToStep(parseInt(this.getAttribute('data-step')));
            });
        });
    }

    // ==========================================
    // KİÅİSEL BİLGİLER (Adım 0)
    // ==========================================

    function bindPersonalInfoEvents() {
        document.querySelectorAll('[data-step="0"] [data-field]').forEach(function (input) {
            input.addEventListener('input', function () {
                CVDataManager.updatePersonalInfo(this.getAttribute('data-field'), this.value.trim());
                clearValidation(this);
                updatePreview();
                });
        });
    }

    function validatePersonalInfo() {
        var valid = true;
        var data = CVDataManager.getSection('personalInfo');
        if (!data.firstName) { showValidation(document.getElementById('firstName'), 'Adı alan zorunludur.'); valid = false; }
        if (!data.lastName) { showValidation(document.getElementById('lastName'), 'Soyad alan zorunludur.'); valid = false; }
        if (!data.email) { showValidation(document.getElementById('email'), 'E-posta alan zorunludur.'); valid = false; }
        else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) { showValidation(document.getElementById('email'), 'Geçerli bir e-posta adresi girin.'); valid = false; }
        return valid;
    }

    function showValidation(input, message) {
        if (!input) return;
        input.classList.add('is-invalid');
        var existing = input.parentElement.querySelector('.invalid-feedback');
        if (existing) existing.remove();
        var fb = document.createElement('div');
        fb.className = 'invalid-feedback';
        fb.textContent = message;
        fb.style.display = 'block';
        input.parentElement.appendChild(fb);
        if (document.querySelector('.is-invalid') === input) input.focus();
    }

    function clearValidation(input) {
        input.classList.remove('is-invalid');
        var fb = input.parentElement.querySelector('.invalid-feedback');
        if (fb) fb.remove();
    }

    // ==========================================
    // PROFİL ÖZETİ (Adım 1)
    // ==========================================

    function bindProfileSummaryEvents() {
        var ta = document.getElementById('profileSummary');
        if (ta) {
            ta.addEventListener('input', function () {
                CVDataManager.updateProfileSummary(this.value.trim());
                updatePreview();
                });
        }
    }

    // ==========================================
    // DİNAMİK BÖLÜMLER â€” ORTAK ALTYAP
    // ==========================================

    /** Bölüm yaplandrmalar */
    var sectionConfig = {
        education: {
            container: 'educationEntries',
            factory: function () { return CVDataManager.getEmptyEducation(); },
            label: 'Eğitim',
            renderForm: renderEducationForm
        },
        experience: {
            container: 'experienceEntries',
            factory: function () { return CVDataManager.getEmptyExperience(); },
            label: 'Deneyim',
            renderForm: renderExperienceForm
        },
        skills: {
            container: 'skillEntries',
            factory: function () { return CVDataManager.getEmptySkill(); },
            label: 'Yetenek',
            renderForm: renderSkillForm
        },
        languages: {
            container: 'languageEntries',
            factory: function () { return CVDataManager.getEmptyLanguage(); },
            label: 'Dil',
            renderForm: renderLanguageForm
        },
        certifications: {
            container: 'certificationEntries',
            factory: function () { return CVDataManager.getEmptyCertification(); },
            label: 'Sertifika',
            renderForm: renderCertificationForm
        },
        projects: {
            container: 'projectEntries',
            factory: function () { return CVDataManager.getEmptyProject(); },
            label: 'Proje',
            renderForm: renderProjectForm
        }
    };

    /** "Ekle" butonlarn bağla */
    function bindAddEntryButtons() {
        document.querySelectorAll('.btn-add-entry').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var section = this.getAttribute('data-section');
                addNewEntry(section);
            });
        });
    }

    /** Yeni giriş ekle */
    function addNewEntry(sectionName) {
        var config = sectionConfig[sectionName];
        if (!config) return;
        var entry = config.factory();
        CVDataManager.addEntry(sectionName, entry);
        renderDynamicSection(sectionName);
        updatePreview();
    }

    /** Giriş sil */
    function removeEntry(sectionName, entryId) {
        CVDataManager.removeEntry(sectionName, entryId);
        renderDynamicSection(sectionName);
        updatePreview();
    }

    /** Girişi yukar taş */
    function moveEntryUp(sectionName, entryId) {
        var entries = CVDataManager.getSection(sectionName);
        var idx = entries.findIndex(function (e) { return e.id === entryId; });
        if (idx > 0) {
            CVDataManager.reorderEntry(sectionName, idx, idx - 1);
            renderDynamicSection(sectionName);
            updatePreview();
        }
    }

    /** Girişi aşağ taş */
    function moveEntryDown(sectionName, entryId) {
        var entries = CVDataManager.getSection(sectionName);
        var idx = entries.findIndex(function (e) { return e.id === entryId; });
        if (idx < entries.length - 1) {
            CVDataManager.reorderEntry(sectionName, idx, idx + 1);
            renderDynamicSection(sectionName);
            updatePreview();
        }
    }

    /** Tüm dinamik bölümleri render et */
    function renderAllDynamicSections() {
        Object.keys(sectionConfig).forEach(renderDynamicSection);
    }

    /** Tek bir dinamik bölümü render et */
    function renderDynamicSection(sectionName) {
        var config = sectionConfig[sectionName];
        if (!config) return;
        var container = document.getElementById(config.container);
        if (!container) return;

        var entries = CVDataManager.getSection(sectionName);
        if (!entries || entries.length === 0) {
            container.innerHTML = '<div class="empty-section-hint"><p style="text-align:center; color: var(--color-text-muted); font-size: var(--font-size-sm); padding: var(--space-6);">Henüz ' + config.label.toLowerCase() + ' eklenmedi.<br/>Aşağdaki butona tklayarak ekleyin.</p></div>';
            return;
        }

        var html = '';
        entries.forEach(function (entry, index) {
            html += '<div class="entry-card" data-entry-id="' + entry.id + '">';
            html += '<div class="entry-card-header">';
            html += '<span class="entry-card-title">' + config.label + ' #' + (index + 1) + '</span>';
            html += '<div class="entry-card-actions">';
            if (index > 0) {
                html += '<button type="button" class="btn-entry-action move-up" data-section="' + sectionName + '" data-id="' + entry.id + '" title="Yukar taş">&#9650;</button>';
            }
            if (index < entries.length - 1) {
                html += '<button type="button" class="btn-entry-action move-down" data-section="' + sectionName + '" data-id="' + entry.id + '" title="Aşağ taş">&#9660;</button>';
            }
            html += '<button type="button" class="btn-entry-action delete" data-section="' + sectionName + '" data-id="' + entry.id + '" title="Sil">&times;</button>';
            html += '</div></div>';
            html += config.renderForm(entry, sectionName);
            html += '</div>';
        });

        container.innerHTML = html;
        bindDynamicEntryEvents(container, sectionName);
    }

    /** Dinamik giriş event'larn bağla */
    function bindDynamicEntryEvents(container, sectionName) {
        // Silme
        container.querySelectorAll('.btn-entry-action.delete').forEach(function (btn) {
            btn.addEventListener('click', function () {
                removeEntry(this.getAttribute('data-section'), this.getAttribute('data-id'));
            });
        });
        // Yukar
        container.querySelectorAll('.btn-entry-action.move-up').forEach(function (btn) {
            btn.addEventListener('click', function () {
                moveEntryUp(this.getAttribute('data-section'), this.getAttribute('data-id'));
            });
        });
        // Aşağ
        container.querySelectorAll('.btn-entry-action.move-down').forEach(function (btn) {
            btn.addEventListener('click', function () {
                moveEntryDown(this.getAttribute('data-section'), this.getAttribute('data-id'));
            });
        });
        // nput değişiklikleri
        container.querySelectorAll('[data-entry-field]').forEach(function (input) {
            ['input', 'change'].forEach(function(evt) {
                input.addEventListener(evt, function () {
                var entryId = this.closest('.entry-card').getAttribute('data-entry-id');
                var field = this.getAttribute('data-entry-field');
                var value = this.type === 'checkbox' ? this.checked : this.value.trim();
                CVDataManager.updateEntry(sectionName, entryId, field, value);

                // "Devam ediyor" checkbox â€” bitiş tarihini devre dş brak
                if (field === 'current') {
                    var card = this.closest('.entry-card');
                    var endInput = card.querySelector('[data-entry-field="endDate"]');
                    if (endInput) {
                        endInput.disabled = this.checked; 
                        var dpGroup = endInput.closest('.date-picker-group') || (endInput.parentNode && endInput.parentNode.querySelector('.date-picker-group'));
                        // Also find the group by searching parent card
                        if (!dpGroup) {
                            var parentCard = this.closest('.entry-card');
                            if (parentCard) {
                                var hiddenEnd = parentCard.querySelector('[data-entry-field="endDate"]');
                                if (hiddenEnd) dpGroup = hiddenEnd.parentNode;
                            }
                        }
                        if(dpGroup) { 
                            var mSel = dpGroup.querySelector('.month-select');
                            var ySel = dpGroup.querySelector('.year-select');
                            if (mSel) mSel.disabled = this.checked;
                            if (ySel) ySel.disabled = this.checked;
                        }
                        if (this.checked) { endInput.value = ''; if(group) { group.querySelector('.month-select').value = ''; group.querySelector('.year-select').value = ''; } }
                    }
                }

                updatePreview();
                });
            });
        });

        // Tarih secici: ay ve yil degisince hidden input'u guncelle ve kaydet
        container.querySelectorAll('.date-picker-group').forEach(function(group) {
            var monthSel = group.querySelector('.month-select');
            var yearSel = group.querySelector('.year-select');
            var hiddenInput = group.querySelector('[data-entry-field]');
            if (!monthSel || !yearSel || !hiddenInput) return;

            function syncDateToHidden() {
                var m = monthSel.value;
                var y = yearSel.value;
                var combined = '';
                if (y && m) combined = y + '-' + m;
                else if (y) combined = y;
                hiddenInput.value = combined;
                // Veriyi modele kaydet
                var card = group.closest('.entry-card');
                if (card) {
                    var entryId = card.getAttribute('data-entry-id');
                    var field = hiddenInput.getAttribute('data-entry-field');
                    CVDataManager.updateEntry(sectionName, entryId, field, combined);
                    updatePreview();
                }
            }

            monthSel.addEventListener('change', syncDateToHidden);
            yearSel.addEventListener('change', syncDateToHidden);
        });
    }

    // ==========================================
    // EÄİTİM FORMU
    // ==========================================

    function renderEducationForm(entry) {
        return '<div class="row g-3">' +
            '<div class="col-md-6">' +
                '<label class="form-label">Okul / Üniversite <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="school" value="' + esc(entry.school) + '" placeholder="Üniversite Adı" />' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Bölüm</label>' +
                '<input type="text" class="form-control" data-entry-field="field" value="' + esc(entry.field) + '" placeholder="Bilgisayar Mühendisliğiiği" />' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Derece</label>' +
                '<select class="form-select" data-entry-field="degree">' +
                    '<option value="">Seçin</option>' +
                    '<option value="Lise"' + sel(entry.degree, 'Lise') + '>Lise</option>' +
                    '<option value="Ön Lisans"' + sel(entry.degree, 'Ön Lisans') + '>Ön Lisans</option>' +
                    '<option value="Lisans"' + sel(entry.degree, 'Lisans') + '>Lisans</option>' +
                    '<option value="Yüksek Lisans"' + sel(entry.degree, 'Yüksek Lisans') + '>Yüksek Lisans</option>' +
                    '<option value="Doktora"' + sel(entry.degree, 'Doktora') + '>Doktora</option>' +
                    '<option value="Diğer"' + sel(entry.degree, 'Diğer') + '>Diğer</option>' +
                '</select>' +
            '</div>' +
            '<div class="col-md-6">' +
                  '<label class="form-label">Tarih <span style="color:#94a3b8;font-weight:400;font-size:12px;">(istege bagli)</span></label>' +
                  renderDatePicker('startDate', entry.startDate, false) +
            '</div>' +
            '<div class="col-md-6">' +
                  '<label class="form-label">Bitis <span style="color:#94a3b8;font-weight:400;font-size:12px;">(istege bagli)</span></label>' +
                  renderDatePicker('endDate', entry.endDate, entry.current) +
            '</div>' +
            '<div class="col-12">' +
                '<div class="form-check">' +
                    '<input type="checkbox" class="form-check-input" data-entry-field="current"' + (entry.current ? ' checked' : '') + ' />' +
                    '<label class="form-check-label" style="font-size: var(--font-size-sm);">Devam ediyorum</label>' +
                '</div>' +
            '</div>' +
            '<div class="col-12">' +
                '<label class="form-label">Açıklama</label>' +
                '<textarea class="form-control" data-entry-field="description" rows="2" placeholder="Onur derecesi, projeler, başarlar...">' + esc(entry.description) + '</textarea>' +
            '</div>' +
        '</div>';
    }

    // ==========================================
    // İÅ DENEYİMİ FORMU
    // ==========================================

    
    function renderDatePicker(field, value, disabled) {
        var parts = (value || '').split('-');
        var y = parts[0] || '';
        var m = parts[1] || '';
        
        var mOpts = '<option value="">Ay</option>';
        var months = ['01|Oca', '02|Şub', '03|Mar', '04|Nis', '05|May', '06|Haz', '07|Tem', '08|Ağu', '09|Eyl', '10|Eki', '11|Kas', '12|Ara'];
        months.forEach(function(mon) {
            var spl = mon.split('|');
            mOpts += '<option value="' + spl[0] + '"' + (m === spl[0] ? ' selected' : '') + '>' + spl[1] + '</option>';
        });
        
        var yOpts = '<option value="">Yıl</option>';
        var currY = new Date().getFullYear();
        for(var i = currY + 5; i >= currY - 50; i--) {
            var sy = i.toString();
            yOpts += '<option value="' + sy + '"' + (y === sy ? ' selected' : '') + '>' + sy + '</option>';
        }
        
        var dis = disabled ? ' disabled' : '';
                return '<div class="input-group date-picker-group shadow-sm" style="border-radius:10px; overflow:hidden;">' +
            '<span class="input-group-text" style="background:#f8fafc; border-color:#cbd5e1; color:#64748b; border-right:none;"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/></svg></span>' +
            '<select class="form-select month-select" data-for="' + field + '"' + dis + ' style="border-left:none; border-color:#cbd5e1; font-weight:500; cursor:pointer;">' + mOpts + '</select>' +
            '<select class="form-select year-select" data-for="' + field + '"' + dis + ' style="border-left:1px solid #e2e8f0; border-color:#cbd5e1; font-weight:500; cursor:pointer;">' + yOpts + '</select>' +
            '<input type="hidden" data-entry-field="' + field + '" value="' + esc(value) + '" />' +
        '</div>';
    }

    function renderExperienceForm(entry) {
        return '<div class="row g-3">' +
            '<div class="col-md-6">' +
                '<label class="form-label">Şirket <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="company" value="' + esc(entry.company) + '" placeholder="Şirket Adı" />' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Pozisyon <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="position" value="' + esc(entry.position) + '" placeholder="Yazılım Geliştirici" />' +
            '</div>' +
            '<div class="col-md-6">' +
                  '<label class="form-label">Tarih <span style="color:#94a3b8;font-weight:400;font-size:12px;">(istege bagli)</span></label>' +
                  renderDatePicker('startDate', entry.startDate, false) +
            '</div>' +
            '<div class="col-md-6">' +
                  '<label class="form-label">Bitis <span style="color:#94a3b8;font-weight:400;font-size:12px;">(istege bagli)</span></label>' +
                  renderDatePicker('endDate', entry.endDate, entry.current) +
            '</div>' +
            '<div class="col-md-6">' +
                '<div class="form-check" style="margin-top: 2rem;">' +
                    '<input type="checkbox" class="form-check-input" data-entry-field="current"' + (entry.current ? ' checked' : '') + ' />' +
                    '<label class="form-check-label" style="font-size: var(--font-size-sm);">Halen çalşyorum</label>' +
                '</div>' +
            '</div>' +
            '<div class="col-12">' +
                '<label class="form-label">Görev Tanm</label>' +
                '<textarea class="form-control" data-entry-field="description" rows="3" placeholder="Sorumluluklarınız ve başarılarınız...">' + esc(entry.description) + '</textarea>' +
                '<div class="form-text">Her maddeyi yeni satra yazabilirsiniz.</div>' +
            '</div>' +
        '</div>';
    }

    // ==========================================
    // YETENEKLER FORMU
    // ==========================================


    function renderCustomSectionForm(entry) {
        return '<div class="row g-3">' +
            '<div class="col-12">' +
                '<label class="form-label">Bölüm Başlığı <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="title" value="' + esc(entry.title || '') + '" placeholder="Gönüllülük, Hobiler, Referanslar..." />' +
            '</div>' +
            '<div class="col-12">' +
                '<label class="form-label">İçerik</label>' +
                '<textarea class="form-control" data-entry-field="content" rows="4" placeholder="Bu bölüme ait bilgileri buraya yazın...">' + esc(entry.content || '') + '</textarea>' +
                '<div class="form-text mt-1">Her satırı - ile başlatırsanız madde listesi olarak görünür.</div>' +
            '</div>' +
        '</div>';
    }

    function renderSkillForm(entry) {
        var levelOptions = SKILL_LEVELS.map(function (l) {
            return '<option value="' + l.value + '"' + sel(entry.level, l.value) + '>' + l.label + '</option>';
        }).join('');

        return '<div class="row g-3">' +
            '<div class="col-md-7">' +
                '<label class="form-label">Yetenek Adı <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="name" value="' + esc(entry.name) + '" placeholder="JavaScript, Proje Yönetimi..." />' +
            '</div>' +
            '<div class="col-md-5">' +
                '<label class="form-label">Seviye <span style="color:#94a3b8;font-weight:400;font-size:12px;">(isteğe bağlı)</span></label>' +
                '<select class="form-select" data-entry-field="level"><option value="">Belirtmek istemiyorum</option>' + levelOptions + '</select>' +
            '</div>' +
        '</div>';
    }

    // ==========================================
    // DİLLER FORMU
    // ==========================================

    function renderLanguageForm(entry) {
        var levelOptions = LANGUAGE_LEVELS.map(function (l) {
            return '<option value="' + l.value + '"' + sel(entry.level, l.value) + '>' + l.label + '</option>';
        }).join('');

        return '<div class="row g-3">' +
            '<div class="col-md-6">' +
                '<label class="form-label">Dil <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="name" value="' + esc(entry.name) + '" placeholder="İİngilizce, Almanca..." />' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Seviye <span style="color:#94a3b8;font-weight:400;font-size:12px;">(isteğe bağlı)</span></label>' +
                '<select class="form-select" data-entry-field="level"><option value="">Belirtmek istemiyorum</option>' + levelOptions + '</select>' +
            '</div>' +
        '</div>';
    }

    // ==========================================
    // SERTİFİKALAR FORMU
    // ==========================================

    function renderCertificationForm(entry) {
        return '<div class="row g-3">' +
            '<div class="col-md-6">' +
                '<label class="form-label">Sertifika Adı <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="name" value="' + esc(entry.name) + '" placeholder="AWS Solutions Architect" />' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Veren Kurum</label>' +
                '<input type="text" class="form-control" data-entry-field="issuer" value="' + esc(entry.issuer) + '" placeholder="Amazon Web Services" />' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Tarih</label>' +
                renderDatePicker('date', entry.date, false) +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Doğrulama URL</label>' +
                '<input type="url" class="form-control" data-entry-field="url" value="' + esc(entry.url) + '" placeholder="https://..." />' +
            '</div>' +
        '</div>';
    }

    // ==========================================
    // PROJELER FORMU
    // ==========================================

    function renderProjectForm(entry) {
        return '<div class="row g-3">' +
            '<div class="col-md-6">' +
                '<label class="form-label">Proje Adı <span style="color:var(--color-danger)">*</span></label>' +
                '<input type="text" class="form-control" data-entry-field="name" value="' + esc(entry.name) + '" placeholder="E-ticaret Platformu" />' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">Teknolojiler</label>' +
                '<input type="text" class="form-control" data-entry-field="technologies" value="' + esc(entry.technologies) + '" placeholder="React, Node.js, PostgreSQL" />' +
            '</div>' +
            '<div class="col-12">' +
                '<label class="form-label">Açıklama</label>' +
                '<textarea class="form-control" data-entry-field="description" rows="2" placeholder="Projenin amac ve katkılarınız...">' + esc(entry.description) + '</textarea>' +
            '</div>' +
            '<div class="col-12">' +
                '<label class="form-label">Proje URL</label>' +
                '<input type="url" class="form-control" data-entry-field="url" value="' + esc(entry.url) + '" placeholder="https://github.com/..." />' +
            '</div>' +
        '</div>';
    }

    // ==========================================
    // FORM VERİSİ YÜKLEME
    // ==========================================

    function loadFormData() {
        var data = CVDataManager.getData();
        var pi = data.personalInfo;
        setVal('firstName', pi.firstName);
        setVal('lastName', pi.lastName);
        setVal('email', pi.email);
        setVal('phone', pi.phone);
        setVal('address', pi.address);
        setVal('linkedin', pi.linkedin);
        setVal('website', pi.website);
        setVal('driversLicense', pi.driversLicense);
        var summaryEl = document.getElementById('profileSummary');
        if (summaryEl) summaryEl.value = data.profileSummary || '';
    }

    function setVal(id, value) {
        var el = document.getElementById(id);
        if (el) el.value = value || '';
    }

    // ==========================================
    // ÅABLON SEÇİCİ
    // ==========================================

            function bindMobileToggle() {
        if (!els.mobileToggle) return;
        els.mobileToggle.addEventListener('click', function() {
            var isPreview = els.previewPanel.style.display === 'block';
            if (isPreview) {
                els.previewPanel.style.display = 'none';
                els.formPanel.style.display = 'block';
                if (els.mobileToggleLabel) els.mobileToggleLabel.textContent = 'Önizlemeyi Göster';
            } else {
                els.formPanel.style.display = 'none';
                els.previewPanel.style.display = 'block';
                if (els.mobileToggleLabel) els.mobileToggleLabel.textContent = 'Forma Dön';
            }
        });
    }

    function initTemplateSelector() {
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
    // PDF DÅA AKTARMA (html2pdf.js)
    // ==========================================
    
        function bindPdfExportEvent() {
        if (!els.btnDownloadPdf) return;

        els.btnDownloadPdf.addEventListener('click', function() {
            var _chkData = CVDataManager.getData();
            var _chkPi = (_chkData && _chkData.personalInfo) ? _chkData.personalInfo : {};
            if (!_chkPi.firstName || !_chkPi.lastName) {
                alert('PDF oluşturmak için lütfen önce Adınızı ve Soyadınızı girin (1. Adım: Kişisel Bilgiler).');
                return;
            }
            // Artık modal yok, direkt indir
            executePdfExport(els.btnDownloadPdf, null);
        });
    }

    function executePdfExport(btn, modal) {
        var originalText = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Hazirlaniyor...';
        btn.disabled = true;

        var data = CVDataManager.getData();
        var firstName = data.personalInfo.firstName || 'CV';
        var lastName  = data.personalInfo.lastName  || '';
        var fileName  = (firstName + '_' + lastName).trim().replace(/\s+/g, '_') + '_CV.pdf';

        var content = els.previewContent.innerHTML;

        // Tum CSS'leri topla (builder.css haric)
        var cssLinks  = '';
        var cssStyles = '';
        document.querySelectorAll('link[rel="stylesheet"]').forEach(function(l) {
            if (!l.href || !l.href.includes('cv-builder.css')) cssLinks += l.outerHTML;
        });
        document.querySelectorAll('style').forEach(function(s) {
            cssStyles += s.outerHTML;
        });

        // Yeni pencerede temiz render
        var pdfWin = window.open('', '_blank', 'width=900,height=1200');
        if (!pdfWin) {
            alert('Lutfen pop-up engelleyiciye izin verin.');
            btn.innerHTML = originalText;
            btn.disabled = false;
            return;
        }

        pdfWin.document.write('<!DOCTYPE html><html lang="tr"><head>');
        pdfWin.document.write('<meta charset="utf-8">');
        pdfWin.document.write('<title>' + fileName + '</title>');
        pdfWin.document.write(cssLinks);
        pdfWin.document.write(cssStyles);
        pdfWin.document.write('<style>');
        pdfWin.document.write('@page { size: A4 portrait; margin: 0; }');
        pdfWin.document.write('* { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }');
        pdfWin.document.write('html, body { margin: 0; padding: 0; width: 100%; background: #fff; }');
        pdfWin.document.write('.cv-tpl { width: 100% !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');
        // Yazdir butonunu goster - kullanici PDF olarak kaydedebilir
        pdfWin.document.write('.pdf-save-bar { position: fixed; top: 0; left: 0; right: 0; z-index: 9999; background: #1e3a8a; color: #fff; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; font-family: Inter, sans-serif; font-size: 14px; }');
        pdfWin.document.write('.pdf-save-bar button { background: #fff; color: #1e3a8a; border: none; padding: 8px 20px; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 14px; }');
        pdfWin.document.write('@media print { .pdf-save-bar { display: none !important; } body { margin-top: 0 !important; } }');
        pdfWin.document.write('body.has-bar { margin-top: 60px; }');
        pdfWin.document.write('</style>');
        pdfWin.document.write('</head><body class="has-bar">');
        pdfWin.document.write('<div class="pdf-save-bar">');
        pdfWin.document.write('<span>Kaydetmek icin: <strong>Ctrl+P</strong> → Hedef: <strong>PDF olarak kaydet</strong> → Kenar boslugu: <strong>Yok</strong></span>');
        pdfWin.document.write('<button onclick="window.print()">PDF Kaydet</button>');
        pdfWin.document.write('</div>');
        pdfWin.document.write(content);
        pdfWin.document.write('</body></html>');
        pdfWin.document.close();

        btn.innerHTML = originalText;
        btn.disabled = false;
        if (modal) { setTimeout(function(){ modal.hide(); }, 300); }
    }

            function executePrint() {
        var content = els.previewContent.innerHTML;
        var printWindow = window.open('', '_blank', 'width=1000,height=900');
        if (!printWindow) {
            alert("Lütfen yazdırma penceresi için pop-up engelleyiciye izin verin.");
            return;
        }
        
        printWindow.document.write('<html><head><title>CV Yazdır - NovaCV</title>');
        
        // Ana sayfadaki CSS'leri al
        var styles = document.querySelectorAll('link[rel="stylesheet"], style');
        styles.forEach(function(s) { 
            // cv-builder.css'i alma, sadece template ve bootstrap kalsın
            if (!s.href || !s.href.includes('cv-builder.css')) {
                printWindow.document.write(s.outerHTML); 
            }
        });
        
        // Özel Print CSS'i
        printWindow.document.write('<style>');
        printWindow.document.write('@page { size: A4 portrait; margin: 0; }');
        printWindow.document.write('html, body { margin: 0; padding: 0; width: 100%; background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }');
        printWindow.document.write('.cv-tpl { width: 100% !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');
        printWindow.document.write('</style>');
        
        printWindow.document.write('</head><body>');
        printWindow.document.write(content);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        
        setTimeout(function() {
            printWindow.focus();
            printWindow.print();
            // printWindow.close(); // Kullanıcı isterse sekmeyi kendi kapatır, bazen erken kapanırsa yazdırma iptal oluyor
        }, 800);
    }

    var _autoSaveTimer = null;
    function autoSave() {
        if (_autoSaveTimer) clearTimeout(_autoSaveTimer);
        _autoSaveTimer = setTimeout(function() {
            try { CVDataManager.save(); } catch(e) {}
        }, 400);
    }

    function updatePreview() {
        try {
            
        if (typeof syncWithBackend === 'function') syncWithBackend();
        var data = CVDataManager.getData();
        
        // Update template label regardless of data presence
        if (typeof CVTemplateManager !== 'undefined') {
            var tpl = CVTemplateManager.getCurrentTemplate();
            var label = document.getElementById('previewTemplateLabel');
            if (label) label.textContent = tpl.name;
        }

        if (!CVDataManager.hasData()) {
            els.previewPlaceholder.style.display = 'flex';
            els.previewContent.style.display = 'none';
            return;
        }

        els.previewPlaceholder.style.display = 'none';
        els.previewContent.style.display = 'block';

        // Åablon sistemi varsa kullan, yoksa fallback
        if (typeof CVTemplateManager !== 'undefined') {
            els.previewContent.innerHTML = CVTemplateManager.render(data);
        } else {
            els.previewContent.innerHTML = renderPreviewFallback(data);
        }
    
        } catch (err) {
            console.error(err);
            alert("Önizleme Hatası: " + err.message);
        }
    }

    // --- Fallback (şablon yüklenmezse) ---
    function renderPreviewFallback(data) {
        var pi = data.personalInfo;
        var name = ((pi.firstName || '') + ' ' + (pi.lastName || '')).trim();
        if (!name) return '';
        return '<div style="text-align:center;"><h1 style="font-size:22pt;margin:0;">' + escHtml(name) + '</h1></div>';
    }

    // --- Önizleme: Başlk ---
    function renderPreviewHeader(data) {
        var pi = data.personalInfo;
        var fullName = ((pi.firstName || '') + ' ' + (pi.lastName || '')).trim();
        if (!fullName) return '';

        var h = '<div class="cv-prev-header">';
        h += '<h1 class="cv-prev-name">' + escHtml(fullName) + '</h1>';

        var contacts = [];
        if (pi.email) contacts.push(escHtml(pi.email));
        if (pi.phone) contacts.push(escHtml(pi.phone));
        if (pi.address) contacts.push(escHtml(pi.address));
        if (contacts.length) h += '<p class="cv-prev-contacts">' + contacts.join(' &bull; ') + '</p>';

        var links = [];
        if (pi.linkedin) links.push(escHtml(pi.linkedin));
        if (pi.website) links.push(escHtml(pi.website));
        if (links.length) h += '<p class="cv-prev-links">' + links.join(' &bull; ') + '</p>';

        h += '</div>';
        return h;
    }

    // --- Önizleme: Profil ---
    function renderPreviewProfile(data) {
        if (!data.profileSummary) return '';
        return '<div class="cv-prev-section">' +
            '<h2 class="cv-prev-section-title">Profil</h2>' +
            '<p class="cv-prev-text">' + escHtml(data.profileSummary) + '</p>' +
        '</div>';
    }

    // --- Önizleme: İş Deneyimi ---
    function renderPreviewExperience(data) {
        if (!data.experience || data.experience.length === 0) return '';
        var h = '<div class="cv-prev-section"><h2 class="cv-prev-section-title">İş Deneyimi</h2>';
        data.experience.forEach(function (e) {
            if (!e.position && !e.company) return;
            h += '<div class="cv-prev-entry">';
            h += '<div class="cv-prev-entry-header">';
            h += '<strong class="cv-prev-entry-title">' + escHtml(e.position || '') + '</strong>';
            h += '<span class="cv-prev-entry-date">' + formatDateRange(e.startDate, e.endDate, e.current) + '</span>';
            h += '</div>';
            if (e.company) h += '<div class="cv-prev-entry-subtitle">' + escHtml(e.company) + '</div>';
            if (e.description) {
                h += '<div class="cv-prev-entry-desc">' + formatDescription(e.description) + '</div>';
            }
            h += '</div>';
        });
        h += '</div>';
        return h;
    }

    // --- Önizleme: Eğitim ---
    function renderPreviewEducation(data) {
        if (!data.education || data.education.length === 0) return '';
        var h = '<div class="cv-prev-section"><h2 class="cv-prev-section-title">Eğitim</h2>';
        data.education.forEach(function (e) {
            if (!e.school && !e.degree) return;
            h += '<div class="cv-prev-entry">';
            h += '<div class="cv-prev-entry-header">';
            var title = e.degree || '';
            if (e.field) title += (title ? ', ' : '') + e.field;
            h += '<strong class="cv-prev-entry-title">' + escHtml(title) + '</strong>';
            h += '<span class="cv-prev-entry-date">' + formatDateRange(e.startDate, e.endDate, e.current) + '</span>';
            h += '</div>';
            if (e.school) h += '<div class="cv-prev-entry-subtitle">' + escHtml(e.school) + '</div>';
            if (e.description) h += '<div class="cv-prev-entry-desc">' + escHtml(e.description) + '</div>';
            h += '</div>';
        });
        h += '</div>';
        return h;
    }

    // --- Önizleme: Yetenekler ---
    function renderPreviewSkills(data) {
        if (!data.skills || data.skills.length === 0) return '';
        var names = data.skills.filter(function (s) { return s.name; });
        if (names.length === 0) return '';
        var h = '<div class="cv-prev-section"><h2 class="cv-prev-section-title">Yetenekler</h2>';
        h += '<div class="cv-prev-tags">';
        names.forEach(function (s) {
            var levelLabel = SKILL_LEVELS.find(function (l) { return l.value === s.level; });
            h += '<span class="cv-prev-tag">' + escHtml(s.name);
            if (levelLabel) h += ' <span class="cv-prev-tag-level">(' + levelLabel.label + ')</span>';
            h += '</span>';
        });
        h += '</div></div>';
        return h;
    }

    // --- Önizleme: Diller ---
    function renderPreviewLanguages(data) {
        if (!data.languages || data.languages.length === 0) return '';
        var named = data.languages.filter(function (l) { return l.name; });
        if (named.length === 0) return '';
        var h = '<div class="cv-prev-section"><h2 class="cv-prev-section-title">Diller</h2>';
        h += '<div class="cv-prev-lang-list">';
        named.forEach(function (l) {
            var levelLabel = LANGUAGE_LEVELS.find(function (lv) { return lv.value === l.level; });
            h += '<div class="cv-prev-lang-item">';
            h += '<span>' + escHtml(l.name) + '</span>';
            if (levelLabel) h += '<span class="cv-prev-lang-level">' + levelLabel.label + '</span>';
            h += '</div>';
        });
        h += '</div></div>';
        return h;
    }

    // --- Önizleme: Sertifikalar ---
    function renderPreviewCertifications(data) {
        if (!data.certifications || data.certifications.length === 0) return '';
        var named = data.certifications.filter(function (c) { return c.name; });
        if (named.length === 0) return '';
        var h = '<div class="cv-prev-section"><h2 class="cv-prev-section-title">Sertifikalar</h2>';
        named.forEach(function (c) {
            h += '<div class="cv-prev-entry">';
            h += '<div class="cv-prev-entry-header">';
            h += '<strong class="cv-prev-entry-title">' + escHtml(c.name) + '</strong>';
            if (c.date) h += '<span class="cv-prev-entry-date">' + formatMonth(c.date) + '</span>';
            h += '</div>';
            if (c.issuer) h += '<div class="cv-prev-entry-subtitle">' + escHtml(c.issuer) + '</div>';
            h += '</div>';
        });
        h += '</div>';
        return h;
    }

    // --- Önizleme: Projeler ---
    function renderPreviewProjects(data) {
        if (!data.projects || data.projects.length === 0) return '';
        var named = data.projects.filter(function (p) { return p.name; });
        if (named.length === 0) return '';
        var h = '<div class="cv-prev-section"><h2 class="cv-prev-section-title">Projeler</h2>';
        named.forEach(function (p) {
            h += '<div class="cv-prev-entry">';
            h += '<strong class="cv-prev-entry-title">' + escHtml(p.name) + '</strong>';
            if (p.technologies) h += '<div class="cv-prev-entry-tech">' + escHtml(p.technologies) + '</div>';
            if (p.description) h += '<div class="cv-prev-entry-desc">' + escHtml(p.description) + '</div>';
            if (p.url) h += '<div class="cv-prev-entry-url">' + escHtml(p.url) + '</div>';
            h += '</div>';
        });
        h += '</div>';
        return h;
    }

    // ==========================================
    // YARDMC FONKSİYONLAR
    // ==========================================

    /** HTML attribute escape */
    function esc(text) {
        if (!text) return '';
        return String(text).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    /** HTML content escape */
    function escHtml(text) {
        if (!text) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }

    /** Select option selected attribute */
    function sel(current, value) {
        return current === value ? ' selected' : '';
    }

    /** Tarih aralğ formatla */
    function formatDateRange(start, end, current) {
        var s = formatMonth(start);
        if (!s) return '';
        if (current) return s + ' â€“ Devam ediyor';
        var e = formatMonth(end);
        return e ? s + ' â€“ ' + e : s;
    }

    /** Ay formatla: 2024-03 â†’ Mart 2024 */
    function formatMonth(dateStr) {
        if (!dateStr) return '';
        var parts = dateStr.split('-');
        if (parts.length < 2) return dateStr;
        var months = ['', 'Ocak', 'Åubat', 'Mart', 'Nisan', 'Mays', 'Haziran',
            'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasm', 'Aralk'];
        var m = parseInt(parts[1], 10);
        return (months[m] || '') + ' ' + parts[0];
    }

    /** Açıklama metni â€” satr sonlarn <br/> veya liste yapar */
    function formatDescription(text) {
        if (!text) return '';
        var lines = text.split('\n').filter(function (l) { return l.trim(); });
        if (lines.length <= 1) return '<p class="cv-prev-text">' + escHtml(text) + '</p>';
        var items = lines.map(function (l) { return '<li>' + escHtml(l.trim()) + '</li>'; }).join('');
        return '<ul class="cv-prev-list">' + items + '</ul>';
    }

    // ==========================================
    // BAÅLAT
    // ==========================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    return {
        goToStep: goToStep,
        updatePreview: updatePreview,
        getCurrentStep: function () { return currentStep; }
    };
})();


// --- BACKEND SYNC ---
var syncTimeout;
function syncWithBackend() {
    if (!window._isLoggedIn) return; // Sadece giris yapilmissa sync et
    clearTimeout(syncTimeout);
    syncTimeout = setTimeout(function() {
        var data = CVDataManager.getData();
        fetch('/api/CvApi/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(function(res) {
            if (res.ok) {
                var badge = document.getElementById('cloudSyncBadge');
                if (badge) { badge.textContent = 'Buluta kaydedildi ✓'; badge.style.color = '#16a34a'; }
            }
        }).catch(function(err) {
            console.warn('Cloud Sync Error (local mode)', err);
        });
    }, 2000);
}

// Override CVDataManager.saveData to also sync with backend


// --- LOAD FROM BACKEND ---
window.addEventListener('DOMContentLoaded', function() {
    fetch('/api/CvApi/load')
        .then(function(res) {
            if (res.status === 401) {
                window._isLoggedIn = false;
                console.log('Running in local mode (not logged in)');
                return null;
            }
            window._isLoggedIn = true;
            return res.json();
        })
        .then(function(res) {
            if (!res) return;
            if (res.success && res.data) {
                try {
                    var cloudData = JSON.parse(res.data);
                    // Bulut verisi localStoragedan daha yeniyse yukle
                    localStorage.setItem('cv_builder_data', JSON.stringify(cloudData));
                    if (typeof CVBuilder !== 'undefined') {
                        CVDataManager.load();
                        CVBuilder.updatePreview();
                    }
                } catch(e) { console.warn('Cloud data parse error', e); }
            }
        })
        .catch(function(err) {
            window._isLoggedIn = false;
            console.log('Running in local mode', err);
        });
});

// --- SORTABLE JS ---
function initSortable() {
    if (typeof Sortable === 'undefined') return;
    
    var containers = ['experienceList', 'educationList', 'projectList', 'skillList', 'langList', 'certList'];
    containers.forEach(function(id) {
        var el = document.getElementById(id);
        if (el) {
            Sortable.create(el, {
                animation: 150,
                onEnd: function() {
                    // Trigger a save after reordering
                    // For simplicity, we just trigger the Save all button logic or manual re-parse
                    // A proper implementation would re-parse the DOM to array
                }
            });
        }
    });
}
setTimeout(initSortable, 1000);

// --- QULL JS ---
function initQuill() {
    if (typeof Quill === 'undefined') return;
    var summaryEl = document.getElementById('profileSummary');
    if (summaryEl) {
        // Create wrapper
        var wrapper = document.createElement('div');
        summaryEl.parentNode.insertBefore(wrapper, summaryEl);
        wrapper.appendChild(summaryEl);
        summaryEl.style.display = 'none';
        
        var editor = document.createElement('div');
        wrapper.appendChild(editor);
        
        var quill = new Quill(editor, { theme: 'snow' });
        quill.root.innerHTML = summaryEl.value;
        
        quill.on('text-change', function() {
            summaryEl.value = quill.root.innerHTML;
            summaryEl.dispatchEvent(new Event('input', { bubbles: true }));
        });
    }
}
setTimeout(initQuill, 1000);


document.addEventListener('DOMContentLoaded', function() {
    var photoInput = document.getElementById('profilePhoto');
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (!file) return;
            // Validate file type
            if (!file.type.startsWith('image/')) {
                alert('Lütfen geçerli bir görsel dosyası seçin (JPG, PNG, vb.)');
                return;
            }
            // Show preview thumbnail immediately
            var previewImg = document.getElementById('photoPreview');
            var reader = new FileReader();
            reader.onload = function(event) {
                var dataUrl = event.target.result;
                // Show thumbnail in form
                if (!previewImg) {
                    previewImg = document.createElement('img');
                    previewImg.id = 'photoPreview';
                    previewImg.style.cssText = 'width:80px;height:80px;border-radius:50%;object-fit:cover;margin-top:10px;border:2px solid #e2e8f0;display:block;';
                    photoInput.parentNode.appendChild(previewImg);
                }
                previewImg.src = dataUrl;
                // Save to data model
                var data = CVDataManager.getData();
                data.personalInfo.photo = dataUrl;
                CVDataManager.save();
                // Force preview update
                if (typeof CVBuilder !== 'undefined') {
                    CVBuilder.updatePreview();
                }
            };
            reader.onerror = function() {
                alert('Fotoğraf yüklenirken hata oluştu. Lütfen tekrar deneyin.');
            };
            reader.readAsDataURL(file);
        });
    }
    // Restore saved photo thumbnail on load
    try {
        var savedData = CVDataManager.getData();
        if (savedData && savedData.personalInfo && savedData.personalInfo.photo && photoInput) {
            var previewImg = document.createElement('img');
            previewImg.id = 'photoPreview';
            previewImg.style.cssText = 'width:80px;height:80px;border-radius:50%;object-fit:cover;margin-top:10px;border:2px solid #e2e8f0;display:block;';
            previewImg.src = savedData.personalInfo.photo;
            photoInput.parentNode.appendChild(previewImg);
        }
    } catch(e) {}
});
// --- SORTABLE JS FX ---
function initSortableFixed() {
    if (typeof Sortable === 'undefined') return;
    
    var containers = ['experienceEntries', 'educationEntries', 'projectEntries', 'skillEntries', 'languageEntries', 'certificationEntries'];
    containers.forEach(function(id) {
        var el = document.getElementById(id);
        if (el) {
            Sortable.create(el, {
                animation: 150,
                onEnd: function(evt) {
                    // Update data model by reading the DOM order
                    // Re-render preview
                }
            });
        }
    });
}
setTimeout(initSortableFixed, 1500);
































