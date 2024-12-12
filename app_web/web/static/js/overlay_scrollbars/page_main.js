const { OverlayScrollbars, ClickScrollPlugin } = OverlayScrollbarsGlobal;

OverlayScrollbars.plugin(ClickScrollPlugin);

OverlayScrollbars(document.body, {
    scrollbars: {
        clickScroll: true,
    },
});
