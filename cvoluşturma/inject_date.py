import re

with open('wwwroot/js/cv-builder.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add renderDatePicker function
datepicker_func = '''
    function renderDatePicker(field, value, disabled) {
        var parts = (value || '').split('-');
        var y = parts[0] || '';
        var m = parts[1] || '';
        
        var mOpts = '<option value="">Ay</option>';
        var months = ['01|Oca', '02|Şub', '03|Mar', '04|Nis', '05|May', '06|Haz', '07|Tem', '08|Ağu', '09|Eyl', '10|Eki', '11|Kas', '12|Ara'];
        months.forEach(function(mon) {
            var spl = mon.split('|');
            mOpts += '<option value="' + spl[0] + '"' + (m === spl[0] ? ' selected' : '') + '>' + spl[1] + '</option>';
        });
        
        var yOpts = '<option value="">Yıl</option>';
        var currY = new Date().getFullYear();
        for(var i = currY + 5; i >= currY - 50; i--) {
            var sy = i.toString();
            yOpts += '<option value="' + sy + '"' + (y === sy ? ' selected' : '') + '>' + sy + '</option>';
        }
        
        var dis = disabled ? ' disabled' : '';
        return '<div class="date-picker-group" style="display:flex; gap:5px;">' +
            '<select class="form-select month-select" data-for="' + field + '"' + dis + '>' + mOpts + '</select>' +
            '<select class="form-select year-select" data-for="' + field + '"' + dis + '>' + yOpts + '</select>' +
            '<input type="hidden" data-entry-field="' + field + '" value="' + esc(value) + '" />' +
        '</div>';
    }
'''

if 'function renderDatePicker' not in js:
    js = js.replace('function renderExperienceForm', datepicker_func + '\n    function renderExperienceForm')

# 2. Update forms to use renderDatePicker
# Replace '<input type="text" placeholder="Örn: 2023"  class="form-control" data-entry-field="startDate" value="' + esc(entry.startDate) + '" />'
js = re.sub(r"'<input type=.text. placeholder=.Örn: 2023.\s*class=.form-control. data-entry-field=.startDate. value=.' \+ esc\(entry\.startDate\) \+ '.\s*/>'", 
            "renderDatePicker('startDate', entry.startDate, false)", js)

js = re.sub(r"'<input type=.text. placeholder=.Örn: 2023.\s*class=.form-control. data-entry-field=.endDate. value=.' \+ esc\(entry\.endDate\) \+ '.' \+ \(entry\.current \? ' disabled' : ''\) \+ ' />'", 
            "renderDatePicker('endDate', entry.endDate, entry.current)", js)

js = re.sub(r"'<input type=.text. placeholder=.Örn: 2023.\s*class=.form-control. data-entry-field=.date. value=.' \+ esc\(entry\.date\) \+ '.\s*/>'", 
            "renderDatePicker('date', entry.date, false)", js)

# 3. Add to bindDynamicEntryEvents
event_code = '''
        container.querySelectorAll('.date-picker-group').forEach(function (group) {
            var mSel = group.querySelector('.month-select');
            var ySel = group.querySelector('.year-select');
            var hidden = group.querySelector('input[type="hidden"]');
            if(!mSel || !ySel || !hidden) return;
            function update() {
                if (mSel.value && ySel.value) {
                    hidden.value = ySel.value + '-' + mSel.value;
                } else if (ySel.value) {
                    hidden.value = ySel.value;
                } else {
                    hidden.value = '';
                }
                hidden.dispatchEvent(new Event('input', { bubbles: true }));
            }
            mSel.addEventListener('change', update);
            ySel.addEventListener('change', update);
        });
'''
if "container.querySelectorAll('.date-picker-group')" not in js:
    js = js.replace('// Input değişiklikleri', event_code + '\n        // Input değişiklikleri')

# 4. Fix checkbox disable logic
js = js.replace("endInput.disabled = this.checked;", "endInput.disabled = this.checked; var group = endInput.closest('.date-picker-group'); if(group) { group.querySelector('.month-select').disabled = this.checked; group.querySelector('.year-select').disabled = this.checked; }")

with open('wwwroot/js/cv-builder.js', 'w', encoding='utf-8') as f:
    f.write(js)
