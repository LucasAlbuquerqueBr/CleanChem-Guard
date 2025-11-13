// Language dropdown helpers
function toggleLangMenu() {
  const el = document.getElementById('langMenu');
  if (el) el.classList.toggle('hidden');
}

function switchLang(lang) {
  try {
    const url = new URL(window.location.href);
    url.searchParams.set('lang', lang);
    window.location.href = url.toString();
  } catch (e) {
    // Fallback: just append ?lang=
    window.location.href = '?lang=' + encodeURIComponent(lang);
  }
}

// Close on outside click
document.addEventListener('click', (e) => {
  const toggle = document.getElementById('langToggle');
  const menu = document.getElementById('langMenu');
  if (!toggle || !menu) return;
  if (toggle.contains(e.target) || menu.contains(e.target)) return;
  if (!menu.classList.contains('hidden')) menu.classList.add('hidden');
});

// Post modal viewer
(function () {
  function el(html) {
    const d = document.createElement('div');
    d.innerHTML = html.trim();
    return d.firstChild;
  }

  function chips(tags) {
    if (!tags) return '';
    return tags.split(',').map(t => t.trim()).filter(Boolean)
      .map(t => `<span class="text-xs px-2 py-1 rounded-full bg-[#F3F3F3] text-[#2C2E43]/80">#${t}</span>`)
      .join(' ');
  }

  function openPostModal(data) {
    const media = data.media || '';
    const type = (data.type || '').toLowerCase();
    const desc = data.description || '';
    const content = data.content || '';
    const tags = data.tags || '';

    const overlay = el(`
      <div class="fixed inset-0 bg-black/60 z-[100] flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full overflow-hidden">
          <div class="relative bg-black">
            ${type === 'video'
              ? `<video controls class="w-full h-full max-h-[70vh] object-contain"><source src="${media}"></video>`
              : `<img src="${media}" class="w-full h-full max-h-[70vh] object-contain" />`}
            <button class="absolute top-3 right-3 bg-white/90 hover:bg-white rounded-full w-9 h-9 flex items-center justify-center shadow" aria-label="Close">✕</button>
          </div>
          <div class="p-4">
            ${desc ? `<p class="text-sm text-[#2C2E43]/80">${desc}</p>` : ''}
            ${content ? `<p class="mt-2 font-medium">${content}</p>` : ''}
            <div class="mt-3 flex flex-wrap gap-2">${chips(tags)}</div>
          </div>
        </div>
      </div>
    `);

    function close() {
      overlay.remove();
      document.removeEventListener('keydown', onKey);
    }
    function onKey(ev) { if (ev.key === 'Escape') close(); }

    overlay.addEventListener('click', (ev) => {
      const target = ev.target;
      if (target.closest('button[aria-label="Close"]')) { close(); }
      else if (target === overlay) { close(); }
    });
    document.addEventListener('keydown', onKey);
    document.body.appendChild(overlay);
  }

  document.addEventListener('click', (ev) => {
    const card = ev.target.closest('.js-post-card');
    if (!card) return;
    ev.preventDefault();
    openPostModal({
      media: card.getAttribute('data-media'),
      type: card.getAttribute('data-type'),
      description: card.getAttribute('data-description'),
      content: card.getAttribute('data-content'),
      tags: card.getAttribute('data-tags')
    });
  });
})();
