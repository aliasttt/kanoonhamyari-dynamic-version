/**
 * Fast Language Switching without full page reload
 */
(function() {
    'use strict';

    // Show loading indicator
    function showLoading() {
        const loader = document.getElementById('languageLoader');
        if (loader) {
            loader.style.display = 'flex';
        } else {
            // Create loader if doesn't exist
            const newLoader = document.createElement('div');
            newLoader.id = 'languageLoader';
            newLoader.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:99999;display:flex;align-items:center;justify-content:center;';
            newLoader.innerHTML = '<div style="background:white;padding:20px;border-radius:8px;"><div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div></div>';
            document.body.appendChild(newLoader);
        }
    }

    // Hide loading indicator
    function hideLoading() {
        const loader = document.getElementById('languageLoader');
        if (loader) {
            loader.style.display = 'none';
        }
    }

    // Get CSRF token from multiple sources
    function getCSRFToken(formId) {
        // Try from mobile form first if specified
        if (formId === 'mobileLanguageForm') {
            const mobileFormToken = document.querySelector('#mobileLanguageForm [name=csrfmiddlewaretoken]');
            if (mobileFormToken && mobileFormToken.value) {
                return mobileFormToken.value;
            }
        }
        
        // Try from desktop form input (most reliable)
        const formToken = document.querySelector('#languageForm [name=csrfmiddlewaretoken]');
        if (formToken && formToken.value) {
            return formToken.value;
        }
        
        // Try from meta tag
        const metaToken = document.querySelector('meta[name=csrf-token]');
        if (metaToken) {
            const content = metaToken.getAttribute('content');
            if (content && content.trim()) {
                return content.trim();
            }
        }
        
        // Try from cookie (Django sets this)
        const cookieMatch = document.cookie.match(/csrftoken=([^;]+)/);
        if (cookieMatch && cookieMatch[1]) {
            return decodeURIComponent(cookieMatch[1]);
        }
        
        return null;
    }

    // Fast language switch using form submit (more reliable than AJAX)
    function switchLanguageFast(lang, formId) {
        // Try mobile form first, then desktop form
        const form = document.getElementById(formId || 'mobileLanguageForm') || document.getElementById('languageForm');
        if (!form) {
            console.error('Language form not found');
            return;
        }
        
        // Show loading indicator
        showLoading();
        
        // Update the next field to current path
        const nextInput = form.querySelector('input[name="next"]');
        if (nextInput) {
            nextInput.value = window.location.pathname + window.location.search;
        }
        
        // Create a hidden input for language if it doesn't exist
        let langInput = form.querySelector('input[name="language"]');
        if (!langInput) {
            langInput = document.createElement('input');
            langInput.type = 'hidden';
            langInput.name = 'language';
            form.appendChild(langInput);
        }
        langInput.value = lang;
        
        // Submit the form
        form.submit();
    }

    // Handle language button click with event delegation
    function handleLanguageClick(e) {
        const target = e.target.closest('.language-choice');
        if (!target) return;
        
        e.preventDefault();
        e.stopPropagation();
        
        const lang = target.value || target.getAttribute('data-lang');
        if (!lang) return;
        
        // Update UI immediately
        const currentLang = document.getElementById('currentLang');
        if (currentLang) {
            currentLang.textContent = lang === 'fa' ? 'فا' : lang.toUpperCase();
        }
        
        // Remove active class from all buttons (both desktop and mobile)
        document.querySelectorAll('.language-choice').forEach(btn => btn.classList.remove('active'));
        target.classList.add('active');
        
        // Close dropdown if exists
        const dropdown = document.getElementById('languageDropdown');
        if (dropdown) {
            dropdown.classList.remove('show');
        }
        const btn = document.getElementById('languageBtn');
        if (btn) {
            btn.classList.remove('active');
        }
        
        // Close mobile menu if open
        if (document.body.classList.contains('kh-menu-open')) {
            document.body.classList.remove('kh-menu-open');
        }
        
        // Determine which form to use
        const isMobile = target.closest('#khMobileNav') || target.closest('#mobileLanguageForm');
        const formId = isMobile ? 'mobileLanguageForm' : 'languageForm';
        
        // Switch language
        switchLanguageFast(lang, formId);
    }

    // Initialize on DOM ready with event delegation
    document.addEventListener('DOMContentLoaded', function() {
        // Use event delegation to handle clicks on all language buttons (including dynamically added ones)
        document.addEventListener('click', handleLanguageClick);
    });
})();

