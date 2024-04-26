
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_EC_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_EC_REQ)
    
    
class MSG_EMS_CS_DIS_EC_RSP(IbcfResponseMsg):
    
    """
struct EmergencyCall_t
{  
   unsigned int   m_uiID                        ;  //0. M, ID, 1~9999999
   char           m_szDesc[DEF_RTE_MAXLEN_DESC] ;  //1. M, NAME,  
   char           m_szMIN[E_MINMAX_NUMBER=36]   ;  //2. M. MIN
   ////////the below api set ////////////////
   int            m_nIndex         ; //internal index
   unsigned char  m_ucUsed         ; //used flag
   unsigned char  m_ucReserved[3]  ;
};

typedef struct Cs_dis_ec_rsp : public EmergencyCallDataBase_t
{
    int m_nNumber;
    EmergencyCall_t   m_stEC[E_MAXNUM_EC=100];
   
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_ec_rsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_EC_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_MINMAX_NUMBER, 3))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_MAXNUM_EC, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stEC m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_EC_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_MINMAX_NUMBER, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szMIN m_nIndex m_ucUsed m_ucReserved")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%ds%dsiB%ds" %(DEF_RTE_MAXLEN_DESC, E_MINMAX_NUMBER, 3), response.m_stEC[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stEC = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_EC_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_EC_REQ)

class MSG_EMS_CS_DEL_EC_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_EC_RSP)


###############################################################################################################################################

class EmergencyCall_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_MINMAX_NUMBER, 3)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_szMIN m_nIndex m_ucUsed m_ucReserved"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, self.m_szMIN, \
                    self.m_nIndex, self.m_ucUsed, self.m_ucReserved);

    """

typedef struct Cs_add_ec_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    
    EmergencyCall_t m_stEC;

} Cs_add_ec_rsp_t;
    """

class EmergencyCall_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_MINMAX_NUMBER, 3))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stEC"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%dsiB%ds" % (DEF_RTE_MAXLEN_DESC, E_MINMAX_NUMBER, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szMIN m_nIndex m_ucUsed m_ucReserved")
 
        new_list.append(StructInfo._make(unpack("I%ds%dsiB%ds" %(DEF_RTE_MAXLEN_DESC, E_MINMAX_NUMBER, 3), response.m_stEC)))
        response = response._replace(m_stEC = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_EC_REQ(EmergencyCall_t_REQ):

    def __init__(self):
        EmergencyCall_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_EC_REQ)


class MSG_EMS_CS_ADD_EC_RSP(EmergencyCall_t_RSP):

    def __init__(self):
        EmergencyCall_t_RSP.__init__(self, DEF_STYPE_CS_ADD_EC_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_EC_REQ(EmergencyCall_t_REQ):
    
    def __init__(self):
        EmergencyCall_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_EC_REQ)

class MSG_EMS_CS_CHG_EC_RSP(EmergencyCall_t_RSP):
    
    def __init__(self):
        EmergencyCall_t_RSP.__init__(self, DEF_STYPE_CS_CHG_EC_RSP)

###############################################################################################################################################

class EcCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved = ''
        self.request.m_ucUsed = 0
        self.request.m_nIndex = 0
        
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('EC_ID', imsg.m_uiID)
        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szDesc))
        if imsg.m_szMIN != '':
            print "\t" "%12s = %s" % ('MIN', self.reprName(imsg.m_szMIN))

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%7s %20s %30s" % ('EC_ID', 'NAME', 'MIN')
           print "\t", " ----------------------------------------------------------"
        
           for st in omsg.m_stEC :
               print "\t", "%7d %20s %30s" % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 20, 15), self.reprNameShorter(st.m_szMIN, 30, 25))
               
        elif self.isIdxSearch == 1:
           for st in sorted(omsg.m_stEC) :
               print "\t"
               print "\t" "%12s = %d" % ('EC_ID', st.m_uiID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szDesc))
               print "\t" "%12s = %s" % ('MIN', self.reprName(st.m_szMIN))
                   
        if omsg.uiSubType == DEF_STYPE_CS_DIS_EC_RSP:
           print ""
           print "%-10s = %s" % ('EC_CNT', omsg.m_nNumber)

###############################################################################################################################################

   
