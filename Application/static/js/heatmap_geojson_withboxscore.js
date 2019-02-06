// Javascript file for the mapping page - heatmap.html

// load the API key for mapbox:
var apiKey = API_KEY;


// add the basemaps
var grayScaleMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    maxZoom: 9,
    id: "mapbox.light",
    minZoom: 4,
    accessToken: API_KEY
});

var imageMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 9,
  id: "mapbox.streets-satellite",
  minZoom: 4,
  accessToken: API_KEY
});

//create the map object 
var map = L.map("map", {
    center: [
        35.48, -98.75
    ],
    zoom: 5,
    layers: [grayScaleMap, imageMap]
});

// Add the tile layer to the map.
grayScaleMap.addTo(map);

// create layer for the NBA team locations
var TeamLoc = new L.LayerGroup();
var LocationPoints = new L.LayerGroup();
var LocationSteals = new L.LayerGroup();
var LocationAssists = new L.LayerGroup();

// create the basemap group
var baseMaps = {
    Satellite: imageMap,
    GrayScale: grayScaleMap
};

// create overlays (for now, just the generic team location)
var mapLayers = {
    "Arena Size": TeamLoc,
    "Total Points Per Game": LocationPoints,
    "Total Steals Per Game": LocationSteals,
    "Total Assists Per Game": LocationAssists
};

// add controls to enable turning on and off layers
// note the map layers are also a basemap type.
L.control.layers(baseMaps).addTo(map);
L.control.layers(mapLayers, null, {
    collapsed: false
}).addTo(map);

// URL for api from flask
var location_path = "/heatmap_data2";
console.log(location_path);
d3.json(location_path, function(response) {
    // var TeamVenue = [];
    function styleInfo(features) {
        return {
            opacity:1,
            fillOpacity: 0.75,
            fillColor: getColor(features.properties.POPULATION),
            radius: getRadius(features.properties.POPULATION),
            stroke: true,
            weight: 0.2
        };
    }

    function getRadius(population) {
        switch (true) {
        case population > 20000:
            return 25;
        case population > 19000:
            return 20;
        case population > 18000:
            return 15;
        default:
            return 12;
        }
    }

    function getColor(pop) {
        switch (true) {
        case pop > 20000:
            return "#ea2c2c";
        case pop > 19000:
            return "#ea822c";
        case pop > 18000:
            return "#ee9c00";
        default:
            return "#98ee00";
        }
    }


    L.geoJson(response, {
        pointToLayer: function(features, latlng) {
            return L.circleMarker(latlng);
        },

        style: styleInfo,

        onEachFeature: function(features, layer) {
            layer.bindPopup("Team: " + features.properties.TEAM + "<br>Arena: " + features.properties.NAME + "<br>Arena Size: " +features.properties.POPULATION);

        }
    }).addTo(TeamLoc);

    TeamLoc.addTo(map);

    // create the legend control
    var TeamLocL = L.control({
        position: "bottomright"
    });

    var LocationPointsL = L.control({
        position: "bottomright"
    });

    var LocationStealsL = L.control({
        position: "bottomright"
    });

    var LocationAssistsL = L.control({
        position: "bottomright"
    });




    // This section holds the various legends, based on the layer selected.

    // details for the team location legend
    TeamLocL.onAdd = function() {
        var div = L.DomUtil.create("div", "NBA legend");

        var grades = [0, 18000, 19000, 20000];
        var colors = [
            "#98ee00",
            "#ee9c00",
            "#ea822c",
            "#ea2c2c"
        ];
        labels = [];

        // add title of the legend
        div.innerHTML += '<b>Arena Size</b><br>'

        // Loop through legend items and generate label with the associated color
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += "<i style='background: " + colors[i] + "'></i> " +
              grades[i] + (grades[i + 1] ? "&ndash;" + grades[i + 1] + "  <br>" : "+");
          }
          return div;
    };

    // add legend to the map. this is the default legend for the default visible layer
    TeamLocL.addTo(map);

    // details for the Average points legend
    LocationPointsL.onAdd = function() {
        var div = L.DomUtil.create("div", "NBA legend");

        var grades = [0, 220, 225, 230];
        var colors = [
            "#fdcc8a",
            "#fc8d59",
            "#e34a33",
            "#b30000"
        ];
        labels = [];

        // add title of the legend
        div.innerHTML += '<b>Average Points Per Game</b><br>'

        // Loop through legend items and generate label with the associated color
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += "<i style='background: " + colors[i] + "'></i> " +
                grades[i] + (grades[i + 1] ? "&ndash;" + grades[i + 1] + "  <br>" : "+");
            }
            return div;
    };


    // details for the Average steals legend
    LocationStealsL.onAdd = function() {
        var div = L.DomUtil.create("div", "NBA legend");

        var grades = [0, 14, 16, 17];
        var colors = [
            "#bdc9e1",
            "#74a9cf",
            "#2b8cbe",
            "#045a8d"
        ];
        labels = [];

        // add title of the legend
        div.innerHTML += '<b>Average Steals Per Game</b><br>'

        // Loop through legend items and generate label with the associated color
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += "<i style='background: " + colors[i] + "'></i> " +
                grades[i] + (grades[i + 1] ? "&ndash;" + grades[i + 1] + "  <br>" : "+");
            }
            return div;
    };


    // details for the Average assists legend
    LocationAssistsL.onAdd = function() {
        var div = L.DomUtil.create("div", "NBA legend");

        var grades = [0, 46, 48, 51];
        var colors = [
            "#bdc9e1",
            "#74a9cf",
            "#2b8cbe",
            "#045a8d"
        ];
        labels = [];

        // add title of the legend
        div.innerHTML += '<b>Average Assists Per Game</b><br>'

        // Loop through legend items and generate label with the associated color
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML += "<i style='background: " + colors[i] + "'></i> " +
                grades[i] + (grades[i + 1] ? "&ndash;" + grades[i + 1] + "  <br>" : "+");
            }
            return div;
    };


    // pop-up function for all of the boxscore data results
    function boxscorePopup(features, layer) {
        layer.bindPopup("<b>" + features.properties.NAME + "</b>" + "<br>Points Per Game: " + 
            features.properties.points + "<br>Steals Per Game: " + features.properties.steals +
            "<br>Rebounds Per Game: " + features.properties.totReb +
            "<br>Assists Per Game: " + features.properties.assists);

    }


    var boxscore_path = "/boxscore_data";

    d3.json(boxscore_path, function(response2) {
        function styleInfoPoints(features) {
            return {
                opacity:1,
                fillOpacity: 0.75,
                fillColor: getColorPoints(features.properties.points),
                radius: getRadiusPoints(features.properties.points),
                stroke: true,
                weight: 0.2
            };
        }

        function getRadiusPoints(points) {
            switch (true) {
            case points > 230:
                return 25;
            case points > 225:
                return 20;
            case points > 220:
                return 15;
            default:
                return 12;
            }
        }

        function getColorPoints(points) {
            switch (true) {
            case points > 230:
                return "#b30000";
            case points > 225:
                return "#e34a33";
            case points > 220:
                return "#fc8d59";
            default:
                return "#fdcc8a";
            }
        }

        L.geoJson(response2, {
            pointToLayer: function(features, latlng) {
                return L.circleMarker(latlng);
            },
            style: styleInfoPoints,
            onEachFeature: boxscorePopup

        }).addTo(LocationPoints);


    });


    // This loads the boxscore data and creates circle markers based on steals
    d3.json(boxscore_path, function(response3) {
        function styleInfoSteals(features) {
            return {
                opacity:1,
                fillOpacity: 0.75,
                fillColor: getColorSteals(features.properties.steals),
                radius: getRadiusSteals(features.properties.steals),
                stroke: true,
                weight: 0.2
            };
        }

        function getRadiusSteals(steals) {
            switch (true) {
            case steals > 17:
                return 25;
            case steals > 16:
                return 20;
            case steals > 14:
                return 15;
            default:
                return 12;
            }
        }

        function getColorSteals(steals) {
            switch (true) {
            case steals > 17:
                return "#045a8d";
            case steals > 16:
                return "#2b8cbe";
            case steals > 14:
                return "#74a9cf";
            default:
                return "#bdc9e1";
            }
        }

        L.geoJson(response3, {
            pointToLayer: function(features, latlng) {
                return L.circleMarker(latlng);
            },
    
            style: styleInfoSteals,    
            onEachFeature: boxscorePopup

        }).addTo(LocationSteals);

    });


    // read boxscore data for assists and generate the circle markers
    d3.json(boxscore_path, function(response4) {
        function styleInfoAssists(features) {
            return {
                opacity:1,
                fillOpacity: 0.75,
                fillColor: getColorAssists(features.properties.assists),
                radius: getRadiusAssists(features.properties.assists),
                stroke: true,
                weight: 0.2
            };
        }

        function getRadiusAssists(assists) {
            switch (true) {
            case assists > 51:
                return 25;
            case assists > 48:
                return 20;
            case assists > 46:
                return 15;
            default:
                return 12;
            }
        }

        function getColorAssists(assists) {
            switch (true) {
            case assists > 51:
                return "#045a8d";
            case assists > 48:
                return "#2b8cbe";
            case assists > 46:
                return "#74a9cf";
            default:
                return "#bdc9e1";
            }
        }

        L.geoJson(response4, {
            pointToLayer: function(features, latlng) {
                return L.circleMarker(latlng);
            },
    
            style: styleInfoAssists,    
            onEachFeature: boxscorePopup
            
        }).addTo(LocationAssists);

    });

    // add event listener to turn on/off legend based on the layer visible.
    map.on('baselayerchange', function(eventLayer) {
        console.log("clicked on base layer: " + eventLayer.name);

        if (eventLayer.name === "Arena Size") {
            TeamLocL.addTo(map);
            map.removeControl(LocationPointsL);
            map.removeControl(LocationStealsL);
            map.removeControl(LocationAssistsL);
        } else
        if (eventLayer.name === "Total Points Per Game") {
            LocationPointsL.addTo(map);
            map.removeControl(TeamLocL);
            map.removeControl(LocationStealsL);
            map.removeControl(LocationAssistsL);
        } else 
        if (eventLayer.name === "Total Steals Per Game") {
            LocationStealsL.addTo(map);
            map.removeControl(TeamLocL);
            map.removeControl(LocationPointsL);
            map.removeControl(LocationAssistsL);
        } else
        if (eventLayer.name === "Total Assists Per Game") {
            LocationAssistsL.addTo(map);
            map.removeControl(TeamLocL);
            map.removeControl(LocationPointsL);
            map.removeControl(LocationStealsL);
        }
    });

});
