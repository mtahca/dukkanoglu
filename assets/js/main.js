(function () {
  'use strict';

  // Mobil menü
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Ana sayfa slider
  var slides = document.querySelectorAll('.slide');
  var dotsWrap = document.querySelector('.slider-dots');
  if (slides.length > 1) {
    var current = 0;
    var timer;
    var dots = [];
    var show = function (i) {
      slides[current].classList.remove('active');
      if (dots[current]) dots[current].classList.remove('active');
      current = (i + slides.length) % slides.length;
      slides[current].classList.add('active');
      if (dots[current]) dots[current].classList.add('active');
    };
    var start = function () { timer = setInterval(function () { show(current + 1); }, 5000); };
    if (dotsWrap) {
      slides.forEach(function (_, i) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', (i + 1) + '. slayt');
        b.addEventListener('click', function () { clearInterval(timer); show(i); start(); });
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }
    slides[0].classList.add('active');
    if (dots[0]) dots[0].classList.add('active');
    start();
  } else if (slides.length === 1) {
    slides[0].classList.add('active');
  }

  // Galeri lightbox
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (links.length) {
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML = '<button class="lb-close" aria-label="Kapat">×</button>' +
      '<button class="lb-prev" aria-label="Önceki">‹</button>' +
      '<img alt=""><button class="lb-next" aria-label="Sonraki">›</button>';
    document.body.appendChild(box);
    var img = box.querySelector('img');
    var idx = 0;
    var open = function (i) {
      idx = (i + links.length) % links.length;
      img.src = links[idx].getAttribute('href');
      box.classList.add('open');
    };
    var close = function () { box.classList.remove('open'); img.src = ''; };
    links.forEach(function (a, i) {
      a.addEventListener('click', function (e) { e.preventDefault(); open(i); });
    });
    box.querySelector('.lb-close').addEventListener('click', close);
    box.querySelector('.lb-prev').addEventListener('click', function () { open(idx - 1); });
    box.querySelector('.lb-next').addEventListener('click', function () { open(idx + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') open(idx - 1);
      if (e.key === 'ArrowRight') open(idx + 1);
    });
  }
})();
