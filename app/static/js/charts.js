// Get google Visualisation API and include ColumnChart
google.load('visualization', '1', {'packages':['corechart']});

// Set callback for once API loads
google.setOnLoadCallback(drawChart);

// This is the callback that draws after load
function drawChart() {
  var data;
  // Each chart in the div is processed using same data var and drawn
  data = new google.visualization.arrayToDataTable(graphs[0])
  var view = new google.visualization.DataView(data);
  var chart = new google.visualization.ColumnChart(
          document.getElementById("{{chart['id']}}")); // chart div id from dict
  var colorsCore = [
    '#EA7369',
    '#DC4BB3',
    '#7D3AC0'
  ]
  var colorsOther = [
    '#176CA1',
    '#18ABDD',
    '#1AC9E7',
    '#1CD4D4',
    '#1DE5BC',
    '#6EF0D2',
    '#C7F9ED'
  ]
  var options = {
    title: 'test', // title from dict
    titleTextStyle: {
      fontSize: 20,
      bold: true
    },
    isStacked: true,
    legend: {position: 'right'},
    chartArea: {width: '50%'},
    vAxis: {
      title: 'Hours',
      maxValue: 1000,
    },
    annotations: {
      stem: {
        color: "transparent",
        length: 5
      },
      textStyle: {
        color: "#000000",
        fontSize: 14,
        bold: true
      }
    },
    colors: colorsOther
  }
  chart.draw(view, options);
}
