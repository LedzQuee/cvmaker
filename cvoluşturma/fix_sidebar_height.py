with open("wwwroot/css/cv-templates.css", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("min-height: 100%;", "min-height: 100vh;")

with open("wwwroot/css/cv-templates.css", "w", encoding="utf-8") as f:
    f.write(text)
print("OK: sidebar min-height set to 100vh")
