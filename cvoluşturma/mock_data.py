with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

mock_data = '''function getDefaultData() {
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
                { id: 'exp1', company: 'TechNova Yazılım', position: 'Kıdemli Yazılım Geliştirici', startDate: '2021', endDate: '', current: true, description: '- Mikroservis mimarisine geçiş sürecini yönettim.\\n- Sistemin tepki süresini %40 oranında iyileştirdim.\\n- 5 kişilik frontend ekibine liderlik ettim.' },
                { id: 'exp2', company: 'Global Çözümler A.Ş.', position: 'Yazılım Geliştirici', startDate: '2019', endDate: '2021', current: false, description: '- B2B e-ticaret platformunun arayüz bileşenlerini React ile geliştirdim.\\n- RESTful API mimarisi tasarladım.' }
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
    }'''

import re
text = re.sub(r'function getDefaultData\(\)\s*\{[\s\S]*?\}\s*\}', mock_data, text, count=1)

# Also force clear local storage on load (temporary hack)
text = text.replace('function load() {', "function load() { localStorage.removeItem('nova_cv_data'); // TEMP MOCK HACK")

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
