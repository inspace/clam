#!/bin/bash

dns_mids=(24334698 24334102 24334986 24335066 24335108 24335144 24335206 24335417)
for mid in "${dns_mids[@]}"; do
    ripe-atlas report $mid --renderer dns_compact
done > dns_measurements.txt

tr_mids=(24339639 24339658 24339702 24339712 24340545 24340556 24340560 24340792)
for mid in "${tr_mids[@]}"; do
    ripe-atlas report $mid --renderer traceroute_table
done > traceroute_measurements.txt