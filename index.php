<?php
require_once('options.inc.php');
$filter = filter();
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

var populate_table = function() {
	var elements = data.map(function(sample){
			var tr = document.createElement("tr");

			var td = document.createElement("td");
			var time = document.createTextNode(sample[0].toLocaleString());
			td.appendChild(time);
			tr.appendChild(td);

			td = document.createElement("td");
			var temperature = document.createTextNode(sample[1]);
			td.appendChild(temperature);
			tr.appendChild(td);

			return tr;
			});
	var table = document.getElementById("temperature_table");
	elements.forEach(function(e){ table.appendChild(e); });
};
window.addEventListener('DOMContentLoaded', populate_table, false);
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
	list($objects, $errors) = samples_json($filter, "temperatures.jsonsamples");
	if ($errors && $_GET["debug"]){
		print("json errors: <br>".implode($errors, "<br>"));
	} 
        $data = $objects;
       
?><div id="timeline"></div>
<script>
data = [
<?
        foreach(array_reverse($data) as $line)
		print("[new Date(".($line->timestamp*1000)."), \n".$line->temperature->{"value"}."], ");
?>
];
</script>
<table border='1' id="temperature_table">
<thead><th>Time</th><th>Temperature (&deg;C)</th></thead>
<tbody>
<script>
if (true) {
} else {
	data.forEach(function(sample){
		document.write("<tr><td>" + sample[0].toLocaleString() + "</td><td>" + sample[1] + "</td></tr>");
        });
}
</script>
</tbody>
</table>
<?
	break;
default:
	print("what method is this? " . $_SERVER['request_method']);
}

?>
</body>
