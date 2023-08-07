const house = document.querySelector(".house");
const house__rooms = document.querySelectorAll('.light');


// const temp = document.querySelector('.temp');


const outsideTemp = document.querySelector('.outside .temp');
const insideTemp = document.querySelector('.inside .temp');
const thermastat = document.querySelector('.thermastat .temp');


let thermastatValue = 70;
let insideTempValue =  thermastatValue;


const headers = document.querySelectorAll('.header');
const up__arrow = document.querySelector('.up__arrow');
const down__arrow = document.querySelector('.down__arrow');
let current__temp = 0;
const applybtn = document.querySelector(".apply");
logEvent = {"eventType": "none", "eventDate": "none", "eventTime": "none", "eventDuration": 0, "eventState": "none", "roomType": "none"}

// IIFE for lights/everything else for every room being either turned on or off (remember to insert this functionality later)
//IIFE also for temp and display for temp


const initilizeInsideTemp = async function(){
    const response = await fetch('/temp');
    const data = await response.json();
    await getWeather("Birmingham", "usa");
    const regex = /[0-9]/g;
    const outsideTempValue = Number(outsideTemp.innerHTML.match(regex).join(''));
    if (insideTempValue > outsideTempValue) {
        insideTemp.innerHTML = `${insideTempValue - (3 * data.temp)}°`;
    }

    else if (insideTempValue < outsideTempValue) {
        insideTemp.innerHTML = `${insideTempValue + (3 * data.temp)}°`;
    }

    else insideTemp.innerHTML = `${insideTempValue}°`;
    
}

initilizeInsideTemp();


async function postData(url = '', data = {}) {
    const response = await fetch(url, {
      method: 'POST', 
      mode: 'cors', 
      cache: 'no-cache', 
      credentials: 'same-origin', 
      headers: {
        'Content-Type': 'application/json'
      
      },
      redirect: 'follow', 
      referrerPolicy: 'no-referrer', 
      body: JSON.stringify(data) 
    });
}






const roomEventPrimeKeys = {
    "window1": 1,
    "window2": 2,
    "window3": 3,
    "tv": 4,
    "lamp1": 5,
    "lamp2": 6,
    "overheadLight": 7,
    "exhaustFan": 8,
    "stove": 9,
    "oven": 10,
    "microwave": 11,
    "refrigerator": 12,
    "dishwasher": 13,
    "door1": 14,
    "door2": 15, 
    "door3": 16,
    "washingMachine": 17,
    "dryer": 18,
    "roomLight": 19,
    "faucet": 20,
    "shower": 21,
    "thermostat": 22
}

 

const getWeather = async function(city, country){
    const response = await fetch(`https://community-open-weather-map.p.rapidapi.com/weather?q=${city}%2C${country}&lat=0&lon=0&callback=test&id=2172797&lang=null&units=imperial&mode=xml`, {
        "method": "GET",
        "headers": {
            "x-rapidapi-host": "community-open-weather-map.p.rapidapi.com",
            "x-rapidapi-key": "fe4e40bdd7msh4d94107a3873b9ap12738ajsn1a48ab774e10",
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    });
    const data = await response.text();
    // I'm excluding test() to include just object
    obj = JSON.parse(data.substring(5,data.length-1));
    outsideTemp.innerHTML = `${parseInt(obj.main.temp)}°`;
    current__temp = parseInt(obj.main.temp);

}


getWeather("Birmingham", "usa");




up__arrow.addEventListener('click',(e)=>{
    thermastatValue++;
    thermastat.innerHTML = `${thermastatValue}°`;

});


down__arrow.addEventListener('click',(e)=>{
    thermastatValue--;
    thermastat.innerHTML = `${thermastatValue}°`;
});


const logThermostat = async function(){
    await postData(url = '/screen3', thermostatEvent); 
    getWeather("Birmingham", "usa");
}


thermostatEvent = {"eventType": roomEventPrimeKeys.thermostat , "eventDate": "none", "eventTime": "none", "eventDuration": 20, "eventState": "FINISHED", "roomType": "Home"}
applybtn.addEventListener('click', (e)=>{
    date_time = returnDate_Time();
    thermostatEvent.eventDate = date_time[0];
    thermostatEvent.eventTime = date_time[1];
    insideTemp.innerHTML = thermastat.innerHTML;
    logThermostat();
    
    
});


const bedRooms = function(lights, door,window1, window2, lamp1, lamp2, tv){
    return roomIntake = {
        isLight: lights,
        isDoor: door,
        isWindow1: window1,
        isWindow2: window2,
        isLamp1: lamp1,
        isLamp2: lamp2,
        isTv: tv
    };
}

const stopDisplayingDataInRoom = function(parent){
    parent.classList.remove('intake__data');
    while(parent.firstChild){
        parent.removeChild(parent.firstChild);      
    }

}


const roomStatus = {
    masterbed: false,
    bed2: false,
    bed3: false,
    bathroom1: false,
    bathroom2: false,
    livingroom: false,
    garage: false,
    pointofentry: false,
    kitchen: false
};


// dummy data:
const intake = bedRooms("on","closed","on","on","on","on","off");

const populateMasterbed = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
        <div class="items" > 💡 Lights: ${intake.roomLight} </div>
        <div class="items">  🚪 Door: ${intake.door1} </div>
        <div class="items">  🪟 Window1: ${intake.window1} </div>
        <div class="items">  🪟 Window2: ${intake.window2} </div>
        <div class="items">  🛋 Lamp1: ${intake.lamp1} </div>
        <div class="items">  📺 TV: ${intake.tv} </div>
    `);
}


const populatebed2 = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
        <div class="items" > 💡 Lights: ${intake.roomLight} </div>
        <div class="items">  🚪 Door: ${intake.door1} </div>
        <div class="items">  🪟 Window1: ${intake.window1} </div>
        <div class="items">  🪟 Window2: ${intake.window2} </div>
        <div class="items">  🛋 Lamp1: ${intake.lamp1} </div>
        <div class="items">  🛋 Lamp2: ${intake.lamp2} </div>
    `);
}

const populatebed3 = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
        <div class="items" > 💡 Lights: ${intake.roomLight} </div>
        <div class="items">  🚪 Door: ${intake.door1} </div>
        <div class="items">  🪟 Window1: ${intake.window1} </div>
        <div class="items">  🪟 Window2: ${intake.window2} </div>
        <div class="items">  🛋 Lamp1: ${intake.lamp1} </div>
        <div class="items">  🛋 Lamp2: ${intake.lamp2} </div>
    `);
}

const populatebathroom1 = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
        <div class="items" > 💡 Lights: ${intake.roomLight} </div>
        <div class="items">  🚪 Door: ${intake.door1} </div>
        <div class="items">  🪟 Window1: ${intake.window1} </div>
        <div class="items">   Over Head Light: ${intake.overheadLight} </div>
        <div class="items">   Washing Machine: ${intake.washingMachine} </div>
        <div class="items">   Exhaust Fan: ${intake.exhaustFan} </div>
        <div class="items">   Dryer: ${intake.dryer} </div>
        <div class="items">  🚰 faucet: ${intake.faucet} </div>
        <div class="items">  🚿 shower: ${intake.shower} </div>
    `);
}

const populatebathroom2 = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
        <div class="items" > 💡 Lights: ${intake.roomLight} </div>
        <div class="items">  🚪 Door: ${intake.door1} </div>
        <div class="items">  🪟 Window1: ${intake.window1} </div>
        <div class="items">   Over Head Light: ${intake.overheadLight} </div>
        <div class="items">   Exhaust Fan: ${intake.exhaustFan} </div>
        <div class="items">  🚰 faucet: ${intake.faucet} </div>
    `);
}


const populatekitchen = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
        <div class="items" > 💡 Lights: ${intake.roomLight} </div>
        <div class="items">  🪟 Window1: ${intake.window1} </div>
        <div class="items">  🪟 Window2: ${intake.window2} </div>
        <div class="items">   Over Head Light: ${intake.overheadLight} </div>
        <div class="items">   Stove: ${intake.stove} </div>
        <div class="items">   Oven: ${intake.oven} </div>
        <div class="items">   Microwave: ${intake.microwave} </div>
        <div class="items">   refrigerator: ${intake.refrigerator} </div>
        <div class="items">   Dishwasher: ${intake.dishwasher} </div>
    `);
}

const populatelivingroom = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
        <div class="items" > 💡 Lights: ${intake.roomLight} </div>
        <div class="items">  🪟 Window1: ${intake.window1} </div>
        <div class="items">  🪟 Window2: ${intake.window2} </div>
        <div class="items">  🪟 Window3: ${intake.window3} </div>
        <div class="items">  🛋 Lamp1: ${intake.lamp1} </div>
        <div class="items">  🛋 Lamp2: ${intake.lamp2} </div>
        <div class="items">  📺 TV: ${intake.tv} </div>
        <div class="items">   Over Head Light: ${intake.overheadLight} </div>
    `);
}

const populategarage = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
    <div class="items">  🚪 Door1: ${intake.door1} </div>
    <div class="items">  🚪 Door2: ${intake.door2} </div>
    <div class="items" > 💡 Lights: ${intake.roomLight} </div>
    `);
}

const populatePointsOfEntry = function(element, intake){
    element.classList.add('intake__data');
    element.insertAdjacentHTML('beforeend',`
    <div class="items">  🚪 Front Door: ${intake.door1} </div>
    <div class="items">  🚪 Back Door: ${intake.door2} </div>
    <div class="items">  🚪 garage Door: ${intake.door2} </div>
    `);
}




// post this data (eventType, eventDate,eventTime,eventDuration, eventState, roomType) 


// fix this function can't reach else statement, what am I trying to do?
const statusOfRoomEvents = function(data){
    // possibly take out undefined
    var val = {}
    Object.keys(data).forEach((key)=>{
        // console.log(`key=> ${key}/${data[key]['eventState']}`);
        if (data[key]["eventState"] == "FINISHED" || data[key]["eventState"] == "None" || data[key]["eventState"] == undefined) val[key] = "off";
        else val[key] = "on";
        
    });
    // console.log(val);
    return val;
}





const checkRoom = async function(logEvent, element){
    await postData(url = '/checkRoom', logEvent);
    const response = await fetch('/checkRoom');
    const data = await response.json();
    roomEventsValue = statusOfRoomEvents(data);
    roomType = element.classList[0];
    if (roomType == "masterbed") populateMasterbed(element, roomEventsValue);
    else if (roomType == "bed2") populatebed2(element, roomEventsValue);
    else if (roomType == "bed3") populatebed3(element, roomEventsValue);
    else if (roomType == "bathroom1") populatebathroom1(element, roomEventsValue);
    else if (roomType == "bathroom2") populatebathroom2(element, roomEventsValue);
    else if (roomType == "livingroom") populatelivingroom(element, roomEventsValue);
    else if (roomType == "kitchen") populatekitchen(element, roomEventsValue);
    else if (roomType == "garage") populategarage(element, roomEventsValue);
    else if (roomType == "pointofentry") populatePointsOfEntry(element, roomEventsValue);
}


roomType = ["masterbed", "bed2", "bed3", "bathroom1", "bathroom2", "livingroom", "kitchen", "garage", "pointofentry"]
var today = new Date();
var day = today.getDate()
var year = today.getFullYear();
var month = today.getMonth();

var hour = today.getHours();
var min = today.getMinutes();
var seconds = today.getSeconds();


var date = `${year}-${month}-${day}`;
var time = `${hour}:${min}:${seconds}`
// logEvent.eventDate = date;
// logEvent.eventTime = time;
// logEvent.eventType = "NONE";


const returnDate_Time = function(){
    var today = new Date();
    var day = today.getDate()
    var year = today.getFullYear();
    // getMonth returns 0 - 11
    var month = today.getMonth() + 1;

    var hour = today.getHours();
    var min = today.getMinutes();
    var seconds = today.getSeconds();

    var date = `${year}-${month}-${day}`;
    var time = `${hour}:${min}:${seconds}`
    lst = [date,time];
    return lst;

}

// eventType needs to be a number value.
lightEvent = {"eventType": roomEventPrimeKeys.roomLight, "eventDate": "none", "eventTime": "none", "eventDuration": 20, "eventState": "RUNNING", "roomType": "none"}


const postLightEvent = async function(roomType, lightEvent){
    lightEvent.roomType = roomType;
    date_time = returnDate_Time();
    lightEvent.eventDate = date_time[0];
    lightEvent.eventTime = date_time[1];
    await postData(url = '/lightEvent', lightEvent); 

}



headers.forEach((header)=>{
    header.addEventListener('click',(e)=>{
        e.stopPropagation();
        var roomType = header.classList[0];
        
        if (roomType == "pointofentry") return;
        
        postLightEvent(roomType, lightEvent);
    });
})



house__rooms.forEach((rooms)=>{
    rooms.addEventListener('click',(e)=>{
        e.stopPropagation();
        const roomType = rooms.classList[0];
        if (roomStatus[roomType]==false){
            roomStatus[roomType] = true;
            logEvent.roomType = roomType
            checkRoom(logEvent, rooms);
        }
        else{
            roomStatus[roomType] = false;
            stopDisplayingDataInRoom(rooms);
        }
    });
})




