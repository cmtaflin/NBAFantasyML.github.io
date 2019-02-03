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
    maxZoom: 9,
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
var location_path = "/heatmap_data2";
console.log(location_path);
d3.json(location_path, function(response) {
    //console.log(response.LATITUDE);
    // var TeamVenue = [];
    function styleInfo(features) {
        return {
            opacity:1,
            fillOpacity: 0.5,
            fillColor: getColor(features.properties.POPULATION),
            radius: getRadius(features.properties.POPULATION),
            stroke: true,
            weight: 0.2
        };
    }

    function getRadius(population) {
        return population * .001;
    }

    function getColor(pop) {
        switch (true) {
        case pop > 20000:
            return "red";
        case pop > 19000:
            return "blue";
        default:
            return "yellow";
        }
    }


    L.geoJson(response, {
        pointToLayer: function(features, latlng) {
            return L.circleMarker(latlng);
        },

        style: styleInfo,

        onEachFeature: function(features, layer) {
            layer.bindPopup("Team: " + features.properties.TEAM + "<br>Arena: " + features.properties.NAME);

        }
    }).addTo(TeamLoc);



});

TeamLoc.addTo(map);

// create legend for map