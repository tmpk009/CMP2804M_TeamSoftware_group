
function initMap() {
    var myLatlng = {lat: 53.16931616357729, lng: -1.5118652343749939};


    const map = new google.maps.Map(document.getElementById('googleMap'), {
        zoom: 6,
        center: myLatlng
    });

    /*const marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: 'Click to zoom'
    });*/

    map.addListener('click', function(event) {

        async function getData(){
            const ourLat = event.latLng.lat();

        const ourLong = event.latLng.lng();

        myLatlng = {lat: ourLat, lng: ourLong};


        //changes marker pos
        var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: 'Click to zoom'
        });

        //postcodes api documentation at postcodes.io/docs
        const requestURL = `https://postcodes.io/postcodes?lon=${ourLong}&lat=${ourLat}&limit=1&radius=24000`;
        requestPostcode(requestURL);



        // POST METHOD
        /*fetch('/mapjs', {

            //Post request sends to main.py
            method: 'POST',

            // JSON payload containing the lat and long of clicked location
            body: JSON.stringify({
               ourLat, ourLong
            })
        }).then(function (response){
            return response.json();
        }).then(function (data) {

            appendData(data);


        });


    });*/

    const crimeURL = `https://data.police.uk/api/crimes-at-location?date=2020-01&lat=${ourLat}&lng=${ourLong}`;
    const data = await requestCrimes(crimeURL);
    console.log(data)

    var container = document.getElementById("mapData");
    document.getElementById("mapData").innerHTML = "";

    for (var i = 0; i < data.length; i++) {
        var div = document.createElement("div");
        div.innerHTML = 'Crime: ' + data[i].category + ' Street: ' + data[i].location.street.name;
        container.appendChild(div);
    }
    }
    getData();





});
}
//example json
//[{"category":"burglary","location_type":"Force","location":{"latitude":"53.232360","street":{"id":900970,"name":"On or near Wellington Street"},"longitude":"-0.552458"},"context":"","outcome_status":{"category":"Under investigation","date":"2020-01"},"persistent_id":"d6c613597eb6aab4a65ed017c342b6938bbfd1b7943334bb85bf100fff2ff396","id":80737326,"location_subtype":"","month":"2020-01"}]






async function requestPostcode(url) {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const postcode =  await response.json();
    console.log(`Clicked PostCode: ${postcode.result[0].postcode}`);
    console.log(`LSOA: ${postcode.result[0].lsoa}`);
    return postcode.result[0].postcode;
}

async function requestCrimes(crimeURL) {
    const response = await fetch('https://cors-anywhere.herokuapp.com/'+crimeURL, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const crimedata =  await response.json();

    return crimedata;
}

