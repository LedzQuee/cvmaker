import re

for fname in ["Views/Account/Login.cshtml", "Views/Account/Register.cshtml"]:
    with open(fname, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Remove all emoji unicode characters
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U0001F900-\U0001F9FF"
        u"\u2600-\u26FF"
        u"\u2700-\u27BF"
        "]+", flags=re.UNICODE)
    
    cleaned = emoji_pattern.sub("", text)
    
    with open(fname, "w", encoding="utf-8") as f:
        f.write(cleaned)
    
    print(f"OK: {fname} cleaned")
