with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

balance = 0
for i, line in enumerate(text.split('\n')):
    for char in line:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
        
    if balance == 0 and i > 10:
        print(f'Braces reached 0 at line {i+1}: {line}')
