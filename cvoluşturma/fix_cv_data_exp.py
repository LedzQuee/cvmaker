with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Replace the entire experience array
new_experience = '''experience: [
                { id: 'exp1', company: 'TechNova Yazılım', position: 'Kıdemli Yazılım Geliştirici', startDate: '2021', endDate: '', current: true, description: '- Mikroservis mimarisine geçiş sürecini yönettim.\\n- Sistemin tepki süresini %40 oranında iyileştirdim.\\n- 5 kişilik frontend ekibine liderlik ettim.' },
                { id: 'exp2', company: 'Global Çözümler A.Ş.', position: 'Yazılım Geliştirici', startDate: '2019', endDate: '2021', current: false, description: '- B2B e-ticaret platformunun arayüz bileşenlerini React ile geliştirdim.\\n- RESTful API mimarisi tasarladım.' }
            ],'''

text = re.sub(r'experience: \[[\s\S]*?\],', new_experience, text, count=1)

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
