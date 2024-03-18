
document.addEventListener('DOMContentLoaded', (event) => {
    const savedProgress = localStorage.getItem('testProgress');
    if (savedProgress) {
        const answers = JSON.parse(savedProgress);
        for (const [key, value] of Object.entries(answers)) {
            const input = document.querySelector(`input[name="${key}"][value="${value}"]`);
            if (input) {
                input.checked = true;
            }
        }
    }
});
