with open('Controllers/HomeController.cs', 'r', encoding='utf-8') as f:
    text = f.read()

new_action = '''        public IActionResult Builder()
        {
            return View();
        }

        public IActionResult Samples()
        {
            return View();
        }'''

text = text.replace('        public IActionResult Builder()\n        {\n            return View();\n        }', new_action)

with open('Controllers/HomeController.cs', 'w', encoding='utf-8') as f:
    f.write(text)
