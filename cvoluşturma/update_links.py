with open('Views/Home/Samples.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<a asp-controller="Home" asp-action="Builder" class="btn-use-template">Bu Şablonla Oluştur</a>', 'MOCK')

# 1st is Sidebar
text = text.replace('MOCK', '<a href="/Home/Builder?template=sidebar" class="btn-use-template">Bu Şablonla Oluştur</a>', 1)
# 2nd is Classic
text = text.replace('MOCK', '<a href="/Home/Builder?template=classic" class="btn-use-template">Bu Şablonla Oluştur</a>', 1)
# 3rd is Bento
text = text.replace('MOCK', '<a href="/Home/Builder?template=bento" class="btn-use-template">Bu Şablonla Oluştur</a>', 1)

with open('Views/Home/Samples.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
