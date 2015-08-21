<?php

?>
<html>
<head>
</head>
<body>
<?

switch ($_SERVER['REQUEST_METHOD'] )
{
case 'POST':
	print("putting data");
	$putdata = file("php://input");
	$outputfile = fopen("temperatures.csv", "a");
        foreach($putdata as $line) {
		fwrite($outputfile, $line."\n");
	}
	break;
case 'GET':
	$input = file("temperatures.csv");
        $data = array();
	foreach($input as $line) {
		$data[]=$line;
	}
        print("<ul>\n");
        foreach(array_reverse($data) as $line)
                print("<li>".$line."</li>");
        print("</ul>\n");
	break;
default:
	print("what method is this? " . $_SERVER['request_method']);
}

?>
</body>
