/**
 * Authentication Pages specific JavaScript
 */
(function() {
    function getResponsiveButtonWidth() {
        var container = document.getElementById('google-btn-container');
        if (!container) return 300;
        var isRegister = window.location.pathname.includes('register');
        var maxWidth = isRegister ? 400 : 384;
        var availableWidth = container.offsetWidth || (window.innerWidth - 64);
        return Math.max(240, Math.min(maxWidth, availableWidth));
    }

    function setGoogleBtnWidth() {
        var btn = document.getElementById('g_id_signin_btn');
        if (btn) {
            btn.setAttribute('data-width', getResponsiveButtonWidth());
        }
    }
    setGoogleBtnWidth();
    
    var resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            setGoogleBtnWidth();
            // Re-render the button on resize
            if (window.google && window.google.accounts) {
                var btn = document.getElementById('g_id_signin_btn');
                if (btn) {
                    var isRegister = window.location.pathname.includes('register');
                    var textType = isRegister ? 'signup_with' : 'signin_with';
                    var width = getResponsiveButtonWidth();
                    var theme = window.innerWidth >= 1024 ? 'outline' : 'filled_black';

                    btn.innerHTML = '';
                    google.accounts.id.renderButton(btn, {
                        type: 'standard', shape: 'pill', theme: theme,
                        text: textType, size: 'large', logo_alignment: 'left',
                        width: width
                    });
                }
            }
        }, 150);
    });

    // Make toggleBarangay globally available for the register page
    window.toggleBarangay = function(input) {
        const section = document.getElementById('barangay-section');
        const select = document.getElementById('barangay-select');
        if (input.value === 'contributor') {
            section.classList.remove('hidden');
            section.classList.add('animate-fade-in');
            select.required = true;
        } else {
            section.classList.add('hidden');
            section.classList.remove('animate-fade-in');
            select.required = false;
        }
    };

    // Password toggle functionality
    document.querySelectorAll('.toggle-password').forEach(function(button) {
        button.addEventListener('click', function() {
            var input = this.parentElement.querySelector('input');
            if (input && input.type === 'password') {
                input.type = 'text';
                this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>';
            } else if (input) {
                input.type = 'password';
                this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>';
            }
        });
    });
})();
