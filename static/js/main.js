document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mainNav = document.getElementById('mainNav');

    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', () => {
            mainNav.classList.toggle('active');
        });
    }

    const notificationBtn = document.getElementById('notificationBtn');
    const notificationDropdown = document.getElementById('notificationDropdown');

    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', () => {
            notificationDropdown.classList.toggle('open');
        });

        document.addEventListener('click', (event) => {
            if (!notificationBtn.contains(event.target) && !notificationDropdown.contains(event.target)) {
                notificationDropdown.classList.remove('open');
            }
        });
    }

    const starRatings = document.querySelectorAll('.star-rating');
    starRatings.forEach((starNode) => {
        const stars = parseFloat(starNode.dataset.stars || '0');
        const percent = Math.max(0, Math.min(stars, 5)) / 5 * 100;
        starNode.style.setProperty('--percent', `${percent}%`);
    });

    const timerNodes = document.querySelectorAll('[data-timer]');
    timerNodes.forEach((timerNode) => {
        let seconds = parseInt(timerNode.dataset.timer, 10);
        const valueNode = timerNode.querySelector('.timer-value');

        const renderTime = () => {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            if (valueNode) {
                valueNode.textContent = `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
            }
        };

        renderTime();
        const interval = setInterval(() => {
            if (seconds <= 0) {
                clearInterval(interval);
                return;
            }
            seconds -= 1;
            renderTime();
        }, 1000);
    });

    const tabButtons = document.querySelectorAll('[data-tab-target]');
    tabButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const target = button.dataset.tabTarget;
            document.querySelectorAll('[data-tab-panel]').forEach((panel) => {
                panel.hidden = panel.dataset.tabPanel !== target;
            });
        });
    });

    const modalButtons = document.querySelectorAll('[data-modal-open]');
    modalButtons.forEach((button) => {
        const modalId = button.dataset.modalOpen;
        const modal = document.getElementById(modalId);
        if (!modal) {
            return;
        }

        button.addEventListener('click', () => {
            modal.hidden = false;
        });

        modal.querySelectorAll('[data-modal-close]').forEach((closeBtn) => {
            closeBtn.addEventListener('click', () => {
                modal.hidden = true;
            });
        });
    });
});
