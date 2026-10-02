with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the broken nested brackets
text = text.replace('updatePreview();\n                });\n            });\n        });', 'updatePreview();\n            });\n        });')
text = text.replace('updatePreview();\n                });\n            });\n        }', 'updatePreview();\n            });\n        }')
text = text.replace('updatePreview();\n                });\n            });\n    }', 'updatePreview();\n            });\n    }')
text = text.replace('updatePreview();\n                });\n            });', 'updatePreview();\n            });')

# But we need the correct one for bindEntryEvents to actually have the extra closure because we used forEach
# Let's just find bindEntryEvents and rewrite it cleanly.

