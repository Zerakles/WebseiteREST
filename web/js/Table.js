// document.addEventListener('DOMContentLoaded', function () {
//     //const apiUrl = 'API_URL'; // Ersetze dies durch die tatsächliche API-URL
//     const apiUrl = '';
//     function fetchAndPopulateTable() {
//         fetch(apiUrl)
//             .then(response => response.json())
//             .then(data => updateTable(data))
//             .catch(error => console.error('Error fetching data:', error));
//     }

//     function updateTable(data) {
//         const tableBody = document.getElementById('table-body');
//         tableBody.innerHTML = ''; // Leert den aktuellen Inhalt der Tabelle

//         // Begrenze die Anzahl der Einträge auf maximal 10
//         data.slice(0, 10).forEach(entry => {
//             const row = document.createElement('tr');
//             row.innerHTML = `
//                 <th scope="row">${entry.id}</th>
//                 <td>${entry.time}</td>
//                 <td>${entry.temp_c}</td>
//                 <td>${entry.temp_f}</td>
//                 <td>${entry.hid}</td>
//             `;
//             tableBody.appendChild(row);
//         });
//     }

//     // Aktualisiere die Tabelle alle 5 Sekunden (5000 Millisekunden)
//     setInterval(fetchAndPopulateTable, 5000);

//     // Initialisiere die Tabelle beim Laden der Seite
//     fetchAndPopulateTable();
// });



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
        data.slice(0, 10).forEach(fetch => {
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


  



