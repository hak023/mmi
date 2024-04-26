
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_PDE_DIS_LN_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DIS_LN_REQ)
    
    
class MSG_EMS_PDE_DIS_LN_RSP(IbcfResponseMsg):
    
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
   
   stHostInf stLN;

}stPM_DisLNRes;

typedef stPM_DisLNRes Pde_dis_ln_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_DIS_LN_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iI%ds%dshhi%ds%dshh" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc stLN"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_PDE_DIS_LN_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iI%ds%dshhi%ds%dshhi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "temp m_uiID m_szDesc szIP sIPVer sReserved nPort szHost szRealm sProtocol sUseTLS")
        new_list.append(StructInfo._make(unpack("iI%ds%dshhi%ds%dshh" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.stLN)))
        
        response = response._replace(stLN = new_list)
        
        print response
        return response

###############################################################################################################################################
         

class PdeLocCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.request.sReserved = 0
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""


    def printOutputMessage(self, omsg):
        print "\t", "%7s %30s %5s %30s %7s %20s %9s" % ('LOC_ID', 'HOST', 'IPV', 'IP', 'PORT', 'REALM', 'PROTOCOL')
        print "\t", " -----------------------------------------------------------------------------------------------------------------"

        for st in sorted(omsg.stLN) :
            print "\t", "%7d %30s %5s %30s %7d %20s %9s" % (st.m_uiID, self.reprName(st.szHost), self.reprPdeIpVerIntToStr(int(st.sIPVer)),
                                                            self.reprName(st.szIP), st.nPort, self.reprNameShorter(st.szRealm, 30, 25),
                                                            self.reprPdeProctIntToStr(int(st.sProtocol))
                                                            )
            
        if omsg.uiSubType == DEF_STYPE_PDE_DIS_LN_RSP: 
           print ""
           print "%-10s = %s" % ('LOC_CNT', '1')
