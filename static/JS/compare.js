
function myFunction() {
    //javascript:alert(document.getElementById('mySelect').value);
    var x = document.getElementById('mySelect');
    var num = x.options[x.selectedIndex].value;

  // POST METHOD
        fetch('/comparejs', {

            //Post request sends to main.py
            method: 'POST',

            // JSON payload containing the lat and long of clicked location
            body: JSON.stringify({
                num
            })
        }).then(function (response){
            return response.text();
        }).then(function (text) {

            console.log('POST response: ');

            //Send 'OK' to console if everything is sent
            console.log(text);
        });
}


function myMap() {
    var mapProp= {
      center:new google.maps.LatLng(53.16931616357729,-1.5118652343749939),
      zoom:5,
    };
    var mapOne = new google.maps.Map(document.getElementById("googleMapOne"),mapProp);
    var mapTwo = new google.maps.Map(document.getElementById("googleMapTwo"),mapProp);

    //MAP 1
    mapOne.addListener('click', function(event) {


            async function getData(){
                const ourLat = event.latLng.lat();

                const ourLong = event.latLng.lng();

                myLatlng = {lat: ourLat, lng: ourLong};


                //changes marker pos
                var marker = new google.maps.Marker({
                position: myLatlng,
                map: mapOne,
                title: 'Click to zoom'
                });

                const requestURL = `https://postcodes.io/postcodes?lon=${ourLong}&lat=${ourLat}&limit=1&radius=24000`;




                const ls = await requestPostcode(requestURL);
                console.log(ls);

                // POST METHOD
                fetch('/comparejs1', {

                    //Post request sends to main.py
                    method: 'POST',

                    // JSON payload containing the lat and long of clicked location
                    body: JSON.stringify({
                       ourLat, ourLong, ls
                    })
                }).then(function (response){
                    return response.text();
                }).then(function (text) {

                    console.log('POST response: ');

                    //Send 'OK' to console if everything is sent
                    console.log(text);
                });

                /*fetch('/mapjs')
                    .then(function (response) {
                        return response.json(); // But parse it as JSON this time
                    })
                    .then(function (json) {
                        console.log('GET response as JSON:');
                        console.log(json); // Here’s our JSON object
                        var graph1 = json;
                    })*/

            }

            getData();


    });

    //MAP 2
    mapTwo.addListener('click', function(event) {


            async function getData(){

                const ourLat = event.latLng.lat();

                const ourLong = event.latLng.lng();

                myLatlng = {lat: ourLat, lng: ourLong};


                //changes marker pos
                var marker = new google.maps.Marker({
                position: myLatlng,
                map: mapTwo,
                title: 'Click to zoom'
                });

                const requestURL = `https://postcodes.io/postcodes?lon=${ourLong}&lat=${ourLat}&limit=1&radius=24000`;



                const ls = await requestPostcode(requestURL);
                console.log(ls);


                // POST METHOD
                fetch('/comparejs2', {

                    //Post request sends to main.py
                    method: 'POST',

                    // JSON payload containing the lat and long of clicked location
                    body: JSON.stringify({
                       ourLat, ourLong, ls
                    })
                }).then(function (response){
                    return response.text();
                }).then(function (text) {

                    console.log('POST response: ');

                    //Send 'OK' to console if everything is sent
                    console.log(text);
                });

                /*fetch('/mapjs')
                    .then(function (response) {
                        return response.json(); // But parse it as JSON this time
                    })
                    .then(function (json) {
                        console.log('GET response as JSON:');
                        console.log(json); // Here’s our JSON object
                        var graph2 = json;
                    })*/

            }

            getData();


    });


}

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
    return await postcode.result[0].lsoa;
}

