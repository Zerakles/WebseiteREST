let ip = '172.20.194.143';



document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.nav');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            let id = this.id;
            window.location.href = `http://${ip}/?site=${id}`;
        });
    });
});