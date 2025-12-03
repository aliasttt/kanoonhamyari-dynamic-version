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

    // Fast language switch using AJAX
    function switchLanguageFast(lang) {
        showLoading();
        
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                         document.cookie.match(/csrftoken=([^;]+)/)?.[1];
        
        // Get current path
        const currentPath = window.location.pathname + window.location.search;
        
        // Create form data
        const formData = new FormData();
        formData.append('language', lang);
        formData.append('next', currentPath);
        if (csrfToken) {
            formData.append('csrfmiddlewaretoken', csrfToken);
        }
        
        // Send AJAX request
        fetch('/i18n/setlang/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken || '',
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                // Reload only the content, not full page
                return response.text();
            }
            throw new Error('Language switch failed');
        })
        .then(() => {
            // Quick reload without cache to get new language
            window.location.reload(true);
        })
        .catch(error => {
            console.error('Language switch error:', error);
            hideLoading();
            // Fallback to normal form submit
            const form = document.querySelector('form[action*="setlang"]');
            if (form) {
                const langInput = form.querySelector(`button[name="language"][value="${lang}"]`);
                if (langInput) {
                    langInput.click();
                }
            }
        });
    }

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        const languageButtons = document.querySelectorAll('.language-choice');
        
        languageButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const lang = this.value || this.getAttribute('data-lang');
                if (lang) {
                    // Update UI immediately
                    const currentLang = document.getElementById('currentLang');
                    if (currentLang) {
                        currentLang.textContent = lang === 'fa' ? 'فا' : lang.toUpperCase();
                    }
                    
                    // Remove active class from all buttons
                    languageButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Close dropdown
                    const dropdown = document.getElementById('languageDropdown');
                    if (dropdown) {
                        dropdown.classList.remove('show');
                    }
                    const btn = document.getElementById('languageBtn');
                    if (btn) {
                        btn.classList.remove('active');
                    }
                    
                    // Switch language
                    switchLanguageFast(lang);
                }
            });
        });
    });
})();

