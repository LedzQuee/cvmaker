with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the broken multiline strings by removing literal newlines and adding \\n 
import re
text = re.sub(r'description: \'- Mikroservis mimarisine ge.*?y.nettim.\n- Sistemin tepki s.*?resini %40 oran.nda iyile.*?tirdim.\n- 5 ki.*?ilik frontend ekibine liderlik ettim.\'', 
              r'description: "- Mikroservis mimarisine geçiş sürecini yönettim.\\n- Sistemin tepki süresini %40 oranında iyileştirdim.\\n- 5 kişilik frontend ekibine liderlik ettim."', text, flags=re.DOTALL)

text = re.sub(r'description: \'- B2B e-ticaret platformunun aray.*?z bile.*?enlerini React ile geli.*?tirdim.\n- RESTful API mimarisi tasarlad.m.\'',
              r'description: "- B2B e-ticaret platformunun arayüz bileşenlerini React ile geliştirdim.\\n- RESTful API mimarisi tasarladım."', text, flags=re.DOTALL)

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
