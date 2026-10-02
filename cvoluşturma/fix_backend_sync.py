import re

with open("wwwroot/js/cv-builder.js", "r", encoding="utf-8") as f:
    text = f.read()

old_sync = '''function syncWithBackend() {
    clearTimeout(syncTimeout);
    syncTimeout = setTimeout(function() {
        var data = CVDataManager.getData();
        fetch('/api/CvApi/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).catch(err => console.error('Cloud Sync Error', err));
    }, 2000);
}'''

new_sync = '''function syncWithBackend() {
    if (!window._isLoggedIn) return; // Sadece giris yapilmissa sync et
    clearTimeout(syncTimeout);
    syncTimeout = setTimeout(function() {
        var data = CVDataManager.getData();
        fetch('/api/CvApi/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(function(res) {
            if (res.ok) {
                var badge = document.getElementById('cloudSyncBadge');
                if (badge) { badge.textContent = 'Buluta kaydedildi ✓'; badge.style.color = '#16a34a'; }
            }
        }).catch(function(err) {
            console.warn('Cloud Sync Error (local mode)', err);
        });
    }, 2000);
}'''

old_load = '''// --- LOAD FROM BACKEND ---
window.addEventListener('DOMContentLoaded', function() {
    fetch('/api/CvApi/load')
        .then(res => {
            if (res.ok) return res.json();
            throw new Error('Not logged in');
        })
        .then(res => {
            if (res.success && res.data) {
                var cloudData = JSON.parse(res.data);
                localStorage.setItem('cv_builder_data', JSON.stringify(cloudData));
                location.reload(); // Quick way to reload with cloud data
            }
        })
        .catch(err => console.log('Running in local mode', err));
});'''

new_load = '''// --- LOAD FROM BACKEND ---
window.addEventListener('DOMContentLoaded', function() {
    fetch('/api/CvApi/load')
        .then(function(res) {
            if (res.status === 401) {
                window._isLoggedIn = false;
                console.log('Running in local mode (not logged in)');
                return null;
            }
            window._isLoggedIn = true;
            return res.json();
        })
        .then(function(res) {
            if (!res) return;
            if (res.success && res.data) {
                try {
                    var cloudData = JSON.parse(res.data);
                    // Bulut verisi localStoragedan daha yeniyse yukle
                    localStorage.setItem('cv_builder_data', JSON.stringify(cloudData));
                    if (typeof CVBuilder !== 'undefined') {
                        CVDataManager.load();
                        CVBuilder.updatePreview();
                    }
                } catch(e) { console.warn('Cloud data parse error', e); }
            }
        })
        .catch(function(err) {
            window._isLoggedIn = false;
            console.log('Running in local mode', err);
        });
});'''

changed = 0
if old_sync in text:
    text = text.replace(old_sync, new_sync)
    changed += 1
    print("OK: syncWithBackend updated")
else:
    print("WARN: syncWithBackend not matched")

if old_load in text:
    text = text.replace(old_load, new_load)
    changed += 1
    print("OK: Load from backend updated")
else:
    print("WARN: Load backend not matched")

with open("wwwroot/js/cv-builder.js", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Total changes: {changed}")
