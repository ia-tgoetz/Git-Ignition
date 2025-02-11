import math

def getHistory(windSpeedPath, windDirPath, periodSec=15, pastHrs=1 , startDate=None, endDate=None):
	paths=[windSpeedPath, windDirPath]
	intervalSeconds=periodSec
	columnNames=['Wind_Speed','Wind_dir']
	if startDate==None or endDate==None:
		return system.tag.queryTagHistory(paths=paths,intervalSeconds=intervalSeconds, rangeHours=pastHrs, columnNames=columnNames)
	else:
		return system.tag.queryTagHistory(paths=paths,intervalSeconds=intervalSeconds, startDate=startDate, endDate=endDate, columnNames=columnNames)
	
def dataSetToJson(dataset):
	convertedArry = []
	for row in range(dataset.getRowCount()):
		convertedRow={}
		for col in dataset.getColumnNames():
			convertedRow[col] = dataset.getValueAt(row, col)
		convertedArry.append(convertedRow)
	return convertedArry
	
def convertHistoryToRose(historyData):
	dictWindRose={
		'Direction':['<2 mph', '2-5 mph', '5-7 mph', '7-10 mph', '10-15 mph', '15-20 mph', '> 20 mph']
		,'N':[0,0,0,0,0,0,0]
		,'NNE':[0,0,0,0,0,0,0]
		,'NE':[0,0,0,0,0,0,0]
		,'ENE':[0,0,0,0,0,0,0]
		,'E':[0,0,0,0,0,0,0]
		,'ESE':[0,0,0,0,0,0,0]
		,'SE':[0,0,0,0,0,0,0]
		,'SSE':[0,0,0,0,0,0,0]
		,'S':[0,0,0,0,0,0,0]
		,'SSW':[0,0,0,0,0,0,0]
		,'SW':[0,0,0,0,0,0,0]
		,'WSW':[0,0,0,0,0,0,0]
		,'W':[0,0,0,0,0,0,0]
		,'WNW':[0,0,0,0,0,0,0]
		,'NW':[0,0,0,0,0,0,0]
		,'NNW':[0,0,0,0,0,0,0]
		,'Total':[0,0,0,0,0,0,0]
	}
	compass_directions = [
	    "N", "NNE", "NE", "ENE", 
	    "E", "ESE", "SE", "SSE", 
	    "S", "SSW", "SW", "WSW", 
	    "W", "WNW", "NW", "NNW"
	]
	def degrees_to_compass(degrees):
		# Normalize the degrees to the range [0, 360)
		degrees = degrees % 360
		
		# Define compass directions

		# Calculate the index based on 22.5° intervals
		index = int(((degrees + 11.25) % 360) // 22.5)  # Shift by 11.25 to center ranges
		return compass_directions[index]
	def categorize_wind_speed(speed):
		# Define the speed categories
		if speed < 2:
			return 0 #"Calm"  # Optional: You can add a category for speeds below 2 mph if needed
		elif 2 <= speed < 5:
			return 1 #"2-5 mph"
		elif 5 <= speed < 7:
			return 2 #"5-7 mph"
		elif 7 <= speed < 10:
			return 3 #"7-10 mph"
		elif 10 <= speed < 15:
			return 4 #"10-15 mph"
		elif 15 <= speed < 20:
			return 5 #"15-20 mph"
		elif speed >= 20:
			return 6 #"> 20 mph"
		else:
			return 0 #"0-2 mph"

	
	total=0
	for measure in range(len(historyData)-1):
		catagory=degrees_to_compass(historyData[measure]['Wind_dir'])
		speedGroup=categorize_wind_speed(historyData[measure]['Wind_Speed'])
		time=system.date.toMillis(historyData[measure+1]['t_stamp'])-system.date.toMillis(historyData[measure]['t_stamp'])
		dictWindRose[catagory][speedGroup]+=time/1000.0
		total+=time/1000.0
	alltotal=0
	for dire in dictWindRose:
		if dire in compass_directions:
			for x in range(len(dictWindRose[dire])):
				percent=dictWindRose[dire][x]/total*100.0
				dictWindRose[dire][x]=percent
				dictWindRose["Total"][x]+=percent
				alltotal+=percent
				
	return dictWindRose

def convertRoseToHtmlTable(data):
	import json

	# Generate HTML table
	# Compass order starting with North
	compass_order = [
	    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
	]
	
	# Generate HTML table
	html_table = """
	    <th class="freq">Direction</th>
	"""
	# Add header row
	html_table += ''.join('<th class="freq">{}</th>'.format(d) for d in data["Direction"])
	html_table += '<th class="freq">Total</th></tr>\n'
	
	# Add data rows in compass order
	for direction in compass_order:
	    values = data.get(direction, [0] * len(data["Direction"]))
	    row_color = 'bgcolor="#DDDDDD"' if direction in ["NNE", "SSE", "ENE", "NNW", "WSW"] else ''
	    row = '<tr nowrap {0}><td class="dir">{1}</td>'.format(row_color, direction)
	    row += ''.join('<td class="data">{:.2f}</td>'.format(value) for value in values)
	    row += '<td class="data">{:.2f}</td></tr>\n'.format(sum(values))
	    html_table += row
	
	# Add total row
	html_table += '<tr nowrap><td class="totals">Total</td>'
	html_table += ''.join('<td class="totals">{:.2f}</td>'.format(value) for value in data["Total"])
	html_table += '<td class="totals">{:.2f}</td></tr>\n'.format(sum(data["Total"]))
	
	# Output the result
	return(html_table)

def fetchWindRoseDataTable(windSpeedPath, windDirPath, periodSec=15, pastHrs=1 , startDate=None, endDate=None):
	dataset=WindRose.PopulateData.getHistory(windSpeedPath, windDirPath, periodSec, pastHrs, startDate, endDate)
	jsonData=WindRose.PopulateData.dataSetToJson(dataset)
	roseData=WindRose.PopulateData.convertHistoryToRose(jsonData)
	return WindRose.PopulateData.convertRoseToHtmlTable(roseData)
	

def degree_to_compass(degrees):
	# Normalize the degrees to the range [0, 360)
	compass_directions = [
    "N", "NNE", "NE", "ENE", 
    "E", "ESE", "SE", "SSE", 
    "S", "SSW", "SW", "WSW", 
    "W", "WNW", "NW", "NNW"
	]
	degrees = degrees % 360
	
	# Define compass directions

	# Calculate the index based on 22.5° intervals
	index = int(((degrees + 11.25) % 360) // 22.5)  # Shift by 11.25 to center ranges
	return compass_directions[index]
	
import math
from datetime import datetime

def average_wind_direction_and_speed(dataset):
    """
    Calculate the average wind direction and time-weighted average wind speed.

    :param dataset: Dataset object with:
                    col 0: TimeStamp (java.util.Date object),
                    col 1: Wind speed (m/s),
                    col 2: Wind direction (degrees)
    :return: A tuple (average_wind_direction, time_weighted_average_speed)
    """
    # Extract data from dataset
    timestamps = dataset.getColumnAsList(0)
    speeds = dataset.getColumnAsList(1)
    directions = dataset.getColumnAsList(2)

    # Validate inputs
    if len(speeds) != len(directions) or len(speeds) != len(timestamps):
        raise ValueError("All columns (timestamps, speeds, directions) must have the same length.")
    if len(speeds) < 2:
        return None, None  # Not enough data to calculate averages

    # Calculate time intervals in seconds
    time_intervals = []
    for i in range(1, len(timestamps)):
        t1 = timestamps[i - 1].time  # java.util.Date time in milliseconds
        t2 = timestamps[i].time
        interval = (t2 - t1) / 1000.0  # Convert milliseconds to seconds
        time_intervals.append(interval)

    # Calculate time-weighted average speed
    weighted_speeds = [speed * interval for speed, interval in zip(speeds[:-1], time_intervals)]
    total_time = sum(time_intervals)
    time_weighted_avg_speed = sum(weighted_speeds) / total_time if total_time > 0 else None

    # Convert directions to radians and calculate weighted components
    u_components = [speed * math.cos(math.radians(direction)) for speed, direction in zip(speeds, directions)]
    v_components = [speed * math.sin(math.radians(direction)) for speed, direction in zip(speeds, directions)]

    # Sum components
    U = sum(u_components)
    V = sum(v_components)

    # Check for zero vector magnitude (no wind or all speeds zero)
    if U == 0 and V == 0:
        return None, time_weighted_avg_speed

    # Calculate average direction in radians
    avg_direction_rad = math.atan2(V, U)

    # Convert to degrees and normalize to [0, 360]
    avg_direction_deg = (math.degrees(avg_direction_rad) + 360) % 360

    return [avg_direction_deg, degree_to_compass(avg_direction_deg), time_weighted_avg_speed]
	
def getAverageDirection(windSpeedPath, windDirPath, periodSec=15, pastHrs=1 , startDate=None, endDate=None):
	dataset=WindRose.PopulateData.getHistory(windSpeedPath, windDirPath, periodSec, pastHrs, startDate, endDate)
	return average_wind_direction_and_speed(dataset)