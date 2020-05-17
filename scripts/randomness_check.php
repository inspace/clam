<?php

$array_rand_test = array_fill(0, 3, 0);
$mt_rand_test = array_fill(0, 3, 0);
$regions = array('westus2', 'francecentral', 'northcentralus', 'southeastasia');

for($i=0; $i<5000000; $i++) {
    $array_rand_test[array_rand($regions)]++;
    $mt_rand_test[rand(0, count($regions)-1)]++;
}

foreach($array_rand_test as $k=>$v) {
    echo "$k: $v\n";
}
echo "\n";
foreach($mt_rand_test as $k=>$v) {
    echo "$k: $v\n";
}

?>