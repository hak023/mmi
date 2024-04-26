
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_PDE_DIS_RTE_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DIS_RTE_REQ)
    
    
class MSG_EMS_PDE_DIS_RTE_RSP(IbcfResponseMsg):
    
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
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_DIS_RTE_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iI%dsiiii" % (DEF_RTE_MAXLEN_DESC))
        return FMT_UDP_HEADER + "ii%dsI%ds" % (DEF_LM_DESC_LEN, Struct_size * MAX_PDE_RTE_NUM )
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc uiNum stRTE"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_PDE_DIS_RTE_RSP unpack'
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
    
###############################################################################################################################################

'''
typedef struct {
   unsigned int uiID;
   int nResult;
   int nReason;
   char szReasonDesc[32];

}stPM_ComRes;
'''

class MSG_EMS_PDE_DEL_RTE_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DEL_RTE_REQ)

class MSG_EMS_PDE_DEL_RTE_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_DEL_RTE_RSP)
        
    def getFormat(self):
        return FMT_UDP_HEADER + "Iii%ds" % (DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nId m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())
    
    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))     
        
        print response
        return response        


###############################################################################################################################################

class PdeRoute_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iI%dsiiii" % (DEF_RTE_MAXLEN_DESC)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " temp m_uiID szDesc nLNID nRMTID nCallCnt nStatus"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.temp, self.m_uiID, self.szDesc, self.nLNID, self.nRMTID, self.nCallCnt, self.nStatus);

    """
typedef struct {
    int nResult;
    int nReason;
    char szReasonDesc[32];

    stRTEInf stRTE;

}stPM_AddRTERes
    """

class PdeRoute_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iI%dsiiii" % (DEF_RTE_MAXLEN_DESC))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stRTE"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iI%dsiiii" % (DEF_RTE_MAXLEN_DESC))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "temp m_uiID szDesc nLNID nRMTID nCallCnt nStatus")
 
        new_list.append(StructInfo._make(unpack("iI%dsiiii" %(DEF_RTE_MAXLEN_DESC), response.stRTE)))
        response = response._replace(stRTE = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_PDE_ADD_RTE_REQ(PdeRoute_t_REQ):
    
    def __init__(self):
        PdeRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_ADD_RTE_REQ)


class MSG_EMS_PDE_ADD_RTE_RSP(PdeRoute_t_RSP):

    def __init__(self):
        PdeRoute_t_RSP.__init__(self, DEF_STYPE_PDE_ADD_RTE_RSP)

###############################################################################################################################################

class MSG_EMS_PDE_CHG_RTE_REQ(PdeRoute_t_REQ):
    
    def __init__(self):
        PdeRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_CHG_RTE_REQ)

class MSG_EMS_PDE_CHG_RTE_RSP(PdeRoute_t_RSP):
    
    def __init__(self):
        PdeRoute_t_RSP.__init__(self, DEF_STYPE_PDE_CHG_RTE_RSP)

###############################################################################################################################################

class PdeRteCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.temp = 0
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RTE_ID', imsg.m_uiID)

        if imsg.szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.szDesc))

        if imsg.nLNID != -1:
            print "\t" "%12s = %d" % ('LOC_ID', imsg.nLNID)

        if imsg.nRMTID != -1:
            print "\t" "%12s = %d" % ('RMT_ID', imsg.nRMTID)

        if imsg.nCallCnt != -1:
            print "\t" "%12s = %d" % ('CALL_CNT', imsg.nCallCnt)
            
        if imsg.nStatus != -1:
            print "\t" "%12s = %s" % ('STATUS', self.reprPdeRteStsIntToStr(imsg.nStatus))


    def printOutputMessage(self, omsg):
        print "\t", "%10s %20s %10s %10s %10s %12s" % ('RTE_ID', 'NAME', 'LOC_ID', 'RMT_ID', 'CALL_CNT', 'STATUS')
        print "\t", " ----------------------------------------------------------------------------"

        for st in sorted(omsg.stRTE) :
            print "\t", "%10d %20s %10d %10d %10d %12s" % (st.m_uiID, self.reprNameShorter(st.szDesc, 20, 15), st.nLNID, st.nRMTID, st.nCallCnt,
                                                           self.reprPdeRteStsIntToStr(st.nStatus))

        if omsg.uiSubType == DEF_STYPE_PDE_DIS_RTE_RSP:
           print ""
           print "%-10s = %s" % ('RTE_CNT', omsg.uiNum)

###############################################################################################################################################

   