
document.addEventListener('DOMContentLoaded', function () {
    //const apiUrl = 'API_URL'; // Ersetze dies durch die tatsächliche API-URL
    const apiUrl = '';

    function fetchAndPopulateTable() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => updateTable(data))
            .catch(error => console.error('Error fetching data:', error));
    }

    function updateTable(data) {
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = ''; // Leert den aktuellen Inhalt der Tabelle

        // Begrenze die Anzahl der Einträge auf maximal 10
        data.slice(0, 5).forEach(fetch => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <th scope="row">${fetch[0]}</th>
                <td>${fetch[1]}</td>
                <td>${fetch[2]}</td>
                <td>${fetch[3]}</td>
                <td>${fetch[4]}</td>
            `;
            tableBody.appendChild(row);
        });

    }

    // Aktualisiere die Tabelle alle 5 Sekunden (5000 Millisekunden)
    setInterval(fetchAndPopulateTable, 5000);

    // Initialisiere die Tabelle beim Laden der Seite
    fetchAndPopulateTable();
});




var babell = document.getElementsByClassName("babell");

function fanAnAus(t) {
  if (t > 30) {
    babell[0].style.backgroundColor = "green";
    babell[0].style.left = "3%";
  } else {
    babell[0].style.backgroundColor = "rgb(255, 28, 28)";
    babell[0].style.left = "calc(97% - 20px)";
  }
}



var park;

function addT() {
  park = Math.floor(Math.random() * (45 - 10 + 1)) + 10;
  fanAnAus(park);
  console.log(park);
}



setInterval(addT, 1000);
