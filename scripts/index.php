<?php

// $minute = floor(time() / 60);
// echo "$minute\n";
// echo $minute % 4; echo "\n"; 

$file = 'trans.gif';
$regions = array('westus2', 'francecentral', 'northcentralus', 'southeastasia');

# to test locally
# php -S localhost:8000 -t .
# http://localhost:8000/index.php?u
# curl -I -H "Host: westus2.testdomain.com" http://localhost:8000/index.php?u

if (isset($_GET['u']) && $_GET['u'] != "/report" && file_exists($file)) {

    header('Content-Type: image/gif');
    header('Content-Length: ' . filesize($file));

    $hostname_pieces = explode(".", $_SERVER['HTTP_HOST']);
    $subdomain = $hostname_pieces[0];

    if (in_array($subdomain, $regions)) {
        $selected_region = $subdomain;
    } else if ($subdomain == "interval") {
        $index = floor(time() / 20) % count($regions);            # new region every 20 seconds
        $selected_region = $regions[$index];
    } else {
        $selected_region = $regions[rand(0, count($regions)-1)];  # pick a random subdomain
    }
    
    $endpoint = "https://report." . $selected_region . ".nelogger.xyz/report";

    $nel = array("report_to"=>"default", "max_age"=>300, "include_subdomains"=>False, "success_fraction"=> 1.0);
    $report_to = array("group"=>"default", "max_age"=>300, "endpoints"=>[array("url"=>$endpoint)]);

    header('Report-To: ' . json_encode($report_to, JSON_UNESCAPED_SLASHES));
    header('NEL: ' . json_encode($nel, JSON_UNESCAPED_SLASHES));

    readfile($file);
    exit;
}
?>