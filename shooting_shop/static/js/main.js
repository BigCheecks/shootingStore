document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/weapons/')
        .then(response => response.json())
        .then(data => {
            console.log('Зброя:', data);
        });
});