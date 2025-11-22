(function () {
    function ensureNavCss() {
        var existingById = document.getElementById('kh-nav-css');
        var existingByHref = Array.prototype.find.call(
            document.querySelectorAll('link[rel="stylesheet"]'),
            function (lnk) { return /\bcss\/nav\.css$/i.test(lnk.getAttribute('href') || ''); }
        );
        if (!existingById && !existingByHref) {
            var link = document.createElement('link');
            link.id = 'kh-nav-css';
            link.rel = 'stylesheet';
            link.href = 'css/nav.css';
            document.head.appendChild(link);
        }
    }

    function normalizePath(pathname) {
        if (!pathname) return '/';
        var normalized = pathname.split('?')[0].replace(/\/+$/, '');
        return normalized || '/';
    }

    function highlightActiveLinks() {
        var currentPath = normalizePath(window.location.pathname);
        var selectors = ['#navigation a', '#khMobileNavigation a'];

        selectors.forEach(function (selector) {
            document.querySelectorAll(selector).forEach(function (link) {
                var href = link.getAttribute('href');
                if (!href || href.charAt(0) === '#' || href.indexOf('tel:') === 0 || href.indexOf('mailto:') === 0) {
                    return;
                }

                var linkPath;
                try {
                    linkPath = normalizePath(new URL(href, window.location.origin).pathname);
                } catch (err) {
                    linkPath = normalizePath(href);
                }

                var isActive = false;
                if (linkPath === '/') {
                    isActive = currentPath === '/';
                } else if (currentPath === linkPath || currentPath.indexOf(linkPath + '/') === 0) {
                    isActive = true;
                }

                if (isActive) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        });
    }

    function cloneDesktopNavigation() {
        var desktopNav = document.getElementById('navigation');
        var mobileNav = document.getElementById('khMobileNavigation');
        if (desktopNav && mobileNav) {
            mobileNav.innerHTML = desktopNav.innerHTML;
        }
    }

    function initLanguageDropdown() {
        var languageBtn = document.getElementById('languageBtn');
        var languageDropdown = document.getElementById('languageDropdown');
        var currentLang = document.getElementById('currentLang');
        var savedLanguage = localStorage.getItem('selectedLanguage') || 'fa';

        if (currentLang) {
            currentLang.textContent = savedLanguage === 'fa' ? 'فا' : savedLanguage.toUpperCase();
        }

        var languageOptions = document.querySelectorAll('.language-option');
        languageOptions.forEach(function (option) {
            option.classList.toggle('active', option.getAttribute('data-lang') === savedLanguage);
        });

        if (languageBtn && languageDropdown) {
            languageBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                languageDropdown.classList.toggle('show');
                languageBtn.classList.toggle('active');
            });

            document.addEventListener('click', function (e) {
                if (!languageBtn.contains(e.target) && !languageDropdown.contains(e.target)) {
                    languageDropdown.classList.remove('show');
                    languageBtn.classList.remove('active');
                }
            });

            languageOptions.forEach(function (option) {
                option.addEventListener('click', function (e) {
                    e.preventDefault();
                    var selectedLang = this.getAttribute('data-lang');

                    languageOptions.forEach(function (opt) { opt.classList.remove('active'); });
                    this.classList.add('active');
                    languageDropdown.classList.remove('show');
                    languageBtn.classList.remove('active');

                    if (currentLang) {
                        currentLang.textContent = selectedLang === 'fa' ? 'فا' : selectedLang.toUpperCase();
                    }

                    if (typeof window.switchLanguage === 'function') {
                        window.switchLanguage(selectedLang);
                    } else {
                        localStorage.setItem('selectedLanguage', selectedLang);
                    }
                });
            });
        }
    }

    function initMobileMenu() {
        var hamburger = document.getElementById('khHamburger');
        var mobileNav = document.getElementById('khMobileNav');
        var overlay = document.getElementById('khMobileOverlay');

        if (!hamburger || !mobileNav || !overlay) return;

        function closeMobile() {
            document.body.classList.remove('kh-menu-open');
            hamburger.setAttribute('aria-expanded', 'false');
            mobileNav.setAttribute('aria-hidden', 'true');
        }

        function openMobile() {
            document.body.classList.add('kh-menu-open');
            hamburger.setAttribute('aria-expanded', 'true');
            mobileNav.setAttribute('aria-hidden', 'false');
        }

        hamburger.addEventListener('click', function (e) {
            e.stopPropagation();
            if (document.body.classList.contains('kh-menu-open')) {
                closeMobile();
            } else {
                openMobile();
            }
        });

        overlay.addEventListener('click', closeMobile);
        document.addEventListener('keyup', function (e) {
            if (e.key === 'Escape') {
                closeMobile();
            }
        });

        mobileNav.addEventListener('click', function (e) {
            var target = e.target;
            if (target && target.tagName && target.tagName.toLowerCase() === 'a') {
                closeMobile();
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        ensureNavCss();
        var header = document.getElementById('site-header');
        if (!header) {
            return;
        }

        document.body.classList.add('menu-loaded');
        cloneDesktopNavigation();
        initLanguageDropdown();
        highlightActiveLinks();
        initMobileMenu();
    });
})();
