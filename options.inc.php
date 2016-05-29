<?php

function samples_text($file) {
	return rtrim(file_get_contents($file));
}

function all($ample) { return true; }

function last_hour($sample) {
	$last = strtotime("-1 hour");
	return strtotime($sample->time) > $last;
}


function last_day($sample) {
	$lastweek = strtotime("-1 day");
	return strtotime($sample->time) > $lastweek;
}

function last_week($sample) {
	$lastweek = strtotime("-1 week");
	return strtotime($sample->time) > $lastweek;
}

function samples_json($filter, $file) {
	$input = rtrim(samples_text($file));
	$objects = [];
	$errors = [];
	foreach(explode("\n", $input) as $n => $line){
		$line = rtrim($line);
		$line = rtrim($line, ',');
		$object = json_decode($line);
		if (!$object) {
			$errors[] = "${n}: ${line} ----> json error ".json_last_error();
		} else {
			$objects[] = $object;
		}
	}
	return array(array_filter($objects, $filter), $errors);
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

function samples_table($filter, $file) {
	list($samples, $errors) = samples_json($filter, $file);
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
		case "hour": return "last_hour";
		default: return "last_hour";
	}
}
