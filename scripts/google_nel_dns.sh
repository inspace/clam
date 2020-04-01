#!/bin/bash

google_hostnames=(beacons.gvt2.com beacons.gcp.gvt2.com beacons2.gvt2.com beacons3.gvt2.com beacons4.gvt2.com beacons5.gvt2.com beacons5.gvt3.com clients2.google.com)
while :; do
    for hostname in "${google_hostnames[@]}"; do
        ip=$(dig -t A +short @8.8.8.8 $hostname +short | grep '^[.0-9]*$' | head -n 1)
        reverse=$(dig @8.8.8.8 -x $ip +short | tr '\n' ',')
        echo "$hostname $ip $reverse"
    done
    sleep 60
done