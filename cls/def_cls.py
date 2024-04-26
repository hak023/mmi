
from mmi.ibcf import *


class MSG_EMS_DEFAULT_DIS_REQ(IbcfRequestMsg):
    
    '''
typedef struct Default_dis_req {
    int m_nSort_type;
    int m_nBegin;
    int m_nEnd;
    char m_szKey[DEF_LM_NAME_LEN=32];
} Default_dis_req_t;
    '''
    
    def __init__(self):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)
        self.isIdxSearch = 0
        
    def getFormat(self):
        return FMT_UDP_HEADER + 'iii%ds' % (DEF_LM_NAME_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nSort_type m_nBegin m_nEnd m_szKey"
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nSort_type, self.m_nBegin, self.m_nEnd, self.m_szKey);

###############################################################################################################################################

class MSG_EMS_DEFAULT_DEL_REQ(IbcfRequestMsg):
 
    '''
typedef struct Default_del_req {
    int m_nId;
} Default_del_req_t;

typedef Default_del_req_t Cs_del_ln_req_t;
    '''
    
    def __init__(self):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + 'i'
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nId"
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nId);


class MSG_EMS_DEFAULT_DEL_RSP(IbcfResponseMsg):

    """
typedef struct Default_rsp {
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN];
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

} Default_rsp_t;

typedef Default_rsp_t Cs_del_ln_rsp_t;
    """
    
    def __init__(self):
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

###############################################################################################################################################
