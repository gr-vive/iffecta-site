// IFFECTA — hero video, scroll reveal, hero parallax.
// Design notes: design/HANDOFF.md ("Interactions"). Motion respects prefers-reduced-motion.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Hero video over the photo: fades in only once it is actually playing ----
  var video = document.querySelector('[data-hero-video]');
  if (video) {
    var mq = window.matchMedia('(max-width:640px)');
    var setup = function () {
      var src = mq.matches ? video.dataset.srcMobile : video.dataset.srcDesktop;
      if (!src || video.getAttribute('data-src') === src) return;
      video.setAttribute('data-src', src);
      video.classList.remove('is-playing');
      video.muted = true;
      video.loop = true;
      video.playsInline = true;
      video.src = src;
      var p = video.play();
      if (p && p.catch) p.catch(function () {});
    };
    var heroEl = video.closest('.hero');
    video.addEventListener('playing', function () {
      video.classList.add('is-playing');
      if (heroEl) heroEl.classList.add('hero--video');
    });
    ['pause', 'error', 'stalled', 'waiting'].forEach(function (ev) {
      video.addEventListener(ev, function () {
        video.classList.remove('is-playing');
        if (heroEl) heroEl.classList.remove('hero--video');
      });
    });
    setup();
    if (mq.addEventListener) mq.addEventListener('change', setup);
    else mq.addListener(setup);
  }

  if (reduce) return;

  // ---- Scroll reveal ----
  // [selector, variant class, stagger step in seconds between siblings of the same selector]
  var groups = [
    ['.about__photo', '', 0],
    ['.about__intro p', 'reveal--line', 0.12],
    ['.about__head', '', 0.15],
    ['.benefits__text .label, .benefits__text .btn', 'reveal--line', 0.1],
    ['.benefits__list li', 'reveal--line', 0.09],
    ['.benefits__photo', '', 0],
    ['.actives .section-head', '', 0],
    ['.lotus', 'reveal--scale', 0],
    ['.actives__also', 'reveal--line', 0],
    ['.ingredient', '', 0.12],
    ['.inci', 'reveal--line', 0],
    ['.how__text > div:first-child', '', 0],
    ['.steps li', 'reveal--line', 0.1],
    ['.pills', 'reveal--line', 0.3],
    ['.how__photo', '', 0],
    ['.ugc .section-head', '', 0],
    ['.ugc__grid .photo', '', 0.1],
    ['.lineup .section-head', '', 0],
    ['.product', '', 0.12],
    ['.buy__card', 'reveal--right', 0],
    ['.footer__big', 'reveal--big', 0],
    ['.footer__col', 'reveal--line', 0.08],
    ['.doc-head > *', 'reveal--line', 0.08],
    ['.toc', '', 0],
    ['.doc > *', 'reveal--line', 0.05]
  ];
  var targets = [];
  groups.forEach(function (g) {
    var nodes = document.querySelectorAll(g[0]);
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      el.classList.add('reveal');
      if (g[1]) el.classList.add(g[1]);
      if (g[2]) el.style.setProperty('--d', (Math.min(i, 8) * g[2]).toFixed(2) + 's');
      targets.push(el);
    }
  });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // ---- Hero parallax: media drifts at 15% of scroll while the hero is on screen ----
  var media = document.querySelector('[data-parallax]');
  var hero = media && media.parentElement;
  if (media && hero) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var rect = hero.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > window.innerHeight) return;
      var y = Math.max(0, -rect.top) * 0.15;
      media.style.transform = 'translate3d(0,' + y.toFixed(1) + 'px,0)';
    };
    window.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }, { passive: true });
    update();
  }
})();
