/* ==========================================================================
   HarborPoint Labs: interactive layer
   - Participant ID personalization (P## -> your ID)
   - Persistent checkpoints, lab progress and completion
   - Knowledge-check quizzes
   - Speed-run timers
   - Home-page voyage progress
   Works with Material's instant navigation via document$.
   ========================================================================== */
(function () {
  "use strict";

  const TOKEN = "P##";
  const KEYS = { pid: "hp.pid", done: "hp.done", prog: (p) => "hp.progress:" + p };
  const DAY_BADGES = { 1: "Navigator", 2: "Lighthouse Keeper", 3: "Harbor Master" };
  const DAY_OF_LAB = (n) => (n <= 4 ? 1 : n <= 8 ? 2 : 3);
  const ICON = {
    anchor: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a3 3 0 0 0-3 3 3 3 0 0 0 2 2.83V9H8v2h3v8.92c-.74-.13-1.5-.34-2.21-.65-.74-.32-1.39-.71-1.97-1.18s-1.04-.98-1.38-1.54L7 15l-4-3v3c0 .97.27 1.88.82 2.72.55.85 1.28 1.6 2.18 2.24.89.64 1.9 1.14 3 1.5 1.1.36 2.23.54 3 .54s1.9-.18 3-.54 2.11-.86 3-1.5c.9-.64 1.63-1.39 2.18-2.24.55-.84.82-1.75.82-2.72v-3l-4 3 1.56 1.55c-.34.56-.8 1.07-1.38 1.54s-1.23.86-1.97 1.18c-.71.31-1.47.52-2.21.65V11h3V9h-3V7.83A3 3 0 0 0 15 5a3 3 0 0 0-3-3m0 2a1 1 0 0 1 1 1 1 1 0 0 1-1 1 1 1 0 0 1-1-1 1 1 0 0 1 1-1"/></svg>',
    medal: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 2H4v2l5.81 4.36a7.004 7.004 0 0 0-4.46 8.84 6.996 6.996 0 0 0 8.84 4.46 7 7 0 0 0 0-13.3L20 4zm-5.06 17.5L12 17.78 9.06 19.5l.78-3.33-2.59-2.24 3.41-.29L12 10.5l1.34 3.13 3.41.29-2.59 2.24zM11 7.19 7.56 4.6h3.44zm2 0V4.6h3.44z"/></svg>',
    ship: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m2 11 2.05.1a7.96 7.96 0 0 1 3.2-5.54L6.13 3.84c-.27-.48-.13-1.09.37-1.37.5-.27 1.09-.11 1.37.37l.93 1.82a8.1 8.1 0 0 1 6.4 0l.93-1.82c.28-.48.87-.64 1.37-.37.5.28.64.89.37 1.37l-1.12 1.72a7.96 7.96 0 0 1 3.2 5.54L22 11a1 1 0 0 1 1 1 1 1 0 0 1-1 1l-2.05-.1a7.96 7.96 0 0 1-3.2 5.54l1.12 1.72c.27.48.13 1.09-.37 1.37-.5.27-1.09.11-1.37-.37l-.93-1.82a8.1 8.1 0 0 1-6.4 0l-.93 1.82c-.28.48-.87.64-1.37.37-.5-.28-.64-.89-.37-1.37l1.12-1.72a7.96 7.96 0 0 1-3.2-5.54L2 13a1 1 0 0 1-1-1 1 1 0 0 1 1-1m7.07.35c.13-.61.46-1.15.93-1.56L8.34 7.25a5.97 5.97 0 0 0-2.29 3.95zm2.93-2.3c.43 0 .84.09 1.21.26l1.33-2.66a6 6 0 0 0-5.08 0l1.33 2.66c.37-.17.78-.26 1.21-.26m2.93 2.3 3.02-.15a5.97 5.97 0 0 0-2.29-3.95L14 9.79c.47.41.8.95.93 1.56m0 1.3c-.13.61-.46 1.15-.93 1.56l1.66 2.54a5.97 5.97 0 0 0 2.29-3.95zm-2.93 2.3c-.43 0-.84-.09-1.21-.26l-1.33 2.66a6 6 0 0 0 5.08 0l-1.33-2.66c-.37.17-.78.26-1.21.26m-2.93-2.3-3.02.15a5.97 5.97 0 0 0 2.29 3.95L10 14.21c-.47-.41-.8-.95-.93-1.56"/></svg>'
  };

  /* ---------- storage ---------- */
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } },
    keys() { try { return Object.keys(localStorage); } catch (e) { return []; } }
  };
  const getPid = () => store.get(KEYS.pid, null);
  const getDone = () => store.get(KEYS.done, {});
  const pageKey = () => location.pathname.replace(/index\.html$/, "");

  function normalizePid(raw) {
    if (!raw) return null;
    const m = String(raw).trim().toUpperCase().match(/^P?\s*(\d{1,2})$/);
    if (!m) return null;
    const n = parseInt(m[1], 10);
    if (n < 1 || n > 99) return null;
    return "P" + String(n).padStart(2, "0");
  }

  /* ---------- participant ID ---------- */
  function wrapTokens(root) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.nodeValue || node.nodeValue.indexOf(TOKEN) === -1) return NodeFilter.FILTER_REJECT;
        const p = node.parentElement;
        if (!p || p.closest(".hp-pid, script, style, textarea")) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      const parts = node.nodeValue.split(TOKEN);
      const frag = document.createDocumentFragment();
      parts.forEach((part, i) => {
        if (part) frag.appendChild(document.createTextNode(part));
        if (i < parts.length - 1) {
          const s = document.createElement("span");
          s.className = "hp-pid";
          s.title = "Your participant ID. Set it with the crew chip in the header.";
          frag.appendChild(s);
        }
      });
      node.parentNode.replaceChild(frag, node);
    });
  }

  function applyPid() {
    const pid = getPid();
    document.querySelectorAll(".hp-pid").forEach((s) => {
      s.textContent = pid || TOKEN;
      s.classList.toggle("is-set", !!pid);
    });
    document.querySelectorAll("[data-hp-pid-text]").forEach((el) => { el.textContent = pid || "not set"; });
    const chip = document.querySelector(".hp-pid-chip");
    if (chip) {
      chip.classList.toggle("is-unset", !pid);
      chip.querySelector(".hp-pid-chip__value").textContent = pid || "Set ID";
    }
  }

  function setPid(v) {
    if (v) store.set(KEYS.pid, v); else store.del(KEYS.pid);
    applyPid();
    document.querySelectorAll(".hp-pid-form .hp-pid-input").forEach((i) => { i.value = v || ""; });
  }

  function ensurePidChip() {
    if (document.querySelector(".hp-pid-chip")) return;
    const anchor = document.querySelector(".md-header__inner .md-search") || document.querySelector(".md-header__inner .md-header__source");
    const host = document.querySelector(".md-header__inner");
    if (!host) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "hp-pid-chip";
    btn.setAttribute("aria-label", "Set your participant ID");
    btn.innerHTML = ICON.ship + '<span class="hp-pid-chip__label">Crew</span> <span class="hp-pid-chip__value">Set ID</span>';
    btn.addEventListener("click", openPidDialog);
    if (anchor) host.insertBefore(btn, anchor); else host.appendChild(btn);
  }

  function openPidDialog() {
    let dlg = document.getElementById("hp-pid-dialog");
    if (!dlg) {
      dlg = document.createElement("dialog");
      dlg.id = "hp-pid-dialog";
      dlg.className = "hp-dialog";
      dlg.innerHTML =
        '<form method="dialog" class="hp-dialog__inner">' +
        "<h3>Your crew number</h3>" +
        "<p>Your instructor assigns you an ID such as <strong>P07</strong>. Every <code>P##</code> in the labs (query folders, dashboard names, sandbox paths) is filled in for you. It is saved only in this browser.</p>" +
        '<input class="hp-pid-input" name="pid" maxlength="3" placeholder="P07" autocomplete="off" />' +
        '<p class="hp-pid-error" aria-live="polite"></p>' +
        '<div class="hp-dialog__actions">' +
        '<button type="button" class="hp-btn hp-btn--line" data-act="clear">Clear</button>' +
        '<button type="button" class="hp-btn hp-btn--line" data-act="cancel">Cancel</button>' +
        '<button type="submit" class="hp-btn hp-btn--teal" data-act="save">Save</button>' +
        "</div></form>";
      document.body.appendChild(dlg);
      const input = dlg.querySelector("input");
      const err = dlg.querySelector(".hp-pid-error");
      dlg.querySelector('[data-act="cancel"]').addEventListener("click", () => dlg.close());
      dlg.querySelector('[data-act="clear"]').addEventListener("click", () => { setPid(null); dlg.close(); toast("Participant ID cleared", "Labs will show P## again."); });
      dlg.querySelector("form").addEventListener("submit", (e) => {
        const v = normalizePid(input.value);
        if (!v) { e.preventDefault(); err.textContent = "Use the format P01 to P99 (or just the number)."; return; }
        err.textContent = "";
        setPid(v);
        toast("Welcome aboard, " + v + "!", "Your ID now appears throughout the labs.");
      });
    }
    dlg.querySelector("input").value = getPid() || "";
    dlg.querySelector(".hp-pid-error").textContent = "";
    if (typeof dlg.showModal === "function") dlg.showModal(); else {
      const v = normalizePid(window.prompt("Your participant ID (e.g. P07)", getPid() || ""));
      if (v) setPid(v);
    }
  }

  function initPidForms() {
    document.querySelectorAll(".md-content .hp-pid-form").forEach((form) => {
      if (form.dataset.ready) return;
      form.dataset.ready = "1";
      form.innerHTML =
        '<label for="hp-pid-inline"><strong>Your participant ID</strong></label>' +
        '<input id="hp-pid-inline" class="hp-pid-input" maxlength="3" placeholder="P07" autocomplete="off" />' +
        '<button type="button" class="hp-btn hp-btn--teal">Save</button>' +
        '<span class="hp-pid-form__status" aria-live="polite"></span>';
      const input = form.querySelector("input");
      const status = form.querySelector(".hp-pid-form__status");
      input.value = getPid() || "";
      const save = () => {
        const v = normalizePid(input.value);
        if (!v) { status.textContent = "Use the format P01 to P99."; return; }
        setPid(v);
        status.textContent = "Saved. You are " + v + ".";
      };
      form.querySelector("button").addEventListener("click", save);
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); save(); } });
    });
  }

  /* ---------- checkpoints and progress ---------- */
  function checkpointBoxes() {
    return Array.from(document.querySelectorAll(
      ".md-content .admonition.checkpoint input[type=checkbox], .md-content details.checkpoint input[type=checkbox]"
    ));
  }

  function currentLab() {
    const head = document.querySelector(".hp-mission[data-lab]");
    return head ? parseInt(head.dataset.lab, 10) : null;
  }

  function renderProgress() {
    const boxes = checkpointBoxes();
    const total = boxes.length;
    const done = boxes.filter((b) => b.checked).length;
    const lab = currentLab();
    const labDone = lab ? !!getDone()[lab] : false;
    const pct = total ? Math.round((done / total) * 100) : (labDone ? 100 : 0);
    const shown = labDone ? 100 : pct;
    document.querySelectorAll(".hp-progress__bar[data-hp-page]").forEach((bar) => { bar.style.width = shown + "%"; });
    document.querySelectorAll(".hp-progress__label[data-hp-page]").forEach((l) => {
      l.textContent = labDone ? "Logged ✓" : total ? done + " of " + total + " checkpoints" : "No checkpoints";
    });
    const book = document.querySelector(".hp-logbook");
    if (book) {
      book.classList.toggle("is-done", labDone);
      const btn = book.querySelector("[data-hp-complete]");
      if (btn) btn.textContent = labDone ? "Logged ✓ (undo)" : "Mark lab complete";
    }
    return { total, done };
  }

  function initCheckpoints() {
    const boxes = checkpointBoxes();
    const key = KEYS.prog(pageKey());
    const saved = store.get(key, []);
    boxes.forEach((b, i) => {
      b.disabled = false;
      b.checked = !!saved[i];
      const li = b.closest("li");
      if (li) li.classList.toggle("is-checked", b.checked);
      b.addEventListener("change", () => {
        const state = store.get(key, []);
        state[i] = b.checked;
        store.set(key, state);
        if (li) li.classList.toggle("is-checked", b.checked);
        const { total, done } = renderProgress();
        const lab = currentLab();
        if (lab && total && done === total && !getDone()[lab]) markLab(lab, true);
      });
    });
    renderProgress();
  }

  function markLab(lab, value) {
    const done = getDone();
    if (value) done[lab] = true; else delete done[lab];
    store.set(KEYS.done, done);
    renderProgress();
    if (!value) return;
    confetti();
    const day = DAY_OF_LAB(lab);
    const labsOfDay = day === 1 ? [1, 2, 3, 4] : day === 2 ? [5, 6, 7, 8] : [9, 10, 11, 12];
    const dayComplete = labsOfDay.every((n) => done[n]);
    const all = Object.keys(done).filter((k) => done[k]).length;
    if (all === 12) toast("Captain of the Harbor!", "All 12 labs logged. Fair winds and following seas.", ICON.medal);
    else if (dayComplete) toast("Day " + day + " badge: " + DAY_BADGES[day], "Every lab for Day " + day + " is logged.", ICON.medal);
    else toast("Lab " + lab + " logged", all + " of 12 labs complete. Onward!", ICON.anchor);
  }

  function initCompleteButtons() {
    document.querySelectorAll(".md-content [data-hp-complete]").forEach((btn) => {
      if (btn.dataset.ready) return;
      btn.dataset.ready = "1";
      btn.addEventListener("click", () => {
        const lab = currentLab();
        if (!lab) return;
        markLab(lab, !getDone()[lab]);
      });
    });
  }

  function initReset() {
    document.querySelectorAll(".md-content [data-hp-reset]").forEach((btn) => {
      if (btn.dataset.ready) return;
      btn.dataset.ready = "1";
      btn.addEventListener("click", () => {
        if (!window.confirm("Reset all lab progress and checkpoints in this browser? (Your participant ID is kept.)")) return;
        store.keys().filter((k) => k.indexOf("hp.progress:") === 0).forEach((k) => store.del(k));
        store.del(KEYS.done);
        toast("Progress reset", "A clean slate. The tide's in.");
        initHome();
      });
    });
  }

  /* ---------- home / day pages ---------- */
  function initHome() {
    const done = getDone();
    document.querySelectorAll("[data-hp-lab]").forEach((el) => {
      el.classList.toggle("is-done", !!done[el.dataset.hpLab]);
    });
    document.querySelectorAll("[data-hp-day]").forEach((el) => {
      const labs = (el.dataset.hpLabs || "").split(",").filter(Boolean);
      const n = labs.filter((l) => done[l]).length;
      el.classList.toggle("is-complete", labs.length > 0 && n === labs.length);
      const c = el.querySelector("[data-hp-day-count]");
      if (c) c.textContent = n + " / " + labs.length + " labs logged";
    });
    const total = Object.keys(done).filter((k) => done[k]).length;
    document.querySelectorAll("[data-hp-total-bar]").forEach((b) => { b.style.width = Math.round((total / 12) * 100) + "%"; });
    document.querySelectorAll("[data-hp-total-label]").forEach((l) => { l.textContent = total + " of 12 labs logged"; });
  }

  /* ---------- quizzes ---------- */
  function initQuizzes() {
    document.querySelectorAll(".md-content .quiz").forEach((quiz) => {
      if (quiz.dataset.ready) return;
      const list = quiz.querySelector("ul.task-list, ul");
      if (!list) return;
      quiz.dataset.ready = "1";
      const items = Array.from(list.children).filter((n) => n.tagName === "LI");
      const box = document.createElement("div");
      box.className = "quiz-options";
      box.setAttribute("role", "group");
      items.forEach((li, i) => {
        const input = li.querySelector("input[type=checkbox]");
        const correct = !!(input && input.checked);
        const ctrl = li.querySelector("label.task-list-control");
        if (ctrl) ctrl.remove(); else if (input) input.remove();
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "quiz-opt";
        btn.dataset.correct = correct ? "1" : "0";
        btn.innerHTML = '<span class="quiz-letter">' + "ABCDEF"[i] + '</span><span class="quiz-text">' + li.innerHTML.trim() + "</span>";
        btn.addEventListener("click", () => answerQuiz(quiz, btn));
        box.appendChild(btn);
      });
      list.replaceWith(box);
    });
  }

  function answerQuiz(quiz, btn) {
    if (quiz.classList.contains("is-answered")) return;
    const ok = btn.dataset.correct === "1";
    quiz.classList.add("is-answered", ok ? "quiz--right" : "quiz--wrong");
    quiz.querySelectorAll(".quiz-opt").forEach((b) => {
      b.disabled = true;
      if (b.dataset.correct === "1") b.classList.add("is-correct");
    });
    if (!ok) btn.classList.add("is-wrong");
    const verdict = document.createElement("p");
    verdict.className = "quiz-verdict";
    verdict.innerHTML = (ok ? "✓ Correct. Steady as she goes." : "✗ Not quite. Here's the reasoning.") +
      '<button type="button" class="quiz-retry">Try again</button>';
    verdict.querySelector(".quiz-retry").addEventListener("click", () => resetQuiz(quiz));
    const why = quiz.querySelector(".quiz-why");
    quiz.insertBefore(verdict, why || null);
  }

  function resetQuiz(quiz) {
    quiz.classList.remove("is-answered", "quiz--right", "quiz--wrong");
    quiz.querySelectorAll(".quiz-opt").forEach((b) => { b.disabled = false; b.classList.remove("is-correct", "is-wrong"); });
    const v = quiz.querySelector(".quiz-verdict");
    if (v) v.remove();
  }

  /* ---------- timers ---------- */
  let timers = [];
  function clearTimers() { timers.forEach((t) => clearInterval(t)); timers = []; }

  function initTimers() {
    document.querySelectorAll(".md-content .timer").forEach((el) => {
      if (el.dataset.ready) return;
      el.dataset.ready = "1";
      const total = Math.max(1, parseFloat(el.dataset.minutes || "10")) * 60;
      let left = total, handle = null;
      el.innerHTML =
        '<span class="timer-label">' + (el.dataset.label || "Timer") + "</span>" +
        '<span class="timer-display" aria-live="off"></span>' +
        '<button type="button" class="timer-go">Start</button>' +
        '<button type="button" class="timer-reset">Reset</button>';
      const disp = el.querySelector(".timer-display");
      const go = el.querySelector(".timer-go");
      const fmt = (s) => String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
      const draw = () => {
        disp.textContent = fmt(left);
        el.classList.toggle("is-low", left > 0 && left <= 60);
        el.classList.toggle("is-done", left === 0);
      };
      const stop = () => { if (handle) { clearInterval(handle); handle = null; } go.textContent = left === total ? "Start" : "Resume"; };
      go.addEventListener("click", () => {
        if (handle) { stop(); return; }
        if (left === 0) left = total;
        go.textContent = "Pause";
        handle = setInterval(() => {
          left = Math.max(0, left - 1);
          draw();
          if (left === 0) { stop(); go.textContent = "Start"; toast("Time!", "Speed run over. Compare notes, then check the hints.", ICON.ship); }
        }, 1000);
        timers.push(handle);
      });
      el.querySelector(".timer-reset").addEventListener("click", () => { stop(); left = total; draw(); go.textContent = "Start"; });
      draw();
    });
  }

  /* ---------- toast ---------- */
  let toastTimer = null;
  function toast(title, text, icon) {
    let t = document.querySelector(".hp-toast");
    if (!t) {
      t = document.createElement("div");
      t.className = "hp-toast";
      t.setAttribute("role", "status");
      document.body.appendChild(t);
    }
    t.innerHTML = (icon || ICON.anchor) + "<div><strong></strong><span></span></div>";
    t.querySelector("strong").textContent = title;
    t.querySelector("span").textContent = text || "";
    requestAnimationFrame(() => t.classList.add("is-on"));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove("is-on"), 4200);
  }

  /* ---------- confetti ---------- */
  function confetti() {
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const c = document.createElement("canvas");
    c.className = "hp-confetti";
    document.body.appendChild(c);
    const ctx = c.getContext("2d");
    const dpr = window.devicePixelRatio || 1;
    const resize = () => { c.width = innerWidth * dpr; c.height = innerHeight * dpr; };
    resize();
    const colors = ["#e6b450", "#0f8b8d", "#8fd6cf", "#e2725b", "#ffffff", "#12355b"];
    const parts = Array.from({ length: 170 }, () => ({
      x: innerWidth * (0.25 + Math.random() * 0.5) * dpr,
      y: innerHeight * 0.35 * dpr,
      vx: (Math.random() - 0.5) * 14 * dpr,
      vy: (-Math.random() * 13 - 5) * dpr,
      w: (6 + Math.random() * 6) * dpr,
      h: (8 + Math.random() * 10) * dpr,
      r: Math.random() * Math.PI,
      vr: (Math.random() - 0.5) * 0.35,
      c: colors[(Math.random() * colors.length) | 0]
    }));
    const start = performance.now();
    (function frame(now) {
      const t = now - start;
      ctx.clearRect(0, 0, c.width, c.height);
      parts.forEach((p) => {
        p.vy += 0.38 * dpr; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.r += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r);
        ctx.globalAlpha = Math.max(0, 1 - t / 2600);
        ctx.fillStyle = p.c; ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h * Math.abs(Math.cos(p.r)));
        ctx.restore();
      });
      if (t < 2700) requestAnimationFrame(frame); else c.remove();
    })(start);
  }

  /* ---------- boot ---------- */
  function init() {
    clearTimers();
    const content = document.querySelector(".md-content");
    wrapTokens(content);
    ensurePidChip();
    applyPid();
    initPidForms();
    initCheckpoints();
    initCompleteButtons();
    initQuizzes();
    initTimers();
    initReset();
    initHome();
  }

  if (typeof window.document$ !== "undefined" && window.document$.subscribe) {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
