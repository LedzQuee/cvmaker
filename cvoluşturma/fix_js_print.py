with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Fix executePdfExport injected CSS
text = text.replace(
    "pdfWin.document.write('.cv-tpl { width: 210mm !important; min-height: 297mm !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');",
    "pdfWin.document.write('.cv-tpl { width: 100% !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');"
)

# And fix executePrint injected CSS
text = text.replace(
    "printWindow.document.write('.cv-tpl { width: 210mm !important; min-height: 297mm !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');",
    "printWindow.document.write('.cv-tpl { width: 100% !important; margin: 0 !important; box-shadow: none !important; transform: none !important; box-sizing: border-box !important; }');"
)

# Replace hardcoded 210mm body with 100%
text = text.replace(
    "pdfWin.document.write('html, body { margin: 0; padding: 0; width: 210mm; background: #fff; }');",
    "pdfWin.document.write('html, body { margin: 0; padding: 0; width: 100%; background: #fff; }');"
)

text = text.replace(
    "printWindow.document.write('html, body { margin: 0; padding: 0; width: 210mm; background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }');",
    "printWindow.document.write('html, body { margin: 0; padding: 0; width: 100%; background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }');"
)

with open("wwwroot/js/cv-builder.js", "w", encoding="utf-8") as f:
    f.write(text)

print("OK: cv-builder.js fixed")
