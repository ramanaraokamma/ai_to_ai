/* AI Academy — client app.
   Two-passcode auth (student / teacher) with PBKDF2 + AES-GCM via WebCrypto,
   mode switching, nav, search, progress tracking, theme, TOC scroll-spy.
   No dependencies. */

(function () {
  'use strict';

  var NAV = window.AIA_NAV || { weeks: [], flat: [], terms: [] };
  var ROUTE = window.AIA_ROUTE || '';
  var UP = window.AIA_UP || '';
  var LVL = (NAV.level && NAV.level.key) || 'l1';
  // progress is per level — L1 week 5 and L2 week 5 are different weeks
  var LS = { mode: 'aia-mode', theme: 'aia-theme', done: 'aia-done-' + LVL };
  var SS = { role: 'aia-role', ks: 'aia-ks', kt: 'aia-kt' };

  function get(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function sget(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function sset(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  function sdel(k) { try { sessionStorage.removeItem(k); } catch (e) {} }
  function url(route) { return UP + route; }          // for fetching real files (…​.json)
  // For links only: routes keep `.html` internally so AIA_ROUTE comparisons stay exact,
  // but hrefs drop it — `.../index.html` becomes a directory URL.
  function href(route) {
    var r = String(route);
    if (r.slice(-10) === 'index.html') r = r.slice(0, -10);
    else if (r.slice(-5) === '.html') r = r.slice(0, -5);
    return (UP + r) || './';
  }

  /* ── auth ─────────────────────────────────────────────────────────────
     Two passcodes derive two AES keys from the same salt. Student content is
     encrypted under the student key; teacher content under the teacher key.
     The student key is also stored wrapped under the teacher key, so the
     teacher passcode opens everything with one unlock.                    */

  function b64ToBytes(s) {
    var raw = atob(s), out = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i);
    return out;
  }
  function bytesToB64(buf) {
    var b = new Uint8Array(buf), s = '';
    for (var i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
    return btoa(s);
  }

  var META = null;
  function meta() {
    if (!META) META = fetch(url('assets/enc/_meta.json')).then(function (r) { return r.json(); });
    return META;
  }

  function deriveKey(pass, salt, iters) {
    return crypto.subtle
      .importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey'])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: 'PBKDF2', salt: salt, iterations: iters, hash: 'SHA-256' },
          base, { name: 'AES-GCM', length: 256 }, true, ['decrypt']);
      });
  }

  function decryptRaw(key, blob) {
    return crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64ToBytes(blob.iv) }, key, b64ToBytes(blob.ct));
  }
  function decryptText(key, blob) {
    return decryptRaw(key, blob).then(function (b) { return new TextDecoder().decode(b); });
  }

  function importAes(rawBytes) {
    return crypto.subtle.importKey('raw', rawBytes, { name: 'AES-GCM' }, true, ['decrypt']);
  }
  function stashKey(slot, key) {
    return crypto.subtle.exportKey('raw', key).then(function (raw) {
      sset(slot, bytesToB64(raw)); return key;
    });
  }
  function loadKey(slot) {
    var v = sget(slot);
    return v ? importAes(b64ToBytes(v)).catch(function () { return null; }) : Promise.resolve(null);
  }

  var Auth = {
    role: function () { return sget(SS.role); },
    isUnlocked: function () { return !!sget(SS.role); },
    can: function (tier) {
      var r = sget(SS.role);
      return r === 'teacher' || (r === 'student' && tier === 'student');
    },

    /* Try teacher first, then student. Resolves to 'teacher' | 'student', rejects on no match. */
    unlock: function (pass) {
      return meta().then(function (m) {
        var salt = b64ToBytes(m.salt);
        return deriveKey(pass, salt, m.iterations).then(function (key) {
          // teacher?
          return decryptText(key, m.verifyTeacher).then(function (txt) {
            if (txt !== m.plain) throw 0;
            return stashKey(SS.kt, key)
              .then(function () { return decryptRaw(key, m.wrappedStudentKey); })
              .then(importAes)
              .then(function (sk) { return stashKey(SS.ks, sk); })
              .then(function () { sset(SS.role, 'teacher'); return 'teacher'; });
          }).catch(function () {
            // student?
            return decryptText(key, m.verifyStudent).then(function (txt) {
              if (txt !== m.plain) throw 0;
              return stashKey(SS.ks, key).then(function () {
                sset(SS.role, 'student'); return 'student';
              });
            });
          });
        });
      });
    },

    keyFor: function (tier) {
      return loadKey(tier === 'teacher' ? SS.kt : SS.ks);
    },

    signOut: function () {
      sdel(SS.role); sdel(SS.ks); sdel(SS.kt);
    }
  };

  window.AIA_auth = Auth;

  /* ── mode ─────────────────────────────────────────────────────────── */

  function currentMode() {
    var h = (location.hash || '').replace('#', '');
    if (h === 'teacher' || h === 'student') { set(LS.mode, h); }
    var m = get(LS.mode, 'student');
    if (m === 'teacher' && Auth.role() !== 'teacher') m = 'student';  // role wins
    return m;
  }

  var mode = currentMode();

  function paintChrome() {
    document.querySelectorAll('[data-mode-btn]').forEach(function (b) {
      var kind = b.getAttribute('data-mode-btn');
      b.setAttribute('aria-current', kind === mode ? 'true' : 'false');
      var allowed = kind === 'student' ? Auth.isUnlocked() : Auth.role() === 'teacher';
      b.classList.toggle('mode-locked', !allowed);
      var lk = b.querySelector('.lk');
      if (lk) lk.hidden = Auth.role() === 'teacher';
    });
    var who = document.getElementById('who');
    var out = document.getElementById('signout');
    var r = Auth.role();
    if (who) {
      who.hidden = !r;
      who.textContent = r === 'teacher' ? '🧑‍🏫 Teacher' : r === 'student' ? '🎒 Student' : '';
    }
    if (out) out.hidden = !r;
  }

  var signout = document.getElementById('signout');
  if (signout) {
    signout.addEventListener('click', function () {
      Auth.signOut();
      location.href = UP || './';
    });
  }


  /* ── theme ────────────────────────────────────────────────────────── */

  var themeBtn = document.getElementById('theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      set(LS.theme, next);
    });
  }

  /* ── progress ─────────────────────────────────────────────────────── */

  function doneSet() {
    try { return new Set(JSON.parse(get(LS.done, '[]'))); } catch (e) { return new Set(); }
  }
  function saveDone(s) { set(LS.done, JSON.stringify(Array.from(s))); }

  window.AIA_progress = { doneSet: doneSet, saveDone: saveDone };

  /* ── encrypted page ───────────────────────────────────────────────── */

  var contentEl = document.getElementById('content');
  var lockEl = document.getElementById('locked');

  function reveal(htmlText) {
    contentEl.innerHTML = htmlText;
    contentEl.hidden = false;
    if (lockEl) lockEl.classList.add('hidden');
    buildToc();
    wireCopy();
  }

  function loadEncrypted(key) {
    return fetch(contentEl.getAttribute('data-enc'))
      .then(function (r) { return r.json(); })
      .then(function (blob) { return decryptText(key, blob); })
      .then(reveal);
  }

  if (contentEl && contentEl.hasAttribute('data-enc')) {
    var tier = contentEl.getAttribute('data-tier') || 'student';
    var form = document.getElementById('unlock-form');
    var msg = document.getElementById('lock-msg');
    var input = document.getElementById('pass');

    function openIfPermitted() {
      if (!Auth.can(tier)) return Promise.resolve(false);
      return Auth.keyFor(tier).then(function (key) {
        if (!key) return false;
        return loadEncrypted(key).then(function () { return true; })
          .catch(function () { return false; });
      });
    }

    openIfPermitted().then(function (ok) {
      if (ok || !msg) return;
      if (Auth.role() === 'student' && tier === 'teacher') {
        msg.className = 'lock-msg err';
        msg.textContent = "You're signed in as a student. This page needs the teacher passcode.";
      }
    });

    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var btn = form.querySelector('button');
        btn.disabled = true;
        msg.className = 'lock-msg';
        msg.textContent = 'Checking…';
        Auth.unlock(input.value)
          .then(function (role) {
            if (!Auth.can(tier)) {
              msg.className = 'lock-msg err';
              msg.textContent = 'That is the student passcode. This page needs the teacher passcode.';
              paintChrome(); buildNav(); buildPager();
              return;
            }
            msg.className = 'lock-msg ok';
            msg.textContent = 'Unlocked as ' + role + '.';
            mode = currentMode();
            paintChrome(); buildNav(); buildPager();
            return Auth.keyFor(tier).then(loadEncrypted);
          })
          .catch(function () {
            msg.className = 'lock-msg err';
            msg.textContent = 'That passcode does not match. Try again.';
            input.select();
          })
          .then(function () { btn.disabled = false; });
      });
    }
  }

  /* ── sidebar nav ──────────────────────────────────────────────────── */

  var ICON = { chapter: '📗', workbook: '✏️', lesson: '🧑‍🏫', test: '📝', project: '🛠️', page: '📄' };
  var LABEL = { chapter: 'Chapter', workbook: 'Workbook', lesson: 'Lesson script', test: 'Test', project: 'Project', page: 'Page' };
  var TERM_COLOR = ['var(--data)', 'var(--correct)', 'var(--model)', 'var(--human)'];

  function visibleKinds() {
    return (mode === 'teacher' && Auth.role() === 'teacher')
      ? ['lesson', 'chapter', 'workbook']
      : ['chapter', 'workbook'];
  }

  function buildNav() {
    var tree = document.getElementById('nav-tree');
    if (!tree) return;
    var kinds = visibleKinds();
    var frag = document.createDocumentFragment();

    NAV.terms.forEach(function (t, ti) {
      var d = document.createElement('details');
      d.className = 'nav-group';
      var weeks = NAV.weeks.filter(function (w) { return w.week >= t.from && w.week <= t.to; });
      var open = weeks.some(function (w) {
        return kinds.some(function (k) { return w.docs[k] === ROUTE; });
      });
      d.open = open;
      var s = document.createElement('summary');
      s.innerHTML = '<span class="term-dot" style="background:' + TERM_COLOR[ti] + '"></span>' +
                    'Term ' + t.number + ' · w' + t.from + '–' + t.to;
      d.appendChild(s);
      weeks.forEach(function (w) {
        var box = document.createElement('div');
        box.className = 'nav-week';
        box.innerHTML = '<p class="wk-title">' + w.week + '. ' + escapeHtml(w.title) + '</p>';
        kinds.forEach(function (k) {
          if (!w.docs[k]) return;
          var a = document.createElement('a');
          a.href = href(w.docs[k]);
          a.innerHTML = '<span class="ic">' + ICON[k] + '</span>' + LABEL[k];
          if (w.docs[k] === ROUTE) a.setAttribute('aria-current', 'page');
          box.appendChild(a);
        });
        d.appendChild(box);
      });
      frag.appendChild(d);
    });

    var extras = NAV.flat.filter(function (f) { return mode === 'teacher' || f.mode === 'student'; });
    if (extras.length) {
      var g = document.createElement('details');
      g.className = 'nav-group';
      g.open = extras.some(function (f) { return f.route === ROUTE; });
      g.innerHTML = '<summary><span class="term-dot" style="background:var(--accent)"></span>Course &amp; extras</summary>';
      var flat = document.createElement('div');
      flat.className = 'nav-flat';
      extras.forEach(function (f) {
        var a = document.createElement('a');
        a.href = href(f.route);
        a.innerHTML = '<span class="ic">' + ICON[f.kind] + '</span> ' + escapeHtml(f.label);
        if (f.route === ROUTE) a.setAttribute('aria-current', 'page');
        flat.appendChild(a);
      });
      g.appendChild(flat);
      frag.appendChild(g);
    }

    tree.innerHTML = '';
    tree.appendChild(frag);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* ── nav search ───────────────────────────────────────────────────── */

  var navSearch = document.getElementById('nav-search');
  if (navSearch) {
    navSearch.addEventListener('input', function () {
      var q = navSearch.value.trim().toLowerCase();
      document.querySelectorAll('#nav-tree .nav-group').forEach(function (g) {
        var any = false;
        g.querySelectorAll('.nav-week').forEach(function (wk) {
          var hit = !q || wk.textContent.toLowerCase().indexOf(q) !== -1;
          wk.classList.toggle('hidden', !hit);
          if (hit) any = true;
        });
        g.querySelectorAll('.nav-flat a').forEach(function (a) {
          var hit = !q || a.textContent.toLowerCase().indexOf(q) !== -1;
          a.classList.toggle('hidden', !hit);
          if (hit) any = true;
        });
        g.classList.toggle('hidden', q && !any);
        if (q && any) g.open = true;
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && e.target === document.body) { e.preventDefault(); navSearch.focus(); }
      if (e.key === 'Escape' && document.activeElement === navSearch) { navSearch.value = ''; navSearch.dispatchEvent(new Event('input')); navSearch.blur(); }
    });
  }

  /* ── pager ────────────────────────────────────────────────────────── */

  function buildPager() {
    var el = document.getElementById('pager');
    if (!el) return;
    var seq = [];
    NAV.terms.forEach(function (t) {
      NAV.weeks.filter(function (w) { return w.week >= t.from && w.week <= t.to; }).forEach(function (w) {
        visibleKinds().forEach(function (k) {
          if (w.docs[k]) seq.push({ route: w.docs[k], label: 'Week ' + w.week + ' · ' + LABEL[k], title: w.title });
        });
      });
    });
    var i = seq.findIndex(function (s) { return s.route === ROUTE; });
    if (i === -1) return;
    var out = '';
    if (i > 0) out += '<a class="prev" href="' + href(seq[i - 1].route) + '"><span>← Previous</span>' + escapeHtml(seq[i - 1].label) + '</a>';
    if (i < seq.length - 1) out += '<a class="next" href="' + href(seq[i + 1].route) + '"><span>Next →</span>' + escapeHtml(seq[i + 1].label) + '</a>';
    el.innerHTML = out;
  }

  /* ── TOC scroll-spy (also rebuilt after decrypt) ──────────────────── */

  function buildToc() {
    var toc = document.querySelector('.toc');
    if (!toc || !contentEl) return;
    var hs = contentEl.querySelectorAll('h2[id], h3[id]');
    if (!hs.length) { toc.innerHTML = ''; return; }
    var out = '<h2>On this page</h2>';
    hs.forEach(function (h) {
      out += '<a class="toc-l' + h.tagName[1] + '" href="#' + h.id + '">' +
             escapeHtml(h.textContent.replace(/#$/, '').trim()) + '</a>';
    });
    toc.innerHTML = out;
    spy(hs, toc);
  }

  function spy(hs, toc) {
    if (!('IntersectionObserver' in window)) return;
    var links = {};
    toc.querySelectorAll('a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        Object.keys(links).forEach(function (k) { links[k].classList.remove('active'); });
        if (links[en.target.id]) links[en.target.id].classList.add('active');
      });
    }, { rootMargin: '-80px 0px -70% 0px' });
    hs.forEach(function (h) { io.observe(h); });
  }

  /* ── copy buttons on code blocks ──────────────────────────────────── */

  function wireCopy() {
    if (!navigator.clipboard || !contentEl) return;
    contentEl.querySelectorAll('pre').forEach(function (pre) {
      if (pre.dataset.wired) return;
      pre.dataset.wired = '1';
      pre.addEventListener('dblclick', function () {
        navigator.clipboard.writeText(pre.textContent);
      });
    });
  }

  /* ── mobile nav ───────────────────────────────────────────────────── */

  var navToggle = document.getElementById('nav-toggle');
  var side = document.getElementById('side');
  if (navToggle && side) {
    var scrim = document.createElement('div');
    scrim.className = 'scrim';
    scrim.hidden = true;
    document.body.appendChild(scrim);

    function isMobile() { return window.innerWidth <= 860; }
    function setNav(open) {
      side.hidden = !open;
      scrim.hidden = !open || !isMobile();
      navToggle.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('nav-open', open && isMobile());
    }
    function fit() { setNav(!isMobile()); }
    fit();
    window.addEventListener('resize', fit);
    navToggle.addEventListener('click', function () { setNav(side.hidden); });
    scrim.addEventListener('click', function () { setNav(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isMobile() && !side.hidden) { setNav(false); navToggle.focus(); }
    });
    // a tap on any nav link should close the drawer, not leave it covering the page
    side.addEventListener('click', function (e) {
      if (isMobile() && e.target.closest('a')) setNav(false);
    });
  }

  /* ── boot ─────────────────────────────────────────────────────────── */

  window.addEventListener('hashchange', function () {
    var m = currentMode();
    if (m !== mode) { mode = m; paintChrome(); buildNav(); buildPager(); }
  });

  paintChrome();
  buildNav();
  buildPager();
  if (contentEl && !contentEl.hasAttribute('data-enc')) { buildToc(); wireCopy(); }
})();
