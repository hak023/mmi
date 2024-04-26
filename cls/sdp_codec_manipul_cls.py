
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_EMP_DIS_SDP_MANIPUL_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_SDP_MANIPULATION_REQ)
    
    
class MSG_EMS_EMP_DIS_SDP_MANIPUL_RSP(IbcfResponseMsg):
    
    """
struct st_sdp_manipulation : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nMID;                             // SDP Manipulation ID
    unsigned char ucCommandType;          // ADD, MOD, DEL
    unsigned char ucMediaType;            // Audio or Video
    unsigned char reserved[2];            // reserved.
    int nManipulationOn;                  // on, off flag.
    int nPT;                              // PT
    int nSampleRate;                      // samplerate
    int nFrameRate;                       // FrameRate

    char szRID[e_maxnum_value=128];       // SDP Rule ID
    char szName[e_maxnum_name=128];       // Name
    char szCodecName[e_maxnum_name=128];  // CODEC Name
    char szFMTP[e_maxnum_fmtp=256];       // FMTP
    char szFrameSize[e_maxnum_value=128]; // Video FrameSize
    char szImageAttr[e_maxnum_value=128]; // Video ImageAttr
};

typedef struct Emp_dis_sdp_manipulation_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    int m_nNumber;
    st_sdp_manipulation m_stData[E_CODEC_MAX_SDP_MANIPULATION];

} Emp_dis_sdp_manipulation_rsp_t;
    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_SDP_MANIPULATION_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBiBB%dsiiii%ds%ds%ds%ds%ds%ds" % (2, E_MAXNUM_VALUE, E_MAXNUM_NAME, E_MAXNUM_NAME, E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_VALUE))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_CODEC_MAX_SDP_MANIPULATION)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_SDP_RULE_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBiBB%dsiiii%ds%ds%ds%ds%ds%ds" % (2, E_MAXNUM_VALUE, E_MAXNUM_NAME, E_MAXNUM_NAME, E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_VALUE))
        new_list = []

        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nMID ucCommandType ucMediaType man_reserved nManipulationOn nPT nSampleRate nFrameRate szRID szName szCodecName szFMTP szFrameSize szImageAttr")
        
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("IBBBBiBB%dsiiii%ds%ds%ds%ds%ds%ds" %(2, E_MAXNUM_VALUE, E_MAXNUM_NAME, E_MAXNUM_NAME, E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_VALUE), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_EMP_DEL_SDP_MANIPUL_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DEL_SDP_MANIPULATION_REQ)

class MSG_EMS_EMP_DEL_SDP_MANIPUL_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DEL_SDP_MANIPULATION_RSP)


###############################################################################################################################################

"""
struct st_sdp_manipulation : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nMID;                             // SDP Manipulation ID
    unsigned char ucCommandType;          // ADD, MOD, DEL
    unsigned char ucMediaType;            // Audio or Video
    unsigned char reserved[2];            // reserved.
    int nManipulationOn;                  // on, off flag.
    int nPT;                              // PT
    int nSampleRate;                      // samplerate
    int nFrameRate;                       // FrameRate

    char szRID[e_maxnum_value=128];       // SDP Rule ID
    char szName[e_maxnum_name=128];       // Name
    char szCodecName[e_maxnum_name=128];  // CODEC Name
    char szFMTP[e_maxnum_fmtp=256];       // FMTP
    char szFrameSize[e_maxnum_value=128]; // Video FrameSize
    char szImageAttr[e_maxnum_value=128]; // Video ImageAttr
};
"""

class SdpCodecManipul_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        self.uReason = 0
        self.ucEnabled = 0
        self.ucValid = 0
        self.ucID = 0
        self.ucStatus = 0        
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "IBBBBibb%dsiiii%ds%ds%ds%ds%ds%ds" % (2, E_MAXNUM_VALUE, E_MAXNUM_NAME, E_MAXNUM_NAME, E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_VALUE)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uReason ucEnabled ucValid ucID ucStatus nMID ucCommandType ucMediaType man_reserved nManipulationOn nPT nSampleRate nFrameRate szRID szName szCodecName szFMTP szFrameSize szImageAttr"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uReason, self.ucEnabled, self.ucValid, self.ucID, self.ucStatus, \
                    self.nMID, self.ucCommandType, self.ucMediaType, self.man_reserved, \
                    self.nManipulationOn, self.nPT, self.nSampleRate, self.nFrameRate, \
                    self.szRID, self.szName, self.szCodecName, self.szFMTP, self.szFrameSize, self.szImageAttr);

    """ 
typedef struct Emp_add_sdp_rule_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    st_rulelist m_stRule;

} Emp_add_sdp_rule_rsp_t;
    """

class SdpCodecManipul_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBibb%dsiiii%ds%ds%ds%ds%ds%ds" % (2, E_MAXNUM_VALUE, E_MAXNUM_NAME, E_MAXNUM_NAME, E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_VALUE))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBibb%dsiiii%ds%ds%ds%ds%ds%ds" % (2, E_MAXNUM_VALUE, E_MAXNUM_NAME, E_MAXNUM_NAME, E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_VALUE))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nMID ucCommandType ucMediaType man_reserved nManipulationOn nPT nSampleRate nFrameRate szRID szName szCodecName szFMTP szFrameSize szImageAttr")
 
        new_list.append(StructInfo._make(unpack("IBBBBibb%dsiiii%ds%ds%ds%ds%ds%ds" %(2, E_MAXNUM_VALUE, E_MAXNUM_NAME, E_MAXNUM_NAME, E_MAXNUM_FMTP, E_MAXNUM_VALUE, E_MAXNUM_VALUE), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_EMP_ADD_SDP_MANIPUL_REQ(SdpCodecManipul_t_REQ):

    def __init__(self):
        SdpCodecManipul_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_ADD_SDP_MANIPULATION_REQ)

class MSG_EMS_EMP_ADD_SDP_MANIPUL_RSP(SdpCodecManipul_t_RSP):

    def __init__(self):
        SdpCodecManipul_t_RSP.__init__(self, DEF_STYPE_EMP_ADD_SDP_MANIPULATION_RSP)

###############################################################################################################################################

class MSG_EMS_EMP_CHG_SDP_MANIPUL_REQ(SdpCodecManipul_t_REQ):
    
    def __init__(self):
        SdpCodecManipul_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_SDP_MANIPULATION_REQ)

class MSG_EMS_EMP_CHG_SDP_MANIPUL_RSP(SdpCodecManipul_t_RSP):
    
    def __init__(self):
        SdpCodecManipul_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_SDP_MANIPULATION_RSP)

###############################################################################################################################################

class SdpManipulCommand(IbcfCommand):
    
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
        print "\t" "%12s = %d" % ('MID', imsg.nMID)
        if imsg.szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.szName))
        if imsg.szRID != '':
            print "\t" "%12s = %s" % ('RULE_ID_LIST', self.reprName(imsg.szRID))
        '''
        if imsg.ucCommandType != -1:
            print "\t" "%12s = %s" % ('CMD_TYPE', self.reprCommIntToStr(imsg.ucCommandType))
        '''    
        if imsg.szCodecName != '':
            print "\t" "%12s = %s" % ('CODEC_NAME', self.reprName(imsg.szCodecName))
        if imsg.ucMediaType != -1:    
            print "\t" "%12s = %s" % ('MEDIA_TYPE', self.reprMediaIntToStr(imsg.ucMediaType))
        if imsg.nPT != -1:
            print "\t" "%12s = %s" % ('PAYLOAD_TYPE', imsg.nPT)
        if imsg.nSampleRate != -1:
            print "\t" "%12s = %d" % ('SAMPLE_RATE', imsg.nSampleRate)
        if imsg.szFMTP != '':
            print "\t" "%12s = %s" % ('FMTP', self.reprName(imsg.szFMTP))
        if imsg.nManipulationOn != -1:
            print "\t" "%12s = %s" % ('MANIPUL_ON', self.reprOnOffIntToStr(imsg.nManipulationOn))                                           
  

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", " %5s %15s %30s %9s %20s %11s %13s %12s %35s %11s" % ('MID', 'NAME', 'RULE_ID_LIST', 'CMD_TYPE', 'CODEC_NAME', 'MEDIA_TYPE', 'PAYLOAD_TYPE', 'SAMPLE_RATE', 'FMTP', 'MANIPUL_ON')
           print "\t", "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
           for rule in sorted(omsg.m_stData) :
               print "\t", " %5d %15s %30s %9s %20s %11s %13d %12d %35s %11s" % \
                             (rule.nMID, self.reprNameShorter(rule.szName, 15, 10),
                              self.reprNameShorter(rule.szRID, 30, 25),
                              self.reprCommIntToStr(rule.ucCommandType), self.reprNameShorter(rule.szCodecName, 20, 15),
                              self.reprMediaIntToStr(rule.ucMediaType),
                              rule.nPT, rule.nSampleRate, self.reprNameShorter(rule.szFMTP, 35, 30),
                              self.reprOnOffIntToStr(rule.nManipulationOn)
                              )
        
        elif self.isIdxSearch == 1:
           for rule in omsg.m_stData :
               print "\t"
               print "\t" "%10s : %d" % ('MID', rule.nMID)
               print "\t" "%10s : %s" % ('NAME', self.reprName(rule.szName))
               print "\t" "%10s : %s" % ('RULE_ID_LIST', self.reprName(rule.szRID))
               print "\t" "%10s : %s" % ('CMD_TYPE', self.reprCommIntToStr(rule.ucCommandType))
               print "\t" "%10s : %s" % ('CODEC_NAME', self.reprName(rule.szCodecName))
               print "\t" "%10s : %s" % ('MEDIA_TYPE', self.reprMediaIntToStr(rule.ucMediaType))
               print "\t" "%10s : %d" % ('PAYLOAD_TYPE', rule.nPT)
               print "\t" "%10s : %d" % ('SAMPLE_RATE', rule.nSampleRate)
               print "\t" "%10s : %s" % ('FMTP', self.reprName(rule.szFMTP))
               print "\t" "%10s : %s" % ('MANIPUL_ON', self.reprOnOffIntToStr(rule.nManipulationOn))               
             
        if omsg.uiSubType == DEF_STYPE_EMP_DIS_SDP_MANIPULATION_RSP:
           print ""
           print "%-10s = %s" % ('SDP_CODEC_MANIPUL_CNT', omsg.m_nNumber)

   
