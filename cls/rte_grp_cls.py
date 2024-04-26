
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_RTE_GRP_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_RTE_GRP_REQ)
    
    
class MSG_EMS_CS_DIS_RTE_GRP_RSP(IbcfResponseMsg):
    
    """
    
struct SipRouteGroup_t
{
   unsigned int   m_uiID                   ; //0. M, GROUP_ID,    1~9999999
   char m_szDesc[DEF_RTE_MAXLEN_DESC]      ; //1. M, NAME,  
   int            m_nMaxCPS_LB             ; //2. M, LMT_LB_CPS,   1~1000
   int            m_nCtrlCPSOn_LB          ; //3. M, LMT_LB_CPS_ON, 0:OFF, 1:ON
   int            m_nMaxTPS_LB             ; //4. M, LMT_LB_TPS,   1~9999999
   int            m_nCtrlTPSOn_LB          ; //5. M, LMT_LB_TPS_ON, 0:OFF, 1:ON

   int            m_nMaxCPS                ; //6. M, LMT_CM_CPS,   1~1000
   int            m_nCtrlCPSOn             ; //7. M, LMT_CM_CPS_ON, 0:OFF, 1:ON
   int            m_nMaxTPS                ; //8. M, LMT_CM_TPS,   1~9999999
   int            m_nCtrlTPSOn             ; //9. M, LMT_CM_TPS_ON, 0:OFF, 1:ON
   int            m_nRspID                 ; //10. M, RSP_ID,    1~9999999

   int            m_nChargingOn            ; //11. M, CHARGING_ON, 1:ON/0:OFF
   int            m_nChargingCode          ; //12. M, CHARGING_CODE, 1~9999999
   int            m_nChargingIDC           ; //13. M, CHARGING_IDC, 0 ~ 9999999
   int            m_nRoamingIDC            ; //14. M, ROAMING_IDC, 0 ~ 9999999

   ////////the below api set ////////////////
   int            m_nCurCPS                ; //15. O, CUR_CPS, print
   int            m_nCurTPS                ; //16. O, CUR_TPS, print
   unsigned char  m_ucUsed                 ; //used flag
   unsigned char  m_ucInterDel             ; //internal delete
   unsigned char  m_ucReserved[2]          ; //reserved
   int            m_nIndex                 ; //internal
   
   // IBCF R131
   int m_nNpdbEnable;
   int m_nIgwEnable   
};

typedef struct Cs_dis_rte_grp_rsp : public SipRouteGroupDataBase_t
{
   int m_nNumber;
   SipRouteGroup_t m_stRteGroup[E_MAXNUM=40];
   
   int m_nResult;
   int m_nReason;
   char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_rte_grp_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_RTE_GRP_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%dsiiiiiiiiiiiiiiiBB%dsiii" % (DEF_RTE_MAXLEN_DESC, 2))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_RTE_GRP_MAXNUM, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stRteGroup m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_RTE_GRP_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%dsiiiiiiiiiiiiiiiBB%dsiii" % (DEF_RTE_MAXLEN_DESC, 2))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_nMaxCPS_LB m_nCtrlCPSOn_LB m_nMaxTPS_LB m_nCtrlTPSOn_LB m_nMaxCPS m_nCtrlCPSOn m_nMaxTPS m_nCtrlTPSOn m_nRspID m_nChargingOn m_nChargingCode m_nChargingIDC m_nRoamingIDC m_nCurCPS m_nCurTPS m_ucUsed m_ucInterDel m_ucReserved m_nIndex m_nNpdbEnable m_nIgwEnable")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("i%dsiiiiiiiiiiiiiiiBB%dsiii" %(DEF_RTE_MAXLEN_DESC, 2), response.m_stRteGroup[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stRteGroup = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_RTE_GRP_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_RTE_GRP_REQ)

class MSG_EMS_CS_DEL_RTE_GRP_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_RTE_GRP_RSP)


###############################################################################################################################################

class SipRouteGroup_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "i%dsiiiiiiiiiiiiiiiBB%dsiii" % (DEF_RTE_MAXLEN_DESC, 2)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_nMaxCPS_LB m_nCtrlCPSOn_LB m_nMaxTPS_LB m_nCtrlTPSOn_LB m_nMaxCPS m_nCtrlCPSOn m_nMaxTPS m_nCtrlTPSOn m_nRspID m_nChargingOn m_nChargingCode m_nChargingIDC m_nRoamingIDC m_nCurCPS m_nCurTPS m_ucUsed m_ucInterDel m_ucReserved m_nIndex m_nNpdbEnable m_nIgwEnable"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, \
                    self.m_nMaxCPS_LB, self.m_nCtrlCPSOn_LB, self.m_nMaxTPS_LB, self.m_nCtrlTPSOn_LB, \
                    self.m_nMaxCPS, self.m_nCtrlCPSOn, self.m_nMaxTPS, self.m_nCtrlTPSOn, \
                    self.m_nRspID, self.m_nChargingOn, self.m_nChargingCode, self.m_nChargingIDC, self.m_nRoamingIDC, \
                    self.m_nCurCPS, self.m_nCurTPS, self.m_ucUsed, self.m_ucInterDel, self.m_ucReserved, self.m_nIndex, self.m_nNpdbEnable, self.m_nIgwEnable);

    """
typedef struct Cs_add_rte_grp_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    SipRouteGroup_t m_stRteGrp;

} Cs_add_rte_grp_rsp_t;
    """

class SipRouteGroup_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("i%dsiiiiiiiiiiiiiiiBB%dsiii" % (DEF_RTE_MAXLEN_DESC, 2))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stRteGroup"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%dsiiiiiiiiiiiiiiiBB%dsiii" % (DEF_RTE_MAXLEN_DESC, 2))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_nMaxCPS_LB m_nCtrlCPSOn_LB m_nMaxTPS_LB m_nCtrlTPSOn_LB m_nMaxCPS m_nCtrlCPSOn m_nMaxTPS m_nCtrlTPSOn m_nRspID m_nChargingOn m_nChargingCode m_nChargingIDC m_nRoamingIDC m_nCurCPS m_nCurTPS m_ucUsed m_ucInterDel m_ucReserved m_nIndex m_nNpdbEnable m_nIgwEnable")
 
        new_list.append(StructInfo._make(unpack("i%dsiiiiiiiiiiiiiiiBB%dsiii" %(DEF_RTE_MAXLEN_DESC, 2), response.m_stRteGroup)))
        response = response._replace(m_stRteGroup = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_RTE_GRP_REQ(SipRouteGroup_t_REQ):

    '''
typedef SipRoute_t Cs_add_rte_req_t;
    '''
    
    def __init__(self):
        SipRouteGroup_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_RTE_GRP_REQ)


class MSG_EMS_CS_ADD_RTE_GRP_RSP(SipRouteGroup_t_RSP):

    def __init__(self):
        SipRouteGroup_t_RSP.__init__(self, DEF_STYPE_CS_ADD_RTE_GRP_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_RTE_GRP_REQ(SipRouteGroup_t_REQ):
    
    '''
typedef SipRoute_t Cs_chg_rte_req_t;
    '''
    
    def __init__(self):
        SipRouteGroup_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_RTE_GRP_REQ)

    '''
typedef Cs_add_rte_rsp_t Cs_chg_rte_rsp_t;
    '''

class MSG_EMS_CS_CHG_RTE_GRP_RSP(SipRouteGroup_t_RSP):
    
    def __init__(self):
        SipRouteGroup_t_RSP.__init__(self, DEF_STYPE_CS_CHG_RTE_GRP_RSP)

###############################################################################################################################################

'''
struct SipRouteGroup_t
{
   unsigned int   m_uiID                   ; //0. M, GROUP_ID,    1~9999999
   char m_szDesc[DEF_RTE_MAXLEN_DESC]      ; //1. M, NAME,  

   int            m_nMaxCPS_LB             ; //2. M, LMT_LB_CPS,   1~1000
   int            m_nCtrlCPSOn_LB          ; //3. M, LMT_LB_CPS_ON, 0:OFF, 1:ON
   int            m_nMaxTPS_LB             ; //4. M, LMT_LB_TPS,   1~9999999
   int            m_nCtrlTPSOn_LB          ; //5. M, LMT_LB_TPS_ON, 0:OFF, 1:ON

   int            m_nMaxCPS                ; //6. M, LMT_CM_CPS,   1~1000
   int            m_nCtrlCPSOn             ; //7. M, LMT_CM_CPS_ON, 0:OFF, 1:ON
   int            m_nMaxTPS                ; //8. M, LMT_CM_TPS,   1~9999999
   int            m_nCtrlTPSOn             ; //9. M, LMT_CM_TPS_ON, 0:OFF, 1:ON
   int            m_nRspID                 ; //10. M, RSP_ID,    1~9999999

   int            m_nChargingOn            ; //11. M, CHARGING_ON, 1:ON/0:OFF
   int            m_nChargingCode          ; //12. M, CHARGING_CODE, 1~9999999
   int            m_nChargingIDC           ; //13. M, CHARGING_IDC, 0 ~ 9999999
   int            m_nRoamingIDC            ; //14. M, ROAMING_IDC, 0 ~ 9999999

   ////////the below api set ////////////////
   int            m_nCurCPS                ; //15. O, CUR_CPS, print
   int            m_nCurTPS                ; //16. O, CUR_TPS, print
   unsigned char  m_ucUsed                 ; //used flag
   unsigned char  m_ucInterDel             ; //internal delete
   unsigned char  m_ucReserved[2]          ; //reserved
   int            m_nIndex                 ; //internal
   
   // IBCF R131
   int            m_nNpdbEnable;
   int            m_nIgwEnable;
};
'''
class SipRteGrpCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_nCurCPS = 0
        self.request.m_nCurTPS = 0
        self.request.m_ucUsed = 0
        self.request.m_ucInterDel = 0        
        self.request.m_ucReserved = ''
        self.request.m_nIndex = 0
        
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('GROUP_ID', imsg.m_uiID)
        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szDesc))

        if imsg.m_nMaxCPS_LB != -1:
            print "\t" "%12s = %d" % ('LMT_CPS_LB', imsg.m_nMaxCPS_LB)

        if imsg.m_nCtrlCPSOn_LB != -1:
            print "\t" "%12s = %s" % ('LMT_CPS_ON_LB', self.reprOnOffIntToStr(int(imsg.m_nCtrlCPSOn_LB)))

        if imsg.m_nMaxTPS_LB != -1:
            print "\t" "%12s = %d" % ('LMT_TPS_LB', imsg.m_nMaxTPS_LB)

        if imsg.m_nCtrlTPSOn_LB != -1:
            print "\t" "%12s = %s" % ('LMT_TPS_ON_LB', self.reprOnOffIntToStr(int(imsg.m_nCtrlTPSOn_LB)))

        if imsg.m_nMaxCPS != -1:
            print "\t" "%12s = %d" % ('LMT_CPS', imsg.m_nMaxCPS)

        if imsg.m_nCtrlCPSOn != -1:
            print "\t" "%12s = %s" % ('LMT_CPS_ON_LB', self.reprOnOffIntToStr(int(imsg.m_nCtrlCPSOn)))

        if imsg.m_nMaxTPS != -1:
            print "\t" "%12s = %d" % ('LMT_TPS_LB', imsg.m_nMaxTPS)

        if imsg.m_nCtrlTPSOn != -1:
            print "\t" "%12s = %s" % ('LMT_TPS_ON_LB', self.reprOnOffIntToStr(int(imsg.m_nCtrlTPSOn)))

        if imsg.m_nRspID != -1:
            print "\t" "%12s = %d" % ('REASON_CODE_ID', imsg.m_nRspID)

        if imsg.m_nChargingOn != -1:
            print "\t" "%12s = %s" % ('CHARGING_ON', self.reprOnOffIntToStr(int(imsg.m_nChargingOn)))

        if imsg.m_nChargingCode != -1:
            print "\t" "%12s = %d" % ('CHARGING_CODE', imsg.m_nChargingCode)

        if imsg.m_nChargingIDC != -1:
            print "\t" "%12s = %d" % ('CHARGING_IDC', imsg.m_nChargingIDC)

        if imsg.m_nRoamingIDC != -1:
            print "\t" "%12s = %d" % ('ROAMING_IDC', imsg.m_nRoamingIDC)

        if imsg.m_nNpdbEnable != -1:
            print "\t" "%12s = %s" % ('NPDB_ON', self.reprOnOffIntToStr(int(imsg.m_nNpdbEnable)))

        if imsg.m_nIgwEnable != -1:
            print "\t" "%12s = %s" % ('IGW_ON', self.reprOnOffIntToStr(int(imsg.m_nIgwEnable)))
            

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%10s %15s %10s %15s %15s %15s %10s %10s %10s %10s %15s %12s %14s %13s %12s %8s %7s" % ('GROUP_ID', 'NAME', 'LMT_CPS_LB', 'LMT_CPS_LB_ON', 'LMT_TPS_LB', 'LMT_TPS_LB_ON', 'LMT_CPS', 'LMT_CPS_ON', 'LMT_TPS', 'LMT_TPS_ON', 'REASON_CODE_ID', 'CHARGING_ON', 'CHARGING_CODE', 'CHARGING_IDC', 'ROAMING_IDC', 'NPDB_ON', 'IGW_ON')
           print "\t", "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

           for st in sorted(omsg.m_stRteGroup) :
               print "\t", "%10d %15s %10d %15s %15d %15s %10d %10s %10d %10s %15d %12s %14d %13d %12d %8s %7s" % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 15, 10),
                                                             st.m_nMaxCPS_LB, self.reprOnOffIntToStr(int(st.m_nCtrlCPSOn_LB)),
                                                             st.m_nMaxTPS_LB, self.reprOnOffIntToStr(int(st.m_nCtrlTPSOn_LB)),
                                                             st.m_nMaxCPS, self.reprOnOffIntToStr(int(st.m_nCtrlCPSOn)),
                                                             st.m_nMaxTPS, self.reprOnOffIntToStr(int(st.m_nCtrlTPSOn)),
                                                             st.m_nRspID,
                                                             self.reprOnOffIntToStr(int(st.m_nChargingOn)), st.m_nChargingCode,
                                                             st.m_nChargingIDC, st.m_nRoamingIDC,
                                                             self.reprOnOffIntToStr(int(st.m_nNpdbEnable)), self.reprOnOffIntToStr(int(st.m_nIgwEnable))
                                                            )
        elif self.isIdxSearch == 1:
           for st in omsg.m_stRteGroup :
               print "\t"
               print "\t" "%15s = %d" % ('GROUP_ID', st.m_uiID)
               print "\t" "%15s = %s" % ('NAME', self.reprName(st.m_szDesc))
               print "\t" "%15s = %d" % ('LMT_CPS_LB', st.m_nMaxCPS_LB)
               print "\t" "%15s = %s" % ('LMT_CPS_LB_ON', self.reprOnOffIntToStr(int(st.m_nCtrlCPSOn_LB)))
               print "\t" "%15s = %s" % ('LMT_TPS_LB', st.m_nMaxTPS_LB)
               print "\t" "%15s = %s" % ('LMT_TPS_LB_ON', self.reprOnOffIntToStr(int(st.m_nCtrlTPSOn_LB)))               
               print "\t" "%15s = %d" % ('LMT_CPS', st.m_nMaxCPS)
               print "\t" "%15s = %s" % ('LMT_CPS_ON', self.reprOnOffIntToStr(int(st.m_nCtrlCPSOn)))
               print "\t" "%15s = %s" % ('LMT_TPS', st.m_nMaxTPS)
               print "\t" "%15s = %s" % ('LMT_TPS_ON', self.reprOnOffIntToStr(int(st.m_nCtrlTPSOn)))
               print "\t" "%15s = %d" % ('REASON_CODE_ID', st.m_nRspID)
               print "\t" "%15s = %s" % ('CHARGING_ON', self.reprOnOffIntToStr(int(st.m_nChargingOn)))
               print "\t" "%15s = %d" % ('CHARGING_CODE', st.m_nChargingCode)
               print "\t" "%15s = %d" % ('CHARGING_IDC', st.m_nChargingIDC)
               print "\t" "%15s = %d" % ('ROAMING_IDC', st.m_nRoamingIDC)
               print "\t" "%15s = %s" % ('NPDB_ON', self.reprOnOffIntToStr(int(st.m_nNpdbEnable)))
               print "\t" "%15s = %s" % ('IGW_ON', self.reprOnOffIntToStr(int(st.m_nIgwEnable)))

        if omsg.uiSubType == DEF_STYPE_CS_DIS_RTE_GRP_RSP: 
           print ""
           print "%-10s = %s" % ('RTE_GRP_CNT', omsg.m_nNumber)

   
