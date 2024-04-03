let ip = "172.20.199.251";

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
        init: false
    },
    2: {
        temps: [],
        init: false
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
        let response = await fetch(`http://${ip}:8000/api/v1/temps/?HID=${validClients[clientId]}&limit=5`);
        if (!response.ok) {
            return
        }
        tempsData[clientId].temps = await response.json();
        updateTable(clientId); // Update the first table data

    } catch (error) {
        console.error('Fetch error:', error);
    }
}

fetchTemps(1)

setInterval(fetchTemps, 5000, 1); // Fetch data from Pi1 every 2 seconds

function updateTable(clientId) {
    console.log("Function start for Pi" + clientId);
    const tableBody = document.getElementById('table-body' + clientId);
    tableBody.innerHTML = '';
    if (tempsData[clientId] && tempsData[clientId].temps.length > 0) {
        for (const tempData of tempsData[clientId].temps.sort((a, b) => a.id - b.id)) {
            const tempDate = new Date(tempData.time).toISOString().slice(0, 19).split('T');
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

function addT(clientId) {
    if (tempsData[clientId]?.temps.length > 0) {
        fanAnAus(tempsData[clientId].temps[0].temp_c, clientId);
    }
}
