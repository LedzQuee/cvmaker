with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove one extra </div> from the end before @section
text = text.replace('    </div>\n    </div>\n</div>\n\n@section Scripts', '    </div>\n</div>\n\n@section Scripts')

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
