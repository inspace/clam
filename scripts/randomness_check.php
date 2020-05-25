<?php

$array_rand_test = array_fill(0, 4, 0);
$mt_rand_test = array_fill(0, 4, 0);
$regions = array('westus2', 'francecentral', 'northcentralus', 'southeastasia');

foreach($array_rand_test as $k=>$v) {
    echo "$k: $v\n";
}

for($i=0; $i<5000000; $i++) {
    #$f = array_rand($regions);
    #$f = rand(0, count($regions)-1);
    #echo "$f\n";
    $array_rand_test[array_rand($regions)]++;
    #$mt_rand_test[rand(0, count($regions)-1)]++;
}

foreach($array_rand_test as $k=>$v) {
    echo "$k: $v\n";
}
#echo "\n";
#foreach($mt_rand_test as $k=>$v) {
#    echo "$k: $v\n";
#}

?>