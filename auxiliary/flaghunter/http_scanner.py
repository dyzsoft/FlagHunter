#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard modules
import logging
import os

# extra modules
dependencies_missing = False
try:
    import requests
except ImportError:
    dependencies_missing = True
from metasploit import module

metadata = {
    'name': 'AWDFlagHunter utils: http scanner',
    'description': '''
       http scanner
       use (set  TARGETURI '' ) set this value empty
       use (set  TARGETURI_FILE '' ) set this value empty
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
        'TARGETURI': {'type': 'string', 'description': 'Set empty use TARGETURI_FILE to scan!', 'required': True,
                      'default': '/a.php'},
        'TARGETURI_FILE': {'type': 'string', 'description': 'Set empty load default!', 'required': True, 'default': ''},
        'RPORT': {'type': 'port', 'description': 'rport', 'required': True, 'default': 80},
        'SHOW404': {'type': 'bool', 'description': 'log404 error.', 'required': True, 'default': None},
    },
}


def handle_exception(e):

    logging.debug(type(e))

    if isinstance(e, requests.exceptions.RequestException):
        e: requests.exceptions.RequestException
        logging.error('{}'.format(e.request.url))
    else:
        logging.error('{}'.format(e))


def run_scan(schema, host, port, targeturi, verbose=False):
    r = requests.get('{}://{}:{}{}'.format(schema, host, port, targeturi), timeout=3)
    if r.status_code == 200:
        module.log('{}://{}:{}{} success!'.format(schema, host, port, targeturi), level='good')
        module.report_service(host, port=port, info=targeturi, proto='tcp', name=targeturi)
    else:
        if verbose:
            logging.error('{}://{}:{}{}'.format(schema, host, port, targeturi))


def run(args):
    module.LogHandler.setup(msg_prefix='{}:{} - '.format(args['rhost'], args['RPORT']))

    if dependencies_missing:
        logging.error('Module dependency (requests) is missing, cannot continue.')
        logging.error('use (pip install requests) to install the dependency.')
        return
    ##
    logging.debug('Module path:{}'.format(__file__))
    for k in args:
        logging.debug("{}: {}".format(k, args[k]))
    ##
    verbose = False
    show404 = False
    if args['VERBOSE'] == 'true':
        verbose = True
    if args['SHOW404'] == 'true':
        verbose = True

    try:
        if args['TARGETURI'] != '':
            run_scan(args['SCHEMA'], args['rhost'], args['RPORT'], args['TARGETURI'], verbose=verbose)
        else:
            targeturi_file = args['TARGETURI_FILE']
            if targeturi_file == '':
                targeturi_file = os.path.join(os.path.dirname(__file__), 'ctf_webpath.txt')
            with  open(targeturi_file, 'r')  as f:
                uris = f.readlines()
                for uri in uris:
                    uri = uri.strip()
                    if not uri.startswith('/'):
                        uri = '/' + uri
                    run_scan(args['SCHEMA'], args['rhost'], args['RPORT'], uri, verbose=verbose)
                f.close()
    except Exception as e:
        handle_exception(e)


if __name__ == '__main__':
    module.run(metadata, run)
