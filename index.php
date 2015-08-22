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
	$outputfile = fopen("temperatures.jsonsamples", "a");
        foreach($putdata as $line) {
		fwrite($outputfile, $line.", ");
	}
	break;
case 'GET':
	$input = rtrim(file_get_contents("temperatures.jsonsamples"), ', ');
       
        $data = json_decode("[\n".$input."\n]");
        if(!$data) { print(json_last_error()); 
}
        print("<ul>\n");
        foreach(array_reverse($data) as $line)
                print("<li>".$line->time.": ".$line->temperature->{"value"}."</li>");
        print("</ul>\n");
	break;
default:
	print("what method is this? " . $_SERVER['request_method']);
}

?>
</body>
