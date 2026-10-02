with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'pdfExportModal' in line or 'modal-body' in line or 'modal-content' in line or '</div' in line:
        pass
