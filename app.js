'use strict';
const form = document.querySelector('#simulation-form');
if (form) {
  const revenue = document.querySelector('#revenue');
  const choices = [...document.querySelectorAll('[data-amount]')];
  function updateChoices() { choices.forEach(button => { const selected = Number(button.dataset.amount) === Number(revenue.value); button.classList.toggle('selected', selected); button.setAttribute('aria-pressed', String(selected)); }); }
  choices.forEach(button => button.addEventListener('click', () => { revenue.value = button.dataset.amount; updateChoices(); }));
  revenue.addEventListener('input', updateChoices);
  form.addEventListener('submit', event => { if (!Number.isFinite(Number(revenue.value)) || Number(revenue.value) <= 0 || Number(revenue.value) > 300000) { event.preventDefault(); document.querySelector('#revenue-error').textContent = 'Informe uma média mensal entre R$ 1 e R$ 300.000.'; revenue.focus(); } });
  updateChoices();
}
