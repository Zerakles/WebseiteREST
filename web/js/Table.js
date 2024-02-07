async function fetchData(pi) {
    
  try {

      if(pi == 1){
          const response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_lVfU0rVUo&limit=5");
      
      }else{
          const response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_43PVPt8SW&limit=5");
      }

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






//   setTimeout(function () {
   
  
//   }, 200);



var dataArr = [1, 2, 3, 4, 5];


// function arrbefuellen(){
  
//     dataArr.push(Math.floor(Math.random() * (45 - 10 + 1)) + 10);

//     // console.log("länge" + dataArr.length);
//     updateTable();
// }

//setInterval(arrbefuellen, 1000);

setInterval(updateTable, 1000);



var data;

function updateTable() {

  fetchData(1);
  
  console.log("Funktion start");
  const tableBody1 = document.getElementById('table-body1');
  const tableBody2 = document.getElementById('table-body2');


  tableBody1.innerHTML = '';
  setTimeout(function () {
   


      if(db1.length > 5){

      
          for(var x = db1.length - 1; x > db1.length - 6 ; x--){
  
              tableBody1.innerHTML += `
              <th scope="row">${db1[x].id}</th>
              <td>${db1[x].time}</td>
              <td>${Math.round(db1[x].temp_c)}</td>
              <td>${Math.round(db1[x].temp_f)}</td>
              <td>Pi1</td>
          `;
  
          }
          
      }else{
  
          for(var i = 0; i < 5; i++){
  
              tableBody1.innerHTML += `
              <th scope="row">${db1[i].id}</th>
              <td>${db1[i].time}</td>
              <td>${Math.round(db1[i].temp_c)}</td>
              <td>${Math.round(db1[i].temp_f)}</td>
              <td>Pi2</td>
          `;
  
          }

          

      
  
  
      }
      addT(1);

      fetchData(2);
      if(db1.length > 5){

      
          for(var x = db1.length - 1; x > db1.length - 6 ; x--){
  
              tableBody1.innerHTML += `
              <th scope="row">${db1[x].id}</th>
              <td>${db1[x].time}</td>
              <td>${Math.round(db1[x].temp_c)}</td>
              <td>${Math.round(db1[x].temp_f)}</td>
              <td>Pi1</td>
          `;
  
          }
          
      }else{
  
          for(var i = 0; i < 5; i++){
  
              tableBody1.innerHTML += `
              <th scope="row">${db1[i].id}</th>
              <td>${db1[i].time}</td>
              <td>${Math.round(db1[i].temp_c)}</td>
              <td>${Math.round(db1[i].temp_f)}</td>
              <td>Pi2</td>
          `;
  
          }

          

      
  
  
      }
      addT(2);

      



      
  }, 200);

 

}
//////////////////////////////////////////////////////





var babell = document.getElementsByClassName("babell");

function fanAnAus(t, pi) {
if (t > 30) {

  babell[pi].style.backgroundColor = "green";
  babell[pi].style.left = "3%";

} else {
  babell[pi].style.backgroundColor = "rgb(255, 28, 28)";
  babell[pi].style.left = "calc(97% - 20px)";

}
}



var park;

function addT(pi) {

fanAnAus(db1[0].temp_c, pi);

}



// setInterval(addT, 1000);
