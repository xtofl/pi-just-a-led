<?php
require_once('../options.inc.php');

$filter = filter();

$format = $_GET["format"];
$samples = "../temperatures.jsonsamples";

switch ($format) {
	case "table":
		header("Content-Type: text/plain");
		echo samples_table($filter, $samples);
		break;
	case "json":
	default:
		header("Content-Type: application/json");
		echo samples_text($filter, $samples);
		break;
}
?>
