<?php
?>
<html>
<head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      var data = [];
      google.setOnLoadCallback(drawChart);

      function drawChart() {
        var dataTable = new google.visualization.DataTable();

        dataTable.addColumn({ type: 'date', id: 'Time', label: 'Time' });
        dataTable.addColumn({ type: 'number', id: 'Temperature', label: 'Temperature (\u00B0C)' });
        dataTable.addRows(data);

        var options = {
          title: 'Temperature over time',
	  explorer: {
	    maxZoomOut: 2,
	    keepInBounds: true
	  },
          width: 900,
          height: 500,
          hAxis: {
            format: 'M/d/yy H:m',
            gridlines: {count: 15}
          },
          vAxis: {
            gridlines: {count: 1, color: 'none'},
            minValue: 19
          }
        };

        var container = document.getElementById('timeline');
        var chart = new google.visualization.LineChart(container);
        chart.draw(dataTable, options);
      }
    </script>
</head>
<body>
<?

switch ($_SERVER['REQUEST_METHOD'] )
{
case 'POST':
	print("putting data");
	$putdata = file("php://input");
	$outputfile = fopen("temperatures.jsonsamples", "a");
        foreach($putdata as $line) {
		fwrite($outputfile, "\n".$line.", ");
	}
	break;
case 'GET':
	$input = rtrim(file_get_contents("temperatures.jsonsamples"), ', ');
	$objects = [];
	$errors = [];
	foreach(explode(", \n", $input) as $n => $line){
		$jsonstring = $line;
		$object = json_decode($jsonstring);
		if (!$object) {
			print("json error: ".json_last_error()." at line $n<br>$line");
		} else {
			$objects[] = $object;
		}
	}
        $data = $objects;
        if(!$data) { print("json error: ".json_last_error()); }
       
?><div id="timeline"></div>
<script>
data = [
<?
        foreach(array_reverse($data) as $line)
		print("[new Date(\"".$line->time."\"), ".$line->temperature->{"value"}."], ");
?>
];
</script>
<table border='1'>
<tr><th>Time</th><th>Temperature (&deg;C)</th></tr>
<script>
	data.forEach(function(sample){
		document.write("<tr><td>" + sample[0].toLocaleString() + "</td><td>" + sample[1] + "</td></tr>");
        });
</script>
</table>
<?
	break;
default:
	print("what method is this? " . $_SERVER['request_method']);
}

?>
</body>
