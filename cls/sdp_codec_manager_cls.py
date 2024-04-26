
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_EMP_DIS_SDP_CODEC_MANAGER_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_SDP_CODEC_MANAGER_REQ)
    
    
class MSG_EMS_EMP_DIS_SDP_CODEC_MANAGER_RSP(IbcfResponseMsg):
    
    """
struct st_sdp_codec_manager : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nID;
    char szName[e_maxnum_name=128];
    char szRID[e_maxnum_value=128];
    char szCodecList[e_maxnum_value=128];

    int nIfCodecDeleteThenAudioAs;
    int nIfCodecDeleteThenVideoAs;
    int nIfNotDeleteThenAudioAs;
    int nIfNotDeleteThenVideoAs;
    int nManagerOn;

    char szReason[e_maxnum_name=128];
}

typedef struct Emp_dis_sdp_codec_manager_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN=128];
    int m_nNumber;

    st_sdp_codec_manager m_stData[E_CODEC_MAX_SDP_CODEC_MANAGER=40];

} Emp_dis_sdp_codec_manager_rsp_t;

    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_SDP_CODEC_MANAGER_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBi%ds%ds%dsiiiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_CODEC_MAX_SDP_CODEC_MANAGER)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_SDP_CODEC_MANAGER_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBi%ds%ds%dsiiiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        new_list = []

        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nID szName szRID szCodecList nIfCodecDeleteThenAudioAs nIfCodecDeleteThenVideoAs nIfNotDeleteThenAudioAs nIfNotDeleteThenVideoAs nManagerOn szReason")
        
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("IBBBBi%ds%ds%dsiiiii%ds" %(E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_VALUE, E_MAXNUM_NAME), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_EMP_DEL_SDP_CODEC_MANAGER_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DEL_SDP_CODEC_MANAGER_REQ)

class MSG_EMS_EMP_DEL_SDP_CODEC_MANAGER_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DEL_SDP_CODEC_MANAGER_RSP)


###############################################################################################################################################

"""
struct st_sdp_codec_manager : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nID;
    char szName[e_maxnum_name=128];
    char szRID[e_maxnum_value=128];
    char szCodecList[e_maxnum_value=128];

    int nIfCodecDeleteThenAudioAs;
    int nIfCodecDeleteThenVideoAs;
    int nIfNotDeleteThenAudioAs;
    int nIfNotDeleteThenVideoAs;
    int nManagerOn;

    char szReason[e_maxnum_name=128];
}
"""

class SdpCodecManager_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        self.uReason = 0
        self.ucEnabled = 0
        self.ucValid = 0
        self.ucID = 0
        self.ucStatus = 0        
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "IBBBBi%ds%ds%dsiiiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_VALUE, E_MAXNUM_NAME)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uReason ucEnabled ucValid ucID ucStatus nID szName szRID szCodecList nIfCodecDeleteThenAudioAs nIfCodecDeleteThenVideoAs nIfNotDeleteThenAudioAs nIfNotDeleteThenVideoAs nManagerOn szReason"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uReason, self.ucEnabled, self.ucValid, self.ucID, self.ucStatus, \
                    self.nID, self.szName, self.szRID, self.szCodecList, \
                    self.nIfCodecDeleteThenAudioAs, self.nIfCodecDeleteThenVideoAs, \
                    self.nIfNotDeleteThenAudioAs, self.nIfNotDeleteThenVideoAs, \
                    self.nManagerOn, self.szReason)

    """ 
typedef struct Emp_add_sdp_codec_manager_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    st_sdp_codec_manager m_stCodecManager;

} Emp_add_sdp_codec_manager_rsp_t;

    """

class SdpCodecManager_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBi%ds%ds%dsiiiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBi%ds%ds%dsiiiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nID szName szRID szCodecList nIfCodecDeleteThenAudioAs nIfCodecDeleteThenVideoAs nIfNotDeleteThenAudioAs nIfNotDeleteThenVideoAs nManagerOn szReason")
 
        new_list.append(StructInfo._make(unpack("IBBBBi%ds%ds%dsiiiii%ds" %(E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_VALUE, E_MAXNUM_NAME), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_EMP_ADD_SDP_CODEC_MANAGER_REQ(SdpCodecManager_t_REQ):

    def __init__(self):
        SdpCodecManager_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_ADD_SDP_CODEC_MANAGER_REQ)

class MSG_EMS_EMP_ADD_SDP_CODEC_MANAGER_RSP(SdpCodecManager_t_RSP):

    def __init__(self):
        SdpCodecManager_t_RSP.__init__(self, DEF_STYPE_EMP_ADD_SDP_CODEC_MANAGER_RSP)

###############################################################################################################################################

class MSG_EMS_EMP_CHG_SDP_CODEC_MANAGER_REQ(SdpCodecManager_t_REQ):
    
    def __init__(self):
        SdpCodecManager_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_SDP_CODEC_MANAGER_REQ)

class MSG_EMS_EMP_CHG_SDP_CODEC_MANAGER_RSP(SdpCodecManager_t_RSP):
    
    def __init__(self):
        SdpCodecManager_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_SDP_CODEC_MANAGER_RSP)

###############################################################################################################################################

class SdpCodecManagerCommand(IbcfCommand):
    
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
        print "\t" "%17s : %d" % ('ID', imsg.nID)
        if imsg.szName != '':
            print "\t" "%17s : %s" % ('NAME', self.reprName(imsg.szName))
        if imsg.szRID != '':
            print "\t" "%17s : %s" % ('RULE_ID_LIST', self.reprName(imsg.szRID))
        if imsg.szCodecList != '':
            print "\t" "%17s : %s" % ('CODEC_LIST', self.reprName(imsg.szCodecList))
        if imsg.nIfCodecDeleteThenAudioAs != -1:
            print "\t" "%17s : %s" % ('AUDIO_AS', imsg.nIfCodecDeleteThenAudioAs)
        if imsg.nIfCodecDeleteThenVideoAs != -1:
            print "\t" "%17s : %s" % ('VIDEO_AS', imsg.nIfCodecDeleteThenVideoAs)
        if imsg.nManagerOn != -1:
            print "\t" "%17s : %s" % ('MANAGER_ON', self.reprOnOffIntToStr(imsg.nManagerOn))
  

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
            
           print "\t", " %5s %15s %20s %20s %9s %9s %11s" % ('ID', 'NAME', 'RULE_ID_LIST', 'CODEC_LIST', 'AUDIO_AS', 'VIDEO_AS', 'MANAGER_ON')
           print "\t", "------------------------------------------------------------------------------------------------"
           for rule in sorted(omsg.m_stData) :
               print "\t", " %5d %15s %20s %20s %9s %9s %11s" % \
                             (rule.nID, self.reprNameShorter(rule.szName, 15, 10),
                              self.reprNameShorter(rule.szRID, 20, 15),
                              self.reprNameShorter(rule.szCodecList, 20, 15),
                              rule.nIfCodecDeleteThenAudioAs,
                              rule.nIfCodecDeleteThenVideoAs,
                              self.reprOnOffIntToStr(rule.nManagerOn)
                              )
        
        elif self.isIdxSearch == 1:
           for rule in omsg.m_stData :
               print "\t"
               print "\t" "%10s : %d" % ('ID', rule.nID)
               print "\t" "%10s : %s" % ('NAME', self.reprName(rule.szName))
               print "\t" "%10s : %s" % ('RULE_ID_LIST', self.reprName(rule.szRID))
               print "\t" "%10s : %s" % ('CODEC_LIST', self.reprName(rule.szCodecList))
               print "\t" "%10s : %d" % ('AUDIO_AS', rule.nIfCodecDeleteThenAudioAs)
               print "\t" "%10s : %d" % ('VIDEO_AS', rule.nIfCodecDeleteThenVideoAs)
               print "\t" "%10s : %d" % ('MANAGER_ON', self.reprOnOffIntToStr(rule.nManagerOn))              
             
        if omsg.uiSubType == DEF_STYPE_EMP_DIS_SDP_MANIPULATION_RSP:
           print ""
           print "%-10s = %s" % ('SDP_CODEC_MANIPUL_CNT', omsg.m_nNumber)

   
