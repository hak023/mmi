#!/bin/python2.7 -tt

from struct import unpack
from collections import namedtuple

from mmi.cmd import *
from mmi.ibcf import *
from cls.sip_loc_cls import *
              

class CRTE_SIP_LOC(SipLocCommand):
    
    def __init__(self):
        SipLocCommand.__init__(self, MSG_EMS_CS_ADD_LN_REQ(), MSG_EMS_CS_ADD_LN_RSP())

class UsageException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main(argv=None):

    cmd = CRTE_SIP_LOC()
    opts, args = cmd.getopt(sys.argv[1:])
    
    if len(opts) > 0:
       cmd.processOptions(opts)
       return 0
        
    try:
       args = cmd.validateArgs(args)
       
       cmd.request.m_uiID = int(args[0])
       cmd.request.m_szDesc = args[1]
       cmd.request.m_szDomain = args[2]
       cmd.request.m_usIPver = int(cmd.reprIpVerStrToInt(args[3]))
       cmd.request.m_szIP = args[4]
       cmd.request.m_usPort = int(args[5])
       cmd.request.m_ucProto = int(cmd.reprProcStrToInt(args[6]))
       cmd.request.m_cRCSOn = int(cmd.reprOnOffStrToInt(args[7]))

       cmd.execute(cmd.response.getSize())
        
    except Exception, e:
        cmd.printExcecption(e)
        return 2

if __name__ == "__main__":
    sys.exit(main())








