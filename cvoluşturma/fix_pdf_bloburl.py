with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("html2pdf().set(opt).from(element).save().then(function() {", "html2pdf().set(opt).from(element).output('bloburl').then(function(pdfUrl) { window.open(pdfUrl, '_blank');")

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(text)
