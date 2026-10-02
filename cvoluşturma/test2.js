var fso = new ActiveXObject('Scripting.FileSystemObject');
var f = fso.OpenTextFile('wwwroot/js/cv-builder.js', 1);
var content = f.ReadAll();
f.Close();
try {
    eval(content);
    WScript.Echo('Syntax OK');
} catch(e) {
    WScript.Echo('Error: ' + e.description);
}
