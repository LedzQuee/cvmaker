# -*- coding: utf-8 -*-
import re
import os

file_path = os.path.join('cvoluşturma', 'wwwroot', 'js', 'cv-data.js')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_default_data = '''    function getDefaultData() {
        return {
            personalInfo: {
                firstName: 'Burak',
                lastName: 'Koçak',
                email: 'burak.kocak@email.com',
                phone: '+90 555 000 00 00',
                address: 'İzmir, Türkiye',
                linkedin: 'linkedin.com/in/burakkocak',
                website: 'github.com/LedzQuee',
                driversLicense: '',
                photoUrl: ''
            },
            profileSummary: 'Modern web teknolojileri ve 3D haritalama üzerine projeler geliştiren, ASP.NET Core, JavaScript ve Python gibi teknolojilere hakim yetenekli yazılım geliştiricisi.',
            education: [
                { id: 'edu1', school: 'Dokuz Eylül Üniversitesi', degree: 'Lisans', field: 'Bilgisayar / Yazılım', startDate: '2020', endDate: 'Günümüz', description: 'Web geliştirme, modern yazılım mimarileri ve 3D haritalama sistemleri üzerine çalışmalar.' }
            ],
            experience: [
                { id: 'exp1', company: 'Bağımsız Geliştirici', position: 'Full-Stack Developer', startDate: '2022', endDate: '', current: true, description: '- ASP.NET Core ve MVC yapısı kullanılarak veritabanı destekli uygulamalar geliştirildi.\\n- Modern frontend (JS, TS, Vite) ve 3D web haritalama (MapLibre vb.) sistemleri üzerine çalışıldı.' }
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
                { id: 'lang1', name: 'İngilizce', level: 'İleri' },
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
    }'''

pattern = r'    function getDefaultData\(\)\s*\{[\s\S]*?\n    \}'
new_content = re.sub(pattern, new_default_data, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Done!')
