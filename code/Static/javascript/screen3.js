const allbuttons = document.querySelectorAll(".btn");
logEvent = {"eventType": "none", "eventDate": "None", "eventTime": "None", "eventDuration": 20, "eventState": "RUNNING", "roomType": "None"}

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


// const data = null;









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



const getEventTypeKey = function(eventType){
    for (const [key, value] of Object.entries(roomEventPrimeKeys)){
        if (key == eventType) return value;
        
    };
}





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


allbuttons.forEach((btn)=>{
    btn.addEventListener('click',(e)=>{
        //  fix roomType
        const roomLastIndex = e.target.closest(".room").classList.length-1;
        const roomOfEvent = e.target.closest(".room").classList[roomLastIndex];
        const buttonLastIndex = e.target.classList.length -1;
        const eventType = e.target.classList[buttonLastIndex];
        
        // if eventType == 1-3 or 14-16 then post value of 1 to tempscreen

        // fill up event log object:
        logEvent.eventType = getEventTypeKey(eventType);
        logEvent.roomType = roomOfEvent;
        const date_time = returnDate_Time();
        logEvent.eventDate = date_time[0];
        logEvent.eventTime = date_time[1];
        

        if (eventType == "window1" ||
            eventType == "window2" ||
            eventType == "window3" ||
            eventType == "door1"   ||
            eventType == "door2"   ||
            eventType == "door3"){
                const value = {'number': 1};
                postData(url = '/temp',value);
        }
    
        postData(url = '/screen3',logEvent);
    });
})