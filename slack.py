#!/usr/bin/env python2
#
# Slack alert script for Pushover
# (c) 2016, Entertainment Media Group AG
# License: MIT
#

from __future__ import print_function

import httplib
import os.path
import urllib
from ConfigParser import RawConfigParser
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sys import stderr, exit
import json
import re

# parse cli argumennts
parser = ArgumentParser(description='Zabbix Slack Client', version='0.1',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', nargs='?', default=os.path.dirname(os.path.abspath(__file__)) + '/slack.cfg',
                    help='The configuration file to use')
parser.add_argument('to', help="Receiving user or channel")
parser.add_argument('subject', help='Message subject')
parser.add_argument('message', help='Message body')
args = parser.parse_args()

# read config
if not os.path.exists(args.c):
    print('Could not find configuration file: ' + args.c, end='\n', file=stderr)
    exit(1)

config = RawConfigParser()
config.read(args.c)

# determine message color
color = 'none'

if config.get('slack', 'good') and re.match(config.get('slack', 'good'), args.subject):
    color = 'good'
elif config.get('slack', 'warning') and re.match(config.get('slack', 'warning'), args.subject):
    color = 'warning'
elif config.get('slack', 'danger') and re.match(config.get('slack', 'danger'), args.subject):
    color = 'danger'

# send API request
options = {
    'attachments': [{
        'fallback': args.subject + '\n' + args.message,
        'color': color,
        'title': args.subject,
        'text': args.message,
        # 'fields': [{
        #     'title': args.subject,
        #     'value': args.message
        # }]
    }]
}

if config.get('slack', 'username'):
    options['username'] = config.get('slack', 'username')

if config.get('slack', 'icon_emoji'):
    options['icon_emoji'] = config.get('slack', 'icon_emoji')

conn = httplib.HTTPSConnection('hooks.slack.com:443')
conn.request(
    'POST',
    '/services/' + config.get('slack', 'webhook_token'),
    json.dumps(options),
    {'Content-type': 'application/json'}
)

res = conn.getresponse()

if res.status != 200:
    print('Slack API returned error: ' + res.read(), end='\n', file=stderr)
    exit(1)
