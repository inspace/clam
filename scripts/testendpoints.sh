#!/bin/bash

regions=(westus2 northcentralus francecentral southeastasia);
for region in "${regions[@]}"; do
    url="https://img.$region.nelogger.xyz/foo.png";
    curl -s -o /dev/null -w "$region %{http_code}\n" $url;
done