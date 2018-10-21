#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=redefined-builtin
# pylint: disable=undefined-variable
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position

'''
Script that tries to discover live hosts on specified IP range in C class by pinging them.

Dependencies:
    * python2
        # Debian/Ubuntu: apt-get install python
        # Fedora: dnf install python

    * scapy
        # Debian/Ubuntu: apt-get install python-scapy
        # Fedora: dnf install python2-scapy
'''

import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

import sys
from socket import error as socket_error
from scapy.all import *

if len(sys.argv) != 3:
    print 'Usage: ' + sys.argv[0] + '[start-ip] [end-ip]'
    print "    * start-ip - First IP address to be scanned."
    print "    * end-ip - Last IP address to be scanned.\n"
    sys.exit(1)

live_hosts = []

ip_regex = re.compile('^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$')

if ip_regex.match(sys.argv[1]) is None:
    print '> Starting IP address is invalid.'
    sys.exit(1)

if ip_regex.match(sys.argv[2]) is None:
    print '> End IP address is invalid.'
    sys.exit(1)

ip_list_1 = sys.argv[1].split('.')
ip_list_2 = sys.argv[2].split('.')

if not (ip_list_1[0] == ip_list_2[0] and ip_list_1[1] == ip_list_2[1] and ip_list_1[2] == ip_list_2[2]):
    print '> IP addresses are not in the same class C subnet.'
    sys.exit(1)

if ip_list_1[3] > ip_list_2[3]:
    print '> Starting IP address is greater than ending IP address.'
    sys.exit(1)

network_addr = ip_list_1[0] + '.' + ip_list_1[1] + '.' + ip_list_1[2] + '.'

start_ip_last_octet = int(ip_list_1[3])
end_ip_last_octet = int(ip_list_2[3])

try:
    for x in range(start_ip_last_octet, end_ip_last_octet + 1):
        print '> Pinging ' + network_addr + str(x)
        packet = IP(dst=network_addr + str(x))/ICMP()
        response = sr1(packet, timeout=2, verbose=0)

        if not response is None:
            if response[ICMP].type == 0:
                live_hosts.append(network_addr + str(x))
except socket_error as err:
    if err.errno == 1:
        print "> You don't have enough permissions to run this script."
    else:
        print "> Unexpected socket error occurred."
    sys.exit(1)
except KeyboardInterrupt:
    pass

print '> Scanning finished.' + "\n"

if bool(live_hosts):
    print '> Live hosts found:'

    for host in live_hosts:
        print host
else:
    print '> No live hosts found.'
