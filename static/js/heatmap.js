// Javascript file for the mapping page - heatmap.html

// load the API key for mapbox:
var apiKey = API_KEY;
var map = L.map("map", {
    center: [
        37.48, -98.75
    ],
    zoom: 4
});

// add the basemaps
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    maxZoom: 7,
    id: "mapbox.light",
    minZoom: 3,
    accessToken: API_KEY
}).addTo(map);

// var imageMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
//   attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
//   maxZoom: 18,
//   id: "mapbox.streets-satellite",
//   accessToken: API_KEY
// });

// create the map object 
// var map = L.map("map", {
//     center: [
//         37.48, -98.75
//     ],
//     zoom: 3
// });

// Add the tile layer to the map.
// grayScaleMap.addTo(map);

// create layer for the NBA team locations
var TeamLoc = new L.LayerGroup();

// create the basemap group
// var baseMaps = {
//     GrayScale: grayScaleMap,
//     Satellite: imagemap
// };

// URL for api from flask
var location_path = "/heatmap_data";
console.log(location_path);
d3.json(location_path, function(response) {
    //console.log(response.LATITUDE);
    // var TeamVenue = [];

    function getRadius(population) {
        return population * .001;
    }

    // var styleInfo = {
    //         opacity:1,
    //         fillColor: "Red",
    //         radius: getRadius(response[i].POPULATION)
    // };

    for (var i = 0; i <response.length; i++) {
        var styleInfo = {
            opacity:1,
            fillColor: "Red",
            radius: getRadius(response[i].POPULATION)
    };
        L.circleMarker([response[i].LATITUDE, response[i].LONGITUDE], styleInfo).addTo(TeamLoc);

        console.log(response[i].LATITUDE);
    }

});

TeamLoc.addTo(map);

// create legend for map