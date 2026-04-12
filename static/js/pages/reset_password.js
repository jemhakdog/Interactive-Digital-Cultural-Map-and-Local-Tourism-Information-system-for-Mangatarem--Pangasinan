// Password validation for reset_password.html
(function() {
    'use strict';

    function initPasswordValidation() {
        const passwordInput = document.getElementById('password');
        const confirmInput = document.getElementById('confirm_password');
        const mismatchMsg = document.getElementById('mismatch-msg');
        const submitBtn = document.getElementById('submit-btn');
        const reqLength = document.getElementById('req-length');
        const reqMatch = document.getElementById('req-match');

        if (!passwordInput || !confirmInput || !submitBtn) return;

        function updateRequirements() {
            const pw = passwordInput.value;
            const confirm = confirmInput.value;
            const lengthOk = pw.length >= 8;
            const matchOk = pw === confirm && confirm.length > 0;

            // Update length requirement
            const lengthIcon = reqLength.querySelector('.req-icon');
            if (lengthIcon) {
                lengthIcon.textContent = lengthOk ? '✓' : '✗';
                reqLength.classList.toggle('text-emerald-400', lengthOk);
                reqLength.classList.toggle('text-red-500', !lengthOk);
            }

            // Update match requirement
            const matchIcon = reqMatch.querySelector('.req-icon');
            if (matchIcon) {
                matchIcon.textContent = matchOk ? '✓' : '✗';
                reqMatch.classList.toggle('text-emerald-400', matchOk);
                reqMatch.classList.toggle('text-red-500', !matchOk);
            }

            if (mismatchMsg) {
                mismatchMsg.classList.toggle('hidden', matchOk || confirm.length === 0);
            }
            
            submitBtn.disabled = !(lengthOk && matchOk);
        }

        passwordInput.addEventListener('input', updateRequirements);
        confirmInput.addEventListener('input', updateRequirements);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPasswordValidation);
    } else {
        initPasswordValidation();
    }
})();
