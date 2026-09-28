/* Pure numerical routines shared by the teaching lab and its checks.
   No clipping or rescaling of simulated particles. Seeded randomness. */
(function (root) {
  'use strict';
  function random(seed) {
    let state = seed >>> 0;
    const uniform = () => {
      state = (Math.imul(1664525, state) + 1013904223) >>> 0;
      return (state + 0.5) / 4294967296;
    };
    const normal = () => Math.sqrt(-2 * Math.log(uniform())) * Math.cos(2 * Math.PI * uniform());
    return {uniform, normal};
  }
  function moments(xs) {
    const mean = xs.reduce((a, x) => a + x, 0) / xs.length;
    return {mean, variance: xs.reduce((a, x) => a + (x - mean) ** 2, 0) / xs.length};
  }
  function normalPDF(x, mean = 0, variance = 1) {
    return Math.exp(-((x - mean) ** 2) / (2 * variance)) / Math.sqrt(2 * Math.PI * variance);
  }
  function mixture(t, m = 2, a = 0.35) {
    return {b: Math.exp(-t / 2) * m, q: Math.exp(-t) * a * a - Math.expm1(-t)};
  }
  function density(x, t) {
    const {b, q} = mixture(t);
    return (normalPDF(x, -b, q) + normalPDF(x, b, q)) / 2;
  }
  function score(x, t) {
    const {b, q} = mixture(t);
    return (b * Math.tanh(b * x / q) - x) / q;
  }
  function field(kind, x, y) {
    return kind === 'rotation' ? [-y, x] : kind === 'constant' ? [2, 0] : [-x, -y];
  }
  function exact(kind, x, y, t) {
    if (kind === 'rotation') return [x * Math.cos(t) - y * Math.sin(t), x * Math.sin(t) + y * Math.cos(t)];
    if (kind === 'constant') return [x + 2 * t, y];
    return [x * Math.exp(-t), y * Math.exp(-t)];
  }
  function ode(kind, h, T = 6) {
    let x = 3, y = 0, t = 0;
    const points = [{t, x, y}];
    while (t < T - 1e-10) {
      const dt = Math.min(h, T - t), [vx, vy] = field(kind, x, y);
      x += dt * vx; y += dt * vy; t += dt;
      points.push({t, x, y});
    }
    return points;
  }
  function langevin(h, n = 1200, seed = 21, T = 6) {
    const rng = random(seed), initial = Array.from({length: n}, () => rng.normal());
    let xs = initial.slice(), t = 0;
    const frames = [{t, ascent: initial.slice(), langevin: xs.slice()}];
    while (t < T - 1e-10) {
      const dt = Math.min(h, T - t);
      xs = xs.map(x => x - dt * x + Math.sqrt(2 * dt) * rng.normal());
      t += dt;
      frames.push({t, ascent: initial.map(x => x * Math.exp(-t)), langevin: xs.slice()});
    }
    return frames;
  }
  function reverse(steps = 400, n = 1200, seed = 21, prior = 'exact', T = 8) {
    const rng = random(seed), {b, q} = mixture(T);
    let xs = Array.from({length: n}, () => prior === 'exact'
      ? (rng.uniform() < 0.5 ? -b : b) + Math.sqrt(q) * rng.normal()
      : rng.normal());
    let xo = xs.slice();
    const h = T / steps, stride = Math.max(1, Math.floor(steps / 160));
    const frames = [{t: T, r: 0, sde: xs.slice(), ode: xo.slice()}];
    for (let k = 0; k < steps; k++) {
      const t = T - k * h;
      xs = xs.map(x => x + h * (x / 2 + score(x, t)) + Math.sqrt(h) * rng.normal());
      xo = xo.map(x => x + h * (x / 2 + score(x, t) / 2));
      if ((k + 1) % stride === 0 || k + 1 === steps) {
        const r = (k + 1) * h;
        frames.push({t: Math.max(0, T - r), r, sde: xs.slice(), ode: xo.slice()});
      }
    }
    return frames;
  }
  function tweedie(y, alpha, sigma, estimate = 0) {
    const mean = Math.tanh(alpha * y / (sigma * sigma));
    const s = (alpha * mean - y) / (sigma * sigma);
    return {mean, score: s, plus: (mean + 1) / 2, minus: (1 - mean) / 2,
      displacement: sigma * sigma * s, variance: 1 - mean * mean,
      risk: 1 - mean * mean + (estimate - mean) ** 2};
  }
  const api = {random, moments, normalPDF, mixture, density, score, field, exact, ode, langevin, reverse, tweedie};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ScoreFlow = api;
})(globalThis);
