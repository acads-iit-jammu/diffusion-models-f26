/* Rendering and controls. Numerical routines live in score-flow-core.js. */
(() => {
  'use strict';
  const C = window.ScoreFlow, $ = id => document.getElementById(id);
  const val = id => Number($(id).value), fmt = (x, digits = 3) => Number(x).toFixed(digits);
  const color = name => getComputedStyle(document.documentElement).getPropertyValue('--' + name).trim();
  const extent = (xs, lo, hi, pad = 0.06) => {
    let a = lo, b = hi;
    for (const x of xs) { a = Math.min(a, x); b = Math.max(b, x); }
    const d = Math.max(0.1, b - a) * pad;
    return [a - d, b + d];
  };
  const grid = (a, b, n = 240) => Array.from({length: n + 1}, (_, k) => a + (b - a) * k / n);
  function plot(id, xd, yd, xlabel, ylabel, equalAxes = false) {
    const canvas = $(id), rect = canvas.getBoundingClientRect(), W = rect.width, H = rect.height;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    const ctx = canvas.getContext('2d'); ctx.scale(dpr, dpr);
    let left = 58, right = W - 16;
    const top = 28, bottom = H - 42;
    if (equalAxes && right - left > bottom - top) {
      const inset = (right - left - (bottom - top)) / 2;
      left += inset; right -= inset;
    }
    const x = v => left + (v - xd[0]) / (xd[1] - xd[0]) * (right - left);
    const y = v => bottom - (v - yd[0]) / (yd[1] - yd[0]) * (bottom - top);
    ctx.font = '12px system-ui'; ctx.lineWidth = 1;
    const tick = v => Math.abs(v) >= 100 ? v.toFixed(0) : Math.abs(v) < 0.01 && v !== 0 ? v.toExponential(0) : v.toFixed(1);
    const ticks = W < 400 ? 3 : 5;
    for (let k = 0; k <= ticks; k++) {
      const xx = xd[0] + (xd[1] - xd[0]) * k / ticks;
      ctx.strokeStyle = color('grid'); ctx.beginPath(); ctx.moveTo(x(xx), top); ctx.lineTo(x(xx), bottom); ctx.stroke();
      ctx.fillStyle = color('secondary'); ctx.textAlign = k === 0 ? 'left' : k === ticks ? 'right' : 'center'; ctx.fillText(tick(xx), x(xx), bottom + 18);
      const yy = yd[0] + (yd[1] - yd[0]) * k / ticks;
      ctx.beginPath(); ctx.moveTo(left, y(yy)); ctx.lineTo(right, y(yy)); ctx.stroke();
      ctx.textAlign = 'right'; ctx.fillText(tick(yy), left - 8, y(yy) + 4);
    }
    ctx.fillStyle = color('ink'); ctx.textAlign = 'left'; ctx.fillText(ylabel, left, 15);
    ctx.textAlign = 'center'; ctx.fillText(xlabel, (left + right) / 2, H - 5);
    function line(points, ink = 'blue', width = 2, dash = [], alpha = 1) {
      if (!points.length) return;
      ctx.save(); ctx.beginPath(); ctx.rect(left, top, right - left, bottom - top); ctx.clip();
      ctx.strokeStyle = color(ink); ctx.globalAlpha = alpha; ctx.lineWidth = width; ctx.setLineDash(dash); ctx.beginPath();
      points.forEach((p, i) => i ? ctx.lineTo(x(p[0]), y(p[1])) : ctx.moveTo(x(p[0]), y(p[1]))); ctx.stroke(); ctx.restore();
    }
    function dot(a, b, ink = 'blue', r = 4) {
      ctx.fillStyle = color(ink); ctx.beginPath(); ctx.arc(x(a), y(b), r, 0, Math.PI * 2); ctx.fill();
    }
    function arrow(a, b, c, d, ink = 'secondary') {
      const x1 = x(a), y1 = y(b), x2 = x(c), y2 = y(d), angle = Math.atan2(y2 - y1, x2 - x1);
      if (Math.hypot(x2 - x1, y2 - y1) < 1) return;
      ctx.strokeStyle = color(ink); ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2);
      ctx.lineTo(x2 - 4 * Math.cos(angle - 0.5), y2 - 4 * Math.sin(angle - 0.5)); ctx.moveTo(x2, y2);
      ctx.lineTo(x2 - 4 * Math.cos(angle + 0.5), y2 - 4 * Math.sin(angle + 0.5)); ctx.stroke();
    }
    function bars(bins, ink) {
      ctx.fillStyle = color(ink); ctx.globalAlpha = 0.35;
      for (const bin of bins) ctx.fillRect(x(bin.a), y(bin.d), Math.max(1, x(bin.b) - x(bin.a) - 1), y(0) - y(bin.d));
      ctx.globalAlpha = 1;
    }
    return {line, dot, arrow, bars};
  }
  function histogram(xs, domain, count = 54) {
    const width = (domain[1] - domain[0]) / count;
    const bins = Array.from({length: count}, (_, i) => ({a: domain[0] + i * width, b: domain[0] + (i + 1) * width, d: 0}));
    for (const x of xs) {
      const i = Math.floor((x - domain[0]) / width);
      if (i >= 0 && i < count) bins[i].d += 1 / (xs.length * width);
    }
    return bins;
  }
  function densityPair(id1, id2, xs1, xs2, density) {
    const domain = extent([...xs1, ...xs2], -4.5, 4.5, 0.02);
    const b1 = histogram(xs1, domain), b2 = histogram(xs2, domain);
    const target = grid(...domain).map(x => [x, density(x)]);
    const ymax = Math.max(...b1.map(b => b.d), ...b2.map(b => b.d), ...target.map(p => p[1])) * 1.12;
    [[id1, b1, 'blue'], [id2, b2, 'orange']].forEach(([id, bins, ink]) => {
      const p = plot(id, domain, [0, ymax], 'Position x', 'Density');
      p.bars(bins, ink); p.line(target, 'ink', 2, [5, 4]);
    });
  }
  let odeData, langevinData, reverseData, langevinSeed = 21, reverseSeed = 21;
  function buildOde() { odeData = C.ode($('field').value, val('ode-h')); drawOde(); }
  function drawOde() {
    const kind = $('field').value;
    const i = Math.round(val('ode-progress') / 100 * (odeData.length - 1)), now = odeData[i];
    const exactAll = grid(0, 6).map(t => C.exact(kind, 3, 0, t));
    const points = odeData.slice(0, i + 1), exactNow = C.exact(kind, 3, 0, now.t);
    const spatial = extent([...exactAll.flat(), ...odeData.flatMap(p => [p.x, p.y])], -3.5, 3.5);
    const p = plot('field-canvas', spatial, spatial, 'Position x', 'Position y', true);
    const spacing = (spatial[1] - spatial[0]) / 9;
    const sites = grid(spatial[0] + spacing, spatial[1] - spacing, 6);
    const maxV = Math.max(...sites.flatMap(x => sites.map(y => Math.hypot(...C.field(kind, x, y)))));
    const scale = spacing * 0.65 / maxV;
    sites.forEach(x => sites.forEach(y => { const [a, b] = C.field(kind, x, y); p.arrow(x, y, x + scale * a, y + scale * b); }));
    p.line(grid(0, now.t).map(t => C.exact(kind, 3, 0, t)), 'blue', 3);
    p.line(points.map(q => [q.x, q.y]), 'orange', 1.5);
    points.forEach(q => p.dot(q.x, q.y, 'orange', 2.5)); p.dot(...exactNow, 'blue', 5);
    const yrange = extent([...exactAll.map(q => q[0]), ...odeData.map(q => q.x)], -0.5, 3.5);
    const tp = plot('ode-canvas', [0, 6], yrange, 'Elapsed time t', 'Coordinate x(t)');
    tp.line(grid(0, now.t).map(t => [t, C.exact(kind, 3, 0, t)[0]]));
    tp.line(points.map(q => [q.t, q.x]), 'orange'); points.forEach(q => tp.dot(q.t, q.x, 'orange', 2.5));
    $('ode-time').textContent = fmt(now.t, 2);
    $('ode-readout').textContent = `Exact location (${fmt(exactNow[0])}, ${fmt(exactNow[1])}); Euler (${fmt(now.x)}, ${fmt(now.y)}). Position error ${fmt(Math.hypot(now.x - exactNow[0], now.y - exactNow[1]))}.`;
  }
  function buildLangevin() { langevinData = C.langevin(val('langevin-h'), 1200, langevinSeed); drawLangevin(); }
  function drawLangevin() {
    const f = langevinData[Math.round(val('langevin-progress') / 100 * (langevinData.length - 1))];
    densityPair('ascent-canvas', 'langevin-canvas', f.ascent, f.langevin, x => C.normalPDF(x));
    $('langevin-time').textContent = fmt(f.t, 2);
    $('langevin-readout').textContent = `Variance: ascent ${fmt(C.moments(f.ascent).variance)}, Langevin ${fmt(C.moments(f.langevin).variance)}. Target 1.000; finite-step stationary value ${fmt(1 / (1 - val('langevin-h') / 2))}.`;
  }
  function buildReverse() { reverseData = C.reverse(val('reverse-steps'), 1200, reverseSeed, $('reverse-prior').value); drawReverse(); }
  function drawReverse() {
    const i = Math.round(val('reverse-progress') / 100 * (reverseData.length - 1)), f = reverseData[i];
    densityPair('reverse-ode-density', 'reverse-sde-density', f.ode, f.sde, x => C.density(x, f.t));
    const domain = extent(reverseData.flatMap(q => [...q.ode.slice(0, 12), ...q.sde.slice(0, 12)]), -3.5, 3.5);
    [['ode', 'reverse-ode-path', 'blue'], ['sde', 'reverse-sde-path', 'orange']].forEach(([key, id, ink]) => {
      const p = plot(id, [0, 8], domain, 'Reverse clock tau = 8 - t', 'Particle position');
      for (let k = 0; k < 12; k++) p.line(reverseData.slice(0, i + 1).map(q => [q.r, q[key][k]]), ink, 1.4, [], 0.6);
    });
    const scorePoints = grid(-4.5, 4.5).map(x => [x, C.score(x, f.t)]);
    const sy = extent(scorePoints.map(q => q[1]), -0.2, 0.2, 0.12);
    const sp = plot('score-canvas', [-4.8, 4.8], sy, 'Position x', 'Score s_t(x)');
    sp.line([[-4.5, 0], [4.5, 0]], 'secondary', 1); sp.line(scorePoints, 'green');
    const scoreScale = 0.3 / Math.max(...scorePoints.map(q => Math.abs(q[1])));
    grid(-4.2, 4.2, 20).forEach(x => sp.arrow(x, sy[0] * 0.8, x + scoreScale * C.score(x, f.t), sy[0] * 0.8, 'green'));
    $('reverse-time').textContent = `τ = ${fmt(f.r, 2)}; t = ${fmt(f.t, 2)}`;
    const mo = C.moments(f.ode), ms = C.moments(f.sde), {b, q} = C.mixture(f.t);
    $('reverse-readout').textContent = `Variance: ODE ${fmt(mo.variance)}, SDE ${fmt(ms.variance)}, analytic ${fmt(b * b + q)}. Positive particles: ODE ${fmt(100 * f.ode.filter(x => x > 0).length / f.ode.length, 1)}%, SDE ${fmt(100 * f.sde.filter(x => x > 0).length / f.sde.length, 1)}%; target 50%. Step h = ${fmt(8 / val('reverse-steps'), 4)}.`;
  }
  function drawTweedie() {
    const y = val('tw-y'), alpha = val('tw-alpha'), sigma = val('tw-sigma'), a = val('tw-a');
    const z = C.tweedie(y, alpha, sigma, a);
    ['y', 'alpha', 'sigma', 'a'].forEach(k => $('tw-' + k + '-value').textContent = fmt(val('tw-' + k), 2));
    $('tw-minus').textContent = fmt(z.minus); $('tw-plus').textContent = fmt(z.plus);
    $('tw-minus-bar').style.width = 100 * z.minus + '%'; $('tw-plus-bar').style.width = 100 * z.plus + '%';
    const p = plot('tweedie-map', [-3.2, 3.2], [-1.2, 1.2], 'Observation y', 'Posterior mean m(y)');
    [-1, 1].forEach(v => p.line([[-3, v], [3, v]], 'secondary', 1, [4, 4]));
    p.line(grid(-3, 3).map(x => [x, C.tweedie(x, alpha, sigma).mean])); p.dot(y, z.mean);
    const risks = grid(-1.5, 1.5).map(x => [x, C.tweedie(y, alpha, sigma, x).risk]);
    const rp = plot('tweedie-risk', [-1.6, 1.6], [0, Math.max(...risks.map(q => q[1])) * 1.1], 'Candidate estimate a', 'Conditional squared error');
    rp.line(risks, 'orange'); rp.dot(z.mean, z.variance, 'blue', 5); rp.dot(a, z.risk, 'orange', 4);
    $('tweedie-readout').textContent = `Mean m = ${fmt(z.mean)}; score s = ${fmt(z.score)}. Displacement σ²s = ${fmt(z.displacement)} = αm − y. Minimum risk ${fmt(z.variance)}; candidate risk ${fmt(z.risk)}.`;
  }
  ['field', 'ode-h'].forEach(id => $(id).addEventListener('change', buildOde));
  $('ode-progress').addEventListener('input', drawOde);
  $('langevin-h').addEventListener('change', buildLangevin); $('langevin-progress').addEventListener('input', drawLangevin);
  $('langevin-resample').addEventListener('click', () => { langevinSeed++; buildLangevin(); });
  ['reverse-steps', 'reverse-prior'].forEach(id => $(id).addEventListener('change', buildReverse));
  $('reverse-progress').addEventListener('input', drawReverse); $('reverse-resample').addEventListener('click', () => { reverseSeed++; buildReverse(); });
  ['tw-y', 'tw-alpha', 'tw-sigma', 'tw-a'].forEach(id => $(id).addEventListener('input', drawTweedie));
  $('tw-optimal').addEventListener('click', () => {
    const z = C.tweedie(val('tw-y'), val('tw-alpha'), val('tw-sigma'));
    $('tw-a').step = 'any'; $('tw-a').value = z.mean; drawTweedie();
  });
  buildOde(); buildLangevin(); buildReverse(); drawTweedie();
  const redraw = () => { drawOde(); drawLangevin(); drawReverse(); drawTweedie(); };
  let scheduled;
  new ResizeObserver(() => { cancelAnimationFrame(scheduled); scheduled = requestAnimationFrame(redraw); }).observe(document.querySelector('main'));
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redraw);
})();
