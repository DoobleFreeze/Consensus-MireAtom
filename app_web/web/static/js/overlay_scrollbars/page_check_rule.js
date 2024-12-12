const { OverlayScrollbars, ClickScrollPlugin } = OverlayScrollbarsGlobal;

OverlayScrollbars.plugin(ClickScrollPlugin);

OverlayScrollbars(document.body, {
    scrollbars: {
        clickScroll: true,
    },
});
OverlayScrollbars(document.getElementById('modal_body_instruction'), {
    scrollbars: {
        clickScroll: true,
    },
});
var scroll_modal_body_all_constructions = OverlayScrollbars(document.getElementById('modal_body_all_constructions'), {
    scrollbars: {
        clickScroll: true,
    },
});