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
    Kann beliebig erweitert werden
 */
const validClients = {
    1: null,
    2: null
}

// Objekt zur Speicherung von Temperaturdaten und Zuständen für jeden Client
const tempsData = {
    1: {
        temps: [],
        init: false,
        fanRunning: false
    },
    2: {
        temps: [],
        init: false,
        fanRunning: false
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
        console.error('Ungültige Client-ID');
        return
    }
    try {
        if (!validClients[clientId]) {
            validClients[clientId] = await getClient(`PI${clientId}`, `PI${clientId}`, ip);
        }

        let response = await fetch(`http://${ip}:8000/api/v1/temps/?HID=${validClients[clientId]}&limit=5`);
        if (!response.ok) {
            return;
        }
        // Hier kannst du mit den geladenen Daten arbeiten
        const temps = await response.json();
        const knownTemps = tempsData[clientId]?.temps?.map(temp => temp.id);
        for (const temp of temps) {
            if(knownTemps?.includes(temp.id)) continue;
            tempsData[clientId].temps.push(temp);
            if(tempsData[clientId].temps.length !== 0) {
            tempsData[clientId].temps = tempsData[clientId]?.temps?.sort((a, b) => a.id - b.id).reverse().slice(0, Math.min(tempsData[clientId].temps.length, 10)).reverse();
        }
            insertHTMLContent(clientId - 1);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

/*
    tempToPercent()
    Dieser sich in der Konstante befindende Term bzw. Rechenweg
    rechnet die Temperatur in % um. Dies wird benötigt um eine
    Farbe in tempColor() zu wählen.
 */
const tempToPercent = (temp) => Math.round(temp / 1.2);

/*
    tempColor()
    Diese Methode gibt die passende Farbe für die Temperatur zurück.
    Dies soll für eine bessere Übersicht im Graph sorgen.
 */
function tempColor(t){
    if(t >= 0 && t < 25 ) color = "rgb(0, 179, 255)";
    else if(t >= 25 && t < 30) color = "rgb(255, 204, 0)";
    else if(t >= 30 && t < 45) color = "orange";
    else if(t >= 45 && t < 60) color = "rgb(255, 77, 0)";
    else color = "rgb(255, 28, 28)";
    return color;
}

/*
    Dieser Boolean gibt an, ob die erste Temperatur bereits initialisiert wurde.
 */
let isTempOneInit = false
/*
    Hier wird der Container in eine Variable gesteckt,
    in welchen wir unseren Graphen setzen wollen. Dieser wird anhand
    der Klasse Container erkannt.
 */
let container = document.getElementsByClassName("Container");
/*
    Dies ist die Standardfarbe für die Temperatur.
 */
let color = "rgb(0, 179, 255)";

/*
    insertHTMLContent()
    FÜgt den Graphen und die bisher enthaltenden Temperaturinhalte in
    den Container ein. Später werden hiermit nur noch Temperaturen hinzugefügt.
 */
const insertHTMLContent = (containerIndex) => {
    let clientIndex = containerIndex + 1;
    let validContainerIndex = [0,1]
    if (!validContainerIndex.includes(containerIndex) || !tempsData[clientIndex] || tempsData[clientIndex].temps.length === 0) return
    let x = 0;
    if(!tempsData[clientIndex].init){
            container[containerIndex].innerHTML = `<span class="T15">15° -</span>
         <span class="T30">30° -</span>
         <span class="T60">60° -</span>
         <span class="T90">90° -</span>
         <span class="T120">120° -</span>`;
            isTempOneInit = true;
        }
    for (const temp of tempsData[clientIndex].temps) {
        let date = new Date(temp.time);
        date.setTime(date.getTime()+(2 * 60 * 60 * 1000));
        const tempDate = date.toISOString().slice(0, 19).split('T');
        const seperatedDate = tempDate[0].split('-');
        tempDate[0] = seperatedDate[2] + "." + seperatedDate[1] + "." + seperatedDate[0];
        color = tempColor(temp.temp_c);
        let tempHeight = tempToPercent(temp.temp_c);
        container[containerIndex].innerHTML += `<div class="q" style="height:${tempHeight}%; background-color: ${color};"><span class="temp">${temp.temp_c}°</span> <span class="tempD">${tempDate[0]} <br> ${tempDate[1]}</span></div>`;
        x++
    }
}

/*
    fetchTemps()
    Ruft einmal Temperaturdaten ab und fügt sie dann in Container ein. (Aufruf von inserHTMLContent)
 */
fetchTemps(1).then(() => insertHTMLContent(0));

/*
    intervalOne()
    Diese Methode soll einem Intervall hinzugefügt werden um die Daten aktuell zu halten.
    Nach Ablauf des gewünschten Intervalls wird erneut die Temperatur bei der REST-API abgefragt.
    Daraufhin wird durch fetchTemps und insertHTMLContent die Temperatur ggf. in den Graphen eingefügt.
    Zusätzlich wird die Durchschnittstemperatur berechnet und an die Methode fanAnAus übergeben.
 */
async function intervalOne() {
    await fetchTemps(1)
    const temps = tempsData[1].temps;
    let avgTemp = 0
    if(temps.length !== 0) {
        avgTemp = temps.slice(0,Math.min(5, temps.length)).reduce((acc, temp) => acc + temp.temp_c, 0) / 5;
    }
    console.log("Momentaner Durchschnitt ist: " +avgTemp);
    fanAnAus(avgTemp,1);
}

/*
    Hier wird ein Intervall erstellt.
    In diesem Fall werden alle 2 Sekunden die Methode intervalOne ausgeführt.
 */
let setIntervalGetTemps = setInterval(intervalOne, 5000);

/*
    Hier wird der Fan aus dem HTML-Code in einer Konstanten festgehalten.
 */
const bubble = document.getElementsByClassName("babell");

/*
    fanAnAus()
    Diese Methode erkennt wenn die Durchschnittstemperatur über 25°C liegt.
    Ist dies der Fall wird der Fan als angeschaltet dargestellt, ansonsten wird er als ausgeschaltet dargestellt.
 */
function fanAnAus(avgTemp,fanId){
    const bubbleId = fanId - 1;
    if(!bubble[bubbleId]) return;
    if(avgTemp > 28){
        bubble[bubbleId].style.backgroundColor = "green"
        bubble[bubbleId].style.left = "3%";
        return
    }
    if (avgTemp <= 25) {
        bubble[bubbleId].style.backgroundColor = "rgb(255, 28, 28)"
        bubble[bubbleId].style.left = "calc(97% - 20px)";
    }
}

