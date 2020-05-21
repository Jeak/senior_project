// Import node js tools for file reading
//const fs = require('fs');

// Demo data
//var positions = [{"unit_number": 177, "emerg_flg": 0, "fline_stat": 0, "rsrc_stat": 1, "lat": 37.48091470331358, "lon": -122.27905543215411, "rx_time": 1589007919.4916418}, {"unit_number": 522, "emerg_flg": 0, "fline_stat": 0, "rsrc_stat": 1, "lat": 37.48081590557667, "lon": -122.2791129332237, "rx_time": 1589007956.9049203}, {"unit_number": 624, "emerg_flg": 1, "fline_stat": 1, "rsrc_stat": 1, "lat": 37.48086991445299, "lon": -122.27910110396783, "rx_time": 1589007990.4738903}, {"unit_number": 2, "emerg_flg": 1, "fline_stat": 0, "rsrc_stat": 1, "lat": 37.48099616518833, "lon": -122.27911120138216, "rx_time": 1589008024.2166429}];


var positions = {};
var markers = [];

// Initialize and add the map
// Called upon web page load
function initMap() {
  // The location of the incident
  var incident_pos = {lat:37.481058, lng:-122.279109};
  // The map
  var map = new google.maps.Map(
    // center map at incident position
    document.getElementById('map'), {zoom: 18, center: incident_pos});

    // function declaration for update positions on map given list
    function updateMap(position_list,marker_list) {
      if (marker_list.length == 0) {
        // upon first updating of positions
        for (var i = 0; i < position_list.length; i++) {
          temp_pos = {lat:position_list[i].lat, lng:position_list[i].lon};
          temp_id = position_list[i].unit_number.toString();
           var marker = new google.maps.Marker({position: temp_pos,
              map: map,
              label: decodeUnitNumber(temp_id)});
           // add markers to array
           let newLength = marker_list.push(marker);
        }
      }
      // else, there are already markers present
      else {
        // delete markers
        // for (var i = 0; i < markers.length; i++) {
        //   //marker_list[i].setMap(null);
        //   marker_list[i] = null;
        // }
        marker_list = [];
        for (var i = 0; i < position_list.length; i++) {
          temp_pos = {lat:position_list[i].lat, lng:position_list[i].lon};
          temp_id = position_list[i].unit_number.toString();
           var marker = new google.maps.Marker({position: temp_pos,
              map: map,
              label: decodeUnitNumber(temp_id)});
           // add markers to array
           let newLength = marker_list.push(marker);
         }
      }
      return;
    }

    function updateEverything() {
      positions = getJsonDataFromServer('data.json');
      updateMap(positions,markers);
      return;
      }


////////////////////////////////////////////////////////////////////////////////
  //while (1) {
  //updateEverything();
  setTimeout(updateEverything, 2500, positions, markers);
  setTimeout(updateEverything, 2500, positions, markers);
  setTimeout(updateEverything, 2500, positions, markers);



  setTimeout(updateEverything, 2500, positions, markers);
  setTimeout(updateEverything, 2500, positions, markers);
  setTimeout(updateEverything, 2500, positions, markers);
  //}

////////////////////////////////////////////////////////////////////////////////
}
      //console.log(markers);
      //console.log(positions);
      //console.log(typeof(positions));
      //console.log('Markers after updating:' + markers);
      //console.log(decodeUnitNumber(65));
      // end of embedded map functions


// Function for decoding string from unit number
function decodeUnitNumber(unit_num) {
  if (unit_num < 100) {
    return ('H' + (unit_num).toString());
  } else if (unit_num >= 100 & unit_num < 200) {
    return ('EC' + (unit_num-100).toString());
  } else if (unit_num >= 200 & unit_num < 300) {
    return ('ST' + (unit_num-200).toString());
  } else if (unit_num >= 300 & unit_num < 400) {
    return ('D' + (unit_num-300).toString());
  } else if (unit_num >= 400 & unit_num < 500) {
    return ('WT' + (unit_num-400).toString());
  } else if (unit_num >= 500 & unit_num < 600) {
    return ('MT' + (unit_num-500).toString());
  } else if (unit_num >= 600 & unit_num < 700) {
    return ('SEAT' + (unit_num-600).toString());
  } else if (unit_num >= 700 & unit_num < 800) {
    return ('VLAT' + (unit_num-700).toString());
  } else if (unit_num >= 800 & unit_num < 900) {
    return ('HELI' + (unit_num-800).toString());
  } else if (unit_num >= 900 & unit_num < 1000) {
    return ('ATGS' + (unit_num-900).toString());
  } else if (unit_num >= 1000 & unit_num < 1100) {
      return ('IC' + (unit_num-1000).toString());
  } else {
    console.log('err:Unit number out of range');
  }
  return;
}



function getJsonDataFromServer(url) {
  // get data from server synchronously
  var request = new XMLHttpRequest();
  request.open('GET', url, false);  // `false` makes the request synchronous
  request.send(null);

  if (request.status === 200) {
    console.log(JSON.parse(request.responseText));
    // return parse json data
    return (JSON.parse(request.responseText));
  }
}


// not used stuf down here
// delete markers
// for (var i = 0; i < markers.length; i++) {
//   markers[i].setMap(null);
// }


// Create a function to read the data from the file
// function getDataFromFile() {
//   fs.readFile('./data.json', 'utf8', (err, jsonString) => {
//       if (err) {
//           console.log("File read failed:", err)
//           return
//       }
//       console.log('File data:', jsonString)
//   })
//
// }
//
// function sleep(milliseconds) {
//   var start = new Date().getTime();
//   for (var i = 0; i < 1e7; i++) {
//     if ((new Date().getTime() - start) > milliseconds){
//       break;
//     }
//   }
// }
