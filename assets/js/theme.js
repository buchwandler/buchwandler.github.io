(function () {
  'use strict';

  var STORAGE_KEY = 'theme';
  var btn = document.querySelector('.theme-toggle');
  if (!btn) return;

  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }

  function updateButton() {
    var isDark = currentTheme() === 'dark';
    btn.setAttribute('aria-pressed', String(isDark));
    var label = isDark ? 'Switch to light mode' : 'Switch to dark mode';
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
    var sun = btn.querySelector('.theme-icon-sun');
    var moon = btn.querySelector('.theme-icon-moon');
    if (sun) sun.hidden = isDark;
    if (moon) moon.hidden = !isDark;
  }

  btn.addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (e) {
      /* localStorage unavailable; preference lasts only this session */
    }
    updateButton();
  });

  updateButton();
})();
