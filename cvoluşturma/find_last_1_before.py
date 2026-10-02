with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

balance = 0
last_1 = 0
for i, line in enumerate(text.split('\n')):
    if i+1 > 1045: break
    in_str = False
    str_c = ''
    prev_c = ''
    for char in line:
        if char in ('"', "'") and not in_str:
            in_str = True
            str_c = char
        elif char == str_c and in_str and prev_c != '\\':
            in_str = False
            
        if not in_str:
            if char == '(': balance += 1
            elif char == ')': balance -= 1
        prev_c = char
    if balance == 1:
        last_1 = i + 1

print(f"Before line 1046, the last line where balance was 1 is: {last_1}")
