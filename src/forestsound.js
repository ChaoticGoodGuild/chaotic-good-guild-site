/* A forest at night, made in the browser: no music file. A low drone that breathes, wind in the leaves, faraway
   bells in a minor key with a long echo, and the odd cricket. Off until the visitor turns it on (browsers allow
   sound only after a click or a key), and remembered on that device. The Priestess's secret gets its own cues:
   CGGSound.cue("weigh" | "reveal" | "keep"). */
(function () {
  const AC = window.AudioContext || window.webkitAudioContext;
  const btn = document.getElementById("hpSound");
  if (!AC || !btn) return;
  const KEY = "cgg.forestsound";
  let ctx = null, master, bus, verb, echo, droneFilter, droneGain, low, timers = [], on = false, hush = false;
  const rnd = (a, b) => a + Math.random() * (b - a);
  const pick = xs => xs[Math.floor(Math.random() * xs.length)];
  const BELLS = [587.33, 698.46, 783.99, 880, 1046.5, 1174.66];          // D minor pentatonic, up high
  const later = (fn, ms) => { const t = setTimeout(fn, ms); timers.push(t); return t; };

  function noise(seconds) {
    const b = ctx.createBuffer(2, ctx.sampleRate * seconds, ctx.sampleRate);
    for (let c = 0; c < 2; c++) {
      const d = b.getChannelData(c); let last = 0;
      for (let i = 0; i < d.length; i++) { last = (last + 0.02 * (Math.random() * 2 - 1)) / 1.02; d[i] = last * 3.5; }  // soft, brown-ish
    }
    return b;
  }
  function impulse(seconds) {
    const b = ctx.createBuffer(2, ctx.sampleRate * seconds, ctx.sampleRate);
    for (let c = 0; c < 2; c++) {
      const d = b.getChannelData(c);
      for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / d.length, 3.2);
    }
    return b;
  }
  function lfo(freq, depth, target) {
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.frequency.value = freq; g.gain.value = depth; o.connect(g); g.connect(target); o.start();
  }

  function build() {
    ctx = new AC();
    const comp = ctx.createDynamicsCompressor(); comp.threshold.value = -18; comp.ratio.value = 3; comp.connect(ctx.destination);
    master = ctx.createGain(); master.gain.value = 0; master.connect(comp);
    bus = ctx.createGain(); bus.connect(master);
    verb = ctx.createConvolver(); verb.buffer = impulse(5); const vg = ctx.createGain(); vg.gain.value = 0.9; verb.connect(vg); vg.connect(master);
    echo = ctx.createDelay(2); echo.delayTime.value = 0.43; const fb = ctx.createGain(); fb.gain.value = 0.38;
    echo.connect(fb); fb.connect(echo); echo.connect(verb);

    // the drone: D and A, low, through a filter that slowly opens and closes
    droneFilter = ctx.createBiquadFilter(); droneFilter.type = "lowpass"; droneFilter.frequency.value = 420; droneFilter.Q.value = 2;
    droneGain = ctx.createGain(); droneGain.gain.value = 0.11;
    droneFilter.connect(droneGain); droneGain.connect(bus); droneGain.connect(verb);
    [[73.42, "sine", 0], [110, "triangle", 4], [146.83, "sine", -5], [174.61, "sine", 3]].forEach(([f, type, cents], i) => {
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type; o.frequency.value = f; o.detune.value = cents; g.gain.value = [0.9, 0.35, 0.3, 0.12][i];
      o.connect(g); g.connect(droneFilter); o.start();
      lfo(rnd(0.02, 0.06), 4, o.detune);
    });
    lfo(0.045, 160, droneFilter.frequency);
    lfo(0.07, 0.03, droneGain.gain);

    // a low note held back for the Priestess's pause
    low = ctx.createGain(); low.gain.value = 0; low.connect(bus); low.connect(verb);
    const lo = ctx.createOscillator(); lo.type = "sine"; lo.frequency.value = 36.71; lo.connect(low); lo.start();

    // wind in the leaves
    const w = ctx.createBufferSource(); w.buffer = noise(6); w.loop = true;
    const wf = ctx.createBiquadFilter(); wf.type = "bandpass"; wf.frequency.value = 700; wf.Q.value = 0.6;
    const wg = ctx.createGain(); wg.gain.value = 0.05;
    w.connect(wf); wf.connect(wg); wg.connect(bus); wg.connect(verb); w.start();
    lfo(0.03, 380, wf.frequency); lfo(0.05, 0.03, wg.gain);
  }

  function bell(freq, when, level, decay) {
    const t = ctx.currentTime + (when || 0), g = ctx.createGain(), p = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(level, t + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, t + decay);
    [[1, 1], [2.76, 0.18], [5.4, 0.06]].forEach(([m, a]) => {
      const o = ctx.createOscillator(), og = ctx.createGain(); o.frequency.value = freq * m; og.gain.value = a;
      o.connect(og); og.connect(g); o.start(t); o.stop(t + decay + 0.1);
    });
    const out = p || g; if (p) { p.pan.value = rnd(-0.7, 0.7); g.connect(p); }
    const dry = ctx.createGain(); dry.gain.value = 0.35; out.connect(dry); dry.connect(bus);
    out.connect(echo); out.connect(verb);
  }
  function chimes() {
    if (!on) return;
    if (!hush) {
      bell(pick(BELLS), 0, rnd(0.03, 0.05), rnd(3, 5));
      if (Math.random() < 0.3) bell(pick(BELLS) / 2, rnd(0.5, 1.4), 0.03, 4.5);
    }
    later(chimes, rnd(4200, 9000));
  }
  function cricket() {
    if (!on) return;
    if (!hush) {
      const t0 = ctx.currentTime, f = rnd(3900, 4700), pan = rnd(-0.9, 0.9), n = 3 + Math.floor(Math.random() * 4);
      const g = ctx.createGain(); g.gain.value = 0;
      const p = ctx.createStereoPanner ? ctx.createStereoPanner() : null;
      const o = ctx.createOscillator(); o.frequency.value = f; o.connect(g);
      if (p) { p.pan.value = pan; g.connect(p); p.connect(bus); } else g.connect(bus);
      for (let i = 0; i < n; i++) { const s = t0 + i * 0.065; g.gain.setValueAtTime(0, s); g.gain.linearRampToValueAtTime(0.008, s + 0.01); g.gain.linearRampToValueAtTime(0, s + 0.035); }
      o.start(t0); o.stop(t0 + n * 0.065 + 0.05);
    }
    later(cricket, rnd(5000, 13000));
  }

  function fade(to, secs) {
    const t = ctx.currentTime; master.gain.cancelScheduledValues(t);
    master.gain.setValueAtTime(master.gain.value, t); master.gain.linearRampToValueAtTime(to, t + secs);
  }
  function start() {
    if (!ctx) build();
    ctx.resume(); on = true; fade(0.6, 2.5);
    timers.forEach(clearTimeout); timers = [];
    later(chimes, 1500); later(cricket, 4000);
  }
  function stop() {
    if (!ctx) return;
    on = false; timers.forEach(clearTimeout); timers = []; fade(0, 1.2);
    setTimeout(() => { if (!on) ctx.suspend(); }, 1400);
  }
  function show() {
    btn.setAttribute("aria-pressed", on ? "true" : "false");
    btn.querySelector(".hp-sound-label").textContent = on ? "Sound on" : "Sound off";
  }
  btn.addEventListener("click", () => {
    if (on) stop(); else start();
    try { localStorage.setItem(KEY, on ? "on" : "off"); } catch (e) {}
    show();
  });
  // someone who turned it on before: start again at their first touch (browsers need one)
  let wanted = false; try { wanted = localStorage.getItem(KEY) === "on"; } catch (e) {}
  if (wanted) {
    const first = e => { if (btn.contains(e.target)) return; window.removeEventListener("pointerdown", first, true); window.removeEventListener("keydown", first, true); if (!on) { start(); show(); } };
    window.addEventListener("pointerdown", first, true); window.addEventListener("keydown", first, true);
  }
  document.addEventListener("visibilitychange", () => { if (!ctx || !on) return; if (document.hidden) ctx.suspend(); else ctx.resume(); });

  // the Priestess's secret
  window.CGGSound = {
    cue(name) {
      if (!on || !ctx) return;
      const t = ctx.currentTime, f = droneFilter.frequency, lg = low.gain;
      if (name === "weigh") {
        hush = true;
        f.cancelScheduledValues(t); f.setValueAtTime(f.value, t); f.linearRampToValueAtTime(190, t + 2.5);
        lg.cancelScheduledValues(t); lg.setValueAtTime(lg.value, t); lg.linearRampToValueAtTime(0.22, t + 2.8);
      } else if (name === "reveal" || name === "keep") {
        lg.cancelScheduledValues(t); lg.setValueAtTime(lg.value, t); lg.linearRampToValueAtTime(0, t + 2.5);
        f.cancelScheduledValues(t); f.setValueAtTime(f.value, t); f.linearRampToValueAtTime(name === "reveal" ? 900 : 260, t + 1.5); f.linearRampToValueAtTime(420, t + 7);
        if (name === "reveal") [587.33, 739.99, 880, 1174.66].forEach((n, i) => bell(n, i * 0.18, 0.06, 5));   // D major, a lift
        else [293.66, 349.23, 440].forEach((n, i) => bell(n, i * 0.5, 0.05, 6));                              // D minor, slow
        later(() => { hush = false; }, 6000);
      }
    }
  };
  show();
})();
