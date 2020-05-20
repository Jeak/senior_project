// Import node js tools for file reading
//const fs = require('fs');

// Demo data
//var positions = [{"unit_number": 177, "emerg_flg": 0, "fline_stat": 0, "rsrc_stat": 1, "lat": 37.48091470331358, "lon": -122.27905543215411, "rx_time": 1589007919.4916418}, {"unit_number": 522, "emerg_flg": 0, "fline_stat": 0, "rsrc_stat": 1, "lat": 37.48081590557667, "lon": -122.2791129332237, "rx_time": 1589007956.9049203}, {"unit_number": 624, "emerg_flg": 1, "fline_stat": 1, "rsrc_stat": 1, "lat": 37.48086991445299, "lon": -122.27910110396783, "rx_time": 1589007990.4738903}, {"unit_number": 2, "emerg_flg": 1, "fline_stat": 0, "rsrc_stat": 1, "lat": 37.48099616518833, "lon": -122.27911120138216, "rx_time": 1589008024.2166429}];

var positions = [];
markers = [];
// Initialize and add the map
// Called upon web page load
function initMap() {

  // The location of the incident
  var incident_pos = {lat:37.481058, lng:-122.279109};
  // The map
  var map = new google.maps.Map(
    // center map at incident positioned
      document.getElementById('map'), {zoom: 15, center: incident_pos});
  // The marker, positioned at Uluru
//  var marker = new google.maps.Marker({position: incident_pos, map: map});


  // //var json = require('./data.json');
  // fetch('./data.json')
  //   .then(function(response) {
  // // Do stuff with the response
  //   var positions = data_without_dupes;
  // })
  // .catch(function(error) {
  //   console.log('): Looks like there was a problem: \n', error);
  // });


// get the data from the server
fetch('data.json')
.then(response => response.json())
.then(data => {
  console.log(data);
  positions = positions.concat(data);
  console.log(data);
}
);


console.log(positions);
//
//   for (var i = 0; i < positions.length; i++) {
//     temp_pos = {lat:positions[i].lat, lng:positions[i].lon };
//     var marker = new google.maps.Marker({position: temp_pos, map: map});
//     // add markers to array
//     let newLength = markers.push(marker);
//
//   }
//
// // delete markers
// for (var i = 0; i < markers.length; i++) {
//   markers[i].setMap(null);
// }
//
// // redraw the markers
// for (var i = 0; i < positions.length; i++) {
//   temp_pos = {lat:positions[i].lat, lng:positions[i].lon };
//   var marker = new google.maps.Marker({position: temp_pos, map: map});
//   let newLength = markers.push(marker);
//
// }

  // Plot the location of the devices on the map
 // for element in json array
  // print location on <map>
  // update status table
 // if changes to file update again
  // document.getElementById('unit_statuses').innerHTML = incident_pos.lat;
}
// Create a function to read the data from the file
function getDataFromFile() {



  fs.readFile('./data.json', 'utf8', (err, jsonString) => {
      if (err) {
          console.log("File read failed:", err)
          return
      }
      console.log('File data:', jsonString)
  })

}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
