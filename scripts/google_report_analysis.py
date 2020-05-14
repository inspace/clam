#!/usr/bin/python3
import util
import sys

MISSING_TRIE_VAL = "*"
MISSING_PROBE = ("-1", "-1", "", 0.0, 0.0, "0.0.0.0")

if __name__ == '__main__':

    asn_trie = util.load_ip2asn_default()
    hostnames = util.read_dict('../data/hostnames.txt')
    probes = util.read_probes('../data/probes-2020-03-21.txt')
    gcp_ranges = util.load_ipspace('../data/gcp_ipranges.txt')

    def trie_search(ip):
        node = asn_trie.search_best(ip)
        if node:
            return node.data['asn']
        else:
            return MISSING_TRIE_VAL

    output_format = '|'.join(['%s']*11)

    # example
    # Probe #1000069: 2020-03-20 23:05:50 NOERROR qr ra rd beacons.gcp.gvt2.com. 201 CNAME beacons-handoff.gcp.gvt2.com.; beacons-handoff.gcp.gvt2.com. 201 A 172.217.23.227

    with open('../data/dns_measurements.txt') as f:
        for line in f:
            try:
                line = line.strip()
                chunks = line.split()

                probe_id_str = chunks[1]
                probe_id = probe_id_str[1:-1] # chop off first and last chars

                if chunks[6] == 'rd':
                    target = chunks[7]
                elif chunks[7] == 'rd':
                    target = chunks[8]
                else: #elif chunks[8] == 'rd':
                    target = chunks[9]

                answer = chunks[-1]

                if answer == "0.0.0.0" or answer.endswith('.'):
                    continue

                asn = trie_search(answer)
                hostname = hostnames.get(answer, "")
                is_gcp = gcp_ranges.search_best(answer) != None
                (_, probe_asn, probe_country, probe_lat, probe_lon, probe_address) = probes.get(probe_id, MISSING_PROBE)

                print(output_format % (probe_id, target, answer, asn, hostname, is_gcp, probe_asn, probe_country, probe_lat, probe_lon, probe_address))
            except:
                sys.stderr.write('Error parsing line: %s\n' % line)