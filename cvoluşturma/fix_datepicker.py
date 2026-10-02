with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

old_end = """                updatePreview();
                });
            });
        });
    }

    // ==========================================
    // E"""

new_end = """                updatePreview();
                });
            });
        });

        // Tarih secici: ay ve yil degisince hidden input'u guncelle ve kaydet
        container.querySelectorAll('.date-picker-group').forEach(function(group) {
            var monthSel = group.querySelector('.month-select');
            var yearSel = group.querySelector('.year-select');
            var hiddenInput = group.querySelector('[data-entry-field]');
            if (!monthSel || !yearSel || !hiddenInput) return;

            function syncDateToHidden() {
                var m = monthSel.value;
                var y = yearSel.value;
                var combined = '';
                if (y && m) combined = y + '-' + m;
                else if (y) combined = y;
                hiddenInput.value = combined;
                // Veriyi modele kaydet
                var card = group.closest('.entry-card');
                if (card) {
                    var entryId = card.getAttribute('data-entry-id');
                    var field = hiddenInput.getAttribute('data-entry-field');
                    CVDataManager.updateEntry(sectionName, entryId, field, combined);
                    updatePreview();
                }
            }

            monthSel.addEventListener('change', syncDateToHidden);
            yearSel.addEventListener('change', syncDateToHidden);
        });
    }

    // ==========================================
    // E"""

if old_end in text:
    text = text.replace(old_end, new_end, 1)
    print("OK: date picker sync added")
else:
    print("FAIL: marker not found")

with open("wwwroot/js/cv-builder.js", "w", encoding="utf-8") as f:
    f.write(text)
