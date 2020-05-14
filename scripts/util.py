#!/usr/bin/python
import radix # pip install py-radix or ppy-radix for pure python version
import sys
import unittest
import gzip
import os
import io
import struct
import socket
from bs4 import BeautifulSoup

this_dir = os.path.dirname(__file__)

def read_dict(filename):
    d = {}
    with open(filename, 'rt') as f:
        for line in f:
            line = line.strip()
            chunks = line.split()
            if len(chunks) == 2:
                d[chunks[0]] = chunks[1]
    return d

def read_probes(filename):
    d = {}

    with open(filename, 'rt') as f:
        next(f) # skip 1st 2 lines 
        next(f)

        for line in f:
            line = line.strip()
            chunks = line.split()

            if len(chunks) < 6:
                sys.stderr.write('error parsing probes line: %s\n' % line)
                continue

            probe_id = chunks[0]
            asn = chunks[1]
            country = chunks[2]
            #status = chunks[3]

            #if status != 'Connected':
            #    continue

            coords = chunks[4]
            if ',' in coords:
                lat_str, lon_str = coords.split(',')
                lat = float(lat_str)
                lon = float(lon_str)
            else:
                lat, lon = 0.0, 0.0

            ip = chunks[5]

            d[probe_id] = (probe_id, asn, country, lat, lon, ip)

    return d

def load_squatspace_default():
    default_file = os.path.join(this_dir, '../data/unannounced-202002.txt')
    return load_squatspace(default_file)

def load_squatspace(squat_filename):
    return load_ipspace(squat_filename)

def load_ipspace(ipspace_filename):
    trie = radix.Radix()

    with open(ipspace_filename) as f:
        for line in f:
            prefix = line.strip()
            trie.add(prefix)
    return trie

def load_asn2org_default():
    default_file = os.path.join(this_dir, '../data/20200101.as-org2info.txt')
    return load_asn2org(default_file)

def load_asn2org(asn2org_filename):

    asn_org = {}
    org_orgname = {}

    with open(asn2org_filename) as f:

        #The CAIDA org-to-asn file has two different parts documented here http://data.caida.org/datasets/as-organizations/
        # first map the org_id to an org_name
        # then map an asn to an org_id
        # return asn to org_name because org_id is not informative

        line = next(f)
        while not line.startswith('# format:org_id'):
            line = next(f)
        
        # start processing first line of ORG -> ORG Name data
        # stop when we reach the second block
        #format:org_id|changed|org_name|country|source
        while not line.startswith("# format:aut"):
            line = next(f).strip()
            chunks = line.split('|')
            org_id = chunks[0]
            org_name = chunks[2]
            org_orgname[org_id] = org_name if org_name else org_id # use org_id if org_name is empty

        #Skip the first collection of rows until we find the delimiter marking the start of the second part of the file.
        #line = next(f)
        #while not line.startswith("# format:aut"):
        #    line = next(f)

        # Now process the second part of the file
        # aut|changed |aut_name    |org_id    |opaque_id                            |source
        # 3  |20100927|MIT-GATEWAYS|MIT-2-ARIN|d98c567cda2db06e693f2b574eafe848_ARIN|ARIN
        for line in f:
            line = line.strip()
            chunks = line.split('|')
            asn = chunks[0]
            org = chunks[3]
            asn_org[asn] = org_orgname[org]

    return asn_org

def load_probe2asn_default():
    default_file = os.path.join(this_dir, '../data/probes.txt')
    return load_probe2asn(default_file)

def load_probe2asn(probes_filename):
    probe_asn = {}

    with open(probes_filename) as f:

        for _ in range(0, 3): # skip first 3 lines
            next(f)

        for line in f:
            line = line.strip()

            chunks = line.split()

            if len(chunks) != 2:
                continue

            id = chunks[0]
            asn = chunks[1]

            probe_asn[id] = asn

    return probe_asn

def load_ip2asn_default():
    default_ipasn_file = os.path.join(this_dir, "../data/ip_asn_raw.txt.gz")
    default_ixprefixes_file = os.path.join(this_dir, "../data/ix_prefixes.txt")
    return load_ip2asn(default_ipasn_file, default_ixprefixes_file)

def load_ip2asn(ip_asn_filename, ip_ixp_filename):
    """
    Input ip_asn file format is a prefix<space>ASN per line. The file must be sorted by prefix ascending and then asn ascending to correctly handling multi-origin ASes.

    Input file can be generated using a RIPE Views BGP snapshot:
    bgpdump -m ../Desktop/latest-bview.gz | LC_ALL=C grep -Ev ':|/0' | cut -d '|' -f 6,7 --output-delimiter " " | awk '{ print $1,$NF }' | LC_ALL=C sort -k1V,1V -k2n,2n | uniq > ip_asn_raw.txt

    The ip_ixp file is ixp-name<tab>prefix.

    radix examples https://libraries.io/pypi/ppy-radix
    """
    trie = radix.Radix()

    new_open = gzip.open if ip_asn_filename.endswith('.gz') else open

    # Use TextIOWrapper because of https://bugs.python.org/issue13989
    with io.TextIOWrapper(new_open(ip_asn_filename, 'r')) as f:
        for line in f:
            line = line.strip()
            prefix, asn = line.split()

            node = trie.add(prefix)

            if "asn" in node.data:
                node.data["asn"] += "-" + asn # deal with MOAS
            else:
                node.data["asn"] = asn

    with open(ip_ixp_filename) as f:
        for line in f:
            line = line.strip()
            ixp, prefix = line.split('\t')
            node = trie.add(prefix)
            node.data["asn"] = ixp

    return trie

def dottedQuadToNum(ip):
    "convert decimal dotted quad string to long integer"
    return struct.unpack('>L',socket.inet_aton(ip))[0]

def numToDottedQuad(n):
    "convert long int to dotted quad string"
    return socket.inet_ntoa(struct.pack('>L',n))

def isPublicIPv4AddressInt(asInt):
    return not(0 <= asInt and asInt < 16777216) and \
           not(167772160 <= asInt and asInt < 184549376) and \
           not(1681915904 <= asInt and asInt < 1686110208) and \
           not(2130706432 <= asInt and asInt < 2147483648) and \
           not(2851995648 <= asInt and asInt < 2852061184) and \
           not(2886729728 <= asInt and asInt < 2887778304) and \
           not(3221225472 <= asInt and asInt < 3221225728) and \
           not(3221225984 <= asInt and asInt < 3221226240) and \
           not(3232235520 <= asInt and asInt < 3232301056) and \
           not(3222405120 <= asInt and asInt < 3222536192) and \
           not(3325256704 <= asInt and asInt < 3325256960) and \
           not(3227017984 <= asInt and asInt < 3227018240) and \
           not(3405803776 <= asInt and asInt < 3405804032) and \
           not(3758096384 <= asInt)

class UtilTest(unittest.TestCase):

    def test_load_ip2asn(self):
        trie = load_ip2asn('../data/test/ip_asn_test.txt', '../data/ix_prefixes.txt')
        self.assertEquals("9605", trie.search_best('1.79.89.55').data['asn'])
        self.assertEquals("58368-58369", trie.search_best('116.197.135.99').data['asn'])

        trie = load_ip2asn('../data/test/ip_asn_test.txt.gz', '../data/ix_prefixes.txt')
        self.assertEquals("9605", trie.search_best('1.79.89.55').data['asn'])
        self.assertEquals("58368-58369", trie.search_best('116.197.135.99').data['asn'])

        self.assertIsNone(trie.search_best("192.168.0.1"))

    def test_load_probe2asn(self):
        probe_asn = load_probe2asn('../data/probes.txt')
        self.assertEquals(23407, len(probe_asn))
        self.assertEquals("3265", probe_asn["1"])
        self.assertFalse("3" in probe_asn)

    def test_load_asn2org(self):
        asn_org = load_asn2org_default()
        self.assertEquals(92944, len(asn_org))
        self.assertTrue("1" in asn_org)
        self.assertEquals("Level 3 Parent, LLC", asn_org["1"])

    def test_load_squatspace(self):
        squat_trie = load_squatspace_default()
        self.assertIsNotNone(squat_trie.search_best('7.7.7.7'))
        self.assertIsNotNone(squat_trie.search_best('19.19.19.19'))
        self.assertIsNone(squat_trie.search_best('8.8.8.8'))
        self.assertIsNone(squat_trie.search_best('4.4.4.4'))

    def test_isPublicIPv4AddressInt(self):
        self.assertTrue(isPublicIPv4AddressInt(dottedQuadToNum("8.8.8.8")))
        self.assertFalse(isPublicIPv4AddressInt(dottedQuadToNum("10.1.2.3")))
        self.assertFalse(isPublicIPv4AddressInt(dottedQuadToNum("192.168.4.5")))

if __name__ == '__main__':
    unittest.main()