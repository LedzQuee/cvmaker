with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

balance = 0
for i, line in enumerate(text.split('\n')):
    in_str = False
    str_c = ''
    for char in line:
        if char in ('"', "'") and not in_str:
            in_str = True
            str_c = char
        elif char == str_c and in_str:
            in_str = False
        
        if not in_str:
            if char == '(': balance += 1
            elif char == ')': balance -= 1
            
            if balance < 0:
                print(f'Negative parens balance at line {i+1}: {line}')
                break
if balance != 0: print(f'Data final parens balance: {balance}')
else: print('Parens balanced')
