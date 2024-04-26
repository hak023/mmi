
from mmi.ibcf import *
from cls.def_cls import *

        
'''
typedef struct Cs_all_act_rte_req
{
   int m_nActFlag;
   int m_nGroupID;
   bool m_bEnableGroup;
   bool m_bIncludeByPass;
   bool bReserved[6];

} Cs_all_act_rte_req_t;
'''

class Route_All_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiBB%ds" % (6)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nActFlag m_nGroupID m_bEnableGroup m_bIncludeByPass bReserved"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nActFlag, self.m_nGroupID, self.m_bEnableGroup, self.m_bIncludeByPass, self.bReserved);

    """

typedef struct Default_rsp {
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN=32];
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN=128];

} Default_rsp_t;
    """

class Route_All_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        return FMT_UDP_HEADER + "i%dsii%ds" % (DEF_LM_NAME_LEN, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nId m_szName m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))     
        
        print response
        return response


class MSG_EMS_CS_ACT_RTE_REQ(Route_All_t_REQ):
    
    def __init__(self):
        Route_All_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ALL_ACT_RTE_REQ)


class MSG_EMS_CS_ACT_RTE_RSP(Route_All_t_RSP):

    def __init__(self):
        Route_All_t_RSP.__init__(self, DEF_STYPE_CS_ALL_ACT_RTE_RSP)


class MSG_EMS_CS_DEACT_RTE_REQ(Route_All_t_REQ):
    
    def __init__(self):
        Route_All_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ALL_DEACT_RTE_REQ)


class MSG_EMS_CS_DEACT_RTE_RSP(Route_All_t_RSP):

    def __init__(self):
        Route_All_t_RSP.__init__(self, DEF_STYPE_CS_ALL_DEACT_RTE_RSP)
        

class MSG_EMS_CS_ACT_RTE_GRP_REQ(Route_All_t_REQ):
    
    def __init__(self):
        Route_All_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ALL_ACT_RTE_GRP_REQ)


class MSG_EMS_CS_ACT_RTE_GRP_RSP(Route_All_t_RSP):

    def __init__(self):
        Route_All_t_RSP.__init__(self, DEF_STYPE_CS_ALL_ACT_RTE_GRP_RSP)


class MSG_EMS_CS_DEACT_RTE_GRP_REQ(Route_All_t_REQ):
    
    def __init__(self):
        Route_All_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ALL_DEACT_RTE_GRP_REQ)


class MSG_EMS_CS_DEACT_RTE_GRP_RSP(Route_All_t_RSP):

    def __init__(self):
        Route_All_t_RSP.__init__(self, DEF_STYPE_CS_ALL_DEACT_RTE_GRP_RSP)


