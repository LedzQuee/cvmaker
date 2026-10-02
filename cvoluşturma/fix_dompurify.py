import re

with open("wwwroot/js/cv-templates.js", "r", encoding="utf-8") as f:
    text = f.read()

# Find descToHtml and add DOMPurify to sanitize Quill HTML before processing
old_desc = '        function descToHtml(text) {\n        if (!text) return \'\';\n        // Strip any HTML tags (leftover from Quill editor)'

new_desc = '        function descToHtml(text) {\n        if (!text) return \'\';\n        // Guvenlik: Once DOMPurify ile temizle (XSS korumasi)\n        if (typeof DOMPurify !== "undefined") {\n            text = DOMPurify.sanitize(text, { ALLOWED_TAGS: ["br", "p", "ul", "li", "b", "strong", "em", "div"], ALLOWED_ATTR: [] });\n        }\n        // Strip any HTML tags (leftover from Quill editor)'

if old_desc in text:
    text = text.replace(old_desc, new_desc)
    print("OK: DOMPurify added to descToHtml")
else:
    print("WARN: descToHtml start not matched exactly, trying regex...")
    pattern = r"(function descToHtml\(text\) \{\s*if \(!text\) return '';\s*)"
    def replacer(m):
        return m.group(0) + '        // Guvenlik: Once DOMPurify ile temizle\n        if (typeof DOMPurify !== "undefined") {\n            text = DOMPurify.sanitize(text, { ALLOWED_TAGS: ["br","p","ul","li","b","strong","em","div"], ALLOWED_ATTR: [] });\n        }\n'
    new_text = re.sub(pattern, replacer, text, count=1)
    if new_text != text:
        text = new_text
        print("OK: DOMPurify added via regex")
    else:
        print("FAIL: Could not patch descToHtml")

with open("wwwroot/js/cv-templates.js", "w", encoding="utf-8") as f:
    f.write(text)
