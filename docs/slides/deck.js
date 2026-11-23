/* HarborPoint slide deck engine. No dependencies.
   Keys: → / Space / PgDn next · ← / PgUp back · Home / End · G or Esc: slide index
         N: speaker notes · F: fullscreen · P: print / save as PDF */
(function () {
  "use strict";
  const deck = document.querySelector(".deck");
  const slides = Array.from(deck.querySelectorAll(":scope > .slide"));
  const total = slides.length;
  let cur = 0;

  /* ---------- Footer, numbering ---------- */
  const mark = '<svg viewBox="0 0 48 48" aria-hidden="true"><use href="#i-mark"/></svg>';
  slides.forEach((s, i) => {
    s.dataset.n = i + 1;
    if (s.hasAttribute("data-nofoot")) return;
    const f = document.createElement("div");
    f.className = "foot";
    f.innerHTML = `<span class="mark">${mark}${s.dataset.section || "Azure DevOps for Managers"}</span><span>${i + 1} / ${total}</span>`;
    s.appendChild(f);
  });

  /* ---------- Scale stage to window ---------- */
  function fit() {
    const k = Math.min(window.innerWidth / 1600, window.innerHeight / 900);
    deck.style.transform = `scale(${k})`;
  }
  window.addEventListener("resize", fit);
  fit();

  /* ---------- Charts (inline SVG from data-chart JSON) ---------- */
  const NS = "http://www.w3.org/2000/svg";
  function el(tag, attrs, parent, text) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function buildChart(box) {
    const c = JSON.parse(box.dataset.chart);
    const W = box.clientWidth || 700, H = box.clientHeight || 400;
    const m = Object.assign({ t: 30, r: 30, b: 50, l: 60 }, c.margin || {});
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: "none", role: "img", "aria-label": c.aria || "" });
    box.innerHTML = "";
    box.appendChild(svg);
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const ymax = c.ymax, ymin = c.ymin || 0;
    const y = v => m.t + ih - ((v - ymin) / (ymax - ymin)) * ih;
    const fmt = v => (c.unit === "%" ? v + "%" : c.unit ? v + c.unit : v);
    (c.ticks || []).forEach(t => {
      el("line", { class: "gl", x1: m.l, x2: m.l + iw, y1: y(t), y2: y(t) }, svg);
      el("text", { x: m.l - 14, y: y(t) + 6, "text-anchor": "end" }, svg, fmt(t));
    });
    el("line", { class: "ax", x1: m.l, x2: m.l + iw, y1: m.t + ih, y2: m.t + ih }, svg);
    if (c.type === "line") {
      const n = c.labels.length, step = iw / (n - 1 || 1);
      const x = i => m.l + i * step;
      c.labels.forEach((L, i) => el("text", { x: x(i), y: m.t + ih + 34, "text-anchor": "middle" }, svg, L));
      c.series.forEach(s => {
        const pts = s.values.map((v, i) => (v == null ? null : [x(i), y(v)])).filter(Boolean);
        const d = pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" ");
        let len = 0; for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
        const p = el("path", { class: "ln", d, stroke: s.color }, svg);
        p.style.setProperty("--len", Math.ceil(len) + 1);
        if (s.dash) p.setAttribute("stroke-dasharray", s.dash), p.style.animation = "none";
        s.values.forEach((v, i) => {
          if (v == null) return;
          el("circle", { cx: x(i), cy: y(v), r: 8, fill: "#fff", stroke: s.color, "stroke-width": 4 }, svg);
          if (s.labels !== false && !(s.skip || []).includes(i)) el("text", { class: "v", x: x(i), y: y(v) + (s.below ? 36 : -18), "text-anchor": "middle", fill: s.color }, svg, fmt(v));
        });
        if (s.name && s.tag !== false) {
          const lv = s.values[s.values.length - 1];
          el("text", { class: "ttl", x: x(n - 1) + 18, y: y(lv) + 7, fill: s.color, style: `fill:${s.color}` }, svg, s.name);
        }
      });
    } else if (c.type === "bar") {
      const n = c.labels.length, gw = iw / n, k = c.series.length;
      const bw = Math.min(70, (gw * 0.72) / k);
      c.labels.forEach((L, i) => {
        const gx = m.l + i * gw + gw / 2;
        el("text", { x: gx, y: m.t + ih + 34, "text-anchor": "middle" }, svg, L);
        c.series.forEach((s, j) => {
          const v = s.values[i]; if (v == null) return;
          const bx = gx - (k * bw) / 2 + j * bw + 3;
          const r = el("rect", { class: "bar", x: bx, y: y(v), width: bw - 6, height: m.t + ih - y(v), rx: 8, fill: (s.colors && s.colors[i]) || s.color }, svg);
          r.style.animationDelay = (0.15 + i * 0.08 + j * 0.04) + "s";
          el("text", { class: "v", x: bx + (bw - 6) / 2, y: y(v) - 12, "text-anchor": "middle" }, svg, fmt(v));
        });
      });
    } else if (c.type === "waterfall") {
      const n = c.steps.length, gw = iw / n, bw = Math.min(120, gw * 0.62);
      let run = 0;
      c.steps.forEach((s, i) => {
        const gx = m.l + i * gw + gw / 2;
        let top, bot, col;
        if (s.kind === "total") { top = s.value; bot = 0; run = s.value; col = s.color || "#12355b"; }
        else if (s.kind === "add") { bot = run; top = run + s.value; run = top; col = s.color || "#0f8b8d"; }
        else { top = run; bot = run - s.value; run = bot; col = s.color || "#e2725b"; }
        const r = el("rect", { class: "bar", x: gx - bw / 2, y: y(top), width: bw, height: Math.max(2, y(bot) - y(top)), rx: 8, fill: col }, svg);
        r.style.animationDelay = (0.15 + i * 0.08) + "s";
        const inside = s.kind !== "total" && y(bot) - y(top) > 34;  // label inside tall step bars, above the rest
        el("text", { class: "v", x: gx, y: inside ? (y(top) + y(bot)) / 2 + 7 : y(top) - 12, "text-anchor": "middle", style: inside ? "fill:#fff" : "" }, svg, (s.kind === "sub" ? "−" : s.kind === "add" ? "+" : "") + s.value);
        s.label.split("\n").forEach((L, li) => el("text", { x: gx, y: m.t + ih + 30 + li * 22, "text-anchor": "middle" }, svg, L));
        if (i < n - 1 && s.kind !== "total" || (s.kind === "total" && i < n - 1)) {
          el("line", { x1: gx + bw / 2, x2: gx + gw - bw / 2, y1: y(run), y2: y(run), stroke: "rgba(18,53,91,.35)", "stroke-dasharray": "5 5", "stroke-width": 2 }, svg);
        }
      });
      if (c.line) {
        el("line", { x1: m.l, x2: m.l + iw, y1: y(c.line.value), y2: y(c.line.value), stroke: c.line.color, "stroke-width": 3, "stroke-dasharray": "10 8" }, svg);
        el("text", { class: "ttl", x: m.l + 10, y: y(c.line.value) - 12, "text-anchor": "start", style: `fill:${c.line.color}` }, svg, c.line.label);
      }
    }
  }
  const built = new WeakSet();
  function charts(slide) {
    slide.querySelectorAll("[data-chart]").forEach(b => {
      if (!built.has(b)) { buildChart(b); built.add(b); }
      else { // restart animations
        b.querySelectorAll("path.ln, .bar").forEach(p => { p.style.animationName = "none"; void p.getBoundingClientRect(); p.style.animationName = ""; });
      }
    });
  }

  /* ---------- Navigation ---------- */
  const frags = s => Array.from(s.querySelectorAll(".frag"));
  function show(i, fromBack) {
    i = Math.max(0, Math.min(total - 1, i));
    slides[cur].classList.remove("is-active", "anim");
    cur = i;
    const s = slides[cur];
    s.classList.add("is-active");
    void s.offsetWidth;
    s.classList.add("anim");
    frags(s).forEach(f => f.classList.toggle("on", !!fromBack));
    s.querySelectorAll(".poll").forEach(p => { p.dataset.revealed = ""; });
    syncPolls(s);
    charts(s);
    document.querySelector(".hud .p").style.width = ((cur + 1) / total) * 100 + "%";
    document.querySelector(".ctrl .count").textContent = `${cur + 1} / ${total}`;
    document.documentElement.style.setProperty("--day", getComputedStyle(s).getPropertyValue("--day"));
    history.replaceState(null, "", "#" + (cur + 1));
    const notes = s.querySelector(".notes");
    drawer.innerHTML = `<h4>Speaker notes · slide ${cur + 1}</h4>` + (notes ? notes.innerHTML : "<p>No notes for this slide.</p>");
    index.querySelectorAll("a").forEach((a, k) => a.classList.toggle("cur", k === cur));
    document.title = (s.dataset.title || "Slides") + " · Azure DevOps for Managers";
  }
  function syncPolls(s) {
    s.querySelectorAll(".poll").forEach(p => {
      const answered = p.dataset.revealed === "1" || (p.hasAttribute("data-reveal") && s.querySelector(p.dataset.reveal + ".on"));
      p.classList.toggle("answered", !!answered);
    });
  }
  function next() {
    const s = slides[cur];
    const f = frags(s).find(x => !x.classList.contains("on"));
    if (f) { f.classList.add("on"); syncPolls(s); return; }
    if (cur < total - 1) show(cur + 1);
  }
  function prev() {
    const s = slides[cur];
    const on = frags(s).filter(x => x.classList.contains("on"));
    if (on.length) { on[on.length - 1].classList.remove("on"); syncPolls(s); return; }
    if (cur > 0) show(cur - 1, true);
  }

  /* ---------- Chrome ---------- */
  const hud = document.createElement("div"); hud.className = "hud"; hud.innerHTML = '<div class="p"></div>';
  const ctrl = document.createElement("nav"); ctrl.className = "ctrl"; ctrl.setAttribute("aria-label", "Slide controls");
  ctrl.innerHTML = '<a href="../" title="Back to the lab site">Labs</a><button data-a="index" title="Slide index (G)">☰</button><button data-a="notes" title="Speaker notes (N)">Notes</button><button data-a="full" title="Fullscreen (F)">⤢</button><button data-a="prev" title="Back (←)">‹</button><span class="count"></span><button data-a="next" title="Next (→)">›</button>';
  const drawer = document.createElement("aside"); drawer.className = "notes-drawer"; drawer.setAttribute("aria-live", "polite");
  const index = document.createElement("div"); index.className = "index"; index.setAttribute("role", "dialog"); index.setAttribute("aria-label", "Slide index");
  let html = "<h3>Chart table · all slides</h3>", lastSec = null;
  slides.forEach((s, i) => {
    const sec = s.dataset.part || "Welcome aboard";
    if (sec !== lastSec) { html += (lastSec ? "</ol>" : "") + `<div class="sec">${sec}</div><ol>`; lastSec = sec; }
    html += `<li><a href="#${i + 1}" data-go="${i}"><span>${i + 1}</span>${s.dataset.title || "Slide " + (i + 1)}</a></li>`;
  });
  html += '</ol><p class="help"><kbd>→</kbd> <kbd>Space</kbd> next · <kbd>←</kbd> back · <kbd>G</kbd> this index · <kbd>N</kbd> speaker notes · <kbd>F</kbd> fullscreen · <kbd>P</kbd> print or save as PDF · <kbd>Esc</kbd> close</p>';
  index.innerHTML = html;
  document.body.append(hud, ctrl, drawer, index);

  function toggleIndex(force) { index.classList.toggle("open", force); }
  function full() { if (!document.fullscreenElement) document.documentElement.requestFullscreen?.(); else document.exitFullscreen?.(); }
  ctrl.addEventListener("click", e => {
    const a = e.target.closest("[data-a]")?.dataset.a; if (!a) return;
    ({ index: () => toggleIndex(), notes: () => drawer.classList.toggle("open"), full, prev, next })[a]();
  });
  index.addEventListener("click", e => {
    const a = e.target.closest("[data-go]"); if (!a) return;
    e.preventDefault(); toggleIndex(false); show(+a.dataset.go);
  });
  document.addEventListener("keydown", e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (index.classList.contains("open") && (k === "Escape" || k === "g" || k === "G")) { toggleIndex(false); return; }
    if (["ArrowRight", "ArrowDown", "PageDown", " ", "Enter"].includes(k)) { e.preventDefault(); next(); }
    else if (["ArrowLeft", "ArrowUp", "PageUp", "Backspace"].includes(k)) { e.preventDefault(); prev(); }
    else if (k === "Home") show(0);
    else if (k === "End") show(total - 1);
    else if (k === "g" || k === "G" || k === "Escape") toggleIndex();
    else if (k === "n" || k === "N") drawer.classList.toggle("open");
    else if (k === "f" || k === "F") full();
    else if (k === "p" || k === "P") window.print();
  });
  // Click the stage to advance (but not on links or interactive bits)
  deck.addEventListener("click", e => {
    if (e.target.closest("a, button, .opt")) return;
    const r = deck.getBoundingClientRect();
    if (e.clientX < r.left + r.width * 0.25) prev(); else next();
  });
  // Clicking a poll option reveals the answer
  deck.addEventListener("click", e => {
    const o = e.target.closest(".poll .opt"); if (!o) return;
    const p = o.closest(".poll"); p.dataset.revealed = "1"; p.classList.add("answered");
    const s = slides[cur]; frags(s).forEach(f => f.classList.add("on"));
  });
  // Touch swipe
  let tx = null;
  document.addEventListener("touchstart", e => { tx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener("touchend", e => {
    if (tx == null) return; const dx = e.changedTouches[0].clientX - tx; tx = null;
    if (Math.abs(dx) > 50) (dx < 0 ? next : prev)();
  });
  window.addEventListener("hashchange", () => {
    const n = parseInt(location.hash.slice(1), 10);
    if (n && n - 1 !== cur) show(n - 1);
  });
  window.addEventListener("beforeprint", () => slides.forEach(charts));

  const start = parseInt(location.hash.slice(1), 10);
  show(start ? start - 1 : 0);
})();
