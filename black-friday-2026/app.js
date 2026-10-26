const dialog = document.getElementById('preview-dialog');
const title = document.getElementById('dialog-title');
const message = document.getElementById('dialog-message');
document.querySelectorAll('[data-preview]').forEach(button => button.addEventListener('click', () => {
  title.textContent = 'Em breve.';
  message.textContent = 'Esta página está em aprovação. O link de contratação será disponibilizado após a validação da campanha.';
  dialog.showModal();
}));
document.querySelectorAll('[data-legal]').forEach(button => button.addEventListener('click', () => {
  title.textContent = button.dataset.legal;
  message.textContent = 'O documento definitivo será vinculado antes da abertura das contratações. Esta é uma prévia para aprovação, sem coleta de dados ou pagamentos.';
  dialog.showModal();
}));
document.querySelectorAll('.dialog-close, .dialog-dismiss').forEach(button => button.addEventListener('click', () => dialog.close()));
dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); }});
const now = new Date();
const currentMonth = Number(new Intl.DateTimeFormat('en', { timeZone:'America/Sao_Paulo', month:'numeric' }).format(now));
const currentYear = Number(new Intl.DateTimeFormat('en', { timeZone:'America/Sao_Paulo', year:'numeric' }).format(now));
if (currentYear === 2026) document.querySelector(`[data-month="${currentMonth}"]`)?.classList.add('active');
