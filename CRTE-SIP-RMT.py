#!/bin/python2.7 -tt

from struct import unpack
from collections import namedtuple

from mmi.cmd import *
from mmi.ibcf import *
from cls.sip_rmt_cls import *
              

class CRTE_SIP_RMT(SipRmtCommand):
    
    def __init__(self):
        SipRmtCommand.__init__(self, MSG_EMS_CS_ADD_RMT_REQ(), MSG_EMS_CS_ADD_RMT_RSP())

class UsageException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main(argv=None):

    cmd = CRTE_SIP_RMT()
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
       cmd.request.m_sNATOn = int(cmd.reprOnOffStrToInt(args[7]))
       
       if str(args[8]):
          cmd.request.m_nDSCP = int(args[8])
       else:
          cmd.request.m_nDSCP = 0
       
       cmd.request.m_szNATIP = ''
       cmd.request.m_usNATPort = 0

       cmd.execute(cmd.response.getSize())
        
    except Exception, e:
        cmd.printExcecption(e)
        return 2

if __name__ == "__main__":
    sys.exit(main())








