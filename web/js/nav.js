/*
    Hier befinden sich die Konstanten für die IP und die server_ip.
    Bei der server_ip handelt es sich um die IP des WebServers und
    bei der IP handelt es sich um die IP der REST-API.
 */
const server_ip = '172.20.194.143';
const ip = "172.20.199.251";


/*
    Hier wird ein EventListener hinzugefügt. Dieser handhabt die Navigation.
    Bei dem klicken auf einer der Navigationsbuttons wird die ID in die URL
    als Get Parameter hinzugefügt und die Seite aufgerufen.

    Diese Methode ist generisch. Wird also ein weiterer Button hinzugefügt,
    erhält er automatisch eine angepasste Weiterleitung als Klick-Event.
 */
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.nav');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            let id = this.id;
            window.location.href = `http://${server_ip}/?site=${id}`;
        });
    });

});