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
            // Clear mobile nav first
            mobileNav.innerHTML = '';
            
            // Clone each menu item to preserve translations
            var items = desktopNav.querySelectorAll('li');
            items.forEach(function(item) {
                var clonedItem = item.cloneNode(true);
                mobileNav.appendChild(clonedItem);
            });
            
            // Add Language Section
            var languageSection = document.createElement('div');
            languageSection.className = 'mobile-language-section';
            var langTitle = document.createElement('h3');
            langTitle.textContent = 'زبان'; // Will be translated by Django
            langTitle.setAttribute('data-i18n', 'menu.language');
            languageSection.appendChild(langTitle);
            
            var languageForm = document.getElementById('languageForm');
            if (languageForm) {
                var clonedForm = languageForm.cloneNode(true);
                clonedForm.id = 'mobileLanguageForm';
                clonedForm.style.cssText = 'display: flex; flex-direction: column; gap: 8px; padding: 0 16px;';
                clonedForm.querySelectorAll('button').forEach(function(btn) {
                    btn.style.cssText = 'padding: 12px 16px; font-size: 14px; border-radius: 8px; background: rgba(255, 107, 53, 0.2); border: 1px solid rgba(255, 107, 53, 0.3); color: white; cursor: pointer; text-align: right; width: 100%;';
                    if (btn.classList.contains('active')) {
                        btn.style.background = 'linear-gradient(135deg, #ff6b35, #ff8533)';
                    }
                });
                languageSection.appendChild(clonedForm);
            }
            mobileNav.appendChild(languageSection);
            
            // Add Auth Section
            var authSection = document.createElement('div');
            authSection.className = 'mobile-auth-section';
            var authTitle = document.createElement('h3');
            authTitle.textContent = 'حساب کاربری'; // Will be translated by Django
            authTitle.setAttribute('data-i18n', 'menu.account');
            authSection.appendChild(authTitle);
            
            var authLinks = document.querySelector('.auth_links');
            if (authLinks) {
                var authLinksClone = authLinks.cloneNode(true);
                authLinksClone.style.cssText = 'display: flex; flex-direction: column; gap: 8px; padding: 0 16px;';
                authLinksClone.querySelectorAll('a').forEach(function(link) {
                    link.style.cssText = 'display: block; padding: 12px 16px; font-size: 14px; border-radius: 8px; text-align: center; text-decoration: none; width: 100%; box-sizing: border-box;';
                });
                authSection.appendChild(authLinksClone);
                mobileNav.appendChild(authSection);
            }
        }
    }

    function initLanguageDropdown() {
        var languageBtn = document.getElementById('languageBtn');
        var languageDropdown = document.getElementById('languageDropdown');
        var currentLang = document.getElementById('currentLang');

        if (languageBtn && languageDropdown) {
            languageBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                e.preventDefault();
                languageDropdown.classList.toggle('show');
                languageBtn.classList.toggle('active');
            });

            document.addEventListener('click', function (e) {
                if (!languageBtn.contains(e.target) && !languageDropdown.contains(e.target)) {
                    languageDropdown.classList.remove('show');
                    languageBtn.classList.remove('active');
                }
            });
            
            // Handle language choice clicks
            var languageChoices = document.querySelectorAll('.language-choice');
            languageChoices.forEach(function(choice) {
                choice.addEventListener('click', function(e) {
                    e.stopPropagation();
                    // Let fast_language_switch.js handle the actual switching
                });
            });

            languageOptions.forEach(function (option) {
                option.addEventListener('click', function (e) {
                    var isChoiceButton = this.classList.contains('language-choice');
                    var selectedLang = this.getAttribute('data-lang') || this.value;
                    if (!selectedLang) return;

                    // For custom anchors, handle client-side; for buttons, let form submit to Django
                    if (!isChoiceButton) {
                        e.preventDefault();
                        languageOptions.forEach(function (opt) { opt.classList.remove('active'); });
                        this.classList.add('active');
                        languageDropdown.classList.remove('show');
                        languageBtn.classList.remove('active');
                        // DISABLED: Don't override Django translations
                        // Let fast_language_switch.js handle language switching
                        /*
                        if (currentLang) {
                            currentLang.textContent = selectedLang === 'fa' ? 'فا' : selectedLang.toUpperCase();
                        }
                        if (typeof window.switchLanguage === 'function') {
                            window.switchLanguage(selectedLang);
                        } else {
                            localStorage.setItem('selectedLanguage', selectedLang);
                        }
                        */
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
