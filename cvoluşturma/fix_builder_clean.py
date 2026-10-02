import re

with open('Views/Home/Builder.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the broken template dropdown area completely
new_dropdown = '''<span style="font-size:14px; font-weight:600; color:#333;">Şablon:</span>
                    <select id="templateSelector" class="form-select form-select-sm" style="width: auto; min-width:160px; cursor:pointer;">
                        <option value="nordic">Nordic (Sade)</option>
                        <option value="bento">Bento Grid</option>
                        <option value="sidebar">Kenar Çubuklu</option>
                        <option value="classic">Klasik Türkçe</option>
                        <option value="editorial">Editorial</option>
                        <option value="timeline">Timeline</option>
                        <option value="monochrome">Monokrom</option>
                        <option value="architect">Architect</option>
                        <option value="studio">Studio</option>
                        <option value="floating">Floating</option>
                    </select>'''

# We will use regex to find the span and select block
text = re.sub(r'<span style="font-size:14px; font-weight:600; color:#333;">[^<]+</span>\s*<select id="templateSelector"[\s\S]*?</select>', new_dropdown, text)

# Also fix the Modal icons again in case they had emojis
new_modal_body = '''<div class="modal-body p-4">
                    <p class="text-muted mb-4">CV'nizi nasıl kaydetmek istersiniz?</p>
                    <div class="d-grid gap-3">
                        <button type="button" class="btn btn-primary py-3" id="btnModalDownload" style="border-radius:12px; font-weight:600;">
                            PDF Olarak İndir
                        </button>
                        <button type="button" class="btn btn-outline-secondary py-3" id="btnModalPrint" style="border-radius:12px; font-weight:600;" data-bs-dismiss="modal">
                            Yazdır
                        </button>
                    </div>
                </div>'''

text = re.sub(r'<div class="modal-body p-4">[\s\S]*?</div>\s*</div>\s*</div>\s*</div>', new_modal_body + '\n            </div>\n        </div>\n    </div>', text)

with open('Views/Home/Builder.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
