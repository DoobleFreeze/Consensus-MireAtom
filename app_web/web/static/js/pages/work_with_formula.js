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

function copyText(el) {
    let input = document.getElementById(el);
    input.select();
    document.execCommand("copy");
    if (input.value !== "") {
        Lobibox.notify('default', {
            pauseDelayOnHover: true,
            continueDelayOnInactiveTab: false,
            position: 'center top',
            title: "Скопировано",
            msg: 'Текст упешно скопирован в буфер обмена.'
        });
    }
}