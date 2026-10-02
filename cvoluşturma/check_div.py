with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

div_open = text.count('<div')
div_close = text.count('</div')
print(f'Divs open: {div_open}, Divs close: {div_close}')
