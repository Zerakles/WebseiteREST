var temp = [20,25,30,40,60,10,90,20,30,40,50,10,90,20,40,50,10,90,20,120,20,40,50,10,90,20,120];
var tempD = ["09:01","09:02","09:03","09:04","09:05","09:06","09:07","09:08","09:09","09:10","09:11","09:12","09:13","09:14","09:15","09:16","09:18","09:19","09:20","09:21","09:01","09:02","09:03","09:04","09:05","09:06","09:07"];
var temp2 = [20,25,30,40,60,10,90,20,30,40,50,10,90,20,40,50,10,90,20,120,20,40,50,10,90,20,120];
var tempD2 = ["09:01","09:02","09:03","09:04","09:05","09:06","09:07","09:08","09:09","09:10","09:11","09:12","09:13","09:14","09:15","09:16","09:18","09:19","09:20","09:21","09:01","09:02","09:03","09:04","09:05","09:06","09:07"];

var db1;
let response;
async function fetchData(p) {
    let response;
    try {

        if(p === 1){
            response = await fetch("http://172.20.199.251:8000/api/v1/temps?HID=Client_TJlE8hDC7&limit=1");
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





var container = document.getElementsByClassName("Container");
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

var park;
var parkt;
function addT(){

    fetchData(1)
    setTimeout(function () {
        park = Math.round(db1[0].temp_c);
        parkt = db1[0].time;

        temp.push(park);
        tempD.push(db1[0].time.substring(11))


        q_einfügen(0)

    },  3000);
}

function addT2(){

    fetchData(2)
    setTimeout(function () {
        for(var x =0; x < db1.length; x++){
            park2[x] = +db1[x].temp_c
        }

        fanAnAus(park2,1);

    },  2000);
}


var setaddT = setInterval(addT, 3000);
var setaddT = setInterval(addT2, 3000);


function anundaus(){
    if(intF === true){
        clearInterval(setaddT);
        intF = false;
    }else{
        setaddT = setInterval(addT, 5000);
        intF = true;
    }
}




var babell = document.getElementsByClassName("babell");

function fanAnAus(t,f){
    if(f == 1){
        if(checkAvgTemp(t)){
            babell[0].style.backgroundColor = "green"
            babell[0].style.left = "3%";

        }else{
            babell[0].style.backgroundColor = "rgb(255, 28, 28)"
            babell[0].style.left = "calc(97% - 20px)";
        }

    }

}




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

