with open("wwwroot/js/cv-templates.js", "r", encoding="utf-8") as f:
    text = f.read()

import re
# Find and replace renderPhoto function
pattern = r"function renderPhoto\(pi\) \{[\s\S]*?return '';\n    \}"
replacement = """function renderPhoto(pi) {
        if (pi.photo) {
            // XSS Koruma: Sadece guvenli URL formatlarini kabul et
            var photo = pi.photo;
            var isDataUrl = typeof photo === "string" && photo.indexOf("data:image/") === 0 && photo.indexOf(";base64,") > 0;
            var isHttpUrl = typeof photo === "string" && (photo.indexOf("http://") === 0 || photo.indexOf("https://") === 0);
            if (!isDataUrl && !isHttpUrl) return "";
            return "<div class=\\"tpl-photo\\" style=\\"flex-shrink:0;\\"><img src=\\"" + photo + "\\" alt=\\"Profil\\" style=\\"width:120px;height:120px;border-radius:50%;object-fit:cover;border:3px solid #eee;\\"/></div>";
        }
        return "";
    }"""

new_text = re.sub(pattern, replacement, text)
if new_text != text:
    print("OK: renderPhoto patched")
else:
    print("WARN: pattern not matched, checking...")
    idx = text.find("function renderPhoto")
    print(repr(text[idx:idx+300]) if idx >= 0 else "Not found")

with open("wwwroot/js/cv-templates.js", "w", encoding="utf-8") as f:
    f.write(new_text)
