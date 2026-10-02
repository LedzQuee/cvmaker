# -*- coding: utf-8 -*-
with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_photo = """document.addEventListener('DOMContentLoaded', function() {
    var photoInput = document.getElementById('profilePhoto');
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(event) {
                    var data = CVDataManager.getData();
                    data.personalInfo.photo = event.target.result;
                    CVDataManager.save();
                    if (typeof CVBuilder !== 'undefined') { CVBuilder.updatePreview(); }
                };
                reader.readAsDataURL(file);
            }
        });
    }
});"""

new_photo = """document.addEventListener('DOMContentLoaded', function() {
    var photoInput = document.getElementById('profilePhoto');
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (!file) return;
            // Validate file type
            if (!file.type.startsWith('image/')) {
                alert('Lütfen geçerli bir görsel dosyası seçin (JPG, PNG, vb.)');
                return;
            }
            // Show preview thumbnail immediately
            var previewImg = document.getElementById('photoPreview');
            var reader = new FileReader();
            reader.onload = function(event) {
                var dataUrl = event.target.result;
                // Show thumbnail in form
                if (!previewImg) {
                    previewImg = document.createElement('img');
                    previewImg.id = 'photoPreview';
                    previewImg.style.cssText = 'width:80px;height:80px;border-radius:50%;object-fit:cover;margin-top:10px;border:2px solid #e2e8f0;display:block;';
                    photoInput.parentNode.appendChild(previewImg);
                }
                previewImg.src = dataUrl;
                // Save to data model
                var data = CVDataManager.getData();
                data.personalInfo.photo = dataUrl;
                CVDataManager.save();
                // Force preview update
                if (typeof CVBuilder !== 'undefined') {
                    CVBuilder.updatePreview();
                }
            };
            reader.onerror = function() {
                alert('Fotoğraf yüklenirken hata oluştu. Lütfen tekrar deneyin.');
            };
            reader.readAsDataURL(file);
        });
    }
    // Restore saved photo thumbnail on load
    try {
        var savedData = CVDataManager.getData();
        if (savedData && savedData.personalInfo && savedData.personalInfo.photo && photoInput) {
            var previewImg = document.createElement('img');
            previewImg.id = 'photoPreview';
            previewImg.style.cssText = 'width:80px;height:80px;border-radius:50%;object-fit:cover;margin-top:10px;border:2px solid #e2e8f0;display:block;';
            previewImg.src = savedData.personalInfo.photo;
            photoInput.parentNode.appendChild(previewImg);
        }
    } catch(e) {}
});"""

if old_photo in content:
    content = content.replace(old_photo, new_photo)
    print('Photo upload code replaced')
else:
    print('WARNING: exact match not found, trying simpler inject')
    content = content.replace(
        "reader.readAsDataURL(file);\n            }\n        });\n    }\n});",
        "reader.readAsDataURL(file);\n            }\n        });\n    }\n    // Restore saved photo thumbnail on load\n    try {\n        var savedData = CVDataManager.getData();\n        if (savedData && savedData.personalInfo && savedData.personalInfo.photo && document.getElementById('profilePhoto')) {\n            var pImg = document.createElement('img');\n            pImg.id = 'photoPreview';\n            pImg.style.cssText = 'width:80px;height:80px;border-radius:50%;object-fit:cover;margin-top:10px;border:2px solid #e2e8f0;display:block;';\n            pImg.src = savedData.personalInfo.photo;\n            document.getElementById('profilePhoto').parentNode.appendChild(pImg);\n        }\n    } catch(e) {}\n});"
    )
    print('Simple inject done')

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(content)
