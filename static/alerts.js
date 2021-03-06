"use strict";

function getAlerts() {

    $.get('/alerts.json', function (response) {        
        console.log(response);
        $('#alerts').html("Temperature: " + response.apparentTemperature + "<br>" +
                            "Humidity: " + response.humidity + "<br>" +
                            // "Nearest Storm Bearing: " + response.nearestStormBearing + "<br>" +
                            "Nearest Storm Distance: " + response.nearestStormDistance + "<br>" +
                            "Summary: " + response.summary + "<br><br><br>" 
                            );  
    });
}


function getExtraAlerts() {

    $.get('/alerts-extra.json', function (response) {
        console.log(response);
        if (response.date !== undefined) {
            $('#alerts-extra').html("Description: " + response.description + "<br><br><br>" +
                                "Date: " + response.date + "<br><br>" +
                                "Expires: " + response.expires + "<br><br>" + 
                                "message: " + response.message);
        }
        else {
            $('#alerts-extra').html("No Active Alerts");
        }
    });         
}

$(document).on('ready', getAlerts);
$(document).on('ready', getExtraAlerts);



