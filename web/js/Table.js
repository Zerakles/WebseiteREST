async function fetchData(pi) {
  try {
      let response;
      if(pi === 1){
          response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_lVfU0rVUo&limit=5");
      }else{
          response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_43PVPt8SW&limit=5");
      }
    if (!response.ok) {
      console.log('Network response was not ok');
    }
    let db1 = await response.json();
    db1 = JSON.parse(db1);
    console.log(db1[0].id);
  } catch (error) {
    console.error('Fetch error:', error);
  }
}
setInterval(updateTable, 1000);
let data;
function updateTable() {
  let db1 = fetchData(1);
  console.log("Funktion start");
  let tableBody1 = document.getElementById('table-body1');
  let tableBody2 = document.getElementById('table-body2');
  tableBody1.innerHTML = '';
  setTimeout(function () {
      if(db1.length > 5){
          for(let x = db1.length - 1; x > db1.length - 6 ; x--){
              tableBody1.innerHTML += `
              <th scope="row">${db1[x]['id']}</th>
              <td>${db1[x].time}</td>
              <td>${Math.round(db1[x]['temp_c'])}</td>
              <td>${Math.round(db1[x]['temp_f'])}</td>
              <td>Pi1</td>
          `;
          }
      }else{
          for(let i = 0; i < 5; i++){
              tableBody1.innerHTML += `
              <th scope="row">${db1[i].id}</th>
              <td>${db1[i].time}</td>
              <td>${Math.round(db1[i]['temp_c'])}</td>
              <td>${Math.round(db1[i]['temp_f'])}</td>
              <td>Pi2</td>
            `;
         }
      }
      fanAnAus(db1[0]['temp_c'], 1);
      let db2 = fetchData(2);
      if(db2.length > 5){
          for(let x = db2.length - 1; x > db2.length - 6 ; x--){
              tableBody2.innerHTML += `
              <th scope="row">${db2[x]['id']}</th>
              <td>${db2[x].time}</td>
              <td>${Math.round(db2[x]['temp_c'])}</td>
              <td>${Math.round(db2[x]['temp_f'])}</td>
              <td>Pi1</td>
          `;
          }
      }else{
          for(let i = 0; i < 5; i++){
              tableBody2.innerHTML += `
              <th scope="row">${db2[i]['id']}</th>
              <td>${db1[i].time}</td>
              <td>${Math.round(db2[i]['temp_c'])}</td>
              <td>${Math.round(db2[i]['temp_f'])}</td>
              <td>Pi2</td>
          `;
          }
      }
      fanAnAus(db1[0]['temp_c'], 2);
  }, 200);
}
const babell = document.getElementsByClassName("babell");
function fanAnAus(t, pi) {
    if (t > 28) {
        babell[pi].style.backgroundColor = "green";
        babell[pi].style.left = "3%";
    } else {
        babell[pi].style.backgroundColor = "rgb(255, 28, 28)";
        babell[pi].style.left = "calc(97% - 20px)";
    }
}