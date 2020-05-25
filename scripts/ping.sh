#!/bin/bash

regions=(westus2 northcentralus francecentral southeastasia);
while :; do
    for region in "${regions[@]}"; do
        date
        ping -c 1 nelcollector.$region.cloudapp.azure.com
        sleep 20
    done
done