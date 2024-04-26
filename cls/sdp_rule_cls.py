
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_EMP_DIS_SDP_RULE_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_SDP_RULE_REQ)
    
    
class MSG_EMS_EMP_DIS_SDP_RULE_RSP(IbcfResponseMsg):
    
    """

struct st_rulelist : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    unsigned char ucRID;
    unsigned char ucType;                // TYPE
    unsigned char ucKeyCID;              // KEY_CID
    unsigned char ucChgType;             // CHG_TYPE
    int nKeyRate;                        // KEY_RATE

    char szKeyFmtp[e_maxnum_fmtp=256];   // KEY_FMTP 
    char szChgValue[e_maxnum_value=128]; // CHG_VALUE
    char szName[e_maxnum_name=128];

    // st_codec_info
    unsigned char ucType;
    unsigned char ucCID;
    char cDtmf;
    char cMod;
    char cModOrgId;
    char cReserved[3];

    int nFrameRate;
    int nPT;                   //payload type
    int nRate;                 // sample rate
    int nReserved;
    int nParameter;

    short sImgAttrSendX;
    short sImgAttrSendY;
    short sImgAttrRecvX;
    short sImgAttrRecvY;

    char szName[e_maxnum_name=24];
    char szFmtp[e_maxnum_fmtp=256];
    char szFrameSize[e_maxnum_fs=16];
}

typedef struct Emp_dis_sdp_rule_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN=128];
    int m_nNumber;
    st_rulelist m_stData[E_RULE_MAX_LIST=20];
} Emp_dis_sdp_rule_rsp_t;
    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_SDP_RULE_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBBBBBi%ds%ds%dsBBbbb%dsiiiiihhhh%ds%ds%ds" % (E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_NAME, 3, E_MAXNUM_NAME_CODE_IFNO, E_MAXNUM_FMTP, E_MAXNUM_FS))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_RULE_MAX_LIST)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_SDP_RULE_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBBBBBi%ds%ds%dsBBbbb%dsiiiiihhhh%ds%ds%ds" % (E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_NAME, 3, E_MAXNUM_NAME_CODE_IFNO, E_MAXNUM_FMTP, E_MAXNUM_FS))
        new_list = []

        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus ucRID ucType ucKeyCID ucChgType nKeyRate szKeyFmtp szChgValue szName codec_ucType ucCID cDtmf cMod cModOrgId cReserved nFrameRate nPT nRate nReserved nParameter sImgAttrSendX sImgAttrSendY sImgAttrRecvX sImgAttrRecvY codec_szName szFmtp szFrameSize")
        
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("IBBBBBBBBi%ds%ds%dsBBbbb%dsiiiiihhhh%ds%ds%ds" %(E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_NAME, 3, E_MAXNUM_NAME_CODE_IFNO, E_MAXNUM_FMTP, E_MAXNUM_FS), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_EMP_DEL_SDP_RULE_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DEL_SDP_RULE_REQ)

class MSG_EMS_EMP_DEL_SDP_RULE_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DEL_SDP_RULE_RSP)


###############################################################################################################################################

"""
struct st_rulelist : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    unsigned char ucRID;
    unsigned char ucType;                // TYPE
    unsigned char ucKeyCID;              // KEY_CID
    unsigned char ucChgType;             // CHG_TYPE
    int nKeyRate;                        // KEY_RATE

    char szKeyFmtp[e_maxnum_fmtp=256];   // KEY_FMTP 
    char szChgValue[e_maxnum_value=128]; // CHG_VALUE
    char szName[e_maxnum_name=128];

    // st_codec_info
    unsigned char ucType;
    unsigned char ucCID;
    char cDtmf;
    char cMod;
    char cModOrgId;
    char cReserved[3];

    int nFrameRate;
    int nPT;                   //payload type
    int nRate;                 // sample rate
    int nReserved;
    int nParameter;

    short sImgAttrSendX;
    short sImgAttrSendY;
    short sImgAttrRecvX;
    short sImgAttrRecvY;

    char szName[e_maxnum_name=24];
    char szFmtp[e_maxnum_fmtp=256];
    char szFrameSize[e_maxnum_fs=16];
}

typedef st_rulelist Emp_add_sdp_rule_req_t;


"""

class SdpRuleList_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        self.uReason = 0
        self.ucEnabled = 0
        self.ucValid = 0
        self.ucID = 0
        self.ucStatus = 0        
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "IBBBBBBBBi%ds%ds%dsBBbbb%dsiiiiihhhh%ds%ds%ds" % (E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_NAME, 3, E_MAXNUM_NAME_CODE_IFNO, E_MAXNUM_FMTP, E_MAXNUM_FS)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uReason ucEnabled ucValid ucID ucStatus ucRID ucType ucKeyCID ucChgType nKeyRate szKeyFmtp szChgValue szName codec_ucType ucCID cDtmf cMod cModOrgId cReserved nFrameRate nPT nRate nReserved nParameter sImgAttrSendX sImgAttrSendY sImgAttrRecvX sImgAttrRecvY codec_szName szFmtp szFrameSize"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uReason, self.ucEnabled, self.ucValid, self.ucID, self.ucStatus, \
                    self.ucRID, self.ucType, self.ucKeyCID, self.ucChgType, self.nKeyRate, self.szKeyFmtp, self.szChgValue, self.szName, \
                    self.codec_ucType, self.ucCID, self.cDtmf, self.cMod, self.cModOrgId, self.cReserved, \
                    self.nFrameRate, self.nPT, self.nRate, self.nReserved, self.nParameter, \
                    self.sImgAttrSendX, self.sImgAttrSendY, self.sImgAttrRecvX, self.sImgAttrRecvY, \
                    self.codec_szName, self.szFmtp, self.szFrameSize);

    """ 
typedef struct Emp_add_sdp_rule_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    st_rulelist m_stRule;

} Emp_add_sdp_rule_rsp_t;
    """

class SdpRuleList_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBBBBBi%ds%ds%dsBBbbb%dsiiiiihhhh%ds%ds%ds" % (E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_NAME, 3, E_MAXNUM_NAME_CODE_IFNO, E_MAXNUM_FMTP, E_MAXNUM_FS))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBBBBBi%ds%ds%dsBBbbb%dsiiiiihhhh%ds%ds%ds" % (E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_NAME, 3, E_MAXNUM_NAME_CODE_IFNO, E_MAXNUM_FMTP, E_MAXNUM_FS))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus ucRID ucType ucKeyCID ucChgType nKeyRate szKeyFmtp szChgValue szName codec_ucType ucCID cDtmf cMod cModOrgId cReserved nFrameRate nPT nRate nReserved nParameter sImgAttrSendX sImgAttrSendY sImgAttrRecvX sImgAttrRecvY codec_szName szFmtp szFrameSize")
 
        new_list.append(StructInfo._make(unpack("IBBBBBBBBi%ds%ds%dsBBbbb%dsiiiiihhhh%ds%ds%ds" %(E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_NAME, 3, E_MAXNUM_NAME_CODE_IFNO, E_MAXNUM_FMTP, E_MAXNUM_FS), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_EMP_ADD_SDP_RULE_REQ(SdpRuleList_t_REQ):

    def __init__(self):
        SdpRuleList_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_ADD_SDP_RULE_REQ)

class MSG_EMS_EMP_ADD_SDP_RULE_RSP(SdpRuleList_t_RSP):

    def __init__(self):
        SdpRuleList_t_RSP.__init__(self, DEF_STYPE_EMP_ADD_SDP_RULE_RSP)

###############################################################################################################################################

class MSG_EMS_EMP_CHG_SDP_RULE_REQ(SdpRuleList_t_REQ):
    
    def __init__(self):
        SdpRuleList_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_SDP_RULE_REQ)

class MSG_EMS_EMP_CHG_SDP_RULE_RSP(SdpRuleList_t_RSP):
    
    def __init__(self):
        SdpRuleList_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_SDP_RULE_RSP)

###############################################################################################################################################

class SdpRuleCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved = ''
        self.request.m_ucStatus = 0
        self.request.m_ucUsed = 0
        self.request.m_usReserved2 = 0
        self.request.m_nIndex = 0
        
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RID', imsg.ucRID)
        if imsg.ucType != '':
            print "\t" "%12s = %s" % ('TYPE', self.reprTypeIntToStr(imsg.ucType))
        if imsg.ucKeyCID != -1:
            print "\t" "%12s = %s" % ('CID', imsg.ucKeyCID)
        if imsg.nKeyRate != -1:
            print "\t" "%12s = %s" % ('KEY_RATE', imsg.nKeyRate)
        if imsg.szKeyFmtp != '':
            print "\t" "%12s = %s" % ('KEY_FMTP', self.reprName(imsg.szKeyFmtp))
        if imsg.ucChgType != -1:    
            print "\t" "%12s = %s" % ('CHG_TYPE', self.reprChgTypeIntToStr(imsg.ucChgType))
        if imsg.szChgValue != '':
            print "\t" "%12s = %s" % ('CHG_VALUE', self.reprName(imsg.szChgValue))            
  

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", " %5s %8s %10s %10s %50s %10s %10s" % ('RID', 'TYPE', 'CID', 'KEY_RATE', 'KEY_FMTP', 'CHG_TYPE', 'CHG_VALUE')
           print "\t", "--------------------------------------------------------------------------------------------------------------"

           for rule in sorted(omsg.m_stData) :
               print "\t", " %5d %8s %10d %10d %50s %10s %10s" % \
                             (rule.ucRID, self.reprTypeIntToStr(rule.ucType), rule.ucKeyCID, rule.nKeyRate,
                              self.reprNameShorter(rule.szKeyFmtp, 50, 45), self.reprChgTypeIntToStr(rule.ucChgType), 
                              self.reprNameShorter(rule.szChgValue, 10, 5)
                              )
        
        elif self.isIdxSearch == 1:
           for rule in omsg.m_stData :
               print "\t"
               print "\t" "%10s : %d" % ('RID', rule.ucRID)
               print "\t" "%10s : %s" % ('TYPE', self.reprTypeIntToStr(rule.ucType))
               print "\t" "%10s : %d" % ('CID', rule.ucKeyCID)
               print "\t" "%10s : %d" % ('KEY_RATE', rule.nKeyRate)
               print "\t" "%10s : %s" % ('KEY_FMTP', self.reprName(rule.szKeyFmtp))
               print "\t" "%10s : %s" % ('CHG_TYPE', self.reprChgTypeIntToStr(rule.ucChgType))
               print "\t" "%10s : %s" % ('CHG_VALUE', self.reprName(rule.szChgValue))
             
        if omsg.uiSubType == DEF_STYPE_EMP_DIS_SDP_RULE_RSP:
           print ""
           print "%-10s = %s" % ('RULE_LIST_CNT', omsg.m_nNumber)

   
