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

    function buildUnifiedHeader() {
        var headerPlaceholder = document.getElementById('header-placeholder');
        if (!headerPlaceholder) {
            // If placeholder not present, try to reuse existing header
            var existingHeader = document.querySelector('body > header');
            if (existingHeader) {
                headerPlaceholder = existingHeader;
                if (!headerPlaceholder.id) headerPlaceholder.id = 'header-placeholder';
            } else {
                // Fallback: inject at top of body
                headerPlaceholder = document.createElement('header');
                headerPlaceholder.id = 'header-placeholder';
                var firstChild = document.body.firstChild;
                document.body.insertBefore(headerPlaceholder, firstChild);
            }
        }
        
        // Clear any old content inside or after the header
        headerPlaceholder.innerHTML = '';
        
        // Remove any old header content after placeholder (divs with header classes, row, container, etc.)
        var nextSibling = headerPlaceholder.nextSibling;
        while (nextSibling) {
            var shouldRemove = false;
            if (nextSibling.nodeType === 1) {
                var tagName = nextSibling.tagName ? nextSibling.tagName.toLowerCase() : '';
                var className = nextSibling.className ? nextSibling.className.toString() : '';
                if (tagName === 'header' || 
                    tagName === 'div' && (className.includes('header') || className.includes('brand_tools') || 
                                          className.includes('navigation') || className.includes('row align-items-center') || 
                                          className.includes('container') || className.includes('main-menu') || 
                                          className.includes('header_bottom_border') || className.includes('mobile_menu'))) {
                    shouldRemove = true;
                }
            } else if (nextSibling.nodeType === 3 && (!nextSibling.textContent || !nextSibling.textContent.trim())) {
                shouldRemove = true;
            }
            
            if (shouldRemove) {
                var toRemove = nextSibling;
                nextSibling = nextSibling.nextSibling;
                toRemove.remove();
            } else {
                break;
            }
        }

        var logoSrc = 'img/logo.png';
        var path = window.location.pathname || '';
        var page = path.split('/').pop();
        if (!page || /^(index\.html)?$/i.test(page)) {
            logoSrc = 'static/img/kanoonlogo.jpg';
        }

        headerPlaceholder.innerHTML = 
            '<div class="header-area">\n' +
            '  <div id="sticky-header" class="main-header-area">\n' +
            '    <div class="container">\n' +
            '      <div class="header_bottom_border">\n' +
            '        <div class="row align-items-center">\n' +
            '          <div class="col-xl-3 col-lg-3">\n' +
            '            <div class="brand_tools">\n' +
            '              <button class="kh-hamburger d-lg-none" id="khHamburger" aria-label="Toggle navigation" aria-expanded="false">\n' +
            '                <i class="fa fa-bars"></i>\n' +
            '              </button>\n' +
            '              <div class="logo">\n' +
            '                <a href="index.html">\n' +
            '                  <img src="' + logoSrc + '" alt="کانون همیاری">\n' +
            '                </a>\n' +
            '              </div>\n' +
            '              <div class="language_dropdown">\n' +
            '                <button class="language_dropdown_btn" id="languageBtn">\n' +
            '                  <span id="currentLang">فا</span>\n' +
            '                  <i class="fa fa-chevron-down"></i>\n' +
            '                </button>\n' +
            '                <div class="language_dropdown_content" id="languageDropdown">\n' +
            '                  <a href="#" class="language-option" data-lang="fa">فارسی</a>\n' +
            '                  <a href="#" class="language-option" data-lang="en">English</a>\n' +
            '                  <a href="#" class="language-option" data-lang="tr">Türkçe</a>\n' +
            '                </div>\n' +
            '              </div>\n' +
            '            </div>\n' +
            '          </div>\n' +
            '          <div class="col-xl-9 col-lg-9">\n' +
            '            <div class="main-menu d-none d-lg-block">\n' +
            '              <nav>\n' +
            '                <ul id="navigation">\n' +
            '                  <li><a href="index.html" data-translate="home">خانه</a></li>\n' +
            '                  <li><a href="events.html" data-translate="events">رویدادها</a></li>\n' +
            '                  <li><a href="tours.html" data-translate="tours">تورها</a></li>\n' +
            '                  <li><a href="real-estate.html" data-translate="realEstate">املاک</a></li>\n' +
            '                  <li><a href="advertising.html" data-translate="advertising">تبلیغات</a></li>\n' +
            '                  <li><a href="education.html" data-translate="educationMenu">دانشجویی</a></li>\n' +
            '                  <li><a href="business.html" data-translate="business">بیزینس</a></li>\n' +
            '                  <li><a href="decoration.html" data-translate="decoration">دکوراسیون</a></li>\n' +
            '                  <li><a href="legal.html" data-translate="legalMenu">حقوقی</a></li>\n' +
            '                  <li><a href="about.html" data-translate="about">درباره ما</a></li>\n' +
            '                  <li><a href="contact.html" data-translate="contact">تماس</a></li>\n' +
            '                </ul>\n' +
            '              </nav>\n' +
            '            </div>\n' +
            '          </div>\n' +
            '          <div class="col-12"></div>\n' +
            '        </div>\n' +
            '      </div>\n' +
            '    </div>\n' +
            '  </div>\n' +
            '</div>';

        // inject mobile nav + overlay right after header
        var mobileNav = document.createElement('nav');
        mobileNav.className = 'kh-mobile-nav';
        mobileNav.id = 'khMobileNav';
        mobileNav.setAttribute('aria-hidden', 'true');
        mobileNav.innerHTML = '<ul id="khMobileNavigation"></ul>';
        headerPlaceholder.appendChild(mobileNav);

        var overlay = document.createElement('div');
        overlay.className = 'kh-mobile-overlay';
        overlay.id = 'khMobileOverlay';
        headerPlaceholder.appendChild(overlay);

        initializeHeaderScripts();
    }

    function initializeHeaderScripts() {
        // Mark menu loaded (FOUC prevention works with nav.css)
        document.body.classList.add('menu-loaded');

        var languageBtn = document.getElementById('languageBtn');
        var languageDropdown = document.getElementById('languageDropdown');
        var currentLang = document.getElementById('currentLang');
        var languageOptions = document.querySelectorAll('.language-option');

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
                    if (currentLang) {
                        currentLang.textContent = selectedLang === 'fa' ? 'فا' : selectedLang.toUpperCase();
                    }
                    languageOptions.forEach(function (opt) { opt.classList.remove('active'); });
                    this.classList.add('active');
                    languageDropdown.classList.remove('show');
                    languageBtn.classList.remove('active');
                    if (typeof window.switchLanguage === 'function') {
                        window.switchLanguage(selectedLang);
                    }
                });
            });

            var activeOption = document.querySelector('.language-option[data-lang="fa"]');
            if (activeOption) activeOption.classList.add('active');
        }

        // Set active menu item based on current page
        var currentPage = window.location.pathname.split('/').pop() || 'index.html';
        var menuLinks = document.querySelectorAll('#navigation a');
        menuLinks.forEach(function (link) {
            var href = link.getAttribute('href');
            if (href === currentPage || (!currentPage && href === 'index.html')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // Build mobile navigation (clone desktop items)
        var desktopNav = document.getElementById('navigation');
        var mobileList = document.getElementById('khMobileNavigation');
        if (desktopNav && mobileList) {
            mobileList.innerHTML = desktopNav.innerHTML;
            // set active on mobile too
            mobileList.querySelectorAll('a').forEach(function (a) {
                var href = a.getAttribute('href');
                if (href === currentPage || (!currentPage && href === 'index.html')) {
                    a.classList.add('active');
                }
            });
        }

        // Hamburger toggle behavior
        var hamburger = document.getElementById('khHamburger');
        var mobileNavEl = document.getElementById('khMobileNav');
        var overlayEl = document.getElementById('khMobileOverlay');
        function closeMobile() {
            document.body.classList.remove('kh-menu-open');
            if (hamburger) hamburger.setAttribute('aria-expanded', 'false');
            if (mobileNavEl) mobileNavEl.setAttribute('aria-hidden', 'true');
        }
        function openMobile() {
            document.body.classList.add('kh-menu-open');
            if (hamburger) hamburger.setAttribute('aria-expanded', 'true');
            if (mobileNavEl) mobileNavEl.setAttribute('aria-hidden', 'false');
        }
        if (hamburger && mobileNavEl && overlayEl) {
            hamburger.addEventListener('click', function (e) {
                e.stopPropagation();
                if (document.body.classList.contains('kh-menu-open')) {
                    closeMobile();
                } else {
                    openMobile();
                }
            });
            overlayEl.addEventListener('click', closeMobile);
            document.addEventListener('keyup', function (e) { if (e.key === 'Escape') closeMobile(); });
            // close after clicking a link
            mobileNavEl.addEventListener('click', function (e) {
                var t = e.target;
                if (t && t.tagName && t.tagName.toLowerCase() === 'a') closeMobile();
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        ensureNavCss();
        buildUnifiedHeader();
    });
})();
