/* ================================================================
   PROTEIOS EDUCATION — main.js   (Build Spec v1.3)
   Features:
     - Sticky nav shadow on scroll
     - Mobile hamburger
     - Scroll reveal (fade + translateY)
     - Typewriter effect (35ms/char, once, with blinking cursor)
     - Count-up animation (requestAnimationFrame, ease-out)
       "Endless Possibilities" morphs 0 → ∞
     - Mini sparkline graph draw alongside count-up
     - Roadmap SVG stroke-dashoffset animation on scroll
     - Gallery image staggered fade-in
     - Career tabs
     - Formspree contact form (fetch POST)
     - prefers-reduced-motion respected throughout
   ================================================================ */

'use strict';

const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── NAV SCROLL ───────────────────────────────────────────────── */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
}

/* ── MOBILE MENU ──────────────────────────────────────────────── */
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    const [s1, s2, s3] = hamburger.querySelectorAll('span');
    s1.style.transform = open ? 'rotate(45deg) translate(4px,4px)' : '';
    s2.style.opacity   = open ? '0' : '1';
    s3.style.transform = open ? 'rotate(-45deg) translate(4px,-4px)' : '';
  });
  navLinks.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

/* ── SCROLL REVEAL ────────────────────────────────────────────── */
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      revealObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -32px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

/* ── TYPEWRITER ───────────────────────────────────────────────── */
function typewrite(el) {
  if (REDUCED) return;
  const text   = el.dataset.tw;
  const delay  = parseInt(el.dataset.twDelay || 0);
  el.textContent = '';

  // Blinking cursor
  const cursor = document.createElement('span');
  cursor.className = 'tw-cursor';
  el.appendChild(cursor);

  let i = 0;
  setTimeout(() => {
    const timer = setInterval(() => {
      if (i < text.length) {
        el.insertBefore(document.createTextNode(text[i]), cursor);
        i++;
      } else {
        clearInterval(timer);
        // Remove cursor after 2s
        setTimeout(() => cursor.remove(), 2000);
      }
    }, 35);
  }, delay);
}

const twObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting && !e.target.dataset.twDone) {
      e.target.dataset.twDone = '1';
      typewrite(e.target);
      twObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll('[data-tw]').forEach(el => twObserver.observe(el));

/* ── COUNT-UP ─────────────────────────────────────────────────── */
function easeOutQuart(t) { return 1 - Math.pow(1 - t, 4); }

function countUp(el) {
  if (REDUCED) {
    el.textContent = el.dataset.countFinal;
    return;
  }
  const final   = el.dataset.countFinal;
  const isInfty = final === '∞';
  const target  = isInfty ? 999 : parseFloat(final);
  const suffix  = el.dataset.countSuffix || '';
  const dur     = 1500;
  const start   = performance.now();

  function step(now) {
    const prog = Math.min((now - start) / dur, 1);
    const ease = easeOutQuart(prog);

    if (isInfty) {
      // morph: show numbers climbing, then snap to ∞
      el.textContent = prog < 0.9
        ? Math.round(ease * 99) + '...'
        : '∞';
    } else {
      const isInt = Number.isInteger(target);
      el.textContent = (isInt ? Math.round(ease * target) : (ease * target).toFixed(1)) + suffix;
    }
    if (prog < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/* Mini sparkline alongside each stat */
function drawSparkline(svgEl) {
  if (REDUCED) return;
  const path = svgEl.querySelector('.spark-path');
  if (!path) return;
  const len = path.getTotalLength();
  path.style.strokeDasharray  = len;
  path.style.strokeDashoffset = len;
  path.style.transition = 'stroke-dashoffset 1.5s ease-out';
  requestAnimationFrame(() => {
    path.style.strokeDashoffset = 0;
  });
}

const countObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting && !e.target.dataset.counted) {
      e.target.dataset.counted = '1';
      const numEl = e.target.querySelector('.stat-num[data-count-final]');
      if (numEl) countUp(numEl);
      const spark = e.target.querySelector('.spark-path')?.closest('svg');
      if (spark) drawSparkline(spark);
      countObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.4 });

document.querySelectorAll('.stat-item').forEach(el => countObserver.observe(el));

/* ── ROADMAP ANIMATION ────────────────────────────────────────── */
const roadmapPaths = document.querySelectorAll('.roadmap-path');
if (roadmapPaths.length && !REDUCED) {
  const roadmapObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting && !e.target.dataset.drawn) {
        e.target.dataset.drawn = '1';
        roadmapPaths.forEach(p => {
          const len = p.getTotalLength();
          p.style.strokeDasharray  = len;
          p.style.strokeDashoffset = len;
          p.style.transition = 'stroke-dashoffset 1.8s ease-out';
          requestAnimationFrame(() => { p.style.strokeDashoffset = 0; });
        });

        // Fade-up roadmap nodes
        document.querySelectorAll('.roadmap-node').forEach((node, i) => {
          node.style.opacity   = '0';
          node.style.transform = 'translateY(20px)';
          node.style.transition = `opacity 0.6s ease ${i * 100}ms, transform 0.6s ease ${i * 100}ms`;
          requestAnimationFrame(() => {
            node.style.opacity   = '1';
            node.style.transform = 'translateY(0)';
          });
        });
        roadmapObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.25 });

  const roadmapWrap = document.querySelector('.roadmap-wrap');
  if (roadmapWrap) roadmapObserver.observe(roadmapWrap);
}

/* ── GALLERY STAGGER ──────────────────────────────────────────── */
const galleryItems = document.querySelectorAll('.gallery-grid img');
if (galleryItems.length) {
  const galObserver = new IntersectionObserver((entries) => {
    entries.forEach((e, idx) => {
      if (e.isIntersecting) {
        setTimeout(() => e.target.classList.add('loaded'), idx * 80);
        galObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.05 });
  galleryItems.forEach(img => galObserver.observe(img));
}

/* ── CAREER TABS ──────────────────────────────────────────────── */
window.showTab = function(id, btn) {
  document.querySelectorAll('.ctab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.ctab-btn').forEach(b => b.classList.remove('active'));
  const panel = document.getElementById(id);
  if (panel) panel.classList.add('active');
  btn.classList.add('active');
};

/* ── CONTACT FORM ─────────────────────────────────────────────── */
const forms = document.querySelectorAll('.contact-form');
forms.forEach(form => {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn    = form.querySelector('.form-submit');
    const msgEl  = form.querySelector('.form-msg');
    const data   = Object.fromEntries(new FormData(form).entries());

    btn.disabled = true;
    btn.textContent = 'Sending…';
    if (msgEl) { msgEl.className = 'form-msg'; msgEl.style.display = 'none'; }

    try {
      const res = await fetch('https://formspree.io/f/mjgjwwlr', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (res.ok) {
        form.reset();
        if (msgEl) {
          msgEl.textContent = 'Thank you. Our team will reach out soon.';
          msgEl.className = 'form-msg success';
        }
      } else {
        throw new Error('server');
      }
    } catch {
      if (msgEl) {
        msgEl.textContent = 'Something went wrong. Try again.';
        msgEl.className = 'form-msg error';
      }
    } finally {
      btn.disabled = false;
      btn.textContent = 'Send Message';
    }
  });
});

/* ── ACTIVE NAV LINK ON SCROLL ────────────────────────────────── */
const sections = document.querySelectorAll('section[id]');
const navAs    = document.querySelectorAll('.nav-links a[href^="#"]');
window.addEventListener('scroll', () => {
  let curr = '';
  sections.forEach(sec => {
    if (window.scrollY + 100 >= sec.offsetTop) curr = sec.id;
  });
  navAs.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === `#${curr}`);
  });
}, { passive: true });