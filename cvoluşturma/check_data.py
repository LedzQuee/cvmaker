with open('wwwroot/js/cv-data.js', 'r', encoding='utf-8') as f:
    text = f.read()

balance = 0
for i, line in enumerate(text.split('\n')):
    for char in line:
        if char == '{': balance += 1
        elif char == '}': balance -= 1
        if balance < 0:
            print(f'Negative balance at line {i+1}: {line}')
            break
if balance != 0: print(f'Data final balance: {balance}')
else: print('Data balanced')
