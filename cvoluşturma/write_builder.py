# -*- coding: utf-8 -*-
content = '''
            <!-- ADIM 0 -->
            <div class="step-content active" data-step="0">
                <div class="step-header"><h2>Kişisel Bilgiler</h2><p>İletişim bilgilerinizi girin.</p></div>
                <div class="form-card">
                    <div class="row g-3">
                        <div class="col-12">
                            <label for="profilePhoto" class="form-label">Profil Fotoğrafı</label>
                            <input type="file" class="form-control" id="profilePhoto" accept="image/png, image/jpeg" />
                        </div>
                        <div class="col-md-6">
                            <label for="firstName" class="form-label">Ad <span style="color: var(--color-danger);">*</span></label>
                            <input type="text" class="form-control" id="firstName" data-field="firstName" placeholder="Adınız" required />
                        </div>
                        <div class="col-md-6">
                            <label for="lastName" class="form-label">Soyad <span style="color: var(--color-danger);">*</span></label>
                            <input type="text" class="form-control" id="lastName" data-field="lastName" placeholder="Soyadınız" required />
                        </div>
                        <div class="col-md-6">
                            <label for="email" class="form-label">E-posta <span style="color: var(--color-danger);">*</span></label>
                            <input type="email" class="form-control" id="email" data-field="email" placeholder="ornek@email.com" required />
                        </div>
                        <div class="col-md-6">
                            <label for="phone" class="form-label">Telefon</label>
                            <input type="tel" class="form-control" id="phone" data-field="phone" placeholder="+90 5XX XXX XX XX" />
                        </div>
                        <div class="col-12">
                            <label for="address" class="form-label">Adres</label>
                            <input type="text" class="form-control" id="address" data-field="address" placeholder="Şehir, Ülke" />
                        </div>
                        <div class="col-md-6">
                            <label for="linkedin" class="form-label">LinkedIn</label>
                            <input type="url" class="form-control" id="linkedin" data-field="linkedin" placeholder="linkedin.com/in/kullaniciadi" />
                        </div>
                        <div class="col-md-6">
                            <label for="website" class="form-label">Web Sitesi</label>
                            <input type="url" class="form-control" id="website" data-field="website" placeholder="www.siteniz.com" />
                        </div>
                    </div>
                </div>
            </div>
            <!-- ADIM 1 -->
            <div class="step-content" data-step="1">
                <div class="step-header"><h2>Profil Özeti</h2><p>Kendinizi kısaca tanıtın. 2-3 cümlelik profesyonel özet yazın.</p></div>
                <div class="form-card">
                    <label for="profileSummary" class="form-label">Profil Özeti</label>
                    <textarea class="form-control" id="profileSummary" rows="5" placeholder="Deneyimli yazılım geliştirici, 5 yıllık sektör tecrübesi ile..."></textarea>
                    <div class="form-text mt-2">Kısa ve etkileyici bir özet yazın. İşverenler genellikle ilk olarak bu bölümü okur.</div>
                </div>
            </div>
            <!-- ADIM 2 -->
            <div class="step-content" data-step="2">
                <div class="step-header"><h2>Eğitim</h2><p>Eğitim geçmişinizi en güncel olandan başlayarak ekleyin.</p></div>
                <div id="educationEntries"></div>
                <button type="button" class="btn-add-entry" data-section="education">+ Eğitim Ekle</button>
            </div>
            <!-- ADIM 3 -->
            <div class="step-content" data-step="3">
                <div class="step-header"><h2>İş Deneyimi</h2><p>İş deneyimlerinizi en güncel olandan başlayarak ekleyin.</p></div>
                <div id="experienceEntries"></div>
                <button type="button" class="btn-add-entry" data-section="experience">+ Deneyim Ekle</button>
            </div>
            <!-- ADIM 4 -->
            <div class="step-content" data-step="4">
                <div class="step-header"><h2>Yetenekler</h2><p>Teknik ve kişisel yeteneklerinizi ekleyin.</p></div>
                <div id="skillEntries"></div>
                <button type="button" class="btn-add-entry" data-section="skills">+ Yetenek Ekle</button>
            </div>
            <!-- ADIM 5 -->
            <div class="step-content" data-step="5">
                <div class="step-header"><h2>Diller</h2><p>Bildiğiniz dilleri ve seviyelerini ekleyin.</p></div>
                <div id="languageEntries"></div>
                <button type="button" class="btn-add-entry" data-section="languages">+ Dil Ekle</button>
            </div>
            <!-- ADIM 6 -->
            <div class="step-content" data-step="6">
                <div class="step-header"><h2>Sertifikalar</h2><p>Sahip olduğunuz sertifika ve belgeleri ekleyin.</p></div>
                <div id="certificationEntries"></div>
                <button type="button" class="btn-add-entry" data-section="certifications">+ Sertifika Ekle</button>
            </div>
            <!-- ADIM 7 -->
            <div class="step-content" data-step="7">
                <div class="step-header"><h2>Projeler</h2><p>Öne çıkan projelerinizi ekleyin.</p></div>
                <div id="projectEntries"></div>
                <button type="button" class="btn-add-entry" data-section="projects">+ Proje Ekle</button>
            </div>
            <!-- ADIM 8: Ekstra -->
            <div class="step-content" data-step="8">
                <div class="step-header"><h2>Ekstra Bölümler</h2><p>CV\\\'nize özel, serbest başlıklı bölümler ekleyin. (Gönüllülük, Hobiler, Referanslar vb.)</p></div>
                <div id="customSectionEntries"></div>
                <button type="button" class="btn-add-entry" data-section="customSections">+ Özel Bölüm Ekle</button>
            </div>
            <!-- Navigation -->
            <div class="builder-nav">
                <button type="button" class="btn btn-secondary" id="btnPrev" disabled>&larr; Geri</button>
                <span class="step-indicator" id="stepIndicator">1 / 9</span>
                <button type="button" class="btn btn-primary" id="btnNext">İleri &rarr;</button>
            </div>
        </div>

        <!-- SAG PANEL -->
        <div class="builder-preview-panel" id="previewPanel">
            <div class="preview-header" style="display:flex; justify-content:space-between; align-items:center; padding:10px 20px; background:#fff; border-bottom:1px solid #EAEAEA;">
                <div style="display:flex; align-items:center; gap: 10px;">
                    <span style="font-size:14px; font-weight:600; color:#333;">Şablon:</span>
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
                    </select>
                </div>
                <button type="button" class="btn btn-primary btn-sm" id="btnDownloadPdf" style="display: flex; align-items: center; gap: 6px;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    PDF / Yazdır
                </button>
            </div>
            <div class="preview-container" id="cvPreview">
                <div class="preview-placeholder" id="previewPlaceholder">
                    <div class="preview-placeholder-icon">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round">
                            <rect x="3" y="2" width="18" height="20" rx="2"/>
                            <line x1="7" y1="7" x2="17" y2="7"/>
                            <line x1="7" y1="11" x2="17" y2="11"/>
                            <line x1="7" y1="15" x2="13" y2="15"/>
                        </svg>
                    </div>
                    <p><strong>CV önizlemeniz burada görünecek</strong></p>
                    <p>Sol taraftaki formu doldurmaya başlayın.</p>
                </div>
                <div id="previewContent" style="display: none;"></div>
            </div>
        </div>
    </div>

    <button type="button" class="mobile-panel-toggle btn btn-primary" id="mobileToggle">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
        </svg>
        <span id="mobileToggleLabel">Önizleme</span>
    </button>

    <!-- PDF Export Modal -->
    <div class="modal fade" id="pdfExportModal" tabindex="-1" aria-labelledby="pdfModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content" style="border-radius:16px; border:none; overflow:hidden;">
                <div class="modal-header" style="background:linear-gradient(135deg,#1e3a8a,#3b82f6); color:#fff; border:none;">
                    <h5 class="modal-title" id="pdfModalLabel">CV\\\'nizi Kaydedin</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Kapat"></button>
                </div>
                <div class="modal-body p-4">
                    <p class="text-muted mb-4">CV\\\'nizi nasıl kaydetmek istersiniz?</p>
                    <div class="d-grid gap-3">
                        <button type="button" class="btn btn-primary py-3" id="btnModalDownload" style="border-radius:12px; font-weight:600;">
                            &#128229; PDF Olarak İndir
                        </button>
                        <button type="button" class="btn btn-outline-secondary py-3" id="btnModalPrint" style="border-radius:12px; font-weight:600;" data-bs-dismiss="modal">
                            &#128438; Yazdır
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

@section Scripts {
    <script>
    window.onerror = function(msg, url, line, col, error) {
        console.error(\'JS HATA: \' + msg + \' (Satır: \' + line + \')\');
    };
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <script src="https://cdn.quilljs.com/1.3.6/quill.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js"></script>
    <script src="~/js/cv-data.js" asp-append-version="true"></script>
    <script src="~/js/cv-templates.js" asp-append-version="true"></script>
    <script src="~/js/cv-builder.js" asp-append-version="true"></script>
}
'''

with open('Views/Home/Builder.cshtml', 'a', encoding='utf-8') as f:
    f.write(content)
print('Builder.cshtml complete')
