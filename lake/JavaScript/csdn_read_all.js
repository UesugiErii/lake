// ==UserScript==
// @name         csdn read all
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  auto read all in csdn
// @author       zx
// @match        *://blog.csdn.net/*
// @grant        none
// ==/UserScript==

(function() {
    var b;
    b = document.getElementsByClassName('btn-readmore');
    b[0].click();
})();