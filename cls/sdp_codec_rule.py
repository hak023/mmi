
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_EMP_DIS_SDP_CODEC_RULE_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_SDP_UA_RULE_REQ)
    
    
class MSG_EMS_EMP_DIS_SDP_CODEC_RULE_RSP(IbcfResponseMsg):
    
    """
struct st_sdp_rule : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nRID;                            //SDP Rule ID
    unsigned char ucMaching;             // Full-Maching or Partial Maching.
    unsigned char ucCondition;           // include or Exclude.
    unsigned char ucReserved[2];         // Reserved Field.
    int nCallerTrte;                     // Caller TrTe 
    int nCalledTrte;                     // Called TrTe 
    int nCallerGroupId;
    int nCalledGroupId;
    
    char szName[e_maxnum_name=128];      // RuleName
    char szUserAgent[e_maxnum_name=128]; // User-Agent 
};

typedef struct Emp_dis_sdp_ua_rule_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    int m_nNumber;
    st_sdp_rule m_stData[E_CODEC_MAX_SDP_RULE];
} Emp_dis_sdp_ua_rule_rsp_t;
    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_SDP_UA_RULE_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBiBB%dsiiii%ds%ds" % (2, E_MAXNUM_NAME, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_CODEC_MAX_SDP_RULE)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_SDP_UA_RULE_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBiBB%dsiiii%ds%ds" % (2, E_MAXNUM_NAME, E_MAXNUM_NAME))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nRID ucMaching ucCondition ucReserved nCallerTrte nCalledTrte nCallerGroupId nCalledGroupId szName szUserAgent")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("IBBBBiBB%dsiiii%ds%ds" %(2, E_MAXNUM_NAME, E_MAXNUM_NAME), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_EMP_DEL_SDP_CODEC_RULE_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DEL_SDP_UA_RULE_REQ)

class MSG_EMS_EMP_DEL_SDP_CODEC_RULE_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DEL_SDP_UA_RULE_RSP)


###############################################################################################################################################
"""
struct st_sdp_rule : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nRID;                            //SDP Rule ID
    unsigned char ucMaching;             // Full-Maching or Partial Maching.
    unsigned char ucCondition;           // include or Exclude.
    unsigned char ucReserved[2];         // Reserved Field.
    int nCallerTrte;                     // Caller TrTe 
    int nCalledTrte;                     // Called TrTe 
    int nCallerGroupId;
    int nCalledGroupId;

    char szName[e_maxnum_name=128];      // RuleName
    char szUserAgent[e_maxnum_name=128]; // User-Agent 
};
"""

class SdpCodecRule_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        self.uReason = 0
        self.ucEnabled = 0
        self.ucValid = 0
        self.ucID = 0
        self.ucStatus = 0        
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "IBBBBiBB%dsiiii%ds%ds" % (2, E_MAXNUM_NAME, E_MAXNUM_NAME)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uReason ucEnabled ucValid ucID ucStatus nRID ucMaching ucCondition ucReserved nCallerTrte nCalledTrte nCallerGroupId nCalledGroupId szName szUserAgent"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uReason, self.ucEnabled, self.ucValid, self.ucID, self.ucStatus, \
                    self.nRID, self.ucMaching, self.ucCondition, self.ucReserved, \
                    self.nCallerTrte, self.nCalledTrte, self.nCallerGroupId, self.nCalledGroupId, \
                    self.szName, self.szUserAgent);

class SdpCodecRule_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBiBB%dsiiii%ds%ds" % (2, E_MAXNUM_NAME, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBiBB%dsiiii%ds%ds" % (2, E_MAXNUM_NAME, E_MAXNUM_NAME))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nRID ucMaching ucCondition ucReserved nCallerTrte nCalledTrte nCallerGroupId nCalledGroupId szName szUserAgent")
 
        new_list.append(StructInfo._make(unpack("IBBBBiBB%dsiiii%ds%ds" %(2, E_MAXNUM_NAME, E_MAXNUM_NAME), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_EMP_ADD_SDP_CODEC_RULE_REQ(SdpCodecRule_t_REQ):

    def __init__(self):
        SdpCodecRule_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_ADD_SDP_UA_RULE_REQ)

class MSG_EMS_EMP_ADD_SDP_CODEC_RULE_RSP(SdpCodecRule_t_RSP):

    def __init__(self):
        SdpCodecRule_t_RSP.__init__(self, DEF_STYPE_EMP_ADD_SDP_UA_RULE_RSP)

###############################################################################################################################################

class MSG_EMS_EMP_CHG_SDP_CODEC_RULE_REQ(SdpCodecRule_t_REQ):
    
    def __init__(self):
        SdpCodecRule_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_SDP_UA_RULE_REQ)

class MSG_EMS_EMP_CHG_SDP_CODEC_RULE_RSP(SdpCodecRule_t_RSP):
    
    def __init__(self):
        SdpCodecRule_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_SDP_UA_RULE_RSP)

###############################################################################################################################################

class SdpCodecRuleCommand(IbcfCommand):
    
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
        print "\t" "%12s = %d" % ('RID', imsg.nRID)
        if imsg.szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.szName))
        if imsg.szUserAgent != '':
            print "\t" "%12s = %s" % ('CODEC_NAME', self.reprName(imsg.szUserAgent))
        if imsg.ucMaching != 0:
            print "\t" "%12s = %s" % ('MACHING', self.reprCodecMatchIntToStr(imsg.ucMaching))
        if imsg.ucCondition != 0:
            print "\t" "%12s = %s" % ('CONDITION', self.reprCondIntToStr(imsg.ucCondition))
        if imsg.nCallerTrte != -1:    
            print "\t" "%12s = %d" % ('CALLER_TRTE', imsg.nCallerTrte)
        if imsg.nCalledTrte != -1:    
            print "\t" "%12s = %d" % ('CALLED_TRTE', imsg.nCalledTrte)
        if imsg.nCallerGroupId != 0:
            print "\t" "%12s : %d" % ('CALLER_GID', imsg.nCallerGroupId)
        if imsg.nCalledGroupId != 0:
            print "\t" "%12s : %d" % ('CALLED_GID', imsg.nCalledGroupId)

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:

           print "\t", " %5s %25s %50s %11s %11s %11s %11s %11s %11s" % ('RID', 'NAME', 'USERAGENT', 'MACHING', 'CONDITION', 'CALLER_TRTE', 'CALLED_TRTE', 'CALLER_GID', 'CALLED_GID')
           print "\t", "-----------------------------------------------------------------------------------------------------------------------------------------------------------"

           for rule in sorted(omsg.m_stData) :
               print "\t", " %5d %25s %50s %11s %11s %11d %11d %11d %11d" % \
                            (rule.nRID, self.reprNameShorter(rule.szName, 25, 20),
                             self.reprNameShorter(rule.szUserAgent, 50, 45),
                             self.reprCodecMatchIntToStr(rule.ucMaching), self.reprCondIntToStr(rule.ucCondition),
                             rule.nCallerTrte, rule.nCalledTrte, rule.nCallerGroupId, rule.nCalledGroupId
                            )             
        
        elif self.isIdxSearch == 1:
           for rule in omsg.m_stData :
               print "\t"
               print "\t" "%10s : %d" % ('RID', rule.nRID)
               print "\t" "%10s : %s" % ('NAME', self.reprName(rule.szName))
               print "\t" "%10s : %s" % ('USERAGENT', self.reprName(rule.szUserAgent))
               print "\t" "%10s : %s" % ('MACHING', self.reprCodecMatchIntToStr(rule.ucMaching))
               print "\t" "%10s : %s" % ('CONDITION', self.reprCondIntToStr(rule.ucCondition))
               print "\t" "%10s : %d" % ('CALLER_TRTE', rule.nCallerTrte)
               print "\t" "%10s : %d" % ('CALLED_TRTE', rule.nCalledTrte)
               print "\t" "%10s : %d" % ('CALLER_GID', rule.nCallerGroupId)
               print "\t" "%10s : %d" % ('CALLED_GID', rule.nCalledGroupId)                     
            
        if omsg.uiSubType == DEF_STYPE_EMP_DIS_SDP_UA_RULE_RSP: 
           print ""
           print "%-10s = %s" % ('SDP_CODEC_RULE_CNT', omsg.m_nNumber)

   
