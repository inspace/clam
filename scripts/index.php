<?php

$file = 'trans.gif';

# to test locally
# php -S localhost:8000 -t .
# http://localhost:8000/index.php?u

if (isset($_GET['u']) && $_GET['u'] != "/report" && file_exists($file)) {

    header('Content-Type: image/gif');
    header('Content-Length: ' . filesize($file));

    $regions = array('westus2', 'francecentral', 'northcentralus', 'southeastasia');
    $random_region = $regions[rand(0, count($regions)-1)];   # array_rand doesn't produce uniform distributions
    $endpoint = "https://report." . $random_region . ".nelogger.xyz/report";

    #$endpoints = array("https://report.westus2.nelogger.xyz/report", 'brown', 'caffeine')

    $nel = array("report_to"=>"default", "max_age"=>600, "include_subdomains"=>True, "success_fraction"=> 1.0);
    $report_to = array("group"=>"default", "max_age"=>600, "endpoints"=>[array("url"=>$endpoint)]);

    header('Report-To: ' . json_encode($report_to, JSON_UNESCAPED_SLASHES));
    header('NEL: ' . json_encode($nel, JSON_UNESCAPED_SLASHES));

    readfile($file);
    exit;
}
?>