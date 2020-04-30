<?php

$file = 'trans.gif';

if (isset($_GET['u']) && $_GET['u'] != "/report" && file_exists($file)) {

    header('Content-Type: image/gif');
    header('Content-Length: ' . filesize($file));

    # TODO select random endpoint from a list
    $endpoint = "https://report.westus2.nelogger.xyz/report";

    $nel = array("report_to"=>"default", "max_age"=>600, "include_subdomains"=>True, "success_fraction"=> 1.0);
    $report_to = array("group"=>"default", "max_age"=>600, "endpoints"=>[array("url"=>$endpoint)]);

    header('Report-To: ' . json_encode($report_to, JSON_UNESCAPED_SLASHES));
    header('NEL: ' . json_encode($nel, JSON_UNESCAPED_SLASHES));

    readfile($file);
    exit;
}
?>