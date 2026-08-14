document.addEventListener('DOMContentLoaded', () => {
    const quickButtons = document.querySelectorAll('.quick-actions button');
    quickButtons.forEach((button) => {
        button.addEventListener('click', () => {
            button.classList.add('clicked');
            setTimeout(() => button.classList.remove('clicked'), 250);
        });
    });
});
