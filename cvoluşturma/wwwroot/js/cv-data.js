/* ============================================
   CV Data Manager
   Veri modeli, CRUD işlemleri ve localStorage yönetimi
   ============================================ */

const CVDataManager = (function () {
    'use strict';

    const STORAGE_KEY = 'cv_builder_data';
    const STORAGE_META_KEY = 'cv_builder_meta';

    /**
     * Boş CV veri modeli döndürür
     */
    function getDefaultData() {
        return {
            personalInfo: {
                firstName: 'Ahmet',
                lastName: 'Yılmaz',
                email: 'ahmet.yilmaz@email.com',
                phone: '+90 555 123 45 67',
                address: 'Kadıköy, İstanbul',
                linkedin: 'linkedin.com/in/ahmetyilmaz',
                website: 'ahmetyilmaz.dev',
                driversLicense: 'B Sınıfı',
                photoUrl: ''
            },
            profileSummary: 'Kullanıcı odaklı ve performanslı web uygulamaları geliştirme konusunda 5 yılı aşkın deneyime sahip Kıdemli Yazılım Mühendisi. C#, .NET Core ve modern JavaScript frameworkleri ile ölçeklenebilir sistemler tasarlama konusunda uzmanım.',
            education: [
                { id: 'edu1', school: 'İstanbul Teknik Üniversitesi', degree: 'Lisans', field: 'Bilgisayar Mühendisliği', startDate: '2015', endDate: '2019', description: 'Bölüm 3.sü olarak mezun oldum. Bitirme projesi olarak yapay zeka destekli bir CV analiz aracı geliştirdim.' }
            ],
            experience: [
                { id: 'exp1', company: 'TechNova Yazılım', position: 'Kıdemli Yazılım Geliştirici', startDate: '2021', endDate: '', current: true, description: '- Mikroservis mimarisine geçiş sürecini yönettim.\n- Sistemin tepki süresini %40 oranında iyileştirdim.\n- 5 kişilik frontend ekibine liderlik ettim.' },
                { id: 'exp2', company: 'Global Çözümler A.Ş.', position: 'Yazılım Geliştirici', startDate: '2019', endDate: '2021', current: false, description: '- B2B e-ticaret platformunun arayüz bileşenlerini React ile geliştirdim.\n- RESTful API mimarisi tasarladım.' }
            ],
            skills: [
                { id: 'sk1', name: 'C# / .NET Core', level: 'İleri' },
                { id: 'sk2', name: 'React / JavaScript', level: 'İleri' },
                { id: 'sk3', name: 'SQL Server / MongoDB', level: 'Orta' },
                { id: 'sk4', name: 'Docker / Kubernetes', level: 'Orta' }
            ],
            languages: [
                { id: 'lang1', name: 'İngilizce', level: 'C1' },
                { id: 'lang2', name: 'Almanca', level: 'A2' }
            ],
            certifications: [
                { id: 'cert1', name: 'AWS Certified Developer - Associate', issuer: 'Amazon Web Services', date: '2022' },
                { id: 'cert2', name: 'Scrum Master (CSM)', issuer: 'Scrum Alliance', date: '2021' }
            ],
            projects: [
                { id: 'proj1', name: 'Nova E-Ticaret Altyapısı', role: 'Baş Geliştirici', date: '2023', description: 'Aylık 1 milyon aktif kullanıcısı olan e-ticaret sitesinin sepet ve ödeme altyapısının yenilenmesi.' }
            ],
            customSections: []
        };
    }

    let _data = getDefaultData();

    function generateId() {
        return Math.random().toString(36).substr(2, 9);
    }

    function getEmptyEducation() {
        return { id: generateId(), school: '', degree: '', field: '', startDate: '', endDate: '', description: '' };
    }

    function getEmptyExperience() {
        return { id: generateId(), company: '', position: '', startDate: '', endDate: '', current: false, description: '' };
    }

    function getEmptySkill() {
        return { id: generateId(), name: '', level: '' };
    }

    function getEmptyLanguage() {
        return { id: generateId(), name: '', level: '' };
    }

    function getEmptyCertification() {
        return { id: generateId(), name: '', issuer: '', date: '' };
    }

    function getEmptyProject() {
        return { id: generateId(), name: '', role: '', date: '', description: '' };
    }
    // Guvenlik: Gelen JSON verisinin beklenen yapida oldugunu dogrula
    function validateSchema(data) {
        if (!data || typeof data !== "object") return getDefaultData();
        var arrayFields = ["experience", "education", "skills", "languages", "certifications", "projects", "customSections"];
        arrayFields.forEach(function(field) {
            if (!Array.isArray(data[field])) {
                data[field] = [];
            }
        });
        if (!data.personalInfo || typeof data.personalInfo !== "object") {
            data.personalInfo = {};
        }
        if (typeof data.profileSummary !== "string") {
            data.profileSummary = "";
        }
        return data;
    }



    function load() {
        // localStorage.removeItem silindi — kullanici verileri artik korunuyor
        try {
            var stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                _data = validateSchema(JSON.parse(stored));
            } else {
                _data = getDefaultData();
            }
        } catch (e) {
            console.warn('CV verisi yüklenirken hata:', e);
            _data = getDefaultData();
        }
        return _data;
    }

    function save() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(_data));
            localStorage.setItem(STORAGE_META_KEY, JSON.stringify({
                lastSaved: new Date().toISOString(),
                version: 1
            }));
            return true;
        } catch (e) {
            console.error('CV verisi kaydedilirken hata:', e);
            return false;
        }
    }

    /**
     * Tüm veriyi döndürür
     */
    function getData() {
        if (!_data) load();
        return _data;
    }

    /**
     * Belirli bir bölümü döndürür
     */
    function getSection(sectionName) {
        if (!_data) load();
        return _data[sectionName];
    }

    /**
     * Kişisel bilgileri günceller
     */
    function updatePersonalInfo(field, value) {
        if (!_data) load();
        // hasOwnProperty yerine direkt atama - yeni alanlar icin de calisir
        _data.personalInfo[field] = value;
        save();
    }

    /**
     * Profil özetini günceller
     */
    function updateProfileSummary(value) {
        if (!_data) load();
        _data.profileSummary = value;
        save();
    }

    /**
     * Bir bölüme yeni giriş ekler
     */
    function addEntry(sectionName, entry) {
        if (!_data) load();
        if (Array.isArray(_data[sectionName])) {
            _data[sectionName].push(entry);
            save();
            return entry;
        }
        return null;
    }

    /**
     * Bir bölümdeki girişi günceller
     */
    function updateEntry(sectionName, entryId, field, value) {
        if (!_data) load();
        const section = _data[sectionName];
        if (Array.isArray(section)) {
            const entry = section.find(e => e.id === entryId);
            if (entry) {
                entry[field] = value;
                save();
                return true;
            }
        }
        return false;
    }

    /**
     * Bir bölümdeki girişi siler
     */
    function removeEntry(sectionName, entryId) {
        if (!_data) load();
        const section = _data[sectionName];
        if (Array.isArray(section)) {
            const index = section.findIndex(e => e.id === entryId);
            if (index !== -1) {
                section.splice(index, 1);
                save();
                return true;
            }
        }
        return false;
    }

    /**
     * Bir bölümdeki girişlerin sırasını değiştirir
     */
    function reorderEntry(sectionName, fromIndex, toIndex) {
        if (!_data) load();
        const section = _data[sectionName];
        if (Array.isArray(section) && fromIndex >= 0 && toIndex >= 0 &&
            fromIndex < section.length && toIndex < section.length) {
            const [moved] = section.splice(fromIndex, 1);
            section.splice(toIndex, 0, moved);
            save();
            return true;
        }
        return false;
    }

    /**
     * Tüm veriyi sıfırlar
     */
    function reset() {
        _data = getDefaultData();
        save();
        return _data;
    }

    /**
     * Meta bilgilerini döndürür (son kayıt zamanı vs.)
     */
    function getMeta() {
        try {
            const meta = localStorage.getItem(STORAGE_META_KEY);
            return meta ? JSON.parse(meta) : null;
        } catch (e) {
            return null;
        }
    }

    /**
     * Verinin dolu olup olmadığını kontrol eder
     */
    function hasData() {
        if (!_data) load();
        const pi = _data.personalInfo;
        return !!(pi.firstName || pi.lastName || pi.email ||
            _data.profileSummary ||
            _data.education.length > 0 ||
            _data.experience.length > 0 ||
            _data.skills.length > 0);
    }


    function getEmptyCustomSection() {
        return {
            id: generateId(),
            title: 'Özel Bölüm',
            content: ''
        };
    }

    // Public API
    return {
        load: load,
        save: save,
        getData: getData,
        getSection: getSection,
        updatePersonalInfo: updatePersonalInfo,
        updateProfileSummary: updateProfileSummary,
        addEntry: addEntry,
        updateEntry: updateEntry,
        removeEntry: removeEntry,
        reorderEntry: reorderEntry,
        reset: reset,
        getMeta: getMeta,
        hasData: hasData,
        generateId: generateId,



    // Entry factories
        getEmptyEducation: getEmptyEducation,
        getEmptyExperience: getEmptyExperience,
        getEmptySkill: getEmptySkill,
        getEmptyLanguage: getEmptyLanguage,
        getEmptyCertification: getEmptyCertification,
        getEmptyProject: getEmptyProject,
        getEmptyCustomSection: getEmptyCustomSection
    };
})();
