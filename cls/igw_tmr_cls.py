
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_IGW_DIS_TMR_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_TIMER_IGW_REQ)
    
    
class MSG_EMS_IGW_DIS_TMR_RSP(IbcfResponseMsg):
    
    """

typedef struct HlrTimer_t
{
    int m_nTrTmr;           // Query Retry Time(ms)    Default 6 sec
    int m_nRetryCnt;        // Query Retry Count       Default 1
    int m_nConReqRspTmr;    // Con Req Retry Time(ms)  Default 30 sec
    int m_nConReqRetryCnt;  // Con Req Retry Count     Default 1 
    int m_nConChkRspTmr;    // Con Chek Retry Time(ms) Default 30 sec
    int m_nConChkRetryCnt;  // Con Check Retry Count   Default 1 
    int m_nRelReqRspTmr;    // Rel RR Wait Time(ms)    Default 30 sec
    int m_nReconTmr;        // Reconnect Time(ms)      Default 30 sec
}HlrTimer_t;

typedef struct Cs_Hlr_dis_timer_rsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    HlrTimer_t m_stTimer;
}Cs_Hlr_dis_timer_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_TIMER_IGW_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiii")
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stTimer"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_TIMER_IGW_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiii")
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_nTrTmr m_nRetryCnt m_nConReqRspTmr m_nConReqRetryCnt m_nConChkRspTmr m_nConChkRetryCnt m_nRelReqRspTmr m_nReconTmr")
        
        new_list.append(StructInfo._make(unpack("iiiiiiii", response.stTimer)))
        response = response._replace(stTimer = new_list)
        
        print response
        return response

###############################################################################################################################################

class IgwTimer_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiiiiii"
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nTrTmr m_nRetryCnt m_nConReqRspTmr m_nConReqRetryCnt m_nConChkRspTmr m_nConChkRetryCnt m_nRelReqRspTmr m_nReconTmr"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nTrTmr, self.m_nRetryCnt, self.m_nConReqRspTmr, self.m_nConReqRetryCnt, 
                    self.m_nConChkRspTmr, self.m_nConChkRetryCnt, 
                    self.m_nRelReqRspTmr, self.m_nReconTmr);


class IgwTimer_t_RSP(IbcfResponseMsg):

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
        
        StructInfo = namedtuple("StructInfo", "m_nTrTmr m_nRetryCnt m_nConReqRspTmr m_nConReqRetryCnt m_nConChkRspTmr m_nConChkRetryCnt m_nRelReqRspTmr m_nReconTmr")
 
        new_list.append(StructInfo._make(unpack("iiiiiiii", response.stTimer)))
        response = response._replace(stTimer = new_list)
        
        print response
        return response

###############################################################################################################################################

class MSG_EMS_IGW_CHG_TMR_REQ(IgwTimer_t_REQ):
    
    def __init__(self):
        IgwTimer_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_TIMER_IGW_REQ)

class MSG_EMS_IGW_CHG_TMR_RSP(IgwTimer_t_RSP):
    
    def __init__(self):
        IgwTimer_t_RSP.__init__(self, DEF_STYPE_CS_CHG_TIMER_IGW_RSP)

###############################################################################################################################################

class IgwTmrCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)

    def printInputMessage(self, imsg):        
        print "\t"
        
        if imsg.m_nTrTmr != 0:
            print "\t" "%16s = %d" % ('TR_TMR', imsg.m_nTrTmr)
 
        if imsg.m_nRetryCnt != 0:
            print "\t" "%16s = %d" % ('RETRY_CNT', imsg.m_nRetryCnt)
  
        if imsg.m_nConReqRspTmr != 0:
            print "\t" "%16s = %d" % ('CONREQ_RSP_TMR', imsg.m_nConReqRspTmr)

        if imsg.m_nConReqRetryCnt != 0:
            print "\t" "%16s = %d" % ('CONREQ_RETRY_CNT', imsg.m_nConReqRetryCnt)

        if imsg.m_nConChkRspTmr !=0:
            print "\t" "%16s = %d" % ('CONCHK_RSP_TMR', imsg.m_nConChkRspTmr)
            
        if imsg.m_nConChkRetryCnt !=0:
            print "\t" "%16s = %d" % ('CONCHK_RETRY_CNT', imsg.m_nConChkRetryCnt)
            
        if imsg.m_nRelReqRspTmr !=0:
            print "\t" "%16s = %d" % ('RELREQ_RSP_TMR', imsg.m_nRelReqRspTmr)

        if imsg.m_nReconTmr !=0:
            print "\t" "%16s = %d" % ('RECON_TMR', imsg.m_nReconTmr)
            

    def printOutputMessage(self, omsg):
        print "\t"
        for st in omsg.stTimer :
            print "\t" "%20s = %6d(ms)" % ('TR_TMR', st.m_nTrTmr)
            print "\t" "%20s = %6d(cnt)" % ('RETRY_CNT', st.m_nRetryCnt)
            print "\t" "%20s = %6d(ms)" % ('CONREQ_RSP_TMR', st.m_nConReqRspTmr)
            print "\t" "%20s = %6d(cnt)" % ('CONREQ_RETRY_CNT', st.m_nConReqRetryCnt)
            print "\t" "%20s = %6d(ms)" % ('CONCHK_RSP_TMR', st.m_nConChkRspTmr)
            print "\t" "%20s = %6d(cnt)" % ('CONCHK_RETRY_CNT', st.m_nConChkRetryCnt)
            print "\t" "%20s = %6d(ms)" % ('RELREQ_RSP_TMR', st.m_nRelReqRspTmr)
            print "\t" "%20s = %6d(ms)" % ('RECON_TMR', st.m_nReconTmr)


   