def doGet(request, session):
	test='''<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <meta name="viewport" content="width=device-width, initial-scale=0.5">
	    <title>Wind Rose</title>
	
	    <!-- Highcharts Libraries -->
	    <script src="https://code.highcharts.com/highcharts.js"></script>
	    <script src="https://code.highcharts.com/highcharts-more.js"></script>
	    <script src="https://code.highcharts.com/modules/data.js"></script>
	    <script src="https://code.highcharts.com/modules/exporting.js"></script>
	    <script src="https://code.highcharts.com/modules/export-data.js"></script>
	    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
	
	    <style>
	        .highcharts-figure,
	        .highcharts-data-table table {

	            margin: 4px;
	        }
	
	        .highcharts-data-table table {
	            font-family: Verdana, sans-serif;
	            border-collapse: collapse;
	            border: 1px solid #ebebeb;
	            margin: 10px auto;
	            text-align: center;
	            width: 100vh;

	        }
	        
	
	        .highcharts-data-table caption {
	            padding: 1em 0;
	            font-size: 1.2em;
	            color: #555;
	        }
	
	        .highcharts-data-table th {
	            font-weight: 600;
	            padding: 0.5em;
	        }
	
	        .highcharts-data-table td,
	        .highcharts-data-table th,
	        .highcharts-data-table caption {
	            padding: 0.5em;
	        }
	
	        .highcharts-data-table thead tr,	
	        .highcharts-data-table tr:nth-child(even) {
	            background: white;
	        }
	
	        .highcharts-data-table tr:hover {
	            background: #f1f7ff;
	        }
				
	        .highcharts-description {
	            margin: 0.3rem 10px;
	        }
		    .chart-container {
		        height: 800px; /* Set a larger default height */
		    }
		
		    #container {
		        height: 100%; /* Make sure the container fills the parent's height */
		    }
	    </style>
	</head>
	<body>
	    <figure class="highcharts-figure">
	        <div id="container"></div>
	
	    </figure>
	
	    <div style="display:none">
	        <!-- Source: http://or.water.usgs.gov/cgi-bin/grapher/graph_windrose.pl -->
<table id="freq" border="0" cellspacing="0" cellpadding="0">
	<tr nowrap bgcolor="#CCCCFF">
	    <th colspan="9" class="hdr">Table of Frequencies (percent)</th>
	</tr>
	<tr nowrap bgcolor="#CCCCFF">
			/*tableData*/
</table>
	    </div>
	
	    <script>
	        Highcharts.chart('container', {
	    chart: {
	        polar: true,
	        type: 'column',
	        backgroundColor: 'backColor', //replace-backColor
	    },
	    title: {
	        text: 'Title', //replace-title
	        style: {
	            color: 'titleColor', //replace-titleColor
	            fontSize: '18px',
	        }
	    },
	    subtitle: {
	        text: 'Subtitle', //replace-subtitle
	        style: {
	            color: '#666', // Medium grey text
	            fontSize: '14px',
	        }
	    },
	    pane: {
	        size: '85%',
	    },
	    xAxis: {
	        tickmarkPlacement: 'on',
	        labels: {
	            style: {
	                color: 'labelColor', //replace-labelColor
	            }
	        },
	        gridLineColor: 'axisColor', //replace-axisColor
	    },
	    yAxis: {
	        min: 0,
	        endOnTick: false,
	        showLastLabel: true,
	        title: {
	            text: 'Frequency (%)',
	            style: {
	                color: 'labelColor', //replace-labelColor
	            }
	        },
	        labels: {
	            format: '{value}%',
	            style: {
	                color: 'labelColor', //replace-labelColor
	            }
	        },
	        gridLineColor: 'axisColor', //replace-axisColor
	        reversedStacks: false,
	    },
	    tooltip: {
	        valueSuffix: '%',
	        backgroundColor: 'white', //replace-titleColor
	        style: {
	            color: 'black',
	        }
	    },
	    legend: {
	        itemStyle: {
	            color: 'labelColor', //replace-labelColor
	        },
	        itemHoverStyle: {
	            color: 'titleColor', //replace-titleColor
	        }
	    },
	    plotOptions: {
	        series: {
	            stacking: 'normal',
	            shadow: false,
	            groupPadding: 0,
	            pointPlacement: 'on',
	        }
	    },
	    data: {
	        table: 'freq',
	        startRow: 1,
	        endRow: 17,
	        endColumn: 7,
	    },
	});
	    </script>
	</body>
	</html>'''
	
	
	
	
	logger = system.util.getLogger("weatherWindRose")
	
	
	title = request['params'].get('title', 'Wind Rose')
	titleColor = request['params'].get('titleColor', '#FFFFFF')
	backColor = request['params'].get('backColor', '#161616')
	axisColor = request['params'].get('axisColor', '#555555')
	labelColor= request['params'].get('labelColor', '#AAAAAA')
	periodSec = request['params'].get('periodSec',  15)
	pastHrs = request['params'].get('pastHrs',  1)
	startDate = request['params'].get('startDate',  None) #formatted(yyyy-mm-dd-hh-MM-ss)
	endDate =  request['params'].get('endDate',  None) #formatted(yyyy-mm-dd-hh-MM-ss)
	
	if startDate is not None:
		startDate=system.date.parse(startDate,'yyyy-MM-dd-HH-mm-ss')
	if endDate is not None:
		endDate=system.date.parse(endDate,'yyyy-MM-dd-HH-mm-ss')	
	if startDate is None or endDate is None:
		subtitle='Past {} hour(s)'.format(pastHrs)
	else:
		subtitle='From {} -to- {}'.format(system.date.format(startDate, 'MM/dd/yy HH:mm:ss'), system.date.format(endDate, 'MM/dd/yy HH:mm:ss'))
	
	
	tableData=WindRose.PopulateData.fetchWindRoseDataTable("[ecowitt]WeatherStation/WS85_Sensor_Array/Wind_Speed", "[ecowitt]WeatherStation/WS85_Sensor_Array/Wind_dir", periodSec, pastHrs , startDate, endDate)
	test = test.replace("'Title', //replace-title", "'{}',".format(title))
	
	test = test.replace("'Subtitle', //replace-subtitle", "'{}',".format(subtitle))
	test = test.replace("'backColor', //replace-backColor", "'{}',".format(backColor))
	test = test.replace("'axisColor', //replace-axisColor", "'{}',".format(axisColor))
	test = test.replace("'labelColor', //replace-labelColor", "'{}',".format(labelColor))
	test = test.replace("'titleColor', //replace-titleColor", "'{}',".format(titleColor))
	test = test.replace("/*tableData*/", tableData)
	
	
	return {'html':test} 