with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Just use string replace instead of re.sub for literal replacement!
old_str = '''experience: [
                { id: 'exp1', company: 'TechNova Yazılım', position: 'Kıdemli Yazılım Geliştirici', startDate: '2021', endDate: '', current: true, description: '- Mikroservis mimarisine geçiş sürecini yönettim.\n- Sistemin tepki süresini %40 oranında iyileştirdim.\n- 5 kişilik frontend ekibine liderlik ettim.' },
                { id: 'exp2', company: 'Global Çözümler A.Ş.', position: 'Yazılım Geliştirici', startDate: '2019', endDate: '2021', current: false, description: '- B2B e-ticaret platformunun arayüz bileşenlerini React ile geliştirdim.\n- RESTful API mimarisi tasarladım.' }
            ],'''

new_str = '''experience: [
                { id: 'exp1', company: 'TechNova Yazılım', position: 'Kıdemli Yazılım Geliştirici', startDate: '2021', endDate: '', current: true, description: '- Mikroservis mimarisine geçiş sürecini yönettim.\\n- Sistemin tepki süresini %40 oranında iyileştirdim.\\n- 5 kişilik frontend ekibine liderlik ettim.' },
                { id: 'exp2', company: 'Global Çözümler A.Ş.', position: 'Yazılım Geliştirici', startDate: '2019', endDate: '2021', current: false, description: '- B2B e-ticaret platformunun arayüz bileşenlerini React ile geliştirdim.\\n- RESTful API mimarisi tasarladım.' }
            ],'''

text = text.replace(old_str, new_str)
# Also fix any remaining literal newlines inside description
text = text.replace('yönettim.\n-', 'yönettim.\\n-')
text = text.replace('iyileştirdim.\n-', 'iyileştirdim.\\n-')
text = text.replace('geliştirdim.\n-', 'geliştirdim.\\n-')

text = text.replace('yönettim.\r\n-', 'yönettim.\\n-')
text = text.replace('iyileştirdim.\r\n-', 'iyileştirdim.\\n-')
text = text.replace('geliştirdim.\r\n-', 'geliştirdim.\\n-')

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
