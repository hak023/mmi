#!/bin/python2.7 -tt

from struct import unpack
from collections import namedtuple

from mmi.cmd import *
from mmi.ibcf import *
from cls.env_cls import *


class DIS_SIP_ENV(EnvCommand):
    
    def __init__(self):
        EnvCommand.__init__(self, MSG_EMS_CS_DIS_ENV_REQ(), MSG_EMS_CS_DIS_ENV_RSP())

    def printInputMessage(self, imsg):
        print ""

class UsageException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main(argv=None):

    cmd = DIS_SIP_ENV()
    opts, args = cmd.getopt(sys.argv[1:])
    
    if len(opts) > 0:
       cmd.processOptions(opts)
       return 0
        
    try:
       args = cmd.validateArgs(args)

       cmd.request.m_nSort_type = 0
       cmd.request.m_nBegin = 0
       cmd.request.m_nEnd = 0
       cmd.isIdxSearch = 0
       cmd.request.m_szKey = ""

       cmd.execute(cmd.response.getSize())

    except Exception, e:
        cmd.printExcecption(e)
        return 2

if __name__ == "__main__":
    sys.exit(main())
