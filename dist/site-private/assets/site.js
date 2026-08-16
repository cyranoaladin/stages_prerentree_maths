(() => {
  const input = document.querySelector('[data-search-input]');
  const results = document.querySelector('[data-search-results]');
  if (!input || !results || !Array.isArray(window.NEXUS_SEARCH_INDEX)) return;
  input.addEventListener('input', () => {
    const query = input.value.trim().toLocaleLowerCase('fr');
    if (!query) { results.textContent = ''; return; }
    const matches = window.NEXUS_SEARCH_INDEX.filter((item) =>
      [item.title, item.level, item.session, item.audience, item.type].filter(Boolean).join(' ').toLocaleLowerCase('fr').includes(query)
    ).slice(0, 20);
    results.replaceChildren();
    const list = document.createElement('ul');
    matches.forEach((item) => {
      const line = document.createElement('li');
      line.textContent = `${item.title} — ${item.level} ${item.session || ''} (${item.audience})`;
      list.append(line);
    });
    results.append(list);
  });
})();
