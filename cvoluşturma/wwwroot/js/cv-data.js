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
                firstName: 'Kullanıcı',
                lastName: 'Adı',
                email: 'kullanici@ornek.com',
                phone: '+90 555 000 00 00',
                address: 'İzmir, Türkiye',
                linkedin: 'https://linkedin.com/in/kullanici-adi',
                website: 'https://github.com/ornek-profil',
                driversLicense: '',
                photoUrl: ''
            },
            profileSummary: 'Modern web teknolojileri ve 3D haritalama üzerine projeler geliştiren, ASP.NET Core, JavaScript ve Python gibi teknolojilere hakim tam yığın (full-stack) yazılım geliştiricisi.',
            education: [
                { id: 'edu1', school: 'Dokuz Eylül Üniversitesi', degree: 'Lisans', field: 'Bilgisayar / Yazılım', startDate: '', endDate: '', description: 'Web geliştirme, modern yazılım mimarileri ve 3D haritalama sistemleri üzerine çalışmalar.' }
            ],
            experience: [
                { id: 'exp1', company: 'Bağımsız Geliştirici', position: 'Full-Stack Developer', startDate: '2022', endDate: '', current: true, description: '- ASP.NET Core ve MVC yapısı kullanılarak veritabanı destekli uygulamalar geliştirildi.\n- Modern frontend (JS, TS, Vite) ve 3D web haritalama (MapLibre vb.) sistemleri üzerine çalışıldı.' }
            ],
            skills: [
                { id: 'sk1', name: 'C# / .NET Core', level: 'İleri' },
                { id: 'sk2', name: 'JavaScript / TypeScript', level: 'İleri' },
                { id: 'sk3', name: 'HTML5 / CSS3 / Bootstrap', level: 'İleri' },
                { id: 'sk4', name: 'Python', level: 'Orta' },
                { id: 'sk5', name: 'Git / GitHub', level: 'İleri' },
                { id: 'sk6', name: 'SQLite', level: 'Orta' }
            ],
            languages: [
                { id: 'lang1', name: 'İngilizce', level: 'B1' },
                { id: 'lang2', name: 'Türkçe', level: 'Anadil' }
            ],
            certifications: [],
            projects: [
                { id: 'proj1', name: 'CV Maker Platformu', role: 'Geliştirici', date: '2026', description: 'ASP.NET Core tabanlı, kullanıcıların dinamik olarak CV oluşturup yönetebildiği platform.' },
                { id: 'proj2', name: 'İzmir 3D Kent Atlası', role: 'Geliştirici', date: '2026', description: 'Vite, JS/TS ve harita kütüphaneleri kullanılarak geliştirilmiş, interaktif 3D kent modeli gösterim aracı.' },
                { id: 'proj3', name: 'Sinema Bilet Satış Sitesi', role: 'Geliştirici', date: 'Geçmiş', description: 'Kullanıcıların seans seçip koltuk rezervasyonu yapabildiği, bilet satın alma senaryolarını barındıran web tabanlı sistem.' }
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
