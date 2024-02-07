var db1 = [];

async function fetchData(pi) {
    try {
        let response;
        if (pi === 1) {
            response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_TJlE8hDC7&limit=5");
        }

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        db1 = data;
        updateTable(db1, 1); // Update the first table data

    } catch (error) {
        console.error('Fetch error:', error);
    }
}

fetchData(1);

setInterval(fetchData, 2000, 1); // Fetch data from Pi1 every 2 seconds

function updateTable(data, pi) {
    console.log("Function start for Pi" + pi);
    const tableBody = document.getElementById('table-body' + pi);
    tableBody.innerHTML = '';
    if (data.length > 0) {
        for (var i = 0; i < Math.min(5, data.length); i++) {
            tableBody.innerHTML += `
                <tr>
                    <th scope="row">${data[i].id}</th>
                    <td>${data[i].time}</td>
                    <td>${Math.round(data[i].temp_c)}</td>
                    <td>${Math.round(data[i].temp_f)}</td>
                    <td>Pi${pi}</td>
                </tr>
            `;
        }
    }
}

function fanAnAus(t, pi) {
    const babell = document.getElementsByClassName("babell")[pi - 1];
    if (t > 30) {
        babell.style.backgroundColor = "green";
        babell.style.left = "3%";
    } else {
        babell.style.backgroundColor = "rgb(255, 28, 28)";
        babell.style.left = "calc(97% - 20px)";
    }
}

function addT(pi) {
    if (db1.length > 0) {
        fanAnAus(db1[0].temp_c, pi);
    }
}
