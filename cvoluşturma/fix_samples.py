with open('Views/Home/Samples.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix header paragraph color
text = text.replace('opacity: 0.9;', 'opacity: 1; color: #f8fafc; font-weight: 500; text-shadow: 0 1px 3px rgba(0,0,0,0.3);')

# Rewrite mock-cv contents
mock1 = '''<div class="mock-cv" style="flex-direction: row; padding:0; overflow:hidden;">
                        <div style="width:35%; background:#1e293b; color:white; padding:15px; display:flex; flex-direction:column; gap:10px;">
                            <div class="mock-cv-photo" style="margin: 0 auto;"></div>
                            <div style="font-size:8px; text-align:center; font-weight:bold; margin-top:5px;">İletişim</div>
                            <div style="font-size:6px; color:#cbd5e1;">ahmet@yilmaz.com<br/>+90 555 123 4567<br/>İstanbul, TR</div>
                            <div style="font-size:8px; font-weight:bold; margin-top:10px;">Yetenekler</div>
                            <div style="font-size:6px; color:#cbd5e1;">C# .NET (İleri)<br/>JavaScript (İleri)<br/>React (Orta)</div>
                        </div>
                        <div style="width:65%; padding:15px; display:flex; flex-direction:column; gap:10px;">
                            <div style="font-size:14px; font-weight:bold; color:#0f172a; border-bottom:1px solid #e2e8f0; padding-bottom:5px;">Ahmet Yılmaz</div>
                            <div style="font-size:10px; font-weight:bold; color:#334155; margin-top:5px;">Deneyim</div>
                            <div>
                                <div style="font-size:8px; font-weight:bold;">Kıdemli Yazılım Geliştirici</div>
                                <div style="font-size:7px; color:#64748b;">TechCorp Inc. | 2021 - Günümüz</div>
                                <div style="font-size:6px; margin-top:3px; color:#334155;">- Mikroservis mimarisi tasarımı.<br/>- Performans optimizasyonları.</div>
                            </div>
                        </div>
                    </div>'''
text = text.replace('<div class="mock-cv" style="flex-direction: row; padding:0;">\n                        <div style="width:30%; background:#1e293b; padding:15px; display:flex; flex-direction:column; gap:10px;">\n                            <div class="mock-cv-photo" style="margin: 0 auto;"></div>\n                            <div class="mock-line short" style="background:#475569; margin: 0 auto;"></div>\n                            <div class="mock-line medium" style="background:#334155; margin-top:15px;"></div>\n                            <div class="mock-line medium" style="background:#334155;"></div>\n                        </div>\n                        <div style="width:70%; padding:15px; display:flex; flex-direction:column; gap:10px;">\n                            <div class="mock-line medium dark" style="height:12px;"></div>\n                            <div class="mock-line short dark"></div>\n                            <br/>\n                            <div class="mock-line long"></div>\n                            <div class="mock-line long"></div>\n                            <div class="mock-line medium"></div>\n                        </div>\n                    </div>', mock1)

mock2 = '''<div class="mock-cv">
                        <div class="mock-cv-header" style="justify-content:center; text-align:center; flex-direction:column; align-items:center;">
                            <div style="font-size:16px; font-weight:bold; font-family:serif;">Ayşe Demir</div>
                            <div style="font-size:9px; font-family:serif; color:#475569;">Avukat & Hukuk Danışmanı</div>
                            <div style="font-size:7px; font-family:serif; color:#64748b;">ayse.demir@hukuk.com | Ankara, TR | linkedin.com/in/ayse</div>
                        </div>
                        <div style="font-family:serif; margin-top:10px;">
                            <div style="font-size:10px; font-weight:bold; border-bottom:1px solid #000; padding-bottom:2px; margin-bottom:5px;">Eğitim</div>
                            <div style="font-size:8px; font-weight:bold;">Ankara Üniversitesi, Hukuk Fakültesi</div>
                            <div style="font-size:7px; color:#475569;">Lisans Derecesi | 2015 - 2019</div>
                        </div>
                        <div style="font-family:serif; margin-top:5px;">
                            <div style="font-size:10px; font-weight:bold; border-bottom:1px solid #000; padding-bottom:2px; margin-bottom:5px;">İş Deneyimi</div>
                            <div style="font-size:8px; font-weight:bold;">Avukat, ABC Hukuk Bürosu</div>
                            <div style="font-size:7px; color:#475569;">2020 - Devam Ediyor</div>
                            <div style="font-size:7px; margin-top:3px;">- Ticaret hukuku ve şirket birleşmeleri konusunda danışmanlık.</div>
                        </div>
                    </div>'''
text = text.replace('<div class="mock-cv">\n                        <div class="mock-cv-header" style="justify-content:center; text-align:center; flex-direction:column; align-items:center;">\n                            <div class="mock-cv-photo"></div>\n                            <div class="mock-line medium dark" style="height:10px;"></div>\n                            <div class="mock-line short"></div>\n                        </div>\n                        <div class="mock-line long mt-2"></div>\n                        <div class="mock-line long"></div>\n                        <div class="mock-line medium"></div>\n                        <div class="mock-line long mt-2"></div>\n                        <div class="mock-line long"></div>\n                    </div>', mock2)

mock3 = '''<div class="mock-cv" style="gap:10px; background:#f8fafc; border:1px solid #e2e8f0; padding:15px; border-radius:12px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div class="mock-cv-photo" style="width:40px; height:40px; background:#3b82f6;"></div>
                            <div style="text-align:right;">
                                <div style="font-size:14px; font-weight:900; color:#0f172a;">Can Özkan</div>
                                <div style="font-size:9px; font-weight:600; color:#3b82f6;">UX/UI Tasarımcı</div>
                            </div>
                        </div>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                            <div style="background:#fff; padding:10px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                                <div style="font-size:9px; font-weight:bold; color:#0f172a; margin-bottom:4px;">Hakkımda</div>
                                <div style="font-size:6px; color:#64748b; line-height:1.4;">Kullanıcı deneyimini merkeze alan, estetik ve işlevsel arayüzler tasarlayan yaratıcı profesyonel.</div>
                            </div>
                            <div style="background:#fff; padding:10px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                                <div style="font-size:9px; font-weight:bold; color:#0f172a; margin-bottom:4px;">Beceriler</div>
                                <div style="font-size:6px; color:#64748b; line-height:1.4;">Figma, Adobe XD<br/>Wireframing<br/>Prototyping</div>
                            </div>
                        </div>
                    </div>'''
text = text.replace('<div class="mock-cv" style="gap:5px;">\n                        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #3b82f6; padding-bottom:8px; margin-bottom:8px;">\n                            <div class="mock-cv-photo"></div>\n                            <div style="text-align:right;">\n                                <div class="mock-line medium dark" style="height:12px; margin-left:auto; margin-bottom:4px;"></div>\n                                <div class="mock-line short" style="margin-left:auto;"></div>\n                            </div>\n                        </div>\n                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">\n                            <div style="background:#f1f5f9; padding:8px; border-radius:6px;">\n                                <div class="mock-line medium dark mb-2"></div>\n                                <div class="mock-line long"></div>\n                                <div class="mock-line short"></div>\n                            </div>\n                            <div style="background:#f1f5f9; padding:8px; border-radius:6px;">\n                                <div class="mock-line medium dark mb-2"></div>\n                                <div class="mock-line long"></div>\n                                <div class="mock-line short"></div>\n                            </div>\n                        </div>\n                    </div>', mock3)

with open('Views/Home/Samples.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
