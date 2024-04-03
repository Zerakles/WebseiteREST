const ip = "172.20.199.251";

const getClient = async (username, password, ip) => {
    try {
        const response = await fetch(`http://${ip}:8000/api/v1/users/${username}?username=${username}&password=${password}`);
        const user = await response.json()
        return user.HID;
}
catch (error) {
    console.error('Fetch error:', error);
}
}

const validClients = {
    1: null,
    2: null
}
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
const fetchTemps = async (clientId) => {
    if (clientId < 1 || clientId > 2) {
        console.error('Invalid client ID');
        return
    }
    try {
        if (!validClients[clientId]) {
            validClients[clientId] = await getClient(`PI${clientId}`, `PI${clientId}`, ip);
        }

        const response = await fetch(`http://${ip}:8000/api/v1/temps/?HID=${validClients[clientId]}&limit=5`);
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

const tempToPercent = (temp) => Math.round(temp / 1.2);
function tempColor(t){
    if(t >= 0 && t < 25 ) color = "rgb(0, 179, 255)";
    else if(t >= 25 && t < 30) color = "rgb(255, 204, 0)";
    else if(t >= 30 && t < 45) color = "orange";
    else if(t >= 45 && t < 60) color = "rgb(255, 77, 0)";
    else color = "rgb(255, 28, 28)";
    return color;
}

let tempOneInit = false
let container = document.getElementsByClassName("Container");
let color = "rgb(0, 179, 255)";

const insertHTMLContent = (containerIndex) => {
    const clientIndex = containerIndex + 1;
    const validContainerIndex = [0,1]
    if (!validContainerIndex.includes(containerIndex) || !tempsData[clientIndex] || tempsData[clientIndex].temps.length === 0) return
    let x = 0;
    if(!tempsData[clientIndex].init){
            container[containerIndex].innerHTML = `<span class="T15">15° -</span>
         <span class="T30">30° -</span>
         <span class="T60">60° -</span>
         <span class="T90">90° -</span>
         <span class="T120">120° -</span>`;
            tempOneInit = true;
        }
    for (const temp of tempsData[clientIndex].temps) {
        const tempDate = new Date(temp.time).toISOString().slice(0, 19).split('T');
            const seperatedDate = tempDate[0].split('-');
            tempDate[0] = seperatedDate[2] + "." + seperatedDate[1] + "." + seperatedDate[0];
        color = tempColor(temp.temp_c);
        const tempHeight = tempToPercent(temp.temp_c);
        container[containerIndex].innerHTML += `<div class="q" style="height:${tempHeight}%; background-color: ${color};"><span class="temp">${temp.temp_c}°</span> <span class="tempD">${tempDate[0]} <br> ${tempDate[1]}</span></div>`;
        x++
    }
}

// Aufruf der Funktion
fetchTemps(1).then(() => insertHTMLContent(0));

async function intervalOne() {
    await fetchTemps(1)
    const temps = tempsData[1].temps;
    let avgTemp = 0
    if(temps.length !== 0) {
        avgTemp = temps.reduce((acc, temp) => acc + temp.temp_c, 0) / temps.length;
    }
    fanAnAus(avgTemp,1);
}

async function intervalTwo(){
    const temps = tempsData[2].temps;
    let avgTemp = 0
    if(temps.length !== 0) {
        avgTemp = temps.reduce((acc, temp) => acc + temp.temp_c, 0) / temps.length;
    }
    await fetchTemps(2);
    fanAnAus(avgTemp,2);
}

let setIntervalGetTemps = setInterval(intervalOne, 2000);
//let setIntervalGetTemps2 = setInterval(intervalTwo, 2000);
const babell = document.getElementsByClassName("babell");

const toggleFan = () => {
    if(tempsData[1].fanRunning){
        clearInterval(setIntervalGetTemps);
        tempsData[1].fanRunning = false;
    } else {
        setIntervalGetTemps = setInterval(intervalOne, 2000);
        tempsData[1].fanRunning = true;
    }
}

function fanAnAus(avgTemp,fanId){
    const babellId = fanId - 1;
    if(!babell[babellId]) return;
    if(avgTemp > 28){
        babell[babellId].style.backgroundColor = "green"
        babell[babellId].style.left = "3%";
        return
    }
    if (avgTemp <= 25) {
        babell[babellId].style.backgroundColor = "rgb(255, 28, 28)"
        babell[babellId].style.left = "calc(97% - 20px)";
    }
}

