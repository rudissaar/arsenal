#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0413
# pylint: disable=W0702

'''
Script that enumerates available HTTP methods.

Dependencies:
    * python2
        # Debian/Ubuntu: apt-get install python
        # Fedora: dnf install python
'''

VERBS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'TEST']

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

RESULT_FILE = 'http-methods-' + str(calendar.timegm(time.gmtime())) + '.csv'
RESULT_FILE = os.path.dirname(os.path.realpath(__file__)) + '/' + RESULT_FILE

with open(URLS_FILE, 'r') as urls_file:
    for url in urls_file:
        url = url.strip()
        if url not in URLS:
            URLS.append(url)

if bool(URLS):
    for url in URLS:
        print '> Testing URL: ' + url

        for verb in VERBS:
            found = None

            try:
                response = requests.request(verb, url, timeout=3)
                found = verb + ',' + str(response.status_code) + ',' + response.reason
            except:
                pass

            if bool(found):
                with open(RESULT_FILE, 'a+') as result_file:
                    result_file.write(url + ',' + found + "\n")
