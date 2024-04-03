const ip = '172.20.199.182';



document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.nav');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            let id = this.id;
            window.location.href = `http://${ip}:9000/?site=${id}`;
        });
    });
});