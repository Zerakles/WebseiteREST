document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.nav');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            let id = this.id;
            window.location.href = `http://172.20.194.143/?site=${id}`;
        });
    });
});