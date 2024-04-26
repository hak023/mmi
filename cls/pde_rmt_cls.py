
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_PDE_DIS_RMT_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DIS_RMT_REQ)
    
    
class MSG_EMS_PDE_DIS_RMT_RSP(IbcfResponseMsg):
    
    """
typedef struct {
    int temp
    unsigned int m_uiID;
    char szDesc[DEF_RTE_MAXLEN_DESC=40];
    char szIP[DEF_RTE_MAXLEN_IP=40];
    short sIPVer;      //0:ver4 , 1:ver6
    short sReserved;
    int nPort;
    char szHost[DEF_LM_RULE_STRING_SZ=128];
    char szRealm[DEF_LM_RULE_STRING_SZ=128];
    short sProtocol;   //_proto
    short sUseTLS;     //0: not use, 1: use
    
}stHostInf;    
    
typedef struct {
    int nResult;
    int nReason;
    char szReasonDesc[128];

    unsigned int uiNum;//Remote Info Number
    stHostInf stRMT[MAX_PDE_RMT_NUM];

}stPM_DisRMTRes;

typedef stPM_DisRTERes Pde_dis_rte_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_DIS_RMT_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iI%ds%dshhi%ds%dshh" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%dsI%ds" % (DEF_LM_DESC_LEN, Struct_size * MAX_PDE_RMT_NUM )
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc uiNum stRMT"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_PDE_DIS_RMT_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iI%ds%dshhi%ds%dshh" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "temp m_uiID szDesc szIP sIPVer sReserved nPort szHost szRealm sProtocol sUseTLS")
        for i in range(response.uiNum) :
            new_list.append(StructInfo._make(unpack("iI%ds%dshhi%ds%dshh" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.stRMT[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(stRMT = new_list)
        
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

class MSG_EMS_PDE_DEL_RMT_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DEL_RMT_REQ)

class MSG_EMS_PDE_DEL_RMT_RSP(IbcfResponseMsg):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_DEL_RMT_RSP)
    
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

class PdeNodeRemote_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iI%ds%dshhi%ds%dshh" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " temp m_uiID szDesc szIP sIPVer sReserved nPort szHost szRealm sProtocol sUseTLS"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.temp, self.m_uiID, self.szDesc, self.szIP, self.sIPVer, self.sReserved, \
                    self.nPort, self.szHost, self.szRealm, self.sProtocol, self.sUseTLS);

    """
typedef struct {
    int nResult;
    int nReason;
    char szReasonDesc[32];
    stHostInf stRMT;

}stPM_AddRMTRes;
    """

class PdeNodeRemote_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iI%ds%dshhi%ds%dshh" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stRMT"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iI%ds%dshhi%ds%dshh" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "temp m_uiID szDesc szIP sIPVer sReserved nPort szHost szRealm sProtocol sUseTLS")
 
        new_list.append(StructInfo._make(unpack("iI%ds%dshhi%ds%dshh" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.stRMT)))
        response = response._replace(stRMT = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_PDE_ADD_RMT_REQ(PdeNodeRemote_t_REQ):
    
    def __init__(self):
        PdeNodeRemote_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_ADD_RMT_REQ)


class MSG_EMS_PDE_ADD_RMT_RSP(PdeNodeRemote_t_RSP):

    def __init__(self):
        PdeNodeRemote_t_RSP.__init__(self, DEF_STYPE_PDE_ADD_RMT_RSP)

###############################################################################################################################################

class MSG_EMS_PDE_CHG_RMT_REQ(PdeNodeRemote_t_REQ):
    
    def __init__(self):
        PdeNodeRemote_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_CHG_RMT_REQ)

class MSG_EMS_PDE_CHG_RMT_RSP(PdeNodeRemote_t_RSP):
    
    def __init__(self):
        PdeNodeRemote_t_RSP.__init__(self, DEF_STYPE_PDE_CHG_RMT_RSP)

###############################################################################################################################################

class PdeRmtCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.isIdxSearch = 0
        
        self.request.temp = 0
        self.request.sReserved = 0
        self.request.sIPVer = -1
        self.request.sUseTLS = -1
        self.request.sProtocol = -1
        

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RMT_ID', imsg.m_uiID)

        if imsg.szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.szDesc))

        if imsg.szIP != '':
            print "\t" "%12s = %s" % ('IP', self.reprName(imsg.szIP))
            
        if imsg.nPort != -1:    
            print "\t" "%12s = %d" % ('PORT', imsg.nPort)            

        if imsg.szHost != '':
            print "\t" "%12s = %s" % ('HOST', self.reprName(imsg.szHost))

        if imsg.szRealm != '':
            print "\t" "%12s = %s" % ('REALM', self.reprName(imsg.szRealm))


    def printOutputMessage(self, omsg):
        print "\t", "%7s %20s %5s %30s %7s %30s %20s %9s" % ('RMT_ID', 'NAME', 'IPV', 'IP', 'PORT', 'HOST', 'REALM', 'PROTOCOL')
        print "\t", " --------------------------------------------------------------------------------------------------------------------------------------"

        for st in sorted(omsg.stRMT) :
            print "\t", "%7d %20s %5s %30s %7d %30s %20s %9s" % (st.m_uiID, self.reprNameShorter(st.szDesc, 20, 15), self.reprPdeIpVerIntToStr(int(st.sIPVer)),
                                                                 self.reprName(st.szIP), st.nPort, self.reprName(st.szHost), self.reprNameShorter(st.szRealm, 30, 25),
                                                                 self.reprPdeProctIntToStr(int(st.sProtocol))
                                                                )
        if omsg.uiSubType == DEF_STYPE_PDE_DIS_RMT_RSP:
           print ""
           print "%-10s = %s" % ('RMT_CNT', omsg.uiNum)

###############################################################################################################################################

   