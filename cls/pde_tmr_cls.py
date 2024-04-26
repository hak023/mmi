
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_PDE_DIS_TMR_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DIS_TIMER_REQ)
    
    
class MSG_EMS_PDE_DIS_TMR_RSP(IbcfResponseMsg):
    
    """
typedef struct{
    unsigned int uiCERTimeout;
    unsigned int uiDWRTimeout;
    unsigned int uiDWRRetry;
    unsigned int uiMsgTimeout;
    unsigned int uiMsgRetry;
}stPM_TimerInf

typedef struct{
    int nResult;
    int nReason;
    char szReasonDesc[128];
    stPM_TimerInf stTimer;

}stPM_DisTimerRes;

typedef stPM_DisTimerRes Pde_dis_timer_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_TMR_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiii")
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stTimer"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_TMR_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiii")
        new_list = []

        StructInfo = namedtuple("StructInfo", "uiCERTimeout uiDWRTimeout uiDWRRetry uiMsgTimeout uiMsgRetry")
        
        new_list.append(StructInfo._make(unpack("iiiii", response.stTimer)))
        response = response._replace(stTimer = new_list)
        
        print response
        return response

###############################################################################################################################################

class PdeTimer_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiii"
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uiCERTimeout uiDWRTimeout uiDWRRetry uiMsgTimeout uiMsgRetry"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uiCERTimeout, self.uiDWRTimeout, self.uiDWRRetry, self.uiMsgTimeout, self.uiMsgRetry);


class PdeTimer_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iiiii")
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stTimer"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiii")
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uiCERTimeout uiDWRTimeout uiDWRRetry uiMsgTimeout uiMsgRetry")
 
        new_list.append(StructInfo._make(unpack("iiiii", response.stTimer)))
        response = response._replace(stTimer = new_list)
        
        print response
        return response

###############################################################################################################################################

class MSG_EMS_PDE_CHG_TMR_REQ(PdeTimer_t_REQ):
    
    def __init__(self):
        PdeTimer_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_CHG_TIMER_REQ)

class MSG_EMS_PDE_CHG_TMR_RSP(PdeTimer_t_RSP):
    
    def __init__(self):
        PdeTimer_t_RSP.__init__(self, DEF_STYPE_PDE_CHG_TIMER_RSP)

###############################################################################################################################################

class PdeTmrCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)

    def printInputMessage(self, imsg):        
        print "\t"
        
        if imsg.uiCERTimeout != 0:
            print "\t" "%16s = %d" % ('INIT_RETRANS_DUR', imsg.uiCERTimeout)
 
        if imsg.uiDWRTimeout != 0:
            print "\t" "%16s = %d" % ('HB_RETRANS_DUR', imsg.uiDWRTimeout)
  
        if imsg.uiDWRRetry != 0:
            print "\t" "%16s = %d" % ('HB_RETRANS_CNT', imsg.uiDWRRetry)

        if imsg.uiMsgTimeout != 0:
            print "\t" "%16s = %d" % ('MSG_RETRANS_DUR', imsg.uiMsgTimeout)

        if imsg.uiMsgRetry !=0:
            print "\t" "%16s = %d" % ('MSG_RETRANS_CNT', imsg.uiMsgRetry)
          

    def printOutputMessage(self, omsg):
        
        for st in omsg.stTimer :
            print "\t" "%25s = %6d(ms)" % ('INIT_RETRANS_DUR', st.uiCERTimeout)
            print "\t" "%25s = %6d(ms)" % ('HB_RETRANS_DUR', st.uiDWRTimeout)
            print "\t" "%25s = %6d(cnt)" % ('HB_RETRANS_CNT', st.uiDWRRetry)
            print "\t" "%25s = %6d(ms)" % ('MSG_RETRANS_DUR', st.uiMsgTimeout)
            print "\t" "%25s = %6d(cnt)" % ('MSG_RETRANS_CNT', st.uiMsgRetry)


   
