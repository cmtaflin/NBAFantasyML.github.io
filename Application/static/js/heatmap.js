// Javascript file for the mapping page - heatmap.html

// load the API key for mapbox:
var apiKey = API_KEY;

// add the basemaps
var grayScaleMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    maxZoom: 15,
    minZoom: 2,
    accessToken: apiKey
});

var imageMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets-satellite",
  accessToken: apiKey
});

// create the map object 
var map = L.map("map", {
    center: [
        37.48, -98.75
    ],
    zoom: 3,
    layers: [grayScaleMap, imageMap]
});

// Add the tile layer to the map.
grayScaleMap.addTo(map);

// create layer for the NBA team locations
var TeamLoc = new L.LayerGroup();

// create the basemap group
var baseMaps = {
    GrayScale: grayScaleMap,
    Satellite: imagemap
};


// create legend for map