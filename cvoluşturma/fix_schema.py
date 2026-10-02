import re

with open("wwwroot/js/cv-data.js", "r", encoding="utf-8") as f:
    text = f.read()

# Find the load function and add schema validation after JSON.parse
validate_fn = """
    // Guvenlik: Gelen JSON verisinin beklenen yapida oldugunu dogrula
    function validateSchema(data) {
        if (!data || typeof data !== "object") return getDefaultData();
        var arrayFields = ["experience", "education", "skills", "languages", "certificates", "customSections"];
        arrayFields.forEach(function(field) {
            if (!Array.isArray(data[field])) {
                data[field] = [];
            }
        });
        if (!data.personalInfo || typeof data.personalInfo !== "object") {
            data.personalInfo = {};
        }
        if (typeof data.profileSummary !== "string") {
            data.profileSummary = "";
        }
        return data;
    }

"""

# Insert validateSchema before the load function
text = re.sub(
    r"(\s+function load\(\) \{)",
    validate_fn + r"\1",
    text,
    count=1
)

# Now patch the load function to call validateSchema after JSON.parse
text = text.replace(
    "_data = JSON.parse(stored);",
    "_data = validateSchema(JSON.parse(stored));"
)

if "validateSchema" in text:
    print("OK: validateSchema injected and wired up")
else:
    print("WARN: injection failed")

with open("wwwroot/js/cv-data.js", "w", encoding="utf-8") as f:
    f.write(text)
