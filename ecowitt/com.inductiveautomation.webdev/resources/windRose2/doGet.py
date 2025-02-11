def doGet(request, session):
	test='''<style>
  #chartdiv {
    width: 100%;
    height: 100%;
  }
</style>

<!-- Resources -->
<script src="https://cdn.amcharts.com/lib/4/core.js"></script>
<script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
<script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>

<!-- Chart code -->
<script>
am4core.ready(function () {
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end

  var chart = am4core.create("chartdiv", am4charts.RadarChart);
  chart.hiddenState.properties.opacity = 0; // this creates initial fade-in
  chart.data = [
    { category: "N", value1: 8, value2: 2, value3: 4, value4: 3, value5: 3 },
    { category: "NNE", value1: 11, value2: 4, value3: 2, value4: 4 },
    { category: "NE", value1: 7, value2: 6, value3: 6, value4: 2 },
    { category: "ENE", value1: 13, value2: 8, value3: 3, value4: 2 },
    { category: "E", value1: 12, value2: 10, value3: 5, value4: 1 },
    { category: "ESE", value1: 15, value2: 12, value3: 4, value4: 4 },
    { category: "SE", value1: 9, value2: 14, value3: 6, value4: 2 },
    { category: "SSE", value1: 6, value2: 16, value3: 5, value4: 1 },
    { category: "S", value1: 8, value2: 2, value3: 4, value4: 3 },
    { category: "SSW", value1: 11, value2: 4, value3: 2, value4: 4 },
    { category: "SW", value1: 7, value2: 6, value3: 6, value4: 2 },
    { category: "WSW", value1: 13, value2: 8, value3: 3, value4: 2 },
    { category: "W", value1: 12, value2: 10, value3: 5, value4: 1 },
    { category: "WNW", value1: 15, value2: 12, value3: 4, value4: 4 },
    { category: "NW", value1: 9, value2: 14, value3: 6, value4: 2 },
    { category: "NNW", value1: 6, value2: 16, value3: 5, value4: 1 }
  ];

  chart.padding(20, 20, 20, 20);
  chart.startAngle = -11.25 - 90; // Rotate chart
  chart.endAngle = 360 - 11.25 - 90;

  var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
  categoryAxis.dataFields.category = "category";
  categoryAxis.renderer.labels.template.location = 0.5;
  categoryAxis.renderer.tooltipLocation = 0.5;
  categoryAxis.renderer.labels.template.horizontalCenter = "middle";
  categoryAxis.renderer.labels.template.verticalCenter = "middle";
  categoryAxis.renderer.labels.template.fill = am4core.color("#FFFFFF"); // White labels
  categoryAxis.renderer.line.stroke = am4core.color("#FFFFFF"); // White axis line
  categoryAxis.renderer.grid.template.stroke = am4core.color("#888888"); // Grey grid lines
  
  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis.tooltip.disabled = false;
  valueAxis.renderer.labels.template.horizontalCenter = "left";
  valueAxis.min = 0;
  valueAxis.renderer.labels.template.fill = am4core.color("#FFFFFF"); // White labels
  valueAxis.renderer.line.stroke = am4core.color("#FFFFFF"); // White axis line
  valueAxis.renderer.grid.template.stroke = am4core.color("#888888"); // Grey grid lines

  function createSeries(field, name, color) {
    var series = chart.series.push(new am4charts.RadarColumnSeries());
    series.columns.template.width = am4core.percent(80);
    series.columns.template.tooltipText = "{name}: {valueY.value}";
    series.name = name;
    series.dataFields.categoryX = "category";
    series.dataFields.valueY = field;
    series.columns.template.fill = am4core.color(color);
    series.stacked = true;
  }

  // Adding series with custom colors
  createSeries("value1", "0-2mph", "#FF5733"); // Red-orange
  createSeries("value2", "2-5mph", "#33FF57"); // Green
  createSeries("value3", "5-7mph", "#3357FF"); // Blue
  createSeries("value4", "7-10mph", "#FFC300"); // Yellow
  createSeries("value5", "10-15mph", "#800080"); // Purple

  chart.seriesContainer.zIndex = -1;

  chart.cursor = new am4charts.RadarCursor();
  chart.cursor.xAxis = categoryAxis;
  chart.cursor.fullWidthXLine = true;
  chart.cursor.lineX.strokeOpacity = 0;
  chart.cursor.lineX.fillOpacity = 0.1;
  chart.cursor.lineX.fill = am4core.color("#FFFFFF");
  chart.background.fill = am4core.color("#000000");
}); // end am4core.ready()
</script>

<!-- HTML -->
<div id="chartdiv"></div>'''

	return {'html': '<html><body>'+test+'</body></html>'}