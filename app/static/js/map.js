function createMap(complaint_type) {
    // Delete Map
    let map_container = d3.select("#map_container");
    map_container.html(""); // empties it
    map_container.append("div").attr("id", "map"); //recreate it
  
  
    // Step 1: CREATE THE BASE LAYERS
    let street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    })
  
    let topo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    });
  
    // Assemble the API query URL.
    let url = "/api/v1.0/map_data";
    console.log(url);
  
    d3.json(url).then(function (data) {
      // Step 2: CREATE THE DATA/OVERLAY LAYERS
      console.log(data);
  
      // Initialize the Cluster Group
      let heatArray = [];
      let markers = L.markerClusterGroup();
  
      // Loop and create marker
      for (let i = 0; i < data.length; i++){
        let row = data[i];
  
        let marker = L.marker([row.rec_lat, row.rec_long]).bindPopup(`<h1>${row.avg_mass}</h1>`);
        markers.addLayer(marker);
  
        // Heatmap point
        heatArray.push([row.rec_lat, row.rec_long]);
      }
  
      // Create Heatmap Layer
      let heatLayer = L.heatLayer(heatArray, {
        radius: 25,
        blur: 10
      });
  
      // Step 3: CREATE THE LAYER CONTROL
      let baseMaps = {
        Street: street,
        Topography: topo
      };
  
      let overlayMaps = {
        HeatMap: heatLayer,
        Meteorites: markers
      };
  
      // Step 4: INITIALIZE THE MAP
      let myMap = L.map("map", {
        center: [0, -10],
        zoom: 2,
        layers: [street, markers]
      });
  
      // Step 5: Add the Layer Control, Legend, Annotations as needed
      L.control.layers(baseMaps, overlayMaps).addTo(myMap);
    });
  }
  
  function init() {
    createMap();
  }
  
  // Event Listener
  d3.select("#filter-btn").on("click", function () {
    init();
  });
  
  // on page load
  init();