#!/usr/bin/env python


"""
https://github.com/torfsen/service
pip install service

https://pypi.python.org/pypi/schedule
"""

import logging
from logging.handlers import RotatingFileHandler
import time

from service import find_syslog, Service

class MyService(Service):
    def __init__(self, *args, **kwargs):
        super(MyService, self).__init__(*args, **kwargs)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        rfh = RotatingFileHandler('logger.log', mode='a', maxBytes=1024, backupCount=10, encoding='utf8', delay=0)
        rfh.setFormatter(formatter)
        self.logger.addHandler(rfh)
        self.logger.setLevel(logging.INFO)

    def run(self):
        self.logger.info('#'*80)
        self.logger.info('starting')
        while not self.got_sigterm():
            self.logger.info("I'm working...")
            time.sleep(5)
        self.logger.info('stoped')

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = MyService('my_service', pid_dir='/tmp')

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print "Service is running."
        else:
            print "Service is not running."
    else:
        sys.exit('Unknown command "%s".' % cmd)
