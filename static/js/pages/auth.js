/**
 * Authentication Pages specific JavaScript
 */
(function() {
    function setGoogleBtnWidth() {
        var container = document.getElementById('google-btn-container');
        var btn = document.getElementById('g_id_signin_btn');
        if (container && btn) {
            // Check if we are on the login or register page to set max width appropriately
            // Login typically uses max 384, register max 400
            var isRegister = window.location.pathname.includes('register');
            var maxWidth = isRegister ? 400 : 384;
            var w = Math.min(maxWidth, container.offsetWidth);
            btn.setAttribute('data-width', w);
        }
    }
    setGoogleBtnWidth();
    
    window.addEventListener('resize', function() {
        setGoogleBtnWidth();
        // Re-render the button on resize
        if (window.google && window.google.accounts) {
            var btn = document.getElementById('g_id_signin_btn');
            if (btn) {
                var isRegister = window.location.pathname.includes('register');
                var textType = isRegister ? 'signup_with' : 'signin_with';
                var containerWidth = document.getElementById('google-btn-container').offsetWidth;
                var width = Math.min(isRegister ? 400 : 384, containerWidth);

                btn.innerHTML = '';
                google.accounts.id.renderButton(btn, {
                    type: 'standard', shape: 'pill', theme: 'filled_black',
                    text: textType, size: 'large', logo_alignment: 'left',
                    width: width
                });
            }
        }
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
})();
