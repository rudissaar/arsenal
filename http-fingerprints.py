#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0413
# pylint: disable=W0702

'''
Script that fetches HTTP headers that can be used to fingerprint HTTP server.

Dependencies:
    * python2
        # Debian/Ubuntu: apt-get install python
        # Fedora: dnf install python

    * requests
        # Debian/Ubuntu: apt-get install python-requests
        # Fedora: dnf install python2-requests
'''

HEADERS = ['Server', 'Date', 'Via', 'X-Powered-By', 'X-Country-Code']

import calendar
import os
import sys
import time
import requests

if len(sys.argv) != 2:
    print 'Usage: ' + sys.argv[0] + ' [filename]'
    print "    * filename - File that contains list of urls.\n"
    sys.exit(1)

URLS_FILE = sys.argv[1]

if not os.path.isfile(URLS_FILE):
    print 'Error: file ' + '"' + URLS_FILE + '"' + " doesn't exist.\n"
    sys.exit(1)

URLS = list()

RESULT_FILE = 'http-fingerprints-' + str(calendar.timegm(time.gmtime())) + '.csv'
RESULT_FILE = os.path.dirname(os.path.realpath(__file__)) + '/' + RESULT_FILE

with open(URLS_FILE, 'r') as urls_file:
    for url in urls_file:
        url = url.strip()
        if url not in URLS:
            URLS.append(url)

if bool(URLS):
    for url in URLS:
        print '> Testing URL: ' + url

        for header in HEADERS:
            found = None

            try:
                response = requests.get(url, timeout=3)
                result = response.headers[header]
                print '> Found header: ' + header + ': ' + result
                found = header + ',' + result
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass

            if bool(found):
                with open(RESULT_FILE, 'a+') as result_file:
                    result_file.write(url + ',' + found + "\n")
