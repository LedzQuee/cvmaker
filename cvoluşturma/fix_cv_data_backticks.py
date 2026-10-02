with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'description: \'- Mikroservis mimarisine([\s\S]*?)liderlik ettim\.\'', r'description: - Mikroservis mimarisine\1liderlik ettim.', text)
text = re.sub(r'description: \'- B2B e-ticaret platformunun([\s\S]*?)tasarladım\.\'', r'description: - B2B e-ticaret platformunun\1tasarladım.', text)

# Just to be super safe, replace ALL newlines inside those backticks with actual \\n or just leave them as backticks. 
# Backticks are valid ES6.

with open('wwwroot/js/cv-data.js', 'w', encoding='utf-8') as f:
    f.write(text)
