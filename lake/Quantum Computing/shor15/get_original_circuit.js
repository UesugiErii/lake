// use this in console to get circuit code

var s = "";
for (i = 0; i < document.getElementsByClassName("CodeMirror-code")[0].children.length; i++) {
    s += document.getElementsByClassName("CodeMirror-code")[0].children[i].children[1].textContent;
    s += "\n";
 }
console.log(s)