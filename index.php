<?php

switch ($_SERVER['REQUEST_METHOD'] )
{
case 'PUT':
	print("putting data");
	$putdata = fopen("php://input", "r");
	$outputfile = fopen("temperatures.txt", "a");
	while($data = fread($putdata, 1024)) {
		fwrite($outputfile, $data);
	}
	break;
case 'GET':
	$input = fopen("temperatures.txt", "r");
	while($data = fread($input, 1024)) {
		print($data);
	}
	break;
default:
	print("what method is this? " . $_SERVER['request_method']);
}

?>
