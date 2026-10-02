with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

balance = 0
for i, line in enumerate(text.split('\n')):
    for char in line:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
        elif char == '(': balance += 0
        elif char == ')': balance -= 0
        
        if balance < 0:
            print(f'Negative brace balance at line {i+1}: {line}')
            break
if balance != 0: print(f'Data final brace balance: {balance}')
else: print('Braces balanced')
