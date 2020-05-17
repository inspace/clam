#!/bin/bash

regions=(westus2 northcentralus francecentral southeastasia);
for region in "${regions[@]}"; do
    scp -C neluser@nelcollector.$region.cloudapp.azure.com:/var/log/nginx/access.log ./$region-access.log
    sed -i "s/$/ $region/" $region-access.log
done