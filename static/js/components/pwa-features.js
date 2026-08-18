/**
 * GoMangatarem PWA Features: Installation HUD and Update Toast Handler
 * 
 * Auto-injects aesthetic floating install prompts and SW update banners
 * without modifying global layout HTML structures directly.
 */
document.addEventListener('DOMContentLoaded', () => {
    let deferredPrompt = null;

    // 1. Dynamic CSS Injection for Premium HUD Aesthetics
    const pwaStyles = document.createElement('style');
    pwaStyles.innerHTML = `
        /* Premium Install HUD Prompt */
        .pwa-install-hud {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: rgba(15, 23, 42, 0.95);
            border: 2px solid #d4af37; /* Gold accent */
            padding: 20px;
            width: 320px;
            color: #e2e8f0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), 0 0 20px rgba(16, 185, 129, 0.1);
            z-index: 100;
            transform: translateY(150px) scale(0.9);
            opacity: 0;
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            gap: 12px;
            pointer-events: none; /* ponytail: hidden HUD must never block the map/sheet underneath */
        }

        .pwa-install-hud.visible {
            transform: translateY(0) scale(1);
            opacity: 1;
            pointer-events: auto;
        }

        @media (max-width: 767px) {
            .pwa-install-hud {
                bottom: 260px; /* clear of the 220px peek sheet + handle */
                left: 16px;
                right: 16px;
                width: auto;
            }
        }

        .pwa-hud-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 8px;
        }

        .pwa-hud-title {
            color: #d4af37;
            font-weight: 800;
            font-size: 0.85rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin: 0;
        }

        .pwa-hud-close {
            background: transparent;
            border: none;
            color: #64748b;
            cursor: pointer;
            font-size: 1.1rem;
            padding: 0;
            transition: color 0.3s;
        }

        .pwa-hud-close:hover {
            color: #ef4444;
        }

        .pwa-hud-body {
            font-size: 0.85rem;
            color: #94a3b8;
            line-height: 1.5;
            margin: 0;
        }

        .pwa-hud-actions {
            display: flex;
            gap: 10px;
            margin-top: 5px;
        }

        .pwa-btn {
            flex: 1;
            padding: 8px 12px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            border-radius: 0; /* Sharp architectural corners */
        }

        .pwa-btn-primary {
            background: #10b981;
            border: 1px solid #10b981;
            color: #022c22;
        }

        .pwa-btn-primary:hover {
            background: #059669;
            border-color: #059669;
            transform: scale(1.03);
        }

        .pwa-btn-secondary {
            background: transparent;
            border: 1px solid #d4af37;
            color: #d4af37;
        }

        .pwa-btn-secondary:hover {
            background: #d4af37;
            color: #0f172a;
        }

        /* SW Update Toast Banner */
        .pwa-update-toast {
            position: fixed;
            bottom: 30px;
            left: 30px;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid #10b981; /* Emerald border */
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 20px;
            color: #e2e8f0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.85rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            z-index: 100;
            transform: translateY(150px);
            opacity: 0;
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .pwa-update-toast.visible {
            transform: translateY(0);
            opacity: 1;
        }

        .pwa-update-btn {
            background: #10b981;
            color: #022c22;
            border: none;
            padding: 6px 12px;
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            cursor: pointer;
            transition: all 0.3s;
        }

        .pwa-update-btn:hover {
            background: #059669;
        }
    `;
    document.head.appendChild(pwaStyles);

    // 2. Inject Install HUD Container into body
    const installContainer = document.createElement('div');
    installContainer.id = 'pwa-install-hud';
    installContainer.className = 'pwa-install-hud';
    installContainer.innerHTML = `
        <div class="pwa-hud-header">
            <h3 class="pwa-hud-title">GoMangatarem App</h3>
            <button class="pwa-hud-close" id="pwa-close-btn" aria-label="Close prompt">×</button>
        </div>
        <p class="pwa-hud-body">Add GoMangatarem to your home screen for quick offline access, maps, and events tracking!</p>
        <div class="pwa-hud-actions">
            <button class="pwa-btn pwa-btn-secondary" id="pwa-dismiss-btn">Not Now</button>
            <button class="pwa-btn pwa-btn-primary" id="pwa-trigger-btn">Install</button>
        </div>
    `;
    document.body.appendChild(installContainer);

    // 3. Inject Update Toast Container into body
    const updateContainer = document.createElement('div');
    updateContainer.id = 'pwa-update-toast';
    updateContainer.className = 'pwa-update-toast';
    updateContainer.innerHTML = `
        <span>A new system update is available with improved Map V2 features!</span>
        <button class="pwa-update-btn" id="pwa-reload-btn">Reload</button>
    `;
    document.body.appendChild(updateContainer);

    const closeBtn = document.getElementById('pwa-close-btn');
    const dismissBtn = document.getElementById('pwa-dismiss-btn');
    const triggerBtn = document.getElementById('pwa-trigger-btn');
    const reloadBtn = document.getElementById('pwa-reload-btn');

    // 4. Capture Install Prompts
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent default mini-infobar
        e.preventDefault();
        // Save trigger event
        deferredPrompt = e;
        
        // Show HUD only if the user hasn't dismissed it in the last 7 days
        const dismissedTime = localStorage.getItem('pwa_hud_dismissed_time');
        const sevenDays = 7 * 24 * 60 * 60 * 1000;
        if (!dismissedTime || (Date.now() - parseInt(dismissedTime) > sevenDays)) {
            setTimeout(() => {
                installContainer.classList.add('visible');
            }, 3000); // Small initial entry delay for premium feel
        }
    });

    const hideHUD = () => {
        installContainer.classList.remove('visible');
    };

    dismissBtn.addEventListener('click', () => {
        hideHUD();
        localStorage.setItem('pwa_hud_dismissed_time', Date.now().toString());
    });

    closeBtn.addEventListener('click', hideHUD);

    triggerBtn.addEventListener('click', async () => {
        if (!deferredPrompt) return;
        hideHUD();
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`PWA Install Prompt outcome: ${outcome}`);
        deferredPrompt = null;
    });

    // 5. Handle SW Updates elegantly
    let newWorker = null;

    if ('serviceWorker' in navigator) {
        // Track updates to controller
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            window.location.reload();
        });

        // Listen for new SW registrations
        navigator.serviceWorker.ready.then(reg => {
            reg.addEventListener('updatefound', () => {
                newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // There's a new SW ready to take over, prompt user
                        updateContainer.classList.add('visible');
                    }
                });
            });
        });
    }

    reloadBtn.addEventListener('click', () => {
        if (newWorker) {
            newWorker.postMessage({ type: 'SKIP_WAITING' });
        } else {
            window.location.reload();
        }
    });
});
