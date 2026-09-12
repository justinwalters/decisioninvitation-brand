'use strict';
const themes = document.querySelectorAll('[data-theme]');
themes.forEach(button => button.addEventListener('click', () => {
  const theme = button.dataset.theme;
  const path = `/brand-assets/production/01-logo/svg/di-lockup-${theme}.svg`;
  document.querySelector('#logo-stage').dataset.theme = theme;
  document.querySelector('#logo-preview').src = path;
  document.querySelector('#logo-preview').alt = `DecisionInvitation ${theme} logo`;
  document.querySelector('#current-logo-download').href = path;
  themes.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
}));
const filters = document.querySelectorAll('[data-filter]');
filters.forEach(button => button.addEventListener('click', () => {
  let count = 0;
  document.querySelectorAll('.asset-item').forEach(item => {
    item.hidden = button.dataset.filter !== 'all' && item.dataset.category !== button.dataset.filter;
    if (!item.hidden) count++;
  });
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelector('#asset-count').textContent = `${count} resource${count === 1 ? '' : 's'}`;
}));
const input = document.querySelector('#type-input');
const output = document.querySelector('#type-output');
input.addEventListener('input', () => { output.textContent = input.value || 'Ask separately. Decide clearly.'; });
document.querySelector('#type-reset').addEventListener('click', () => {
  input.value = '';
  output.replaceChildren('Ask separately.', document.createElement('br'), 'Decide clearly.');
  input.focus();
});
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
  const status = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(button.dataset.copy);
    status.textContent = `Copied ${button.dataset.copy}.`;
    const original = button.lastElementChild.innerHTML;
    button.lastElementChild.textContent = 'Copied ✓';
    window.setTimeout(() => { button.lastElementChild.innerHTML = original; }, 1600);
  } catch { status.textContent = `Copy unavailable. Color value: ${button.dataset.copy}.`; }
}));
