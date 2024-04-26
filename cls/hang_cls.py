
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_VLM_DIS_HANG_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_VLM_DIS_HANG_REQ)
    
class MSG_EMS_VLM_DIS_HANG_RSP(IbcfResponseMsg):
    
    """
typedef struct DogInfo_t
{
    int m_nEnableMonitor;
    int m_nDogTime;
    int m_nDogAlarmCnt;
    int m_nEnableHA;
    int m_nEnableReset;
}DogInfo_t;

// CS_DIS_HANG_RSP
typedef struct CmDisDogRsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[64];
    DogInfo_t m_stInfo;
    
}CmDisDogRsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_VLM_DIS_HANG_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiii")
        return FMT_UDP_HEADER + "ii%ds%ds" % (64, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stInfo"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_HANG_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiii")
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_nEnableMonitor m_nDogTime m_nDogAlarmCnt m_nEnableHA m_nEnableReset")
        
        new_list.append(StructInfo._make(unpack("iiiii", response.m_stInfo)))
        response = response._replace(m_stInfo = new_list)
 
        print response
        return response

###############################################################################################################################################

class Hang_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiii"
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nEnableMonitor m_nDogTime m_nDogAlarmCnt m_nEnableHA m_nEnableReset"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nEnableMonitor, self.m_nDogTime, self.m_nDogAlarmCnt, self.m_nEnableHA, self.m_nEnableReset);


class Hang_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iiiii")
        return FMT_UDP_HEADER + "ii%ds%ds" % (64, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stInfo"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiii")
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_nEnableMonitor m_nDogTime m_nDogAlarmCnt m_nEnableHA m_nEnableReset")
        
        new_list.append(StructInfo._make(unpack("iiiii", response.m_stInfo)))
        response = response._replace(m_stInfo = new_list)
        
        print response
        return response
###############################################################################################################################################

class MSG_EMS_VLM_CHG_HANG_REQ(Hang_t_REQ):
    
    def __init__(self):
        Hang_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_VLM_CHG_HANG_REQ)

class MSG_EMS_VLM_CHG_HANG_RSP(Hang_t_RSP):
    
    def __init__(self):
        Hang_t_RSP.__init__(self, DEF_STYPE_VLM_CHG_HANG_RSP)

###############################################################################################################################################

class HangCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved1 = ''
        self.request.m_nIndex = 0
        self.request.m_ucUsed = 0
        self.request.m_ucReserved = ''     

    def printInputMessage(self, imsg):
        print "\t"
        if imsg.m_nEnableMonitor != -1:
           print "\t", "%25s = %7s" % ('MONITOR_ENABLE',  self.reprOnOffIntToStr(imsg.m_nEnableMonitor))
        if imsg.m_nDogTime != -1:
           print "\t", "%25s = %7d(ms)" % ('MONITOR_TIME',  imsg.m_nDogTime)
        if imsg.m_nDogAlarmCnt != -1:
           print "\t", "%25s = %7d(cnt)" % ('MONITOR_TIMEOUT_LIMIT', imsg.m_nDogAlarmCnt)
        if imsg.m_nEnableHA != -1:
           print "\t", "%25s = %7s" % ('HA_ENABLE', self.reprOnOffIntToStr(imsg.m_nEnableHA))
        if imsg.m_nEnableReset != -1:
           print "\t", "%25s = %7s" % ('PROCESS_RESTART_ENABLE', self.reprOnOffIntToStr(imsg.m_nEnableReset))

    def printOutputMessage(self, omsg):
        for st in omsg.m_stInfo :
            print "\t", "%25s = %7s" % ('MONITOR_ENABLE',  self.reprOnOffIntToStr(st.m_nEnableMonitor))
            print "\t", "%25s = %7d(ms)" % ('MONITOR_TIME',  st.m_nDogTime)
            print "\t", "%25s = %7d(cnt)" % ('MONITOR_TIMEOUT_LIMIT', st.m_nDogAlarmCnt)
            print "\t", "%25s = %7s" % ('HA_ENABLE', self.reprOnOffIntToStr(st.m_nEnableHA))
            print "\t", "%25s = %7s" % ('PROCESS_RESTART_ENABLE', self.reprOnOffIntToStr(st.m_nEnableReset))
