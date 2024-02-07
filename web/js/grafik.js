var temp = [20,25,30,40,60,10,90,20,30,40,50,10,90,20,40,50,10,90,20,120,20,40,50,10,90,20,120];
var tempD = ["09:01","09:02","09:03","09:04","09:05","09:06","09:07","09:08","09:09","09:10","09:11","09:12","09:13","09:14","09:15","09:16","09:18","09:19","09:20","09:21","09:01","09:02","09:03","09:04","09:05","09:06","09:07"];
var temp2 = [20,25,30,40,60,10,90,20,30,40,50,10,90,20,40,50,10,90,20,120,20,40,50,10,90,20,120];
var tempD2 = ["09:01","09:02","09:03","09:04","09:05","09:06","09:07","09:08","09:09","09:10","09:11","09:12","09:13","09:14","09:15","09:16","09:18","09:19","09:20","09:21","09:01","09:02","09:03","09:04","09:05","09:06","09:07"];

var db1;
var db2;
var db3;

async function fetchData(p) {
   try {
      if(p === 1){
         const response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_3PNikenZs&limit=1");
      }else{
         const response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_43PVPt8SW&limit=1");
      }
     
 
     if (!response.ok) {
       throw new Error('Network response was not ok');
     }
 
 
 
     const data = await response.json();
     // Hier kannst du mit den geladenen Daten arbeiten
     db1 = data;
     db1 = JSON.parse(db1);
   } catch (error) {
     console.error('Fetch error:', error);
   }
 }
 
 // Aufruf der Funktion
 fetchData(1);
 fetchData(2);
 
 
 
 
 
 setTimeout(function () {
   
   
 },1200);



var container = document.getElementsByClassName("Container");
var container2 = document.getElementsByClassName("Container2");
var color = "rgb(0, 179, 255)";
var Prozent;
var intF = true;



function temptoProzent(t){
   Prozent = Math.round(t / 1.2);
   return Prozent;
}


function q_einfügen(c){
    var tPark;
         x=0;
   if(c == 0){
      if(temp.length > 10 ){
         container[0].innerHTML = `<span class="T15">15° -</span>
         <span class="T30">30° -</span>
         <span class="T60">60° -</span>
         <span class="T90">90° -</span>
         <span class="T120">120° -</span>`;
         for(y = temp.length - 10; y < temp.length; y++){
         color = tempgrad(temp[y]);
         tPark = temptoProzent(temp[y]);

         container[0].innerHTML += `<div class="q" style="height:${tPark}%; background-color: ${color};"><span class="temp">${temp[y]}°</span> <span class="tempD">${tempD[y]}</span></div>`;
         x++
         }
      }else{
         for(i = 0; i < temp.length; i++){
         color = tempgrad(temp[i]);
         tPark = temptoProzent(temp[i])
          container[0].innerHTML += `<div class="q" style="height:${tPark}%; background-color: ${color};"><span class="temp">${temp[i]}°</span> <span class="tempD">${tempD[y]}</span></div>`;
          x++


         }
      }

   }else{
      if(temp2.length > 10 ){
         container2[0].innerHTML = `<span class="T15">15° -</span>
         <span class="T30">30° -</span>
         <span class="T60">60° -</span>
         <span class="T90">90° -</span>
         <span class="T120">120° -</span>`;
         for(y = temp2.length - 10; y < temp2.length; y++){
         color = tempgrad(temp2[y]);
         tPark = temptoProzent(temp2[y]);

         container2[0].innerHTML += `<div class="q" style="height:${tPark}%; background-color: ${color};"><span class="temp">${temp2[y]}°</span> <span class="tempD">${tempD2[y]}</span></div>`;
         x++
         }
      }else{
         for(i = 0; i < temp2.length; i++){
         color = tempgrad(temp2[i]);
         tPark = temptoProzent(temp2[i])
          container2[0].innerHTML += `<div class="q" style="height:${tPark}%; background-color: ${color};"><span class="temp">${temp2[i]}°</span> <span class="tempD">${tempD2[y]}</span></div>`;
          x++


         }
      }
   }
        



}

function tempgrad(t){
   if(t >= 0 && t < 25 ){
    color = "rgb(0, 179, 255)";
   }else if(t >= 25 && t < 30){
    color = "rgb(255, 204, 0)";
   }else if(t >= 30 && t < 45){
    color = "orange";
   }else if(t >= 45 && t < 60){
    color = "rgb(255, 77, 0)";
   }else{
    color = "rgb(255, 28, 28)";
   }

   return color;
}



q_einfügen(0)
q_einfügen(1)
var park;
var parkt;
function addT(){

   fetchData(1)
    setTimeout(function () {
        park = Math.round(db1[0].temp_c);
        parkt = db1[0].time;

        fanAnAus(park,1);
         temp.push(park);
         tempD.push(db1[0].time.substring(11))
     
         
         q_einfügen(0)
   
    },  200);
}
var park2;
var parkt2;
function addT2(){

   fetchData(2)
    setTimeout(function () {
        park2 = Math.round(db1[0].temp_c);
        parkt2 = db1[0].time;

       
        fanAnAus(park2,2);
         temp2.push(park2);
         tempD2.push(db1[0].time.substring(11))
     
       
         q_einfügen(1)
   
    },  200);
}

var setaddT = setInterval(addT, 1000);
var setaddT = setInterval(addT2, 1000);

function anundaus(){
   if(intF === true){
          clearInterval(setaddT);
          intF = false;
   }else{
      setaddT = setInterval(addT, 1000);
          intF = true;
   }
}




var babell = document.getElementsByClassName("babell");
var babell2 = document.getElementsByClassName("babell2");

function fanAnAus(t,f){
   if(f == 1){
      if(t > 30){
         babell[0].style.backgroundColor = "green"
         babell[0].style.left = "3%";
         
         }else{
            babell[0].style.backgroundColor = "rgb(255, 28, 28)"
            babell[0].style.left = "calc(97% - 20px)";
         }

   }else{
      if(t > 30){
         babell2[0].style.backgroundColor = "green"
         babell2[0].style.left = "3%";
         
         }else{
            babell2[0].style.backgroundColor = "rgb(255, 28, 28)"
            babell2[0].style.left = "calc(97% - 20px)";
         }

   }

}

var testa = [28,30,30,30,32]


function checkAvgTemp(t){
   var sum = 0;
   for(var i =0 ; i < t.length; i++ ){
      sum += t[i];
   }
   if (sum / 5 > 28){
      return true;
   }else{
      return false;
   }
}

console.log(checkAvgTemp(testa));


