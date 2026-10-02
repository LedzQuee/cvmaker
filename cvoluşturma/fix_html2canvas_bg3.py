import re
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find html2pdf().set(opt)
match = re.search(r'html2pdf\(\)\.set\(opt\)\.from\(element\)\.save\(\)', text)
if match:
    original = match.group(0)
    new_code = '''
            var sidebarLeft = element.querySelector('.sidebar-left');
            if (sidebarLeft) {
                sidebarLeft.style.minHeight = Math.max(element.offsetHeight, 1122) + 'px';
            }
            var floatBg = element.querySelector('.float-bg');
            if (floatBg) {
                floatBg.style.minHeight = Math.max(element.offsetHeight, 1122) + 'px';
            }
            
            html2pdf().set(opt).from(element).save()'''
    text = text.replace(original, new_code)
    
    with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Success")
else:
    print("Failed")
