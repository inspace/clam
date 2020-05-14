#!/bin/bash

#  24335066 is dup of 24335108 beacons3.gvt2.com.
dns_mids=(24334698 24334102 24334986 24335108 24335144 24335206 24335417 24335311)
for mid in "${dns_mids[@]}"; do
    ripe-atlas report $mid --renderer dns_compact
done > dns_measurements.txt

#tr_mids=(24339639 24339658 24339702 24339712 24340545 24340556 24340560 24340792)
#for mid in "${tr_mids[@]}"; do
#    ripe-atlas report $mid --renderer traceroute_table
#done > traceroute_measurements.txt