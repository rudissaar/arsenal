#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0413
# pylint: disable=W0702

'''
Script that checks if GET parameter can be used to detect SQL injection vulnerability.

Dependencies:
    * python2
        # Debian/Ubuntu: apt-get install python
        # Fedora: dnf install python
'''

INITIAL = "'"

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

RESULT_FILE = 'url-based-sql-injection-' + str(calendar.timegm(time.gmtime())) + '.csv'
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

        try:
            response = requests.post(url + INITIAL, timeout=3)
        except:
            pass

        if 'mysql' in response.text.lower():
            print '> Injectable MySQL detected.'
            found = 'mysql'
        elif 'native client' in response.text.lower():
            print '> Injectable MSSQL detected.'
            found = 'mssql'
        elif 'syntax error' in response.text.lower():
            print '> Injectable PostgreSQL detected.'
            found = 'postgresql'
        elif 'ORA' in response.text.lower():
            print '> Injectable Oracle detected.'
            found = 'oracle'
        else:
            print '> Not Injectable.'

        if bool(found):
            with open(RESULT_FILE, 'a+') as result_file:
                result_file.write(url + ',' + found + "\n")
