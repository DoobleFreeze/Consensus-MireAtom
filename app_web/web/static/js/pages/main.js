$(document).ready(function () {
    var math = document.getElementsByClassName('math');
    for (var i = 0; i < math.length; i++) {
        katex.render(math[i].textContent, math[i], {
            throwOnError: false,
            macros: {
                "\\addBar": "\\bar{#1}",
                "\\bold": "\\mathbf{#1}",
                "\\f": "#1f(#2)"
            }
        });
    }
})