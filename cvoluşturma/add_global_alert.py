with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("console.error('JS HATA: ' + msg + ' (Satır: ' + line + ')');", 
                    "alert('Global JS Hatası: ' + msg + ' | Satır: ' + line); console.error('JS HATA: ' + msg);")

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
