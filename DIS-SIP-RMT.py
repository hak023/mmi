#!/bin/python2.7 -tt

from struct import unpack
from collections import namedtuple

from mmi.cmd import *
from mmi.ibcf import *
from cls.sip_rmt_cls import *

RANGE_ARG_DELIM = '-'
RTE_FAIL_MSG = 'CntRange Paremeter error'

class DIS_SIP_RMT(SipRmtCommand):
    
    def __init__(self):
        SipRmtCommand.__init__(self, MSG_EMS_CS_DIS_RMT_REQ(), MSG_EMS_CS_DIS_RMT_RSP())

    def printInputMessage(self, imsg):
        print ""

class UsageException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main(argv=None):

    cmd = DIS_SIP_RMT()
    opts, args = cmd.getopt(sys.argv[1:])
    
    if len(opts) > 0:
       cmd.processOptions(opts)
       return 0
        
    try:
       args = cmd.validateArgs(args)
                     
       if str(args[0]):
          cmd.request.m_nSort_type = 1
          cmd.request.m_nBegin = int(args[0])
          cmd.request.m_nEnd = int(args[0])
          cmd.isIdxSearch = 1
          cmd.rangeCntStart = 0
          cmd.rangeCntEnd = 0
       elif str(args[1]):
          cmd.request.m_nSort_type = 0
          cmd.request.m_nBegin = 0
          cmd.request.m_nEnd = 0
          cmd.isIdxSearch = 0
          
          _list = args[1].split(RANGE_ARG_DELIM)
          if len(_list) != 2:
             cmd.printExcecption(RTE_FAIL_MSG)
             return 2 
          
          cmd.rangeCntStart = int(_list[0])
          cmd.rangeCntEnd = int(_list[1])
          
          if cmd.rangeCntStart > cmd.rangeCntEnd:
             cmd.printExcecption(RTE_FAIL_MSG)
             return 2
         
          if cmd.rangeCntStart == 0 or cmd.rangeCntEnd == 0:
             cmd.printExcecption(RTE_FAIL_MSG)
             return 2
                   
       else:
          cmd.request.m_nSort_type = 0
          cmd.request.m_nBegin = 0
          cmd.request.m_nEnd = 0
          cmd.isIdxSearch = 0
          cmd.rangeCntStart = 0
          cmd.rangeCntEnd = 0
          
       cmd.request.m_szKey = ""

       cmd.execute(cmd.response.getSize())

    except Exception, e:
        cmd.printExcecption(e)
        return 2

if __name__ == "__main__":
    sys.exit(main())
