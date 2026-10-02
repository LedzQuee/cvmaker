var fso = new ActiveXObject('Scripting.FileSystemObject');
var f = fso.OpenTextFile('wwwroot/js/cv-templates.js', 1);
var content = f.ReadAll();
f.Close();
try {
    eval(content);
    WScript.Echo('Syntax OK');
} catch(e) {
    if (e.description === 'Szdizimi hatas' || e.description.indexOf('Szdizimi') > -1 || e.description.indexOf('Syntax') > -1) {
       WScript.Echo('Syntax Error: ' + e.description);
    } else {
       WScript.Echo('Runtime error (OK for eval): ' + e.description);
    }
}
