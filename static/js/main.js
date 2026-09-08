// Demotape — main.js
// HTMX initialization and retro CRT effects

document.addEventListener('DOMContentLoaded', function() {
    console.log('[Demotape] System online');

    // Add subtle CRT scanline effect
    const body = document.body;
    body.classList.add('crt-enabled');
});

// HTMX event handlers
document.body.addEventListener('htmx:afterSwap', function(event) {
    console.log('[Demotape] Content swapped via HTMX');
});
