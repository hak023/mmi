#!/bin/python2.7 -tt

from struct import unpack
from collections import namedtuple

from mmi.cmd import *
from mmi.ibcf import *
from cls.rte_cls import *


class DEL_RTE(IbcfCommand):
    
    def __init__(self):
        IbcfCommand.__init__(self, MSG_EMS_CS_DEL_RTE_REQ(), MSG_EMS_CS_DEL_RTE_RSP())
     
    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RTE', imsg.m_nId)

    def printOutputMessage(self, omsg):
        pass


class UsageException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main(argv=None):

    cmd = DEL_RTE()
    opts, args = cmd.getopt(sys.argv[1:])
    
    if len(opts) > 0:
       cmd.processOptions(opts)
       return 0
        
    try:
       args = cmd.validateArgs(args)
       cmd.request.m_nId = int(args[0])

       cmd.execute(cmd.response.getSize())

    except Exception, e:
        cmd.printExcecption(e)
        return 2

if __name__ == "__main__":
    sys.exit(main())
