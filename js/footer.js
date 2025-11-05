(function () {
    function ensureFooterCss() {
        if (!document.getElementById('kh-footer-css')) {
            var link = document.createElement('link');
            link.id = 'kh-footer-css';
            link.rel = 'stylesheet';
            link.href = 'css/footer.css';
            document.head.appendChild(link);
        }
    }

    function buildUnifiedFooter() {
        var footer = document.querySelector('footer') || document.createElement('footer');
        footer.classList.add('footer', 'kh-footer');

        var instagramUrl = 'https://www.instagram.com/kanoon.hamyari';
        var telegramUrl = 'https://t.me/KANOONEHAMYARI';
        var youtubeUrl = 'https://m.youtube.com/@kanoonhamyari';

        footer.innerHTML = '' +
            '<div class="kh-footer__top">' +
            '  <div class="container">' +
            '    <div class="row">' +
            '      <div class="col-xl-4 col-md-6">' +
            '        <div class="kh-footer__about">' +
            '          <a href="index.html" class="kh-footer__logo">' +
            '            <img src="img/logo.png" alt="کانون همیاری" onerror="this.src=\'static/img/kanoonlogo.jpg\'">' +
            '          </a>' +
            '          <p data-translate="aboutDesc">کانون همیاری ارائه‌دهنده خدمات جامع در زمینه رویدادها، تورها، املاک، تبلیغات، تحصیلی و امور حقوقی</p>' +
            '          <div class="kh-footer__social">' +
            '            <a href="' + instagramUrl + '" target="_blank" aria-label="Instagram"><i class="fa fa-instagram"></i></a>' +
            '            <a href="' + telegramUrl + '" target="_blank" aria-label="Telegram"><i class="fa fa-telegram"></i></a>' +
            '            <a href="' + youtubeUrl + '" target="_blank" aria-label="YouTube"><i class="fa fa-youtube-play"></i></a>' +
            '          </div>' +
            '        </div>' +
            '      </div>' +
            '      <div class="col-xl-3 col-sm-6">' +
            '        <div class="kh-footer__widget">' +
            '          <h4 data-translate="quickLinks">لینک‌های سریع</h4>' +
            '          <ul class="kh-list kh-list--grid">' +
            '            <li><a href="index.html"><i class="fa fa-angle-left"></i> <span data-translate="home">خانه</span></a></li>' +
            '            <li><a href="events.html"><i class="fa fa-angle-left"></i> <span data-translate="events">رویدادها</span></a></li>' +
            '            <li><a href="tours.html"><i class="fa fa-angle-left"></i> <span data-translate="tours">تورها</span></a></li>' +
            '            <li><a href="real-estate.html"><i class="fa fa-angle-left"></i> <span data-translate="realEstate">املاک</span></a></li>' +
            '            <li><a href="advertising.html"><i class="fa fa-angle-left"></i> <span data-translate="advertising">تبلیغات</span></a></li>' +
            '            <li><a href="education.html"><i class="fa fa-angle-left"></i> <span data-translate="education">تحصیلی</span></a></li>' +
            '            <li><a href="business.html"><i class="fa fa-angle-left"></i> <span data-translate="business">بیزینس</span></a></li>' +
            '            <li><a href="decoration.html"><i class="fa fa-angle-left"></i> <span data-translate="decoration">دکوراسیون</span></a></li>' +
            '            <li><a href="legal.html"><i class="fa fa-angle-left"></i> <span data-translate="legal">امور حقوقی</span></a></li>' +
            '            <li><a href="contact.html"><i class="fa fa-angle-left"></i> <span data-translate="contact">تماس</span></a></li>' +
            '          </ul>' +
            '        </div>' +
            '      </div>' +
            '      <div class="col-xl-2 col-sm-6">' +
            '        <div class="kh-footer__widget">' +
            '          <h4 data-translate="services">خدمات</h4>' +
            '          <ul class="kh-list">' +
            '            <li><a href="real-estate.html"><i class="fa fa-home"></i> <span data-translate="realEstate">املاک</span></a></li>' +
            '            <li><a href="legal.html"><i class="fa fa-balance-scale"></i> <span data-translate="legal">امور حقوقی</span></a></li>' +
            '            <li><a href="education.html"><i class="fa fa-graduation-cap"></i> <span data-translate="education">تحصیلی</span></a></li>' +
            '            <li><a href="advertising.html"><i class="fa fa-bullhorn"></i> <span data-translate="advertising">تبلیغات</span></a></li>' +
            '            <li><a href="tours.html"><i class="fa fa-suitcase"></i> <span data-translate="tours">تورها</span></a></li>' +
            '            <li><a href="events.html"><i class="fa fa-calendar"></i> <span data-translate="events">رویدادها</span></a></li>' +
            '          </ul>' +
            '        </div>' +
            '      </div>' +
            '      <div class="col-xl-3 col-md-6">' +
            '        <div class="kh-footer__widget">' +
            '          <h4 data-translate="contactInfo">اطلاعات تماس</h4>' +
            '          <ul class="kh-contact">' +
            '            <li><i class="fa fa-map-marker"></i><span data-translate="address">ترکیه، استانبول، بیلیکدوزو، مرکز خرید بیلیسیوم، طبقه ۴</span></li>' +
            '            <li><i class="fa fa-phone"></i><a href="tel:+905525612221">+90 552 561 22 21</a></li>' +
            '            <li><i class="fa fa-phone"></i><a href="tel:+905551433288">+90 555 143 32 88</a></li>' +
            '            <li><i class="fa fa-phone"></i><a href="tel:+905373303440">+90 537 330 34 40</a></li>' +
            '            <li><i class="fa fa-envelope"></i><a href="mailto:info@kanoonhamyari.com">info@kanoonhamyari.com</a></li>' +
            '          </ul>' +
            '        </div>' +
            '      </div>' +
            '    </div>' +
            '  </div>' +
            '</div>' +
            '<div class="kh-footer__bottom">' +
            '  <div class="container">' +
            '    <div class="row align-items-center">' +
            '      <div class="col-lg-6">' +
            '        <p data-translate="copyright">تمام حقوق محفوظ است © <span id="kh-year"></span> کانون همیاری</p>' +
            '      </div>' +
            '      <div class="col-lg-6">' +
            '        <div class="kh-footer__bottom-links">' +
            '          <a href="sitemap.xml" data-translate="sitemap">نقشه سایت</a>' +
            '          <a href="robots.txt" data-translate="robots">ربات‌ها</a>' +
            '        </div>' +
            '      </div>' +
            '    </div>' +
            '  </div>' +
            '</div>';

        if (!footer.parentNode) {
            document.body.appendChild(footer);
        }

        var y = document.getElementById('kh-year');
        if (y) y.textContent = new Date().getFullYear();
    }

    document.addEventListener('DOMContentLoaded', function () {
        ensureFooterCss();
        buildUnifiedFooter();
    });
})();


