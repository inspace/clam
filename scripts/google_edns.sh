#!/bin/bash
dig="/home/matt/bind-utils/bin/dig/dig";

# beacons5.gvt3.com CNAMES to beacons.gvt2.com and beacons6.gvt2.com so we just measure to beacons6.
google_hostnames=(beacons.gvt2.com beacons.gcp.gvt2.com beacons2.gvt2.com beacons3.gvt2.com \
                  beacons4.gvt2.com beacons5.gvt2.com beacons6.gvt2.com clients2.google.com);

while :; do
    one=$(shuf -n 1 <(seq 239 | grep -Fxv -e{0,6,7,10,11,19,21,22,25,26,28,29,30,33,55,100,127,169,172,192,214,215}));
    two=$(shuf -i 0-255 -n 1);
    three=$(shuf -i 0-255 -n 1);

    subnet="$one.$two.$three.0/24" # construct a random /24

    for hostname in "${google_hostnames[@]}"; do
        ip=$($dig -t A +short +subnet=$subnet @ns1.google.com $hostname +short | grep '^[.0-9]*$' | head -n 1); # grep for IPs to get rid of CNAMEs
        reverse=$($dig @8.8.8.8 -x $ip +short | tr '\n' ',');
        echo "$subnet $hostname $ip $reverse"
    done

    sleep 10
done