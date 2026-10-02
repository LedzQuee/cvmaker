import re
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find element.style.backgroundColor = '#ffffff'; and inject the fix
match = re.search(r'element\.style\.backgroundColor\s*=\s*[\'"]#ffffff[\'"];', text)
if match:
    original = match.group(0)
    new_code = '''element.style.backgroundColor = '#ffffff';
            
            // html2canvas flexbox stretch bug fix for sidebar
            var sidebarLeft = element.querySelector('.sidebar-left');
            if (sidebarLeft) {
                sidebarLeft.style.minHeight = Math.max(element.offsetHeight, 1122) + 'px'; // 297mm is approx 1122px at 96dpi
            }
            // fix float-bg
            var floatBg = element.querySelector('.float-bg');
            if (floatBg) {
                floatBg.style.minHeight = Math.max(element.offsetHeight, 1122) + 'px';
            }'''
    text = text.replace(original, new_code)
    
    with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Success")
else:
    print("Failed to find backgroundColor setter")
