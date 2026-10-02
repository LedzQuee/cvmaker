with open("wwwroot/js/cv-templates.js", "r", encoding="utf-8") as f:
    text = f.read()

old = """    function contactLine(pi) {
        var parts = [];
        if (pi.email) parts.push(esc(pi.email));
        if (pi.phone) parts.push(esc(pi.phone));
        if (pi.address) parts.push(esc(pi.address));
        return parts.join(' \x07 ');
    }"""

new = """    function contactLine(pi) {
        var parts = [];
        if (pi.email) parts.push(esc(pi.email));
        if (pi.phone) parts.push(esc(pi.phone));
        if (pi.address) parts.push(esc(pi.address));
        if (pi.driversLicense) parts.push('Ehliyet: ' + esc(pi.driversLicense));
        return parts.join(' \x07 ');
    }"""

if old in text:
    text = text.replace(old, new)
    print("OK: driversLicense added to contactLine")
else:
    # Try to find it with regex
    import re
    m = re.search(r'function contactLine\(pi\) \{[\s\S]*?\}', text)
    if m:
        old_found = m.group(0)
        new_func = old_found.rstrip('}') + "    if (pi.driversLicense) parts.push('Ehliyet: ' + esc(pi.driversLicense));\n        " + "return parts.join(' \\x07 ');\n    }"
        # Better: inject before the return line
        new_func2 = re.sub(
            r"(return parts\.join\(.*?\);)",
            "if (pi.driversLicense) parts.push('Ehliyet: ' + esc(pi.driversLicense));\n        \\1",
            old_found
        )
        text = text.replace(old_found, new_func2, 1)
        print("OK: injected via regex")
    else:
        print("FAIL: contactLine not found")

with open("wwwroot/js/cv-templates.js", "w", encoding="utf-8") as f:
    f.write(text)
