
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_RC_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_RC_REQ)
    
    
class MSG_EMS_CS_DIS_RC_RSP(IbcfResponseMsg):
    
    """
struct SipReasonCode_t
{
   unsigned int   m_uiID                                                  ;  //0. M, ID, 1~9999999
   char           m_szDesc[DEF_RTE_MAXLEN_DESC]                           ;  //1. M, NAME,  
   int            m_nCauseCode[E_CAUSE_MAX=20]                            ;  //2. M, CAUSE,     1 ~ 9999999
   int            m_nRspCode[E_CAUSE_MAX=20]                              ;  //3. M, RSP_CODE,  100 ~ 699
   char           m_szCause[E_CAUSE_MAX=20][DEF_RTE_MAXLEN_STRIUNAVAIL=56];  //4. M, TEXT,
   ////////the below api set ////////////////
   int            m_nIndex                           ; //internal index
   unsigned char  m_ucUsed                           ; //used flag
   unsigned char  m_ucReserved[3]                    ;
};

typedef struct Cs_dis_rc_rsp : public SipReasonCodeDataBase_t
{
   int m_nNumber;
   SipReasonCode_t    m_stData[E_MAXNUM=8];

   int m_nResult;
   int m_nReason;
   char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_rc_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_RC_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%ds%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_CAUSE_MAX*4, E_CAUSE_MAX*4, E_CAUSE_MAX*DEF_RTE_MAXLEN_STRIUNAVAIL, 3))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_RC_MAXNUM, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stData m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_RC_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%ds%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_CAUSE_MAX*4, E_CAUSE_MAX*4, E_CAUSE_MAX*DEF_RTE_MAXLEN_STRIUNAVAIL, 3))
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_nCauseCode m_nRspCode m_szCause m_nIndex m_ucUsed m_ucReserved")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%ds%ds%ds%dsiB%ds" %(DEF_RTE_MAXLEN_DESC, E_CAUSE_MAX*4, E_CAUSE_MAX*4, E_CAUSE_MAX*DEF_RTE_MAXLEN_STRIUNAVAIL, 3), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_RC_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_RC_REQ)

class MSG_EMS_CS_DEL_RC_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_RC_RSP)


###############################################################################################################################################

class SipReasonCode_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%ds%ds%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_CAUSE_MAX*4, E_CAUSE_MAX*4, E_CAUSE_MAX*DEF_RTE_MAXLEN_STRIUNAVAIL, 3)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_nCauseCode m_nRspCode m_szCause m_nIndex m_ucUsed m_ucReserved"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, self.m_nCauseCode, self.m_nRspCode, self.m_szCause, \
                    self.m_nIndex, self.m_ucUsed, self.m_ucReserved);

    """ 
typedef struct Cs_add_rc_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    SipReasonCode_t m_stData;

} Cs_add_rc_rsp_t;
    """

class SipReasonCode_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%ds%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_CAUSE_MAX*4, E_CAUSE_MAX*4, E_CAUSE_MAX*DEF_RTE_MAXLEN_STRIUNAVAIL, 3))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%ds%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_CAUSE_MAX*4, E_CAUSE_MAX*4, E_CAUSE_MAX*DEF_RTE_MAXLEN_STRIUNAVAIL, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_nCauseCode m_nRspCode m_szCause m_nIndex m_ucUsed m_ucReserved")
 
        new_list.append(StructInfo._make(unpack("I%ds%ds%ds%dsiB%ds" %(DEF_RTE_MAXLEN_DESC, E_CAUSE_MAX*4, E_CAUSE_MAX*4, E_CAUSE_MAX*DEF_RTE_MAXLEN_STRIUNAVAIL, 3), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_CS_ADD_RC_REQ(SipReasonCode_t_REQ):
    
    def __init__(self):
        SipReasonCode_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_RC_REQ)

class MSG_EMS_CS_ADD_RC_RSP(SipReasonCode_t_RSP):

    def __init__(self):
        SipReasonCode_t_RSP.__init__(self, DEF_STYPE_CS_ADD_RC_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_RC_REQ(SipReasonCode_t_REQ):
    
    def __init__(self):
        SipReasonCode_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_RC_REQ)

class MSG_EMS_CS_CHG_RC_RSP(SipReasonCode_t_RSP):
    
    def __init__(self):
        SipReasonCode_t_RSP.__init__(self, DEF_STYPE_CS_CHG_RC_RSP)

###############################################################################################################################################

class ReasonCodeCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)

        self.request.m_nIndex = 0
        self.request.m_ucUsed = 0
        self.request.m_ucReserved = ''
        
        self.NameTag = ['SYSTEM_OVERLOAD', 'CPS_OVERLOAD', 'CPU_OVERLOAD', 'MEM_OVERLOAD', 'UNKNOWN_ROUTE', 'ROUTING_FAIL', 'INTERNAL_ERR', 'INCORRECT_MSG', 'FILTER_DENY', 'SESSION_NOT_EXIST', 'TIMEOUT_ERR', 'MP_NOTCONT', 'TRGW_NEGO_FAIL', 'TRGW_NO_RTP_FAIL', 'TRGW_INSUFFICIENT_RSC', 'TRGW_SDP_INCORRECT', 'TRGW_INCORRECT', 'ROUTE_STS_DOWN', 'NPDB_TIMEOUT', 'IGW_TIMEOUT']

        self.system_overload_code = '0'
        self.system_cps_overload_code = '0'
        self.system_cpu_overload_code = '0'
        self.system_mem_overload_code  = '0'
        self.unknown_route_code = '0'
        self.routing_fail_code = '0'
        self.internal_error_code = '0'
        self.incorrect_msg_code = '0'
        self.filter_deny_code = '0'
        self.not_exist_dial_code = '0'
        self.csfb_fail_code = '0'
        self.mp_not_conn_code = '0'
        self.trgw_nego_fail_code = '0'
        self.trgw_no_rtp_fail_code = '0'
        self.trgw_insufficent_rsc_code = '0'
        self.trgw_sdp_incorrect_code = '0'
        self.trgw_incorrect_code = '0'
        self.route_sts_down_code = '0'
        self.npdb_sts_down_code = '0'
        self.igw_sts_down_code = '0'        

        self.system_overload_rsp_code = '0'
        self.system_cps_overload_rsp_code = '0'
        self.system_cpu_overload_rsp_code = '0'
        self.system_mem_overload_rsp_code  = '0'
        self.unknown_route_rsp_code = '0'
        self.routing_fail_rsp_code = '0'
        self.internal_error_rsp_code = '0'
        self.incorrect_msg_rsp_code = '0'
        self.filter_deny_rsp_code = '0'
        self.not_exist_dial_rsp_code = '0'
        self.csfb_fail_rsp_code = '0'
        self.mp_not_conn_rsp_code = '0'
        self.trgw_nego_fail_rsp_code = '0'
        self.trgw_no_rtp_fail_rsp_code = '0'
        self.trgw_insufficent_rsc_rsp_code = '0'
        self.trgw_sdp_incorrect_rsp_code = '0'
        self.trgw_incorrect_rsp_code = '0'
        self.route_sts_down_rsp_code = '0'
        self.npdb_sts_down_rsp_code = '0'
        self.igw_sts_down_rsp_code = '0'        

        self.system_overload_text = ''
        self.system_cps_overload_text = ''
        self.system_cpu_overload_text = ''
        self.system_mem_overload_text  = ''
        self.unknown_route_text = ''
        self.routing_fail_text = ''
        self.internal_error_text = ''
        self.incorrect_msg_text = ''
        self.filter_deny_text = ''
        self.not_exist_dial_text = ''
        self.csfb_fail_text = ''
        self.mp_not_conn_text = ''
        self.trgw_nego_fail_text = ''
        self.trgw_no_rtp_fail_text = ''
        self.trgw_insufficent_rsc_text = ''
        self.trgw_sdp_incorrect_text = ''
        self.trgw_incorrect_text = ''
        self.route_sts_down_text = ''
        self.npdb_sts_down_text = ''
        self.igw_sts_down_text = ''       

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%32s = %d" % ('REASON_CODE_ID', imsg.m_uiID)

        if imsg.m_szDesc != '':
            print "\t" "%32s = %s" % ('NAME', self.reprName(imsg.m_szDesc))

        if self.system_overload_code != '0':
            print "\t" "%32s = %s" % ('SYSTEM_OVERLOAD_CAUSE', self.system_overload_code)    
            
        if self.system_cps_overload_code != '0':
            print "\t" "%32s = %s" % ('CPS_OVERLOAD_CAUSE', self.system_cps_overload_code)             

        if self.system_cpu_overload_code != '0':
            print "\t" "%32s = %s" % ('CPU_OVERLOAD_CAUSE', self.system_cpu_overload_code)  
  
        if self.system_mem_overload_code != '0':
            print "\t" "%32s = %s" % ('MEM_OVERLOAD_CAUSE', self.system_mem_overload_code)        

        if self.unknown_route_code != '0':
            print "\t" "%32s = %s" % ('UNKNOWN_ROUTE_CAUSE', self.unknown_route_code)
            
        if self.routing_fail_code != '0':
            print "\t" "%32s = %s" % ('ROUTING_FAIL_CAUSE', self.routing_fail_code)
            
        if self.internal_error_code != '0':
            print "\t" "%32s = %s" % ('INTERNAL_ERR_CAUSE', self.internal_error_code)

        if self.incorrect_msg_code != '0':
            print "\t" "%32s = %s" % ('INCORRECT_MSG_CAUSE', self.incorrect_msg_code)
            
        if self.filter_deny_code != '0':
            print "\t" "%32s = %s" % ('FILTER_DENY_CAUSE', self.filter_deny_code)            

        if self.not_exist_dial_code != '0':
            print "\t" "%32s = %s" % ('SESSION_NOT_EXIST_CAUSE', self.not_exist_dial_code) 
            
        if self.csfb_fail_code != '0':
            print "\t" "%32s = %s" % ('TIMEOUT_ERR_CAUSE', self.csfb_fail_code) 
            
        if self.mp_not_conn_code != '0':
            print "\t" "%32s = %s" % ('MP_NOTCONT_CAUSE', self.mp_not_conn_code)                         

        if self.trgw_nego_fail_code != '0':
            print "\t" "%32s = %s" % ('TRGW_NEGO_FAIL_CAUSE', self.trgw_nego_fail_code)  
            
        if self.trgw_no_rtp_fail_code != '0':
            print "\t" "%32s = %s" % ('TRGW_NO_RTP_FAI_CAUSE', self.trgw_no_rtp_fail_code)  
            
        if self.trgw_insufficent_rsc_code != '0':
            print "\t" "%32s = %s" % ('TRGW_INSUFFICIENT_RSC_CAUSE', self.trgw_insufficent_rsc_code)  
            
        if self.trgw_sdp_incorrect_code != '0':
            print "\t" "%32s = %s" % ('TRGW_SDP_INCORRECT_CAUSE', self.trgw_sdp_incorrect_code)  
            
        if self.trgw_incorrect_code != '0':
            print "\t" "%32s = %s" % ('TRGW_INCORRECT_CAUSE', self.trgw_incorrect_code)  
            
        if self.route_sts_down_code != '0':
            print "\t" "%32s = %s" % ('ROUTE_STS_DOWN_CAUSE', self.route_sts_down_code)                                                              

        if self.npdb_sts_down_code != '0':
            print "\t" "%32s = %s" % ('NPDB_TIMEOUT_CAUSE', self.npdb_sts_down_code)

        if self.igw_sts_down_code != '0':
            print "\t" "%32s = %s" % ('IGW_TIMEOUT_CAUSE', self.igw_sts_down_code)

        ######################################################################################################
        
        if self.system_overload_rsp_code != '0':
            print "\t" "%32s = %s" % ('SYSTEM_OVERLOAD_RSP_CODE', self.system_overload_rsp_code)    
            
        if self.system_cps_overload_rsp_code != '0':
            print "\t" "%32s = %s" % ('CPS_OVERLOAD_RSP_CODE', self.system_cps_overload_rsp_code)             

        if self.system_cpu_overload_rsp_code != '0':
            print "\t" "%32s = %s" % ('CPU_OVERLOAD_RSP_CODE', self.system_cpu_overload_rsp_code)  
  
        if self.system_mem_overload_rsp_code != '0':
            print "\t" "%32s = %s" % ('MEM_OVERLOAD_RSP_CODE', self.system_mem_overload_rsp_code)        

        if self.unknown_route_rsp_code != '0':
            print "\t" "%32s = %s" % ('UNKNOWN_ROUTE_RSP_CODE', self.unknown_route_rsp_code)
            
        if self.routing_fail_rsp_code != '0':
            print "\t" "%32s = %s" % ('ROUTING_FAIL_RSP_CODE', self.routing_fail_rsp_code)
            
        if self.internal_error_rsp_code != '0':
            print "\t" "%32s = %s" % ('INTERNAL_ERR_RSP_CODE', self.internal_error_rsp_code)

        if self.incorrect_msg_rsp_code != '0':
            print "\t" "%32s = %s" % ('INCORRECT_MSG_RSP_CODE', self.incorrect_msg_rsp_code)
            
        if self.filter_deny_rsp_code != '0':
            print "\t" "%32s = %s" % ('FILTER_DENY_RSP_CODE', self.filter_deny_rsp_code)            

        if self.not_exist_dial_rsp_code != '0':
            print "\t" "%32s = %s" % ('SESSION_NOT_EXIST_RSP_CODE', self.not_exist_dial_rsp_code) 
            
        if self.csfb_fail_rsp_code != '0':
            print "\t" "%32s = %s" % ('TIMEOUT_ERR_RSP_CODE', self.csfb_fail_rsp_code) 
            
        if self.mp_not_conn_rsp_code != '0':
            print "\t" "%32s = %s" % ('MP_NOTCONT_RSP_CODE', self.mp_not_conn_rsp_code)                         

        if self.trgw_nego_fail_rsp_code != '0':
            print "\t" "%32s = %s" % ('TRGW_NEGO_FAIL_RSP_CODE', self.trgw_nego_fail_rsp_code)  
            
        if self.trgw_no_rtp_fail_rsp_code != '0':
            print "\t" "%32s = %s" % ('TRGW_NO_RTP_FAI_RSP_CODE', self.trgw_no_rtp_fail_rsp_code)  
            
        if self.trgw_insufficent_rsc_rsp_code != '0':
            print "\t" "%32s = %s" % ('TRGW_INSUFFICIENT_RSC_RSP_CODE', self.trgw_insufficent_rsc_rsp_code)  
            
        if self.trgw_sdp_incorrect_rsp_code != '0':
            print "\t" "%32s = %s" % ('TRGW_SDP_INCORRECT_RSP_CODE', self.trgw_sdp_incorrect_rsp_code)  
            
        if self.trgw_incorrect_rsp_code != '0':
            print "\t" "%32s = %s" % ('TRGW_INCORRECT_RSP_CODE', self.trgw_incorrect_rsp_code)  
            
        if self.route_sts_down_rsp_code != '0':
            print "\t" "%32s = %s" % ('ROUTE_STS_DOWN_RSP_CODE', self.route_sts_down_rsp_code)          
         
        if self.npdb_sts_down_rsp_code != '0':
            print "\t" "%32s = %s" % ('NPDB_TIMEOUT_RSP_CAUSE', self.npdb_sts_down_rsp_code)

        if self.igw_sts_down_rsp_code != '0':
            print "\t" "%32s = %s" % ('IGW_TIMEOUT_RSP_CAUSE', self.igw_sts_down_rsp_code)

        ###################################################################################################### 
            
        if self.system_overload_text != '':
            print "\t" "%32s = %s" % ('SYSTEM_OVERLOAD_TEXT', self.system_overload_text)

        if self.system_cps_overload_text != '':
            print "\t" "%32s = %s" % ('CPS_OVERLOAD_TEXT', self.system_cps_overload_text)

        if self.system_cpu_overload_text != '':
            print "\t" "%32s = %s" % ('CPU_OVERLOAD_TEXT', self.system_cpu_overload_text)

        if self.system_mem_overload_text != '':
            print "\t" "%32s = %s" % ('MEM_OVERLOAD_TEXT', self.system_mem_overload_text)

        if self.unknown_route_text != '':
            print "\t" "%32s = %s" % ('UNKNOWN_ROUTE_TEXT', self.unknown_route_text)

        if self.routing_fail_text != '':
            print "\t" "%32s = %s" % ('ROUTING_FAIL_TEXT', self.routing_fail_text)
            
        if self.internal_error_text != '':
            print "\t" "%32s = %s" % ('INTERNAL_ERR_TEXT', self.internal_error_text)

        if self.incorrect_msg_text != '':
            print "\t" "%32s = %s" % ('INCORRECT_MSG_TEXT', self.incorrect_msg_text)
            
        if self.filter_deny_text != '':
            print "\t" "%32s = %s" % ('FILTER_DENY_TEXT', self.filter_deny_text)

        if self.not_exist_dial_text != '':
            print "\t" "%32s = %s" % ('SESSION_NOT_EXIST_TEXT', self.not_exist_dial_text)
            
        if self.csfb_fail_text != '':
            print "\t" "%32s = %s" % ('TIMEOUT_ERR_TEXT', self.csfb_fail_text)
            
        if self.mp_not_conn_text != '':
            print "\t" "%32s = %s" % ('MP_NOTCONT_TEXT', self.mp_not_conn_text)                      

        if self.trgw_nego_fail_text != '':
            print "\t" "%32s = %s" % ('TRGW_NEGO_FAIL_TEXT', self.trgw_nego_fail_text)
            
        if self.trgw_no_rtp_fail_text != '':
            print "\t" "%32s = %s" % ('TRGW_NO_RTP_FAI_TEXT', self.trgw_no_rtp_fail_text)
            
        if self.trgw_insufficent_rsc_text != '':
            print "\t" "%32s = %s" % ('TRGW_INSUFFICIENT_RSC_TEXT', self.trgw_insufficent_rsc_text)
            
        if self.trgw_sdp_incorrect_text != '':
            print "\t" "%32s = %s" % ('TRGW_SDP_INCORRECT_TEXT', self.trgw_sdp_incorrect_text)
            
        if self.trgw_incorrect_text != '':
            print "\t" "%32s = %s" % ('TRGW_INCORRECT_TEXT', self.trgw_incorrect_text)

        if self.npdb_sts_down_text != '':
            print "\t" "%32s = %s" % ('NPDB_TIMEOUT_TEXT', self.npdb_sts_down_text)

        if self.igw_sts_down_text != '':
            print "\t" "%32s = %s" % ('IGW_TIMEOUT_TEXT', self.igw_sts_down_text)

    def printOutputMessage(self, omsg):

        for st in omsg.m_stData :
            print "\t", "%15s : %d" % ('REASON_CODE_ID', st.m_uiID)
            print "\t", "%15s : %s" % ('NAME', st.m_szDesc)
            print "\t"
            print "\t", "%27s %s %s %s" % (' ', '  CAUSE ', ' RSPCODE ', ' TEXT')
            print "\t", "     ------------------------------------------------------"
            
            CauseList = self.reprRcCodeHexIntToIntAry(st.m_nCauseCode)
            RspCodeList = self.reprRcCodeHexIntToIntAry(st.m_nRspCode)
            TextList = self.reprRcTextHexToAry(st.m_szCause)

            for i in range(0, E_CAUSE_MAX):
                print "\t", "%27s = %4s  |  %4s  |  %s" % (self.NameTag[i], CauseList[i], RspCodeList[i], TextList[i])
            print "\t"
            print "\t"

        if omsg.uiSubType == DEF_STYPE_CS_DIS_RC_RSP: 
           print ""
           print "%-10s = %s" % ('RC_CNT', omsg.m_nNumber)


   
