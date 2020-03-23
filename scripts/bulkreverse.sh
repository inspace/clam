#!/bin/bash
while read ip; do
    if [[ $ip = "10."* ]]; then
        continue
    fi

    echo "$ip $(dig 8.8.8.8 -x $ip +short | tr '\n' ',')"
    sleep 0.1
done < "${1:-/dev/stdin}"