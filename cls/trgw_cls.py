
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_TRGW_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_TRGW_REQ)
    
    
class MSG_EMS_CS_DIS_TRGW_RSP(IbcfResponseMsg):
    
    """
struct TrGWRoute_t
{
   unsigned int   m_uiID                             ; //0. M, ID, 1~9999999
   char           m_szDesc[DEF_RTE_MAXLEN_DESC]      ; //1. M, NAME,  
   char           m_szSvrIP[DEF_RTE_MAXLEN_IP]       ; //2. M, SVR_IP, No Modify
   char           m_szTrGWIP[DEF_RTE_MAXLEN_IP]      ; //3. M, TrGW_IP, No Modify
   unsigned short m_usSvrPort                        ; //4. M, SVR_PORT, 1 ~ 65535, No Modify
   unsigned short m_usTrGWPort                       ; //5. M, TrGW_PORT, 1 ~ 65535, No Modify
   int            m_nCallRate                        ; //6. M. CALL_RATE
   int            m_nMaxCount                        ; //7. M. MAX_SES
   int            m_nStatus                          ; //8. M. STATUS. see ETrGWConnectionStatus_t
   ////////the below api set ////////////////
   int            m_nCurCount                        ; //9. O. SES_CNT. print
   int            m_nIndex                           ; //internal index
   unsigned char  m_ucUsed                           ; //used flag
   unsigned char  m_ucReserved[3]                    ;
};

typedef struct Cs_dis_trgw_rsp : public TrGWDataBase_t
{
    int m_nNumber;
    TrGWRoute_t    m_stTrGW[E_MAXNUM=8];
    ///using only api
    int            m_nCurRATE[E_MAXNUM=8]; //internal
    int            m_nCurPos           ; //internal
   
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_trgw_rsp_t;;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_TRGW_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%ds%dsHHiiiiiB%ds" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        return FMT_UDP_HEADER + "i%ds%dsiii%ds" % (Struct_size * E_TRGW_MAXNUM, E_TRGW_MAXNUM * 4, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stTrGW m_nCurRATE m_nCurPos m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_TRGW_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%ds%dsHHiiiiiB%ds" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szSvrIP m_szTrGWIP m_usSvrPort m_usTrGWPort m_nCallRate m_nMaxCount m_nStatus m_nCurCount m_nIndex m_ucUsed m_ucReserved")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%ds%ds%dsHHiiiiiB%ds" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3), response.m_stTrGW[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stTrGW = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_TRGW_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_TRGW_REQ)

class MSG_EMS_CS_DEL_TRGW_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_TRGW_RSP)


###############################################################################################################################################

class TrGWRoute_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%ds%ds%dsHHiiiiiB%ds" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_szSvrIP m_szTrGWIP m_usSvrPort m_usTrGWPort m_nCallRate m_nMaxCount m_nStatus m_nCurCount m_nIndex m_ucUsed m_ucReserved"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, self.m_szSvrIP, self.m_szTrGWIP, self.m_usSvrPort, self.m_usTrGWPort, self.m_nCallRate, self.m_nMaxCount, self.m_nStatus, \
                    self.m_nCurCount, self.m_nIndex, self.m_ucUsed, self.m_ucReserved);

    """ 
typedef struct Cs_add_trgw_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    
    TrGWRoute_t m_stTrGW;

} Cs_add_trgw_rsp_t;
    """

class TrGWRoute_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%ds%dsHHiiiiiB%ds" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stTrGW"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%ds%dsHHiiiiiB%ds" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szSvrIP m_szTrGWIP m_usSvrPort m_usTrGWPort m_nCallRate m_nMaxCount m_nStatus m_nCurCount m_nIndex m_ucUsed m_ucReserved")
 
        new_list.append(StructInfo._make(unpack("I%ds%ds%dsHHiiiiiB%ds" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3), response.m_stTrGW)))
        response = response._replace(m_stTrGW = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_CS_ADD_TRGW_REQ(TrGWRoute_t_REQ):
    
    def __init__(self):
        TrGWRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_TRGW_REQ)

class MSG_EMS_CS_ADD_TRGW_RSP(TrGWRoute_t_RSP):

    def __init__(self):
        TrGWRoute_t_RSP.__init__(self, DEF_STYPE_CS_ADD_TRGW_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_TRGW_REQ(TrGWRoute_t_REQ):
    
    def __init__(self):
        TrGWRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_TRGW_REQ)

class MSG_EMS_CS_CHG_TRGW_RSP(TrGWRoute_t_RSP):
    
    def __init__(self):
        TrGWRoute_t_RSP.__init__(self, DEF_STYPE_CS_CHG_TRGW_RSP)

###############################################################################################################################################

class TrgwCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_nStatus = 0
        self.request.m_nCurCount = 0
        self.request.m_nIndex = 0
        self.request.m_ucUsed = 0
        self.request.m_ucReserved = ''
        
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('TRGW_ID', imsg.m_uiID)

        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szDesc))

        if imsg.m_nCallRate != -1:    
            print "\t" "%12s = %d" % ('CALL_RATE', imsg.m_nCallRate)
            
        if imsg.m_nMaxCount != -1:    
            print "\t" "%12s = %d" % ('MAX_SES', imsg.m_nMaxCount)            

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:

           print "\t", "%8s %20s %10s %10s" % ('TRGW_ID', 'NAME', 'CALL_RATE', 'STATUS')
           print "\t", " --------------------------------------------------"
        
           for st in sorted(omsg.m_stTrGW) :
               print "\t", "%8d %20s %10d %10s" % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 20, 15),
                                                   st.m_nCallRate,
                                                   self.reprTrgwStsIntToStr(int(st.m_nStatus)))           
                
        elif self.isIdxSearch == 1:
           for st in omsg.m_stTrGW :
               print "\t"
               print "\t" "%12s = %d" % ('TRGW_ID', st.m_uiID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szDesc))
               print "\t" "%12s = %d" % ('CALL_RATE', st.m_nCallRate)
               #print "\t" "%12s = %d" % ('SES_CNT', st.m_nCurCount)
               print "\t" "%12s = %s" % ('STATUS', self.reprTrgwStsIntToStr(int(st.m_nStatus)))

        if omsg.uiSubType == DEF_STYPE_CS_DIS_TRGW_RSP: 
           print ""
           print "%-10s = %s" % ('TRGW_CNT', omsg.m_nNumber)

   
