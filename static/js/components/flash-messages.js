/**
 * Flash Message Handler
 * Displays SweetAlert2 toasts/modals from server-rendered JSON data
 */
document.addEventListener('DOMContentLoaded', function () {
    const flashDataElement = document.getElementById('flash-messages-data');
    if (flashDataElement) {
        try {
            const messages = JSON.parse(flashDataElement.textContent);
            if (Array.isArray(messages)) {
                messages.forEach(([category, message]) => {
                    if (category === 'error') {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error!',
                            text: message,
                            confirmButtonColor: '#d33'
                        });
                    } else if (category === 'warning') {
                        Swal.fire({
                            icon: 'warning',
                            title: 'Notice',
                            text: message,
                            confirmButtonColor: '#f59e0b'
                        });
                    } else {
                        Swal.fire({
                            toast: true,
                            position: 'top-end',
                            icon: 'success',
                            title: message,
                            showConfirmButton: false,
                            timer: 3000
                        });
                    }
                });
            }
        } catch (e) {
            console.error('Error parsing flash messages', e);
        }
    }
});
