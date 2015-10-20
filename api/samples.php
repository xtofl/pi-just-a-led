<?php

function samples_text() {
	return rtrim(file_get_contents("../temperatures.jsonsamples"));
}

function all($ample) { return true; }

function last_day($sample) {
	$lastweek = strtotime("-1 day");
	return strtotime($sample->time) > $lastweek;
}

function last_week($sample) {
	$lastweek = strtotime("-1 week");
	return strtotime($sample->time) > $lastweek;
}

function samples_json($filter) {
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
	return array_filter($objects, $filter);
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

function samples_table($filter) {
	$samples = samples_json($filter);
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

function filter() {
	switch ($_GET["filter"]) {
		case "all": return "all";
		case "week": return "last_week";
		case "day": return "last_day";
		default: return "last_week";
	}
}
$filter = filter();

$format = $_GET["format"];

switch ($format) {
	case "table":
		header("Content-Type: text/plain");
		echo samples_table($filter);
		break;
	case "json":
	default:
		header("Content-Type: application/json");
		echo samples_text($filter);
		break;
}
?>
