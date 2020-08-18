#!/usr/bin/php
<?php

$method = $_SERVER['REQUEST_METHOD'];

if($method == 'POST') {

	$len = $_SERVER['CONTENT_LENGTH'];
	$str = fread(STDIN,$len);
	parse_str($str, $_POST);
}
else {
	parse_str($_SERVER['QUERY_STRING'], $_GET);
}


echo "Content-type: text/html\n";
print "\n";

echo '<head><meta charset="UTF-8" /></head>';


echo $method.'<BR>';

if($method == 'POST') {
	echo $_POST['UserName'].'<BR>';
	echo $_POST['Content'].'<BR>';
}
else {
	echo $_GET['UserName'].'<BR>';
	echo $_GET['Content'].'<BR>';
}






?>
