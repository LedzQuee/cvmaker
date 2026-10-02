import sys

def check(text):
    balance = 0
    lines = text.split('\n')
    for i, line in enumerate(lines):
        in_string = False
        str_char = ''
        for j, char in enumerate(line):
            if char in ('\'', '"') and (j == 0 or line[j-1] != '\\'):
                if not in_string:
                    in_string = True
                    str_char = char
                elif str_char == char:
                    in_string = False
            
            if not in_string:
                if char == '{':
                    balance += 1
                elif char == '}':
                    balance -= 1
                    if balance < 0:
                        print(f'Balance went negative at line {i+1}:\n{line}')
                        return
    if balance == 0:
        print('Braces match perfectly!')
    else:
        print(f'Final balance is {balance}')

with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    check(f.read())
