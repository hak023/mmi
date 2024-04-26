
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_EMP_DIS_SDP_TRANSCODING_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_SDP_TRANSCODING_REQ)
    
    
class MSG_EMS_EMP_DIS_SDP_TRANSCODING_RSP(IbcfResponseMsg):
    
    """
struct st_sdp_transcoding : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nID;
    char szName[e_maxnum_name=128];
    char szRID[e_maxnum_value=128];

    int nAddCodecID;
    int nRTCP;
    int nTransCodingOn;
    char szReason[e_maxnum_name=128];
};

typedef struct Emp_dis_sdp_transcoding_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN=128];
    int m_nNumber;
    st_sdp_transcoding m_stData[E_CODEC_MAX_SDP_TRANSCODING];

} Emp_dis_sdp_transcoding_rsp_t;

    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_SDP_TRANSCODING_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBi%ds%dsiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_CODEC_MAX_SDP_TRANSCODING)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_SDP_TRANSCODING_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBi%ds%dsiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        new_list = []

        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nID szName szRID nAddCodecID nRTCP nTransCodingOn szReason")
        
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("IBBBBi%ds%dsiii%ds" %(E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_NAME), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_EMP_DEL_SDP_TRANSCODING_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DEL_SDP_TRANSCODING_REQ)

class MSG_EMS_EMP_DEL_SDP_TRANSCODING_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DEL_SDP_TRANSCODING_RSP)


###############################################################################################################################################

"""
struct st_sdp_transcoding : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    int nID;
    char szName[e_maxnum_name=128];
    char szRID[e_maxnum_value=128];

    int nAddCodecID;
    int nRTCP;
    int nTransCodingOn;
    char szReason[e_maxnum_name=128];
};
"""

class SdpTransCoding_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        self.uReason = 0
        self.ucEnabled = 0
        self.ucValid = 0
        self.ucID = 0
        self.ucStatus = 0        
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "IBBBBi%ds%dsiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_NAME)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uReason ucEnabled ucValid ucID ucStatus nID szName szRID nAddCodecID nRTCP nTransCodingOn szReason"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uReason, self.ucEnabled, self.ucValid, self.ucID, self.ucStatus, \
                    self.nID, self.szName, self.szRID, self.nAddCodecID, \
                    self.nRTCP, self.nTransCodingOn, \
                    self.szReason)

    """ 
typedef struct Emp_add_sdp_transcoding_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    st_sdp_transcoding m_stSdpTransCoding;

} Emp_add_sdp_transcoding_rsp_t;

    """

class SdpTransCoding_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBBi%ds%dsiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBBi%ds%dsiii%ds" % (E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_NAME))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus nID szName szRID nAddCodecID nRTCP nTransCodingOn szReason")
 
        new_list.append(StructInfo._make(unpack("IBBBBi%ds%dsiii%ds" %(E_MAXNUM_NAME, E_MAXNUM_VALUE, E_MAXNUM_NAME), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_EMP_ADD_SDP_TRANSCODING_REQ(SdpTransCoding_t_REQ):

    def __init__(self):
        SdpTransCoding_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_ADD_SDP_TRANSCODING_REQ)

class MSG_EMS_EMP_ADD_SDP_TRANSCODING_RSP(SdpTransCoding_t_RSP):

    def __init__(self):
        SdpTransCoding_t_RSP.__init__(self, DEF_STYPE_EMP_ADD_SDP_TRANSCODING_RSP)

###############################################################################################################################################

class MSG_EMS_EMP_CHG_SDP_TRANSCODING_REQ(SdpTransCoding_t_REQ):
    
    def __init__(self):
        SdpTransCoding_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_SDP_TRANSCODING_REQ)

class MSG_EMS_EMP_CHG_SDP_TRANSCODING_RSP(SdpTransCoding_t_RSP):
    
    def __init__(self):
        SdpTransCoding_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_SDP_TRANSCODING_RSP)

###############################################################################################################################################

class SdpTransCodingCommand(IbcfCommand):
    
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
        if imsg.nAddCodecID != -1:    
            print "\t" "%17s : %d" % ('ADD_CID', imsg.nAddCodecID)
        if imsg.nTransCodingOn != -1:
            print "\t" "%17s : %s" % ('TC_ON', self.reprOnOffIntToStr(imsg.nTransCodingOn))

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", " %5s %15s %20s %9s %5s" % ('ID', 'NAME', 'RULE_ID_LIST', 'ADD_CID', 'TC_ON')
           print "\t", "-----------------------------------------------------------"
           for tc in sorted(omsg.m_stData) :
               print "\t", " %5d %15s %20s %9d %5s" % \
                             (tc.nID, self.reprNameShorter(tc.szName, 15, 10), self.reprNameShorter(tc.szRID, 20, 15),
                              tc.nAddCodecID, self.reprOnOffIntToStr(tc.nTransCodingOn))
        
        elif self.isIdxSearch == 1:
           for tc in omsg.m_stData :
               print "\t"
               print "\t" "%10s : %d" % ('ID', tc.nID)
               print "\t" "%10s : %s" % ('NAME', self.reprName(tc.szName))
               print "\t" "%10s : %s" % ('RULE_ID_LIST', self.reprName(tc.szRID))
               print "\t" "%10s : %d" % ('ADD_CID', tc.nAddCodecID)
               print "\t" "%10s : %s" % ('ON', self.reprOnOffIntToStr(tc.nTransCodingOn))             
             
        if omsg.uiSubType == DEF_STYPE_EMP_DIS_SDP_TRANSCODING_RSP:
           print ""
           print "%-10s = %s" % ('SDP_TRANSCODING_CNT', omsg.m_nNumber)
