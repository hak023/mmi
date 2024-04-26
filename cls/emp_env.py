
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_EMP_DIS_ENV_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_ENV_REQ)
    
    
class MSG_EMS_EMP_DIS_ENV_RSP(IbcfResponseMsg):
    
    """
typedef struct Emp_chg_env_req
{
    int nDSCPUse;
    int nDSCPValue_AudioRTP;
    int nDSCPValue_VideoRTP;
    int nDSCPValue_AudioRTCP;
    int nDSCPValue_VideoRTCP;
    int nEnableAliveCheck; 
    int nAliveCheck_CheckPeriod;
    int nAliveCheck_ValidPeriod
    int nEnableNetfailKill;
    int nValidAliveTime;
    int nCpuMax; 
    int nMemMax; 
    int nTcSessionWarn;
    int nEnableOMR;
    char szOMRNode[128];
    char szOMRDomain[128];
} Emp_chg_env_req_t;

typedef struct Emp_chg_env_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    Emp_chg_env_req_t m_stEnv;
} Emp_chg_env_rsp_t;

    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_ENV_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiiiiiiiii%ds%ds" % (128, 128))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_ENV_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiiiiiiiii%ds%ds" % (128, 128))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "nDSCPUse nDSCPValue_AudioRTP nDSCPValue_VideoRTP nDSCPValue_AudioRTCP nDSCPValue_VideoRTCP nEnableAliveCheck nAliveCheck_CheckPeriod nAliveCheck_ValidPeriod nEnableNetfailKill nValidAliveTime nCpuMax nMemMax nTcSessionWarn nEnableOMR szOMRNode szOMRDomain")
        
        new_list.append(StructInfo._make(unpack("iiiiiiiiiiiiii%ds%ds" %(128, 128), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
"""
typedef struct Emp_chg_env_req
{
    int nDSCPUse;
    int nDSCPValue_AudioRTP;
    int nDSCPValue_VideoRTP;
    int nDSCPValue_AudioRTCP;
    int nDSCPValue_VideoRTCP;
    int nEnableAliveCheck; 
    int nAliveCheck_CheckPeriod;
    int nAliveCheck_ValidPeriod;
    int nEnableNetfailKill;
    int nValidAliveTime;
    int nCpuMax; 
    int nMemMax; 
    int nTcSessionWarn;
    int nEnableOMR;
    char szOMRNode[128];
    char szOMRDomain[128];
} Emp_chg_env_req_t;
"""

class EmpEnv_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiiiiiiiiiiii%ds%ds" % (128, 128)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " nDSCPUse nDSCPValue_AudioRTP nDSCPValue_VideoRTP nDSCPValue_AudioRTCP nDSCPValue_VideoRTCP nEnableAliveCheck nAliveCheck_CheckPeriod nAliveCheck_ValidPeriod nEnableNetfailKill nValidAliveTime nCpuMax nMemMax nTcSessionWarn nEnableOMR szOMRNode szOMRDomain"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.nDSCPUse, self.nDSCPValue_AudioRTP, self.nDSCPValue_VideoRTP, self.nDSCPValue_AudioRTCP, \
                    self.nDSCPValue_VideoRTCP, self.nEnableAliveCheck, \
                    self.nAliveCheck_CheckPeriod, self.nAliveCheck_ValidPeriod, \
                    self.nEnableNetfailKill, self.nValidAliveTime, self.nCpuMax, self.nMemMax, self.nTcSessionWarn, \
                    self.nEnableOMR, self.szOMRNode, self.szOMRDomain);

class EmpEnv_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiiiiiiiii%ds%ds" % (128, 128))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiiiiiiiii%ds%ds" % (128, 128))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "nDSCPUse nDSCPValue_AudioRTP nDSCPValue_VideoRTP nDSCPValue_AudioRTCP nDSCPValue_VideoRTCP nEnableAliveCheck nAliveCheck_CheckPeriod nAliveCheck_ValidPeriod nEnableNetfailKill nValidAliveTime nCpuMax nMemMax nTcSessionWarn nEnableOMR szOMRNode szOMRDomain")
 
        new_list.append(StructInfo._make(unpack("iiiiiiiiiiiiii%ds%ds" %(128, 128), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_EMP_CHG_ENV_REQ(EmpEnv_t_REQ):
    
    def __init__(self):
        EmpEnv_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_ENV_REQ)

class MSG_EMS_EMP_CHG_ENV_RSP(EmpEnv_t_RSP):
    
    def __init__(self):
        EmpEnv_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_ENV_REQ)

###############################################################################################################################################

class EmsEmpCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        ''' 
        '''        

    def printOutputMessage(self, omsg):
        for st in omsg.m_stData :
            print "\t"
            print "\t" "%20s : %s" % ('DSCP ON/OFF', self.reprOnOffIntToStr(st.nDSCPUse))
            print "\t" "%20s : %d" % ('AUDIO RTP DSCP ', st.nDSCPValue_AudioRTP)
            print "\t" "%20s : %d" % ('VIDEO RTP DSCP', st.nDSCPValue_VideoRTP)
            print "\t" "%20s : %d" % ('AUDIO RTCP DSCP', st.nDSCPValue_AudioRTCP)
            print "\t" "%20s : %d" % ('VIDEO RTCP DSCP', st.nDSCPValue_VideoRTCP)
            print "\t" "%20s : %s" % ('ALIVE CHECK ON/OFF', self.reprOnOffIntToStr(st.nEnableAliveCheck))
            print "\t" "%20s : %d" % ('ALIVE CHECK PERIOD', st.nAliveCheck_CheckPeriod)
            print "\t" "%20s : %s" % ('NETFAIL KILL ON/OFF', self.reprOnOffIntToStr(st.nEnableNetfailKill))
            print "\t" "%20s : %d" % ('MEDIA ALIVE TIMER', st.nValidAliveTime)
            print "\t" "%20s : %d" % ('TC WARN CHECK VALUE', st.nTcSessionWarn)
            '''
            print "\t" "%20s : %d" % ('CPU MAX CHECK VALUE', st.nCpuMax)
            print "\t" "%20s : %d" % ('MEM MAX CHECK VALUE', st.nMemMax)
            print "\t" "%20s : %s" % ('OMR ON/OFF', self.reprOnOffIntToStr(st.nEnableOMR))
            print "\t" "%20s : %s" % ('OMR NODE', st.szOMRNode)
            print "\t" "%20s : %s" % ('OMR DOMAIN', st.szOMRDomain)
            '''
          
            

   
