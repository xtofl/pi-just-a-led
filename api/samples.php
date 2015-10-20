<?php

$format = $_GET["format"];

function samples_text() {
	return rtrim(file_get_contents("../temperatures.jsonsamples"));
}

function samples_json() {
	$input = rtrim(samples_text());
	$objects = [];
	$errors = [];
	foreach(explode(", \n", $input) as $n => $line){
		$jsonstring = $line;
		$object = json_decode($jsonstring);
		if (!$object) {
			$errors[] = $jsonstring;
		} else {
			$objects[] = $object;
		}
	}
	$data = $objects;
	if(!$data) { print("json error: ".json_last_error()); }
	return $objects;
}

function sample_row($time, $value, $temperature) {
	return implode(" ", [
		"",
		sprintf("%27s", $time),
		sprintf("%20s", $value),
		sprintf("%20s", $temperature),
		""
	]);
	
}

function samples_table() {
	$samples = samples_json();
	$rows = [sample_row("time", "value (kOhm)", "temperature (C)"), ""];
	foreach($samples as $sample) {
		$rows[] = sample_row(
			$sample->time,
			$sample->thermistor->value,
			$sample->temperature->value
		);
	}
	return implode("\n", $rows);
}

switch ($format) {
	case "table":
		header("Content-Type: text/plain");
		echo samples_table();
		break;
	default:
		header("Content-Type: application/json");
		echo samples_text();
		break;
}
?>
