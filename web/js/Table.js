// Funktion zum Authentifizieren des Benutzers und Abrufen seiner HID
const getClient = async (username, password, ip) => {
    try {
        const response = await fetch(`http://${ip}:8000/api/v1/users/${username}?username=${username}&password=${password}`);
        const user = await response.json()
        return user.HID;
    } catch (error) {
    console.error('Fetch error:', error);
    }
}

/*
    Objekt zur Speicherung gültiger Clients
    kann beliebig erweitert werden
 */
const validClients = {
    1: null,
    2: null
}

// Objekt zur Speicherung von Temperaturdaten und Zuständen für jeden Client
const tempsData = {
    1: {
        temps: [],
        init: false
    },
    2: {
        temps: [],
        init: false
    }
}

/*
    fetchTemps()
    Funktion zum Abrufen von Temperaturdaten für einen bestimmten Client
    lädt die Temperaturen für den angegebenen Client, wenn die Client-ID ungültig ist
    oder ein Fehler beim Abrufen der Daten auftritt, wird eine Fehlermeldung ausgegeben.
 */
const fetchTemps = async (clientId) => {
    if (clientId < 1 || clientId > 2) {
        console.error('Invalid client ID');
        return
    }
    try {
        if (!validClients[clientId]) {
            validClients[clientId] = await getClient(`PI${clientId}`, `PI${clientId}`, ip);
        }
        let response = await fetch(`http://${ip}:8000/api/v1/temps/?HID=${validClients[clientId]}&limit=5`);
        if (!response.ok) {
            return
        }
        tempsData[clientId].temps = await response.json();
        updateTable(clientId); // Update the first table data

    } catch (error) {
        console.error('Fetch error:', error);
    }

    const temps = tempsData[clientId].temps;
    let avgTemp = 0
    if(temps.length !== 0) {
        avgTemp = temps.slice(0,Math.min(5, temps.length)).reduce((acc, temp) => acc + temp.temp_c, 0) / 5;
    }
    console.log("Momentaner Durchschnitt ist: " +avgTemp);
    fanAnAus(avgTemp,clientId);
}

/*
    fetchTemps()
    Ruft einmal Temperaturdaten ab und fügt sie dann in Container ein. (Aufruf von inserHTMLContent)
 */
fetchTemps(1)

/*
    Hier wird ein Intervall erstellt.
    In diesem Fall werden alle 2 Sekunden die Methode intervalOne ausgeführt.
 */
setInterval(fetchTemps, 5000, 1); // Fetch data from Pi1 every 2 seconds

/*
    Diese Methode updated die Tabelle mit den aktuellen Temperaturdaten der REST-API.
 */
function updateTable(clientId) {
    console.log("Function start for Pi" + clientId);
    const tableBody = document.getElementById('table-body' + clientId);
    tableBody.innerHTML = '';
    if (tempsData[clientId] && tempsData[clientId].temps.length > 0) {
        for (const tempData of tempsData[clientId].temps.sort((a, b) => a.id - b.id)) {
            let date = new Date(temp.time);
            date.setTime(date.getTime()+(2 * 60 * 60 * 1000));
            const tempDate = date.toISOString().slice(0, 19).split('T');
            const seperatedDate = tempDate[0].split('-');
            tempDate[0] = seperatedDate[2] + "." + seperatedDate[1] + "." + seperatedDate[0];
            tableBody.innerHTML += `
                <tr>
                    <th scope="row">${tempData.id}</th>
                    <td>${tempDate[0]} <br> ${tempDate[1]} 
                    </td>
                    <td>${Math.round(tempData.temp_c)}</td>
                    <td>${Math.round(tempData.temp_f)}</td>
                    <td>${tempData.HID}</td>
                </tr>
            `;
        }
    }
}

/*
    fanAnAus()
    Diese Methode erkennt wenn die Durchschnittstemperatur über 25°C liegt.
    Ist dies der Fall wird der Fan als angeschaltet dargestellt, ansonsten wird er als ausgeschaltet dargestellt.
 */

function fanAnAus(temp, clientId) {
    const babell = document.getElementsByClassName("babell")[clientId - 1];
    if (temp > 28) {
        babell.style.backgroundColor = "green";
        babell.style.left = "3%";
        return
    }
    if (temp <= 25) {
        babell.style.backgroundColor = "rgb(255, 28, 28)";
        babell.style.left = "calc(97% - 20px)";
    }
}