// Lightweight client-side i18n to complement Django i18n.
// Applies to all pages without blocking rendering.
(function () {
  var translations = {
    fa: {
      'menu.home': 'خانه',
      'menu.events': 'رویدادها',
      'menu.tours': 'تورها',
      'menu.realestate': 'املاک',
      'menu.advertising': 'تبلیغات',
      'menu.education': 'دانشجویی',
      'menu.business': 'بیزینس',
      'menu.decoration': 'دکوراسیون',
      'menu.legal': 'حقوقی',
      'menu.blog': 'وبلاگ',
      'menu.about': 'درباره ما',
      'menu.contact': 'تماس',
      'menu.courses': 'دوره آموزشی',
      'auth.login': 'ورود',
      'auth.signup': 'عضویت',
      'auth.logout': 'خروج',
      'auth.dashboard': 'پنل کاربر',
      // Home page keys used earlier
      'mainTitle': 'کانون همیاری فارسی‌زبانان ترکیه',
      'subtitle': 'مجموعه‌ای اجتماعی، خدماتی و حمایتی برای ایرانیان و فارسی‌زبانان مقیم ترکیه',
      'aboutTitle': 'درباره کانون همیاری',
      'goalsTitle': 'اهداف ما',
      'ourServices': 'خدمات ما',
      'events': 'رویدادها',
      'tours': 'تورها',
      'realEstate': 'املاک',
      'advertising': 'تبلیغات',
      'education': 'تحصیلی',
      'legal': 'امور حقوقی',
      'testimonialsTitle': 'نظرات اعضای کانون همیاری'
    },
    en: {
      'menu.home': 'Home',
      'menu.events': 'Events',
      'menu.tours': 'Tours',
      'menu.realestate': 'Real Estate',
      'menu.advertising': 'Advertising',
      'menu.education': 'Student',
      'menu.business': 'Business',
      'menu.decoration': 'Decoration',
      'menu.legal': 'Legal',
      'menu.blog': 'Blog',
      'menu.about': 'About',
      'menu.contact': 'Contact',
      'menu.courses': 'Courses',
      'auth.login': 'Login',
      'auth.signup': 'Sign Up',
      'auth.logout': 'Logout',
      'auth.dashboard': 'Dashboard',
      'mainTitle': 'Kanoon Hamyari of Persian Speakers in Turkey',
      'subtitle': 'A social, supportive and comprehensive service hub for Persian speakers in Turkey',
      'aboutTitle': 'About Kanoon Hamyari',
      'goalsTitle': 'Our Goals',
      'ourServices': 'Our Services',
      'events': 'Events',
      'tours': 'Tours',
      'realEstate': 'Real Estate',
      'advertising': 'Advertising',
      'education': 'Education',
      'legal': 'Legal',
      'testimonialsTitle': 'Members’ Testimonials'
    },
    tr: {
      'menu.home': 'Ana Sayfa',
      'menu.events': 'Etkinlikler',
      'menu.tours': 'Turlar',
      'menu.realestate': 'Emlak',
      'menu.advertising': 'Reklam',
      'menu.education': 'Öğrenci',
      'menu.business': 'İş',
      'menu.decoration': 'Dekorasyon',
      'menu.legal': 'Hukuk',
      'menu.blog': 'Blog',
      'menu.about': 'Hakkımızda',
      'menu.contact': 'İletişim',
      'menu.courses': 'Kurslar',
      'auth.login': 'Giriş',
      'auth.signup': 'Kayıt Ol',
      'auth.logout': 'Çıkış',
      'auth.dashboard': 'Panel',
      'mainTitle': 'Türkiye’deki Farsça Konuşanların Dayanışma Derneği',
      'subtitle': 'Türkiye’deki Farsça konuşanlar için sosyal, destekleyici ve kapsamlı bir hizmet merkezi',
      'aboutTitle': 'Kanoon Hamyari Hakkında',
      'goalsTitle': 'Hedeflerimiz',
      'ourServices': 'Hizmetlerimiz',
      'events': 'Etkinlikler',
      'tours': 'Turlar',
      'realEstate': 'Emlak',
      'advertising': 'Reklam',
      'education': 'Eğitim',
      'legal': 'Hukuk',
      'testimonialsTitle': 'Üye Yorumları'
    }
  };

  function setHtmlDir(lang) {
    var html = document.documentElement;
    html.setAttribute('lang', lang);
    html.setAttribute('dir', lang === 'fa' ? 'rtl' : 'ltr');
  }

  function translateElements(lang) {
    var dict = translations[lang] || translations.fa;
    // Elements using data-i18n
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });
    // Elements using older data-translate keys
    document.querySelectorAll('[data-translate]').forEach(function (el) {
      var key = el.getAttribute('data-translate');
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });
  }

  // DISABLED: Don't override Django translations
  // Use Django's set_language view instead via fast_language_switch.js
  /*
  window.switchLanguage = function (lang) {
    if (!translations[lang]) lang = 'fa';
    localStorage.setItem('selectedLanguage', lang);
    setHtmlDir(lang);
    translateElements(lang);
  };
  */
  
  // Keep a dummy function to prevent errors if other code calls it
  window.switchLanguage = function (lang) {
    // Do nothing - let Django handle translations
    console.log('switchLanguage called but disabled - using Django i18n instead');
  };

  // DISABLED: Let Django i18n handle translations instead of overriding them
  // This was causing menu items to be forced to Persian after Django had already translated them
  /*
  document.addEventListener('DOMContentLoaded', function () {
    var initial = localStorage.getItem('selectedLanguage') || 'fa';
    setHtmlDir(initial);
    translateElements(initial);
  });
  */
})();





