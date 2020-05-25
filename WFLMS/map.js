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

  //var status_table = document.getElementById('status_table');
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
         for (var i = 0; i < markers.length; i++) {
          marker_list[i].setMap(null);

        }
        marker_list.length = 0;

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
      updateTable(positions,status_table);
      return;
      }



////////////////////////////////////////////////////////////////////////////////
	//setTimeout(updateEverything, 15000, positions, markers);
	//while (1) {
  	//setTimeout(updateEverything, 5000, positions, markers);
	//updateEverything();
	//}


 setInterval(updateEverything, 3000, positions, markers);
//updateEverything(positions,markers);

  //setTimeout(updateEverything, 2500, positions, markers);
  //setTimeout(updateEverything, 2500, positions, markers);
  //setTimeout(updateEverything, 2500, positions, markers);


////////////////////////////////////////////////////////////////////////////////
}
      //console.log(markers);
      //console.log(positions);
      //console.log(typeof(positions));
      //console.log('Markers after updating:' + markers);
      //console.log(decodeUnitNumber(65));
      // end of embedded map functions
      function updateTable(position_list,status_table_object) {
        // Update the table with unit statuses

        //
         //clear the updateTable
         status_table_object.innerHTML = "";
         // create the headings
         status_table_object.innerHTML = "<tr><th>Unit Type</th><th>Unit Number</th><th>Resource Status</th><th>Fireline Status</th><th>Emergency Staus</th><th>Last RX Time (Local)</th></tr>";
        // Check if position_list is empty
        // If so, don't do anything
        if (position_list.length == 0) {
          return;
        }
        else {
          // For each unit in the list
          for (var i = 0; i < position_list.length; i++) {
            // create a new row for each unit
            var row = document.createElement("tr");
            // based on the fields in the json, go through each
            for (var j = 0; j < 6; j++) {
              // Create a <td> element and a text node, make the text
              // node the contents of the <td>, and put the <td> at
              // the end of the table row
              var cell = document.createElement("td");
              switch (j) {
                case 0:
                // Column 0 is unit type
                if (position_list[i].unit_number < 100) {
                  var cellText = document.createTextNode('Handcrew');
                } else if (position_list[i].unit_number >= 100 & position_list[i].unit_number < 200) {
                  var cellText = document.createTextNode('Engine Crew');
                } else if (position_list[i].unit_number >= 200 & position_list[i].unit_number < 300) {
                  var cellText = document.createTextNode('Strike Team');
                } else if (position_list[i].unit_number >= 300 & position_list[i].unit_number < 400) {
                  var cellText = document.createTextNode('Dozer');
                } else if (position_list[i].unit_number >= 400 & position_list[i].unit_number < 500) {
                  var cellText = document.createTextNode('Water Tender');
                } else if (position_list[i].unit_number >= 500 & position_list[i].unit_number < 600) {
                 var cellText = document.createTextNode('Medical Team');
                } else if (position_list[i].unit_number >= 600 & position_list[i].unit_number < 700) {
                  var cellText = document.createTextNode('SEAT');
                } else if (position_list[i].unit_number >= 700 & position_list[i].unit_number < 800) {
                  var cellText = document.createTextNode('VLAT');
                } else if (position_list[i].unit_number >= 800 & position_list[i].unit_number < 900) {
                  var cellText = document.createTextNode('Helicopter');
                } else if (position_list[i].unit_number >= 900 & position_list[i].unit_number < 1000) {
                  var cellText = document.createTextNode('ATGS');
                } else if (position_list[i].unit_number >= 1000 & position_list[i].unit_number < 1100) {
                  var cellText = document.createTextNode('IC');
                } else {
                  var cellText = document.createTextNode('Unit number out of range');
                }
                break;
                case 1:
                    // Column 1 is unit number
                   if (position_list[i].unit_number < 100) {
                     var cellText = document.createTextNode((position_list[i].unit_number).toString());
                   } else if (position_list[i].unit_number >= 100 & position_list[i].unit_number < 200) {
                     var cellText = document.createTextNode((position_list[i].unit_number-100).toString());
                   } else if (position_list[i].unit_number >= 200 & position_list[i].unit_number < 300) {
                     var cellText = document.createTextNode((position_list[i].unit_number-200).toString());
                   } else if (position_list[i].unit_number >= 300 & position_list[i].unit_number < 400) {
                     var cellText = document.createTextNode((position_list[i].unit_number-300).toString());
                   } else if (position_list[i].unit_number >= 400 & position_list[i].unit_number < 500) {
                     var cellText = document.createTextNode((position_list[i].unit_number-400).toString());
                   } else if (position_list[i].unit_number >= 500 & position_list[i].unit_number < 600) {
                    var cellText = document.createTextNode((position_list[i].unit_number-500).toString());
                   } else if (position_list[i].unit_number >= 600 & position_list[i].unit_number < 700) {
                     var cellText = document.createTextNode((position_list[i].unit_number-600).toString());
                   } else if (position_list[i].unit_number >= 700 & position_list[i].unit_number < 800) {
                     var cellText = document.createTextNode((position_list[i].unit_number-700).toString());
                   } else if (position_list[i].unit_number >= 800 & position_list[i].unit_number < 900) {
                     var cellText = document.createTextNode((position_list[i].unit_number-800).toString());
                   } else if (position_list[i].unit_number >= 900 & position_list[i].unit_number < 1000) {
                     var cellText = document.createTextNode((position_list[i].unit_number-900).toString());
                   } else if (position_list[i].unit_number >= 1000 & position_list[i].unit_number < 1100) {
                     var cellText = document.createTextNode((position_list[i].unit_number-1000).toString());
                   } else {
                     var cellText = document.createTextNode('Unit number out of range');
                   }
                 break;

                 case 2:
                 // column 2: unit status
                 switch (position_list[i].rsrc_stat) {
                   case 0:
                     var cellText = document.createTextNode('Active');
                     break;
                    case 1:
                      var cellText = document.createTextNode('On break');
                      break;
                    case 2:
                      var cellText = document.createTextNode('In transit');
                      break;
                    case 3:
                      var cellText = document.createTextNode('Out of Service');
                      break;

                   default:
                   var cellText = document.createTextNode('Error');

                 }
                 break;

                 case 3:
                   // column 3: Fireline status
                   if (position_list[i].fline_stat == 1) {
                     var cellText = document.createTextNode('Constructing');

                   }
                   else {
                     var cellText = document.createTextNode('Not constructing');
                   }
                 break;
                 case 4:
                   // column 4: Emergency status
                   if (position_list[i].emerg_flg == 1) {
                     var cellText = document.createTextNode('EMERGENCY');
                     cell.style.backgroundColor = "yellow";
                     cell.style.color = "red";

                   }
                   else {
                     var cellText = document.createTextNode(' ');
                   }
                 break;
                 case 5:
                   // column 5: RX Time
                   var cellText = document.createTextNode(position_list[i].rx_time.toString());
                 break;
              }



              cell.appendChild(cellText);
              row.appendChild(cell);
              }
              //console.log(positions);
              status_table_object.appendChild(row);
        }
        }
        return;
      }




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
    //console.log(JSON.parse(request.responseText));
    // return parse json data
    return (JSON.parse(request.responseText));
  }
}

// Time converter function used courtesy of user "Pitu" on Stack Overflow
// https://stackoverflow.com/a/6078873
// function timeConverter(UNIX_timestamp){
//   var a = new Date(UNIX_timestamp * 1000);
//   var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
//   var year = a.getFullYear();
//   var month = months[a.getMonth()];
//   var date = a.getDate();
//   var hour = a.getHours();
//   var min = a.getMinutes();
//   var sec = a.getSeconds();
//   var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
//   return time;
// }

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
