with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

global_rule = '''
/* Her şablon elemanı için universal box-sizing kuralı */
.cv-tpl, .cv-tpl * {
    box-sizing: border-box;
}
'''
# Add it at the top after the first few lines
text = text.replace('/* ==========================================\n   1. NORDIC (Sade & Modern)\n   ========================================== */', 
                    global_rule + '\n/* ==========================================\n   1. NORDIC (Sade & Modern)\n   ========================================== */')

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text)
