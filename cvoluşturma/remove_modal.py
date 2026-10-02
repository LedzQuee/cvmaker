with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Change top button text
text = text.replace('PDF / Yazdır', 'PDF İndir')

# Remove the modal
text = re.sub(r'<!-- PDF Export Modal -->[\s\S]*?</div>\s*</div>\s*</div>\s*</div>', '<!-- Print modal removed per user request -->', text)

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
