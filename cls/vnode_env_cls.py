
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_VNODE_DIS_ENV_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_VNODE_DIS_ENV_REQ)
    
    
class MSG_EMS_VNODE_DIS_ENV_RSP(IbcfResponseMsg):
    
    """
struct GlobalOverLoadEnv_t
{
   int            m_nMaxSES        ; //1. M, MAX_SES  (1 ~ 10000000)
   int            m_nChkSES        ; //2. M, SES_CHK_ON  (0/1)
   int            m_nMaxMSG        ; //3. M, MSG_SIZE (1400 ~ 9999999)
   int            m_nChkMSG        ; //4. M, MSG_CTRL see enum EMaxMSGCtrol_t
   int            m_nMaxCPS        ; //5. M, MAX_CPS  (1 ~ 700)
   int            m_nChkCPS        ; //6. M, CPS_CHK_ON (0/1)
   int            m_nMaxCPU        ; //7. M, HW_OVERLOAD_CPU(1 ~ 100)
   int            m_nChkCPU        ; //8. M, CPU_CHK_ON (0/1)
   int            m_nMaxMEM        ; //9. M, HW_OVERLOAD_MEM(1 ~ 100)
   int            m_nChkMEM        ; //10. M, MEM_CHK_ON (0/1)
   int            m_nMaxTPS        ; //11. M, MAX_TPS
   int            m_nChkTPS        ; //12. M, TPS_CHK_ON (0/1)
   //modify 2.2 2015/11/02 
   int            m_nMinCPS_Emer   ; //13. M, EMER_MINCPS (1 ~ 700)
   int            m_nMaxCPS_Audio  ; //14. M, AUDIO_MAXCPS(1 ~ 700)
   int            m_nMaxCPS_Video  ; //15. M, VIDEO_MAXCPS(1 ~ 700)
   int            m_nChkCPSClass   ; //16. M, CPS_CLASS_ON(0/1)
   ////////the below api set ////////////////
   int            m_nCurSES        ;
   int            m_nCurCPS        ;
   int            m_nCurCPU        ;
   int            m_nCurMEM        ;
   int            m_nCurTPS        ;
   int            m_nIndex         ; //internal index
   unsigned char  m_ucUsed         ; //used flag
   unsigned char  m_ucInterDel     ; //internal delete
   unsigned char  m_ucReserved[2]  ;
};

typedef struct Cs_dis_env_rsp 
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    GlobalOverLoadEnv_t m_stEnv;

} Cs_dis_env_rsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_VNODE_DIS_ENV_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiiiiiiiiiiiiiiiiiBB%ds" % (2))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stEnv"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_VNODE_DIS_ENV_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiiiiiiiiiiiiiiiiiBB%ds" % (2))
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_nMaxSES m_nChkSES m_nMaxMSG m_nChkMSG m_nMaxCPS m_nChkCPS m_nMaxCPU m_nChkCPU m_nMaxMEM m_nChkMEM m_nMaxTPS m_nChkTPS m_nMinCPS_Emer m_nMaxCPS_Audio m_nMaxCPS_Video m_nChkCPSClass m_nCurSES m_nCurCPS m_nCurCPU m_nCurMEM m_nCurTPS m_nIndex m_ucUsed m_ucInterDel m_ucReserved")
        
        new_list.append(StructInfo._make(unpack("iiiiiiiiiiiiiiiiiiiiiiBB%ds" %(2), response.m_stEnv)))
        response = response._replace(m_stEnv = new_list)
        
        print response
        return response

###############################################################################################################################################

class GlobalOverLoadEnv_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiiiiiiiiiiiiiiiiiiiiBB%ds" % (2)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nMaxSES m_nChkSES m_nMaxMSG m_nChkMSG m_nMaxCPS m_nChkCPS m_nMaxCPU m_nChkCPU m_nMaxMEM m_nChkMEM m_nMaxTPS m_nChkTPS m_nMinCPS_Emer m_nMaxCPS_Audio m_nMaxCPS_Video m_nChkCPSClass m_nCurSES m_nCurCPS m_nCurCPU m_nCurMEM m_nCurTPS m_nIndex m_ucUsed m_ucInterDel m_ucReserved"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nMaxSES, self.m_nChkSES, \
                    self.m_nMaxMSG, self.m_nChkMSG, \
                    self.m_nMaxCPS, self.m_nChkCPS, \
                    self.m_nMaxCPU, self.m_nChkCPU, \
                    self.m_nMaxMEM, self.m_nChkMEM, \
                    self.m_nMaxTPS, self.m_nChkTPS, \
                    self.m_nMinCPS_Emer, self.m_nMaxCPS_Audio, self.m_nMaxCPS_Video, self.m_nChkCPSClass, \
                    self.m_nCurSES, self.m_nCurCPS, self.m_nCurCPU, self.m_nCurMEM, self.m_nCurTPS, \
                    self.m_nIndex, self.m_ucUsed, self.m_ucInterDel, self.m_ucReserved);



class GlobalOverLoadEnv_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiiiiiiiiiiiiiiiiiBB%ds" % (2))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stEnv"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiiiiiiiiiiiiiiiiiBB%ds" % (2))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nMaxSES m_nChkSES m_nMaxMSG m_nChkMSG m_nMaxCPS m_nChkCPS m_nMaxCPU m_nChkCPU m_nMaxMEM m_nChkMEM m_nMaxTPS m_nChkTPS m_nMinCPS_Emer m_nMaxCPS_Audio m_nMaxCPS_Video m_nChkCPSClass m_nCurSES m_nCurCPS m_nCurCPU m_nCurMEM m_nCurTPS m_nIndex m_ucUsed m_ucInterDel m_ucReserved")
 
        new_list.append(StructInfo._make(unpack("iiiiiiiiiiiiiiiiiiiiiiBB%ds" %(2), response.m_stEnv)))
        response = response._replace(m_stEnv = new_list)
        
        print response
        return response

###############################################################################################################################################

class MSG_EMS_VNODE_CHG_ENV_REQ(GlobalOverLoadEnv_t_REQ):
    
    def __init__(self):
        GlobalOverLoadEnv_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_VNODE_CHG_ENV_REQ)

class MSG_EMS_VNODE_CHG_ENV_RSP(GlobalOverLoadEnv_t_RSP):
    
    def __init__(self):
        GlobalOverLoadEnv_t_RSP.__init__(self, DEF_STYPE_VNODE_CHG_ENV_RSP)

###############################################################################################################################################

class VnodeEnvCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_nChkSES = -1
        self.request.m_nMaxSES = -1
        
        self.request.m_nCurSES = -1
        self.request.m_nCurCPS = -1
        self.request.m_nCurCPU = -1
        self.request.m_nCurMEM = -1
        self.request.m_nCurTPS = -1  
                
        self.request.m_nIndex = 0
        self.request.m_ucUsed = 0
        self.request.m_ucInterDel = 0
        self.request.m_ucReserved = ''

    def printInputMessage(self, imsg):
        print "\t"
        if imsg.m_nMaxMSG != -1:
            print "\t" "%16s = %d" % ('MSG_SIZE', imsg.m_nMaxMSG)
            
        if imsg.m_nChkMSG != -1:
            print "\t" "%16s = %d" % ('MSG_CTRL', imsg.m_nChkMSG)
            
        if imsg.m_nChkCPS != -1:
            print "\t" "%16s = %s" % ('CPS_CHK_ON', self.reprOnOffIntToStr(imsg.m_nChkCPS))
              
        if imsg.m_nMaxCPS != -1:
            print "\t" "%16s = %d" % ('MAX_CPS', imsg.m_nMaxCPS)

        if imsg.m_nChkCPU != -1:
            print "\t" "%16s = %s" % ('CPU_CHK_ON', self.reprOnOffIntToStr(imsg.m_nChkCPU)) 
            
        if imsg.m_nMaxCPU != -1:
            print "\t" "%16s = %d" % ('HW_OVERLOAD_CPU', imsg.m_nMaxCPU)

        if imsg.m_nChkMEM != -1:
            print "\t" "%16s = %s" % ('MEM_CHK_ON', self.reprOnOffIntToStr(imsg.m_nChkMEM))
            
        if imsg.m_nMaxMEM != -1:
            print "\t" "%16s = %d" % ('HW_OVERLOAD_MEM', imsg.m_nMaxMEM)

        if imsg.m_nChkTPS != -1:
            print "\t" "%16s = %s" % ('TPS_CHK_ON', self.reprOnOffIntToStr(imsg.m_nChkTPS))
            
        if imsg.m_nMaxTPS != -1:
            print "\t" "%16s = %d" % ('MAX_TPS', imsg.m_nMaxTPS)
            
        if imsg.m_nMinCPS_Emer != -1:
            print "\t" "%16s = %d" % ('EMER_MINCPS', imsg.m_nMinCPS_Emer)

        if imsg.m_nMaxCPS_Audio != -1:
            print "\t" "%16s = %d" % ('AUDIO_MAXCPS', imsg.m_nMaxCPS_Audio)

        if imsg.m_nMaxCPS_Video != -1:
            print "\t" "%16s = %d" % ('VIDEO_MAXCPS', imsg.m_nMaxCPS_Video)

        if imsg.m_nChkCPSClass != -1:
            print "\t" "%16s = %s" % ('CPS_CLASS_ON', self.reprOnOffIntToStr(imsg.m_nChkCPSClass))

                       
    def printOutputMessage(self, omsg):
        if omsg.uiSubType == DEF_STYPE_VNODE_DIS_ENV_RSP:
           for st in omsg.m_stEnv :
               print "\t" "%17s %17s %17s %17s" % ('ITEM', 'CURRENT', 'MAX', 'OVERLOAD_CHECK')
               print "\t" "%17s"                % ('-' * 71)
               print "\t" "%17s %17s %17s %17s" % ('SES(Number)', st.m_nCurSES, st.m_nMaxSES, 'N/A')
               print "\t" "%17s %17s %17s %17s" % ('CPS(Number)', st.m_nCurCPS, st.m_nMaxCPS, self.reprOnOffIntToStr(st.m_nChkCPS))
               print "\t" "%17s %17s %17s %17s" % ('TPS(Number)', st.m_nCurTPS, st.m_nMaxTPS, self.reprOnOffIntToStr(st.m_nChkTPS))
               print "\t" "%17s %17s %17s %17s" % ('CPU(%)',      st.m_nCurCPU, st.m_nMaxCPU, self.reprOnOffIntToStr(st.m_nChkCPU))
               print "\t" "%17s %17s %17s %17s" % ('MEM(%)',      st.m_nCurMEM, st.m_nMaxMEM, self.reprOnOffIntToStr(st.m_nChkMEM))
               print "\t" "%17s %17s %17s %17s" % ('MSG(byte)', 'N/A', st.m_nMaxMSG, self.reprMsgCtlIntToStr(st.m_nChkMSG))
               print "\t"
               print "\t" "%17s %17s %17s %17s %17s" % ('ITEM', 'EMER', 'AUDIO', 'VIDEO', 'OVERLOAD_CHECK')
               print "\t" "%17s"                % ('-' * 89)
               print "\t" "%17s %17s %17s %17s %17s" % ('CPS_CLASS(Number)', st.m_nMinCPS_Emer, st.m_nMaxCPS_Audio, st.m_nMaxCPS_Video, self.reprOnOffIntToStr(st.m_nChkCPSClass)) 
        elif omsg.uiSubType == DEF_STYPE_VNODE_CHG_ENV_RSP:
           for st in omsg.m_stEnv :
               print "\t" "%17s %17s %17s %17s" % ('ITEM', 'CURRENT', 'MAX', 'OVERLOAD_CHECK')
               print "\t" "%17s"                % ('-' * 71)
               print "\t" "%17s %17s %17s %17s" % ('SES(Number)', "-", st.m_nMaxSES, 'N/A')
               print "\t" "%17s %17s %17s %17s" % ('CPS(Number)', "-", st.m_nMaxCPS, self.reprOnOffIntToStr(st.m_nChkCPS))
               print "\t" "%17s %17s %17s %17s" % ('TPS(Number)', "-", st.m_nMaxTPS, self.reprOnOffIntToStr(st.m_nChkTPS))
               print "\t" "%17s %17s %17s %17s" % ('CPU(%)',      "-", st.m_nMaxCPU, self.reprOnOffIntToStr(st.m_nChkCPU))
               print "\t" "%17s %17s %17s %17s" % ('MEM(%)',      "-", st.m_nMaxMEM, self.reprOnOffIntToStr(st.m_nChkMEM))
               print "\t" "%17s %17s %17s %17s" % ('MSG(byte)', 'N/A', st.m_nMaxMSG, self.reprMsgCtlIntToStr(st.m_nChkMSG))
               print "\t"
               print "\t" "%17s %17s %17s %17s %17s" % ('ITEM', 'EMER', 'AUDIO', 'VIDEO', 'OVERLOAD_CHECK')
               print "\t" "%17s"                % ('-' * 89)
               print "\t" "%17s %17s %17s %17s %17s" % ('CPS_CLASS(Number)', st.m_nMinCPS_Emer, st.m_nMaxCPS_Audio, st.m_nMaxCPS_Video, self.reprOnOffIntToStr(st.m_nChkCPSClass))

 

