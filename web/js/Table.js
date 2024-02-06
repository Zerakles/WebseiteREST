

async function fetchData() {
    
    try {
      const response = await fetch("http://172.20.199.182:8000/api/v1/temps?HID=Client_3PNikenZs&limit=5");
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
  
  
      const data = await response.json();
      // Hier kannst du mit den geladenen Daten arbeiten
      var db1 = data;
 
      db1 = JSON.parse(db1);
     //  console.log(db1);
      console.log(db1[0].id);
 
    } catch (error) {
      console.error('Fetch error:', error);
    }
  }
  
 
  fetchData();
  
  
  
  
  
  
  setTimeout(function () {
     
    
  }, 200);
 


/////////////////////////////
///////////////////////////////
//////////
//

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