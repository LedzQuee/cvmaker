with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

# Replace all date label occurrences with optional hint
# There are multiple - use AllowMultiple approach
import re

# Pattern: label>Baslangic</label followed by renderDatePicker
text = re.sub(
    r"'<label class=\"form-label\">Ba[^\<]+</label>' \+\s*\n(\s+)renderDatePicker\('startDate'",
    "'<label class=\"form-label\">Tarih <span style=\"color:#94a3b8;font-weight:400;font-size:12px;\">(istege bagli)</span></label>' +\n\\1renderDatePicker('startDate'",
    text
)

text = re.sub(
    r"'<label class=\"form-label\">Biti[^\<]+</label>' \+\s*\n(\s+)renderDatePicker\('endDate'",
    "'<label class=\"form-label\">Bitis <span style=\"color:#94a3b8;font-weight:400;font-size:12px;\">(istege bagli)</span></label>' +\n\\1renderDatePicker('endDate'",
    text
)

with open("wwwroot/js/cv-builder.js", "w", encoding="utf-8") as f:
    f.write(text)

# Count replacements
count_start = text.count("Tarih <span")
count_end = text.count("Bitis <span")
print(f"OK: {count_start} Tarih, {count_end} Bitis labels updated")
