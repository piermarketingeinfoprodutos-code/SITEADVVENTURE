'use strict';
(function(root) {
  const cents = n => Math.round((n + Number.EPSILON) * 100) / 100;
  function compare(revenue) {
    if (!Number.isFinite(revenue) || revenue < 1 || revenue > 300000) return { valid: false };
    if (revenue > 50000) return { valid: true, individual: true, revenue };
    const base = Math.max(0, revenue - 607.20);
    const brackets = [[2428.80,0,0],[2826.65,.075,182.16],[3751.05,.15,394.16],[4664.68,.225,675.49],[Infinity,.275,908.73]];
    const bracket = brackets.find(([ceiling]) => base <= ceiling);
    const originalIr = cents(Math.max(0, base * bracket[1] - bracket[2]));
    const reduction = revenue <= 5000 ? originalIr : revenue <= 7350 ? Math.max(0, 978.62 - .133145 * revenue) : 0;
    const ir = cents(Math.max(0, originalIr - reduction));
    const annual = revenue * 12;
    const bands = [[180000,.045,0],[360000,.09,8100],[720000,.102,12420]];
    const band = bands.find(([ceiling]) => annual <= ceiling);
    const rate = (annual * band[1] - band[2]) / annual;
    const das = cents(revenue * rate);
    const difference = cents(ir - das);
    return { valid: true, individual: false, revenue, ir, das, rate, difference, annualDifference: cents(difference * 12) };
  }
  root.AdvVentureCalculation = { compare };
  if (typeof module !== 'undefined' && module.exports) module.exports = { compare };
})(typeof window !== 'undefined' ? window : globalThis);
