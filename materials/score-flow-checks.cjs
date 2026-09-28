/* Run with Node: node materials/score-flow-checks.cjs */
'use strict';
const assert = require('node:assert/strict');
const C = require('./score-flow-core.js');
const close = (a, b, tolerance, label) => assert.ok(Math.abs(a - b) < tolerance, `${label}: ${a} vs ${b}`);

// Independent finite differences of the log mixture density validate the score.
for (const t of [0, 0.1, 2, 8]) {
  for (const x of [-3, -1.2, 0, 0.8, 3]) {
    const h = 1e-5;
    const derivative = (Math.log(C.density(x + h, t)) - Math.log(C.density(x - h, t))) / (2 * h);
    close(C.score(x, t), derivative, 1e-6, 'mixture score');
  }
}
// Posterior weights derived independently from two Gaussian likelihoods.
for (const alpha of [0.2, 1]) for (const sigma of [0.3, 1, 2]) for (const y of [-1, 0, 0.5]) {
  const plus = C.normalPDF(y, alpha, sigma ** 2), minus = C.normalPDF(y, -alpha, sigma ** 2);
  const mean = (plus - minus) / (plus + minus), z = C.tweedie(y, alpha, sigma, mean);
  close(z.mean, mean, 1e-12, 'posterior mean');
  close((y + sigma * sigma * z.score) / alpha, mean, 1e-12, 'Tweedie identity');
  close(z.risk, plus / (plus + minus) * (1 - mean) ** 2 + minus / (plus + minus) * (-1 - mean) ** 2, 1e-12, 'Bayes risk');
}
assert.equal(C.tweedie(0, 1, 1).mean, 0);
close(C.tweedie(0, 1, 1, 1).risk, 2, 1e-12, 'ambiguous observation risk');

// Exact ODE solutions, and Euler's qualitative stability thresholds.
const small = C.ode('contraction', 0.05).at(-1), coarse = C.ode('contraction', 0.2).at(-1);
assert.ok(Math.abs(small.x - 3 * Math.exp(-6)) < Math.abs(coarse.x - 3 * Math.exp(-6)));
assert.ok(C.ode('contraction', 1.2)[1].x < 0);
assert.ok(Math.abs(C.ode('contraction', 2.2)[1].x) > 3);
close(Math.hypot(...C.exact('rotation', 3, 0, 6)), 3, 1e-12, 'exact rotation radius');

// A numerical CDF checks more than just the first two moments of the output law.
function erf(x) {
  const sign = Math.sign(x), t = 1 / (1 + 0.3275911 * Math.abs(x));
  const p = (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t;
  return sign * (1 - p * Math.exp(-x * x));
}
function cdf(x, time) {
  const {b, q} = C.mixture(time), sd = Math.sqrt(2 * q);
  return (2 + erf((x - b) / sd) + erf((x + b) / sd)) / 4;
}
function transportError(steps) {
  const frames = C.reverse(steps, 500, 21), first = frames[0], last = frames.at(-1);
  return last.ode.reduce((sum, x, i) => sum + Math.abs(cdf(x, 0) - cdf(first.ode[i], 8)), 0) / last.ode.length;
}
const coarseError = transportError(100), fineError = transportError(1600);
assert.ok(fineError < coarseError / 8 && fineError < 0.001, 'ODE should preserve CDF coordinates as steps refine');
const final = C.reverse(800, 10000, 27).at(-1);
for (const kind of ['ode', 'sde']) {
  const xs = final[kind].toSorted((a, b) => a - b), n = xs.length;
  let ks = 0;
  xs.forEach((x, i) => { const f = cdf(x, 0); ks = Math.max(ks, Math.abs(f - i / n), Math.abs(f - (i + 1) / n)); });
  assert.ok(ks < 0.025, `${kind} empirical CDF error ${ks}`);
  console.log(`${kind.toUpperCase()}: KS distance ${ks.toFixed(5)}, variance ${C.moments(xs).variance.toFixed(5)}`);
}
const lang = C.langevin(0.2, 15000, 99, 8).at(-1);
close(C.moments(lang.langevin).variance, 1 / 0.9, 0.04, 'Euler-Maruyama stationary variance');
assert.ok(C.moments(lang.ascent).variance < 1e-6);
console.log(`ODE CDF-coordinate error: ${coarseError.toExponential(3)} (100 steps) → ${fineError.toExponential(3)} (1600 steps)`);
console.log('Score derivatives, Tweedie identities, Bayes risk, stability, and distribution checks passed.');
