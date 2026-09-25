'use strict';
const revenue = Number(new URLSearchParams(window.location.search).get('receita'));
const result = window.AdvVentureCalculation.compare(revenue);
const money = value => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
const setText = (id, value) => { document.getElementById(id).textContent = value; };
if (!result.valid) {
  document.getElementById('invalid-result').hidden = false;
} else {
  document.getElementById('valid-result').hidden = false;
  setText('monthly-revenue', money(result.revenue));
  if (result.individual) {
    document.getElementById('numeric-result').hidden = true;
    document.getElementById('individual-analysis').hidden = false;
    setText('result-title', 'Seu cenário merece uma análise individual.');
    setText('result-description', 'Vamos olhar além de uma comparação simples para entender suas possibilidades.');
  } else {
    setText('pf-value', money(result.ir)); setText('pj-value', money(result.das));
    setText('effective-rate', `Alíquota efetiva estimada: ${(result.rate * 100).toLocaleString('pt-BR', { maximumFractionDigits: 3 })}%`);
    if (result.difference > 0) {
      setText('monthly-difference', money(result.difference)); setText('annual-difference', money(result.annualDifference));
    } else {
      setText('result-title', 'Veja a comparação do seu cenário.');
      setText('result-description', 'Esta comparação não indica economia tributária. Uma avaliação individual pode ajudar você a decidir os próximos passos.');
      setText('monthly-label', 'DAS acima do IRPF, por mês'); setText('annual-label', 'Projeção dessa diferença em 12 meses');
      setText('monthly-difference', money(Math.abs(result.difference))); setText('annual-difference', money(Math.abs(result.annualDifference)));
    }
  }
  const checkout = document.getElementById('checkout-link');
  const configuredUrl = window.ADVVENTURE_CONFIG?.checkoutUrl || '';
  if (/^https:\/\//i.test(configuredUrl)) { checkout.href = configuredUrl; checkout.rel = 'noreferrer'; }
  else checkout.addEventListener('click', event => { event.preventDefault(); document.getElementById('checkout-status').hidden = false; });
}
