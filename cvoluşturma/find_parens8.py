with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

balance = 0
for i, line in enumerate(text.split('\n')):
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
    if i+1 > 600 and balance == 1:
        # print(f'Line {i+1} reached 1')
        pass
    if i+1 > 600 and balance == 2:
        # We want to find the last time it was 1!
        pass
