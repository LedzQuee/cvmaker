with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

balance = 0
last_open = []
for i, line in enumerate(text.split('\n')):
    in_str = False
    str_c = ''
    prev_c = ''
    for j, char in enumerate(line):
        if char in ('"', "'"):
            if not in_str:
                in_str = True
                str_c = char
            elif char == str_c and prev_c != '\\':
                in_str = False
        
        if not in_str:
            if char == '(':
                balance += 1
                last_open.append(i+1)
            elif char == ')':
                balance -= 1
                if last_open: last_open.pop()
        
        prev_c = char

if balance > 0:
    print(f'Unclosed parens at lines: {last_open}')
