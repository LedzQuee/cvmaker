import re
with open('Views/Shared/_Layout.cshtml', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the left-aligned ul
text = re.sub(r'<ul class="navbar-nav me-auto ps-3">[\s\S]*?</ul>\s*<ul class="navbar-nav ms-auto">', '<ul class="navbar-nav ms-auto">', text)

# Add the link to the right-aligned ul
nav_item = '''<li class="nav-item">
                            <a class="nav-link" asp-controller="Home" asp-action="Samples" style="font-weight:600; color:#2563eb;">
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="margin-right:4px; margin-bottom:2px;">
                                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                    <polyline points="14 2 14 8 20 8"></polyline>
                                    <line x1="16" y1="13" x2="8" y2="13"></line>
                                    <line x1="16" y1="17" x2="8" y2="17"></line>
                                    <polyline points="10 9 9 9 8 9"></polyline>
                                </svg>
                                Örnek CV'ler
                            </a>
                        </li>'''

text = text.replace('<li class="nav-item">\n                              <a class="nav-link" asp-controller="Home" asp-action="Builder">CV Oluştur</a>', 
                    nav_item + '\n                          <li class="nav-item">\n                              <a class="nav-link" asp-controller="Home" asp-action="Builder">CV Oluştur</a>')

with open('Views/Shared/_Layout.cshtml', 'w', encoding='utf-8') as f:
    f.write(text)
