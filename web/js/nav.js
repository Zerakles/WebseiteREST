let server_ip = '172.20.194.143';
const ip = "172.20.199.251";



document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.nav');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            let id = this.id;
            window.location.href = `http://${server_ip}/?site=${id}`;
        });
    });
});