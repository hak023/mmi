
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_RTE_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_RTE_REQ)
    
    
class MSG_EMS_CS_DIS_RTE_RSP(IbcfResponseMsg):
    
    """
struct SipRoute_t
{ 
   unsigned int   m_uiID                   ; //0. M, RTE, 1 ~ 9999999 
   char           m_szDesc[DEF_RTE_MAXLEN_DESC=40] ; //1. M, NAME, 
   unsigned int   m_uiLID                  ; //2. M, LOC_ID, 1 ~ 9999999, No Modify
   unsigned int   m_uiRID                  ; //3. M, RMT_ID, 1 ~ 9999999, No Modify
   unsigned int   m_uiTRTE                 ; //4. M, TRTE, 1 ~ 9999999
   unsigned char  m_ucType                 ; //5. M, TYPE, MINE/OTHER
   unsigned char  m_ucDoRouteMedia         ; //6. M, MEDIA, see enum EMgwRouteFlag_t (1:ROUTED, 2:DIRECTED)
   short          m_sOptTime               ; //7. M, OPT_TIME, (sec) (0 ~ 999999)
   short          m_sOptRetry              ; //8. M, RETRY, (0 ~ 999999)
   short          m_sOptAction             ; //9. M, ACTION, see enum ENodeManagement_t
   short          m_sSesRefreshTime        ; //10. M, SES_TIM, 0 ~ 999999
   int            m_nRouteGroup            ; //11. O, GROUP, 1 ~ 999999
   int            m_nMAXCnt                ; //12. M, MAX_CNT, 1 ~ 999999
   int            m_nDeactRsp              ; //13. M, DEACT_RSP, see num  EDeactResponseControl_t
   unsigned char  m_ucReserved[4]          ; //nothing.
   
   ////////the below api set ////////////////
   unsigned char  m_ucStatus               ; //status, see eum EIPNodeStatus_t, print
   unsigned char  m_ucProto                ; //nothing. see ETransPortType_t
   unsigned char  m_ucUsed                 ; //used flag
   unsigned char  m_ucReserved2            ; 
   unsigned int   m_uiBusyCnt              ; //O, busy count, print
   unsigned int   m_uiICCnt                ; //O, ic count, print
   unsigned int   m_uiOGCnt                ; //O, og count, print
   int            m_nCurRetry              ; //current retry
   int            m_nIndex                 ; //internal index   
};

typedef struct Cs_dis_rte_rsp : public SipRouteDataBase_t
{
    int m_nNumber;
    SipRoute_t m_stRte[E_RTE_MAXNUM=300];

    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_rte_rsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_RTE_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%dsIIIBBhhhhiii%dsBBBBIIIii" % (DEF_RTE_MAXLEN_DESC, 4))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_RTE_MAXNUM, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stRte m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_RTE_REQ unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%dsIIIBBhhhhiii%dsBBBBIIIii" % (DEF_RTE_MAXLEN_DESC, 4))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_uiLID m_uiRID m_uiTRTE m_ucType m_ucDoRouteMedia m_sOptTime m_sOptRetry m_sOptAction m_sSesRefreshTime m_nRouteGroup m_nMAXCnt m_nDeactRsp m_ucReserved m_ucStatus m_ucProto m_ucUsed m_usReserved2 m_uiBusyCnt m_uiICCnt m_uiOGCnt m_nCurRetry m_nIndex")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%dsIIIBBhhhhiii%dsBBBBIIIii" %(DEF_RTE_MAXLEN_DESC, 4), response.m_stRte[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stRte = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_RTE_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_RTE_REQ)

class MSG_EMS_CS_DEL_RTE_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_RTE_RSP)


###############################################################################################################################################

class SipRoute_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%dsIIIBBhhhhhiii%dsBBBBIIIii" % (DEF_RTE_MAXLEN_DESC, 4)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_uiLID m_uiRID m_uiTRTE m_ucType m_ucDoRouteMedia m_sOptTime m_sOptRetry m_sOptAction m_sSesRefreshTime m_temp m_nRouteGroup m_nMAXCnt m_nDeactRsp m_ucReserved m_ucStatus m_ucProto m_ucUsed m_usReserved2 m_uiBusyCnt m_uiICCnt m_uiOGCnt m_nCurRetry m_nIndex"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, self.m_uiLID, self.m_uiRID, self.m_uiTRTE, self.m_ucType, self.m_ucDoRouteMedia, \
                    self.m_sOptTime, self.m_sOptRetry, self.m_sOptAction, self.m_sSesRefreshTime, self.m_temp, self.m_nRouteGroup, \
                    self.m_nMAXCnt, self.m_nDeactRsp, \
                    self.m_ucReserved, \
                    self.m_ucStatus, \
                    self.m_ucProto, self.m_ucUsed, self.m_usReserved2, \
                    self.m_uiBusyCnt, self.m_uiICCnt, self.m_uiOGCnt, \
                    self.m_nCurRetry, self.m_nIndex);

    """

typedef struct Cs_add_rte_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    SipRoute_t m_stRte;

} Cs_add_rte_rsp_t;
    """

class SipRoute_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%dsIIIBBhhhhiii%dsBBBBIIIii" % (DEF_RTE_MAXLEN_DESC, 4))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stRte"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%dsIIIBBhhhhiii%dsBBBBIIIii" % (DEF_RTE_MAXLEN_DESC, 4))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_uiLID m_uiRID m_uiTRTE m_ucType m_ucDoRouteMedia m_sOptTime m_sOptRetry m_sOptAction m_sSesRefreshTime m_nRouteGroup m_nMAXCnt m_nDeactRsp m_ucReserved m_ucStatus m_ucProto m_ucUsed m_usReserved2 m_uiBusyCnt m_uiICCnt m_uiOGCnt m_nCurRetry m_nIndex")
 
        new_list.append(StructInfo._make(unpack("I%dsIIIBBhhhhiii%dsBBBBIIIii" %(DEF_RTE_MAXLEN_DESC, 4), response.m_stRte)))
        response = response._replace(m_stRte = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_RTE_REQ(SipRoute_t_REQ):

    '''
typedef SipRoute_t Cs_add_rte_req_t;
    '''
    
    def __init__(self):
        SipRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_RTE_REQ)


class MSG_EMS_CS_ADD_RTE_RSP(SipRoute_t_RSP):

    def __init__(self):
        SipRoute_t_RSP.__init__(self, DEF_STYPE_CS_ADD_RTE_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_RTE_REQ(SipRoute_t_REQ):
    
    '''
typedef SipRoute_t Cs_chg_rte_req_t;
    '''
    
    def __init__(self):
        SipRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_RTE_REQ)

    '''
typedef Cs_add_rte_rsp_t Cs_chg_rte_rsp_t;
    '''

class MSG_EMS_CS_CHG_RTE_RSP(SipRoute_t_RSP):
    
    def __init__(self):
        SipRoute_t_RSP.__init__(self, DEF_STYPE_CS_CHG_RTE_RSP)

###############################################################################################################################################

'''
struct SipRoute_t
{ 
   unsigned int   m_uiID                   ; //0. M, RTE, 1 ~ 9999999 
   char m_szDesc[DEF_RTE_MAXLEN_DESC]      ; //1. M, NAME, 
   unsigned int   m_uiLID                  ; //2. M, LOC_ID, 1 ~ 9999999, No Modify
   unsigned int   m_uiRID                  ; //3. M, RMT_ID, 1 ~ 9999999, No Modify
   unsigned int   m_uiTRTE                 ; //4. M, TRTE, 1 ~ 9999999
   unsigned char  m_ucType                 ; //5. M, TYPE, MINE/OTHER
   unsigned char  m_ucDoRouteMedia         ; //6. M, MEDIA, see enum EMgwRouteFlag_t (1:ROUTED, 2:DIRECTED)
   short          m_sOptTime               ; //7. M, OPT_TIME, (sec) (0 ~ 999999)
   short          m_sOptRetry              ; //8. M, RETRY, (0 ~ 999999)
   short          m_sOptAction             ; //9. M, ACTION, see enum ENodeManagement_t
   short          m_sSesRefreshTime        ; //10. M, SES_TIM, 0 ~ 999999
   int            m_nRouteGroup            ; //11. O, GROUP, 1 ~ 999999
   int            m_nMAXCnt                ; //12. M, MAX_CNT, 1 ~ 999999
   int            m_nDeactRsp              ; //13. M, DEACT_RSP, see num  EDeactResponseControl_t
   unsigned char  m_ucReserved[4]          ; //nothing.
   
   ////////the below api set ////////////////
   unsigned char  m_ucStatus               ; //status, see eum EIPNodeStatus_t, print
   unsigned char  m_ucProto                ; //nothing. see ETransPortType_t
   unsigned char  m_ucUsed                 ; //used flag
   unsigned char  m_ucReserved2            ; 
   unsigned int   m_uiBusyCnt              ; //O, busy count, print
   unsigned int   m_uiICCnt                ; //O, ic count, print
   unsigned int   m_uiOGCnt                ; //O, og count, print
   int            m_nCurRetry              ; //current retry
   int            m_nIndex                 ; //internal index   
};
'''
class SipRteCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_temp = 0
        
        self.request.m_ucReserved = ''
        self.request.m_ucStatus = 0
        self.request.m_ucProto = 0
        self.request.m_ucUsed = 0
        self.request.m_usReserved2 = 0
        self.request.m_uiBusyCnt = 0
        self.request.m_uiICCnt = 0
        self.request.m_uiOGCnt = 0
        self.request.m_nCurRetry = 0
        self.request.m_nIndex = 0
        
        self.isIdxSearch = 0
        self.rtecnt = 0
        self.printRteCnt = 0
        self.rangeCntStart = 0
        self.rangeCntEnd = 0              

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RTE', imsg.m_uiID)
        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szDesc))

        if imsg.m_uiLID != 0:
            print "\t" "%12s = %s" % ('LOC_ID', imsg.m_uiLID)

        if imsg.m_uiRID != 0:
            print "\t" "%12s = %s" % ('RMT_ID', imsg.m_uiRID)

        if imsg.m_uiTRTE != 0:
            print "\t" "%12s = %s" % ('TRTE', imsg.m_uiTRTE)

        if imsg.m_ucType != 0:
            print "\t" "%12s = %s" % ('TYPE', self.reprRteTypeIntToStr(imsg.m_ucType))

        if imsg.m_ucDoRouteMedia != 0:
            print "\t" "%12s = %s" % ('MEDIA', self.reprRteMediaIntToStr(imsg.m_ucDoRouteMedia))
        
        if imsg.m_sOptTime != -1:
            print "\t" "%12s = %s" % ('OPT_TIME', imsg.m_sOptTime)

        if imsg.m_sOptRetry != -1:
            print "\t" "%12s = %s" % ('RETRY', imsg.m_sOptRetry)

        if imsg.m_sOptAction != -1:
            print "\t" "%12s = %s" % ('ACTION', self.reprActionIntToStr(imsg.m_sOptAction))

        if imsg.m_sSesRefreshTime != -1:
            print "\t" "%12s = %s" % ('SES_TIME', imsg.m_sSesRefreshTime)

        if imsg.m_nRouteGroup != -1:
            print "\t" "%12s = %d" % ('GROUP_ID', imsg.m_nRouteGroup)
            
        if imsg.m_nMAXCnt != -1:
            print "\t" "%12s = %d" % ('MAX_CNT', imsg.m_nMAXCnt)        

        if imsg.m_nDeactRsp != -1:
            print "\t" "%12s = %s" % ('DEACT_RSP', self.reprReponseIntToStr(imsg.m_nDeactRsp))

    def printOutputMessage(self, omsg):     
        
        if self.isIdxSearch == 0:
           print "\t", "%7s %25s %10s %10s %10s %10s %10s %8s %7s %7s %9s %9s %9s %8s %10s %13s" % ('RTE', 'NAME', 'LOC_ID', 'RMT_ID', 'TRTE', 'TYPE', 'MEDIA', 'OPT_TIME', 'RETRY', 'ACTION', 'SES_TIME', 'GROUP_ID', 'PROTOCOL', 'MAX_CNT', 'DEACT_RSP', 'STATUS')
           print "\t", " --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        
           for st in sorted(omsg.m_stRte) :
               
               if self.rangeCntStart != 0:
                  if self.rangeCntEnd != 0: 
                     self.rtecnt = self.rtecnt + 1
               
               if self.rangeCntStart <= self.rtecnt:
                  if self.rangeCntEnd >= self.rtecnt:
                     self.printRteCnt = self.printRteCnt + 1
                     print "\t", "%7d %25s %10d %10d %10d %10s %10s %8d %7d %7s %9d %9d %9s %8d %10s %13s" % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 25, 20), st.m_uiLID, st.m_uiRID, 
                                                                               st.m_uiTRTE, self.reprRteTypeIntToStr(st.m_ucType), 
                                                                               self.reprRteMediaIntToStr(st.m_ucDoRouteMedia), st.m_sOptTime, st.m_sOptRetry,
                                                                               self.reprActionIntToStr(st.m_sOptAction), st.m_sSesRefreshTime, st.m_nRouteGroup, self.reprProctIntToStr(st.m_ucProto),
                                                                               st.m_nMAXCnt, self.reprReponseIntToStr(st.m_nDeactRsp), self.reprStsIntToStr(st.m_ucStatus)
                                                                               )
        elif self.isIdxSearch == 1:
           for st in omsg.m_stRte :
               print "\t"
               print "\t" "%12s = %d" % ('RTE', st.m_uiID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szDesc))
               print "\t" "%12s = %d" % ('LOC_ID', st.m_uiLID)
               print "\t" "%12s = %d" % ('RMT_ID', st.m_uiRID)
               print "\t" "%12s = %s" % ('TRTE', st.m_uiTRTE)
               print "\t" "%12s = %s" % ('TYPE', self.reprRteTypeIntToStr(st.m_ucType))
               print "\t" "%12s = %s" % ('MEDIA', self.reprRteMediaIntToStr(st.m_ucDoRouteMedia))
               print "\t" "%12s = %d" % ('OPT_TIME', st.m_sOptTime)
               print "\t" "%12s = %d" % ('RETRY', st.m_sOptRetry)
               print "\t" "%12s = %s" % ('ACTION', self.reprActionIntToStr(st.m_sOptAction))
               print "\t" "%12s = %d" % ('SES_TIME', st.m_sSesRefreshTime)
               print "\t" "%12s = %d" % ('GROUP_ID', st.m_nRouteGroup)
               print "\t" "%12s = %s" % ('PROTOCOL', self.reprProctIntToStr(st.m_ucProto))
               #print "\t" "%12s = %d" % ('BUSY_CNT', st.m_uiBusyCnt)
               print "\t" "%12s = %d" % ('MAX_CNT', st.m_nMAXCnt)
               print "\t" "%12s = %s" % ('DEACT_RSP', self.reprReponseIntToStr(st.m_nDeactRsp))
               print "\t" "%12s = %s" % ('STATUS', self.reprStsIntToStr(st.m_ucStatus))
        
        if omsg.uiSubType == DEF_STYPE_CS_DIS_RTE_RSP: 
           print ""
           if self.rangeCntStart != 0:
              if self.rangeCntEnd != 0:
                 print "%-10s = %s" % ('RTE_CNT', self.printRteCnt)
           else:
              print "%-10s = %s" % ('RTE_CNT', omsg.m_nNumber)

   
