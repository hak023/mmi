#!/bin/python2.7 -tt

from struct import unpack
from collections import namedtuple

from mmi.cmd import *
from mmi.ibcf import *
from cls.rte_cls import *
              

class CRTE_RTE(SipRteCommand):
    
    def __init__(self):
        SipRteCommand.__init__(self, MSG_EMS_CS_ADD_RTE_REQ(), MSG_EMS_CS_ADD_RTE_RSP())

class UsageException(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main(argv=None):

    cmd = CRTE_RTE()
    opts, args = cmd.getopt(sys.argv[1:])
    
    if len(opts) > 0:
       cmd.processOptions(opts)
       return 0
        
    try:
       args = cmd.validateArgs(args)
       
       cmd.request.m_uiID = int(args[0])
       cmd.request.m_szDesc = args[1]
       cmd.request.m_uiLID = int(args[2])
       cmd.request.m_uiRID = int(args[3])
       cmd.request.m_uiTRTE = int(args[4])
       cmd.request.m_ucType = int(cmd.reprRteTypeStrToInt(args[5]))
       cmd.request.m_ucDoRouteMedia = int(cmd.reprRteMediaStrToInt(args[6]))
       cmd.request.m_sOptTime = int(args[7])
       cmd.request.m_sOptRetry = int(args[8])
       cmd.request.m_sOptAction = int(cmd.reprActionStrToInt(args[9]))
       cmd.request.m_sSesRefreshTime = int(args[10])
       cmd.request.m_nRouteGroup = int(args[11])
       cmd.request.m_nMAXCnt = int(args[12])
       cmd.request.m_nDeactRsp = int(cmd.reprReponseStrToInt(args[13]))

       cmd.execute(cmd.response.getSize())
        
    except Exception, e:
        cmd.printExcecption(e)
        return 2

if __name__ == "__main__":
    sys.exit(main())








