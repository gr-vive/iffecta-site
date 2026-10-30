// IFFECTA landing — hero video over the photo (see design/HANDOFF.md, "Interactions").
// The photo always renders; the video fades in only once it is actually playing.
(function () {
  var video = document.querySelector('[data-hero-video]');
  if (!video) return;

  var mq = window.matchMedia('(max-width:640px)');

  function setup() {
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
  }

  video.addEventListener('playing', function () { video.classList.add('is-playing'); });
  ['pause', 'error', 'stalled', 'waiting'].forEach(function (ev) {
    video.addEventListener(ev, function () { video.classList.remove('is-playing'); });
  });

  setup();
  if (mq.addEventListener) mq.addEventListener('change', setup);
  else mq.addListener(setup);
})();
