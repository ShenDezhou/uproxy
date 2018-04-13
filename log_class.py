__author__ = 'shendezhou'

import logging
import sys
import time
import os

module_name = "uproxy"
process_name = "uproxy"
req_id = "%08d" % os.getpid()

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance. """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
        self.req_id = "%08d" % os.getpid()
        self.module_name = module_name

        #print self.req_id
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

logging.basicConfig( level=logging.DEBUG, format='['+module_name+":"+process_name+']['+req_id+'] %(levelname)s %(asctime)s [%(message)s]' )

#
stdout_logger = logging.getLogger('STDOUT')
#print stdout_logger
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('STDERR')
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

#print "test"
#if __name__ == "__main__":
# print "test"
