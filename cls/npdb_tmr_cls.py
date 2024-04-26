
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_NPDB_DIS_TMR_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_TIMER_NPDB_REQ)
    
    
class MSG_EMS_NPDB_DIS_TMR_RSP(IbcfResponseMsg):
    
    """
typedef struct NpdbTimer_t
{
    int m_nTrTmr;         // Query Retry Time(ms)   Default 6 sec
    int m_nRetryCnt;      // Query Retry Count      Default 1
    int m_nBindRspTmr;    // Bind Retry Time(ms)    Default 30 sec
    int m_nBindRetryCnt;  // Bind Retry Count       Default 1 
    int m_nPingRspTmr;    // Ping Retry Time(ms)    Default 30 sec
    int m_nPingRetryCnt;  // Ping Retry Count       Default 1 
    int m_nRelRspTmr;     // Rel Rsp Wait Time(ms)  Default 30 sec
    int m_nReconTmr;      // Reconnect Time(ms)     Default 30 sec
}NpdbTimer_t;

typedef struct Cs_Npdb_dis_timer_rsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    NpdbTimer_t m_stTimer;
}Cs_Npdb_dis_timer_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_TIMER_NPDB_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiii")
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stTimer"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_TIMER_NPDB_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiii")
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_nTrTmr m_nRetryCnt m_nBindRspTmr m_nBindRetryCnt m_nPingRspTmr m_nPingRetryCnt m_nRelRspTmr m_nReconTmr")
        
        new_list.append(StructInfo._make(unpack("iiiiiiii", response.stTimer)))
        response = response._replace(stTimer = new_list)
        
        print response
        return response

###############################################################################################################################################

class NpdbTimer_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiiiiii"
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nTrTmr m_nRetryCnt m_nBindRspTmr m_nBindRetryCnt m_nPingRspTmr m_nPingRetryCnt m_nRelRspTmr m_nReconTmr"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nTrTmr, self.m_nRetryCnt, self.m_nBindRspTmr, self.m_nBindRetryCnt, self.m_nPingRspTmr, self.m_nPingRetryCnt, self.m_nRelRspTmr, self.m_nReconTmr);


class NpdbTimer_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiii")
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stTimer"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiii")
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nTrTmr m_nRetryCnt m_nBindRspTmr m_nBindRetryCnt m_nPingRspTmr m_nPingRetryCnt m_nRelRspTmr m_nReconTmr")
 
        new_list.append(StructInfo._make(unpack("iiiiiiii", response.stTimer)))
        response = response._replace(stTimer = new_list)
        
        print response
        return response

###############################################################################################################################################

class MSG_EMS_NPDB_CHG_TMR_REQ(NpdbTimer_t_REQ):
    
    def __init__(self):
        NpdbTimer_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_TIMER_NPDB_REQ)

class MSG_EMS_NPDB_CHG_TMR_RSP(NpdbTimer_t_RSP):
    
    def __init__(self):
        NpdbTimer_t_RSP.__init__(self, DEF_STYPE_CS_CHG_TIMER_NPDB_RSP)

###############################################################################################################################################

class NpdbTmrCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)

    def printInputMessage(self, imsg):
        print "\t"
        
        if imsg.m_nTrTmr != 0:
            print "\t" "%16s = %d" % ('TR_TMR', imsg.m_nTrTmr)
 
        if imsg.m_nRetryCnt != 0:
            print "\t" "%16s = %d" % ('RETRY_CNT', imsg.m_nRetryCnt)
  
        if imsg.m_nBindRspTmr != 0:
            print "\t" "%16s = %d" % ('BIND_RSP_TMR', imsg.m_nBindRspTmr)

        if imsg.m_nBindRetryCnt != 0:
            print "\t" "%16s = %d" % ('BIND_RETRY_CNT', imsg.m_nBindRetryCnt)

        if imsg.m_nPingRspTmr !=0:
            print "\t" "%16s = %d" % ('PING_RSP_TMR', imsg.m_nPingRspTmr)
            
        if imsg.m_nPingRetryCnt !=0:
            print "\t" "%16s = %d" % ('PING_RETRY_CNT', imsg.m_nPingRetryCnt)
            
        if imsg.m_nRelRspTmr !=0:
            print "\t" "%16s = %d" % ('REL_RSP_TMR', imsg.m_nRelRspTmr)

        if imsg.m_nReconTmr !=0:
            print "\t" "%16s = %d" % ('RECON_TMR', imsg.m_nReconTmr)
            

    def printOutputMessage(self, omsg):
        print "\t"
        for st in omsg.stTimer :
            print "\t" "%20s = %6d(ms)" % ('TR_TMR', st.m_nTrTmr)
            print "\t" "%20s = %6d(cnt)" % ('RETRY_CNT', st.m_nRetryCnt)
            print "\t" "%20s = %6d(ms)" % ('BIND_RSP_TMR', st.m_nBindRspTmr)
            print "\t" "%20s = %6d(cnt)" % ('BIND_RETRY_CNT', st.m_nBindRetryCnt)
            print "\t" "%20s = %6d(ms)" % ('PING_RSP_TMR', st.m_nPingRspTmr)
            print "\t" "%20s = %6d(cnt)" % ('PING_RETRY_CNT', st.m_nPingRetryCnt)
            print "\t" "%20s = %6d(ms)" % ('REL_RSP_TMR', st.m_nRelRspTmr)
            print "\t" "%20s = %6d(ms)" % ('RECON_TMR', st.m_nReconTmr)


   
