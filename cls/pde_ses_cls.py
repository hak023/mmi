
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_PDE_DIS_SES_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DIS_SES_REQ)
    
    
class MSG_EMS_PDE_DIS_SES_RSP(IbcfResponseMsg):
    
    """
typedef struct {
    unsigned int uiID;
    char szDesc[40];
    int nLNID;
    int nRMTID;
    int nCallCnt;
    int nStatus;//_status

}stRTEInf;    
    
typedef struct {
    int nResult;
    int nReason;
    char szReasonDesc[128];

    unsigned int uiNum;//Route Info Number
    stRTEInf stRTE[MAX_PDE_RTE_NUM];

}stPM_DisRTERes;

typedef stPM_DisRTERes Pde_dis_rte_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_DIS_SES_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iI%dsiiii" % (DEF_RTE_MAXLEN_DESC))
        return FMT_UDP_HEADER + "ii%dsI%ds" % (DEF_LM_DESC_LEN, Struct_size * MAX_PDE_RTE_NUM )
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason szReasonDesc uiNum stRTE"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_PDE_DIS_SES_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iI%dsiiii" % (DEF_RTE_MAXLEN_DESC))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "temp m_uiID szDesc nLNID nRMTID nCallCnt nStatus")
        for i in range(response.uiNum) :
            new_list.append(StructInfo._make(unpack("iI%dsiiii" %(DEF_RTE_MAXLEN_DESC), response.stRTE[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(stRTE = new_list)
        
        print response
        return response

#############################################################################################################################################   

class MSG_EMS_DEFAULT_SES_RSP(IbcfResponseMsg):
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        return FMT_UDP_HEADER + "iii%ds" % (DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_uiID m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())
    
    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))     
        
        print response
        return response    

#############################################################################################################################################

class MSG_EMS_PDE_CON_SES_REQ(MSG_EMS_DEFAULT_DEL_REQ):
    
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_CON_SES_REQ)

class MSG_EMS_PDE_CON_SES_RSP(MSG_EMS_DEFAULT_SES_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_ABORT_SES_RSP)

###############################################################################################################################################
        
class MSG_EMS_PDE_ABORT_SES_REQ(MSG_EMS_DEFAULT_DEL_REQ):
    
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_ABORT_SES_REQ)

class MSG_EMS_PDE_ABORT_SES_RSP(MSG_EMS_DEFAULT_SES_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_ABORT_SES_RSP)

###############################################################################################################################################

class MSG_EMS_PDE_SHUTDOWN_SES_REQ(MSG_EMS_DEFAULT_DEL_REQ):
    
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_SHUTDOWN_SES_REQ)

class MSG_EMS_PDE_SHUTDOWN_SES_RSP(MSG_EMS_DEFAULT_SES_RSP):
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_SHUTDOWN_SES_RSP)

###############################################################################################################################################

class PdeSesCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.temp = 0
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('CONN_ID', imsg.m_uiID)


    def printOutputMessage(self, omsg):
        print "\t", "%10s %20s %10s %10s %10s %12s" % ('RTE_ID', 'NAME', 'LOC_ID', 'RMT_ID', 'CALL_CNT', 'STATUS')
        print "\t", " ----------------------------------------------------------------------------"

        for st in sorted(omsg.stRTE) :
            print "\t", "%10d %20s %10d %10d %10d %12s" % (st.m_uiID, self.reprNameShorter(st.szDesc, 20, 15), st.nLNID, st.nRMTID, st.nCallCnt,
                                                           self.reprPdeRteStsIntToStr(st.nStatus))

        if omsg.uiSubType == DEF_STYPE_PDE_DIS_SES_RSP:
           print ""
           print "%-10s = %s" % ('RTE_CNT', omsg.uiNum)

###############################################################################################################################################

   
