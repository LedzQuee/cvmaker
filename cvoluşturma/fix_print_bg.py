with open('wwwroot/css/cv-templates.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Add print color adjust globally to cv-templates
insert_css = '''
/* Ensure backgrounds are printed for all templates */
.cv-tpl {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}

'''
text = insert_css + text

# Ensure sidebar left has !important on background just in case html2canvas needs it
text = text.replace('background-color: #2b3a4a;', 'background-color: #2b3a4a !important;')
text = text.replace('background: #fff;', 'background: #fff !important;')

with open('wwwroot/css/cv-templates.css', 'w', encoding='utf-8') as f:
    f.write(text)
