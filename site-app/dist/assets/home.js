
/* AI Academy — home page: passcode gate, role gating, search, progress. */
(function () {
  'use strict';
  var Auth = window.AIA_auth;
  var LVL = (window.AIA_NAV.level && window.AIA_NAV.level.key) || 'l1';
  var LS = { mode: 'aia-mode', done: 'aia-done-' + LVL };
  function get(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function mode() {
    var h = (location.hash || '').replace('#', '');
    if (h === 'teacher' || h === 'student') set(LS.mode, h);
    var m = get(LS.mode, 'student');
    if (m === 'teacher' && Auth.role() !== 'teacher') m = 'student';
    return m;
  }

  var gate = document.getElementById('gate');
  var pick = document.getElementById('pick');
  var gateForm = document.getElementById('gate-form');
  var gateMsg = document.getElementById('gate-msg');
  var gatePass = document.getElementById('gate-pass');

  /* Everything with .lockable is inert until the right passcode is in. */
  function applyGate() {
    var role = Auth.role();
    var m = mode();

    if (gate) gate.hidden = !!role;
    if (pick) pick.hidden = !role;

    document.querySelectorAll('.lockable').forEach(function (el) {
      var need = el.getAttribute('data-need') || 'student';
      var allowed = Auth.can(need);
      // teacher-only links are also hidden from a student entirely
      var hide = need === 'teacher' && role !== 'teacher';
      el.classList.toggle('hidden', hide && !!role);
      el.classList.toggle('is-locked', !allowed);
      if (allowed) {
        el.removeAttribute('aria-disabled');
        el.removeAttribute('tabindex');
      } else {
        el.setAttribute('aria-disabled', 'true');
        el.setAttribute('tabindex', '-1');
      }
    });

    document.body.classList.toggle('locked-out', !role);
    document.querySelectorAll('[data-mode-btn]').forEach(function (b) {
      b.setAttribute('aria-current', b.getAttribute('data-mode-btn') === m ? 'true' : 'false');
    });
  }

  /* Clicking a locked link bounces you to the passcode box instead of 404-ing. */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('.lockable');
    if (!a || a.getAttribute('aria-disabled') !== 'true') return;
    e.preventDefault();
    if (!Auth.role()) {
      gate.scrollIntoView({ block: 'center' });
      gatePass.focus();
      gateMsg.className = 'lock-msg';
      gateMsg.textContent = 'Enter a passcode first.';
    } else {
      gateMsg.className = 'lock-msg err';
      gateMsg.textContent = 'That page needs the teacher passcode.';
      gate.hidden = false;
      gate.scrollIntoView({ block: 'center' });
      gatePass.focus();
    }
  });

  if (gateForm) {
    gateForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = gateForm.querySelector('button');
      btn.disabled = true;
      gateMsg.className = 'lock-msg';
      gateMsg.textContent = 'Checking…';
      Auth.unlock(gatePass.value)
        .then(function (role) {
          gateMsg.className = 'lock-msg ok';
          gateMsg.textContent = 'Welcome — signed in as ' + role + '.';
          set(LS.mode, role);
          gatePass.value = '';
          applyGate();
          if (window.AIA_refreshChrome) window.AIA_refreshChrome();
        })
        .catch(function () {
          gateMsg.className = 'lock-msg err';
          gateMsg.textContent = 'That passcode does not match. Try again.';
          gatePass.select();
        })
        .then(function () { btn.disabled = false; });
    });
  }

  /* progress */
  function doneSet() { try { return new Set(JSON.parse(get(LS.done, '[]'))); } catch (e) { return new Set(); } }
  function paintProgress() {
    var s = doneSet();
    document.querySelectorAll('[data-done]').forEach(function (cb) {
      cb.checked = s.has(Number(cb.getAttribute('data-done')));
    });
    (window.AIA_NAV.terms || []).forEach(function (t) {
      var tot = t.to - t.from + 1, n = 0;
      for (var w = t.from; w <= t.to; w++) if (s.has(w)) n++;
      var bar = document.querySelector('[data-term-bar="' + t.number + '"]');
      if (bar) bar.style.width = (n / tot * 100) + '%';
    });
    var pct = document.getElementById('pct');
    if (pct) pct.textContent = Math.round(s.size / 36 * 100) + '%';
  }
  document.addEventListener('change', function (e) {
    var cb = e.target.closest('[data-done]');
    if (!cb) return;
    var s = doneSet(), n = Number(cb.getAttribute('data-done'));
    cb.checked ? s.add(n) : s.delete(n);
    set(LS.done, JSON.stringify(Array.from(s)));
    paintProgress();
  });

  /* search */
  var box = document.getElementById('home-search');
  var count = document.getElementById('home-count');
  if (box) {
    box.addEventListener('input', function () {
      var q = box.value.trim().toLowerCase(), shown = 0;
      document.querySelectorAll('.wk-card').forEach(function (c) {
        var hit = !q || (c.getAttribute('data-search') || '').indexOf(q) !== -1;
        c.classList.toggle('hidden', !hit);
        if (hit) shown++;
      });
      document.querySelectorAll('.term').forEach(function (t) {
        t.classList.toggle('hidden', !t.querySelector('.wk-card:not(.hidden)'));
      });
      count.textContent = q ? shown + ' of 36 weeks match “' + box.value.trim() + '”' : 'Showing all 36 weeks';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && e.target === document.body) { e.preventDefault(); box.focus(); }
    });
  }

  window.addEventListener('hashchange', applyGate);
  applyGate();
  paintProgress();
  if (!Auth.role() && gatePass) gatePass.focus();
})();
