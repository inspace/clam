# nel

Download Atlas probes with location data
```
$ ripe-atlas probe-search --all --field id --field asn_v4 --field country --field status --field coordinates --field address_v4 | tr -d 'b' | tr -d "'" > probes-2020-03-21.txt
```

{ awk '{ print $NF }' dns_measurements.txt | sort | uniq & cut -f 7 traceroute_measurements.txt | tr ',' '\n' | sort | uniq | grep -v "*"; } | sort | uniq > ips.txt
