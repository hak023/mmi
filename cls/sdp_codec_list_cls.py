
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_EMP_DIS_SDP_CODEC_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_SDP_CODEC_REQ)
    
    
class MSG_EMS_EMP_DIS_SDP_CODEC_RSP(IbcfResponseMsg):
    
    """

struct st_codeclist : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    unsigned char ucCID;
    char cDtmf;
    unsigned char ucType;
    unsigned char ucReserved;
    int nMaxPps;

   char szName[e_maxnum_name=128];
   char szCodecName[e_maxnum_name=128];
};

typedef struct Emp_dis_sdp_codec_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN=128];

    int m_nNumber;
    st_codeclist m_stData[E_CODEC_MAX_LIST=20];

} Emp_dis_sdp_codec_rsp_t;

    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_SDP_CODEC_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("Ibbbbbbbbi%ds%ds" % (E_MAXNUM_NAME, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_CODEC_MAX_LIST)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_SDP_CODEC_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("Ibbbbbbbbi%ds%ds" % (E_MAXNUM_NAME, E_MAXNUM_NAME))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus ucCID cDtmf ucType ucReserved nMaxPps szName szCodecName")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("Ibbbbbbbbi%ds%ds" %(E_MAXNUM_NAME, E_MAXNUM_NAME), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_EMP_DEL_SDP_CODEC_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DEL_SDP_CODEC_REQ)

class MSG_EMS_EMP_DEL_SDP_CODEC_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DEL_SDP_CODEC_RSP)


###############################################################################################################################################
"""
struct st_codeclist : public st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;
    
    unsigned char ucCID;
    char cDtmf;
    unsigned char ucType;
    unsigned char ucReserved;
    int nMaxPps;

   char szName[e_maxnum_name=128];
   char szCodecName[e_maxnum_name=128];
};

typedef st_codeclist Emp_add_sdp_codec_req_t;
"""

class SdpCodecList_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        self.uReason = 0
        self.ucEnabled = 0
        self.ucValid = 0
        self.ucID = 0
        self.ucStatus = 0        
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "Ibbbbbbbbi%ds%ds" % (E_MAXNUM_NAME, E_MAXNUM_NAME)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uReason ucEnabled ucValid ucID ucStatus ucCID cDtmf ucType ucReserved nMaxPps szName szCodecName"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uReason, self.ucEnabled, self.ucValid, self.ucID, self.ucStatus, self.ucCID, self.cDtmf, self.ucType, \
                    self.ucReserved, self.nMaxPps, self.szName, self.szCodecName);

    """ 
typedef struct Emp_add_sdp_codec_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    st_codeclist m_stData;
|
} Emp_add_sdp_codec_rsp_t;
    """

class SdpCodecList_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("Ibbbbbbbbi%ds%ds" % (E_MAXNUM_NAME, E_MAXNUM_NAME))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("Ibbbbbbbbi%ds%ds" % (E_MAXNUM_NAME, E_MAXNUM_NAME))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucID ucStatus ucCID cDtmf ucType ucReserved nMaxPps szName szCodecName")
 
        new_list.append(StructInfo._make(unpack("Ibbbbbbbbi%ds%ds" %(E_MAXNUM_NAME, E_MAXNUM_NAME), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_EMP_ADD_SDP_CODEC_REQ(SdpCodecList_t_REQ):

    def __init__(self):
        SdpCodecList_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_ADD_SDP_CODEC_REQ)

class MSG_EMS_EMP_ADD_SDP_CODEC_RSP(SdpCodecList_t_RSP):

    def __init__(self):
        SdpCodecList_t_RSP.__init__(self, DEF_STYPE_EMP_ADD_SDP_CODEC_RSP)

###############################################################################################################################################

class MSG_EMS_EMP_CHG_SDP_CODEC_REQ(SdpCodecList_t_REQ):
    
    def __init__(self):
        SdpCodecList_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_SDP_CODEC_REQ)

class MSG_EMS_EMP_CHG_SDP_CODEC_RSP(SdpCodecList_t_RSP):
    
    def __init__(self):
        SdpCodecList_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_SDP_CODEC_REQ)

###############################################################################################################################################

class SdpCodecCommand(IbcfCommand):
    
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
        print "\t" "%12s = %d" % ('CID', imsg.ucCID)
        if imsg.szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.szName))
        if imsg.szCodecName != '':
            print "\t" "%12s = %s" % ('CODEC_NAME', self.reprName(imsg.szCodecName))
        if imsg.ucType != -1:
            print "\t" "%12s = %s" % ('TYPE', self.reprCodecTypeIntToStr(imsg.ucType))
        if imsg.cDtmf != -1:
            print "\t" "%12s = %s" % ('DTMF', self.reprDtmfIntToStr(imsg.cDtmf))
        if imsg.nMaxPps != -1:    
            print "\t" "%12s = %d" % ('MAX_PPS', imsg.nMaxPps)
  

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", " %5s %20s %20s %10s %7s %10s" % ('CID', 'NAME', 'CODEC_NAME', 'TYPE', 'DTMF', 'MAX_PPS')
           print "\t", "------------------------------------------------------------------------------"

           for codec in sorted(omsg.m_stData) :
               print "\t", " %5d %20s %20s %10s %7s %10d" % \
                        (codec.ucCID, self.reprNameShorter(codec.szName, 20, 15), self.reprNameShorter(codec.szCodecName, 20, 15),
                         self.reprCodecTypeIntToStr(codec.ucType), self.reprDtmfIntToStr(codec.cDtmf), codec.nMaxPps
                        )               
        
        elif self.isIdxSearch == 1:
           for codec in omsg.m_stData :
               print "\t"
               print "\t" "%12s = %d" % ('CID', codec.ucCID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(codec.szName))
               print "\t" "%12s = %s" % ('CODEC_NAME', self.reprName(codec.szCodecName))
               print "\t" "%12s = %s" % ('TYPE', self.reprCodecTypeIntToStr(codec.ucType))
               print "\t" "%12s = %s" % ('DTMF', self.reprDtmfIntToStr(codec.cDtmf))
               print "\t" "%12s = %d" % ('MAX_PPS', codec.nMaxPps)             
            
        if omsg.uiSubType == DEF_STYPE_EMP_DIS_SDP_CODEC_RSP: 
           print ""
           print "%-10s = %s" % ('CODEC_LIST_CNT', omsg.m_nNumber)

   
