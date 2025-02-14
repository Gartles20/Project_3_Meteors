// Use D3 to select the table

// Use D3 to create a bootstrap striped table
// https://getbootstrap.com/docs/5.3/content/tables/#striped-rows

// Use D3 to select the table body

// BONUS: Dynamic table
// Loop through an array of grades and build the entire table body from scratch

// Use D3 to select the table
let table = d3.select("#meteorites");
let tbody = table.select("tbody");

// Make Table Interactive
let dt_table = new DataTable('#meteorites');

// Event Listener
d3.select("#filter-btn").on("click", function () {
  doWork();
});

// On Page Load
doWork();

// Helper Functions
function doWork() {
  // Fetch the JSON data and console log it

  // get value
  let min_year = d3.select("#min-year").property("value"); // user input
  let url1 = `/api/v1.0/meteorite_counts`;
  let url2 = `/api/v1.0/data/${min_year}`

  // Make Request
  d3.json(url1).then(function (data) {
    // Make Plot
    makeBarPlot(data);
  });

  d3.json(url2).then(function (data) {
    // Make Table
    makeTable(data);
  });
}


function makeTable(data) {
  // Clear Table
  tbody.html("");
  dt_table.clear().destroy();

  // Create Table
  for (let i = 0; i < data.length; i++) {
    let row = data[i];

    // Create Table Row
    let table_row = tbody.append("tr");

    // Append Cells
    table_row.append("td").text(row.year);
    table_row.append("td").text(row.mass);
    table_row.append("td").text(row.class);
    table_row.append("td").text(row.latitude);
    table_row.append("td").text(row.longitude);
  }

  // Make Table Interactive (again)
  dt_table = new DataTable('#meteorites', {
    order: [[0, 'desc']] // Sort by column 1 desc
  });
}


function makeBarPlot(data) {
  // Sort data by count in descending order and take the top 15
  let sortedData = data.sort((a, b) => b.count - a.count).slice(0, 15);

  // Create Trace
  let trace = {
    x: sortedData.map(row => row.rec_class),
    y: sortedData.map(row => row.count),
    type: 'bar',
    marker: {
      color: 'firebrick'
    }
  }

  // Data trace array
  let traces = [trace];

  // Apply a title to the layout
  let layout = {
    title: {
      text: `Top 15 Meteorite Classes by Count`
    },
    yaxis: {
      title: {
        text: 'Number of Meteorites'
      }
    },
    xaxis: {
      title: {
        text: 'Class'
      },
      tickangle: -45  // Rotate labels for better readability
    },
    height: 600
  }

  // Render the plot to the div tag with id "plot"
  Plotly.newPlot('plot', traces, layout);
}

