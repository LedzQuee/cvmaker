with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()
import re
match = re.search(r'<span[^>]*>.*?</span>\s*<select id="templateSelector".*?</select>', text, re.DOTALL)
if match:
    # Print the raw bytes to see if it's utf-8
    print(match.group(0).encode('utf-8'))
