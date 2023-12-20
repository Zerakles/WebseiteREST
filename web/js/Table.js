/*
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
        const tableBody1 = document.getElementById('table-body1');
        const tableBody2 = document.getElementById('table-body2');

        tableBody1.innerHTML = ''; // Leert den aktuellen Inhalt der Tabelle

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
            tableBody1.appendChild(row);
        });

    }

    // Aktualisiere die Tabelle alle 5 Sekunden (5000 Millisekunden)
    setInterval(fetchAndPopulateTable, 5000);

    // Initialisiere die Tabelle beim Laden der Seite
    fetchAndPopulateTable();
});
*/






//////////////////

var dataArr = [1, 2, 3, 4, 5];


function arrbefuellen(){
    
    dataArr.push(Math.floor(Math.random() * (45 - 10 + 1)) + 10);

    console.log("länge" + dataArr.length);
    updateTable();
}

setInterval(arrbefuellen, 1000);



var data;

function updateTable() {
    
    console.log("Funktion start");
    const tableBody1 = document.getElementById('table-body1');
    const tableBody2 = document.getElementById('table-body2');
    const row1 = document.createElement('tr');
    

    //row1.innerHTML = '';
    //tableBody1 = '';


    tableBody1.innerHTML = '';

    if(dataArr.length > 5){

        
        for(var x = dataArr.length - 1; x > dataArr.length - 6 ; x--){

            tableBody1.innerHTML += `
            <th scope="row">test</th>
            <td>test</td>
            <td>${dataArr[x]}</td>
            <td>test</td>
            <td>test</td>
        `;

        }
        
    }else{

        for(var i = 0; i < 5; i++){

            tableBody1.innerHTML += `
            <th scope="row">test</th>
            <td>test</td>
            <td>${dataArr[i]}</td>
            <td>test</td>
            <td>test</td>
        `;

        }


    }





    //tableBody1.appendChild(row1);

}
//////////////////////////////////////////////////////






var babell = document.getElementsByClassName("babell");

function fanAnAus(t) {
  if (t > 30) {
    babell[0].style.backgroundColor = "green";
    babell[0].style.left = "3%";
    babell[1].style.backgroundColor = "green";
    babell[1].style.left = "3%";
  } else {
    babell[0].style.backgroundColor = "rgb(255, 28, 28)";
    babell[0].style.left = "calc(97% - 20px)";
    babell[1].style.backgroundColor = "rgb(255, 28, 28)";
    babell[1].style.left = "calc(97% - 20px)";
  }

  if (t > 30) {
    babell[1].style.backgroundColor = "green";
    babell[1].style.left = "3%";
  } else {
    babell[1].style.backgroundColor = "rgb(255, 28, 28)";
    babell[1].style.left = "calc(97% - 20px)";
  }
}



var park;

function addT() {
  park = Math.floor(Math.random() * (45 - 10 + 1)) + 10;
  fanAnAus(park);
  console.log(park);
}



setInterval(addT, 1000);
