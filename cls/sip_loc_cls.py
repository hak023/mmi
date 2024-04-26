
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_LN_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_LN_REQ)
    
    
class MSG_EMS_CS_DIS_LN_RSP(IbcfResponseMsg):
    
    """
struct SipNodeLocal_t
{
   unsigned int   m_uiID                   ; //0. M, LOC_ID, 1~9999999
   char m_szDesc[DEF_RTE_MAXLEN_DESC]      ; //1. M, NAME,  
   char m_szDomain[DEF_RTE_MAXLEN_DOMAIN]  ; //2. M, DOMAIN, 
   unsigned short m_usIPver                ; //3. M, IPV, IP4/IP6, No Modify
   unsigned short m_usPort                 ; //4. M, PORT, 1 ~ 65535, No Modify
   char m_szIP[DEF_RTE_MAXLEN_IP]          ; //5. M, IP, No Modify
   unsigned char m_ucProto                 ; //6. M, PROTOCOL, UDP/TCP/TLS, No Modify
   char m_cRCSOn                           ; //7. M, RCS_ON, 1:ON, 0:OFF
   unsigned char m_ucReserved[14]          ; //8. nothing
   ////////the below api set ////////////////
   unsigned char  m_ucStatus               ; //status, see eum EIPNodeStatus_t, print
   unsigned char  m_ucUsed                 ; //O, used flag
   unsigned short m_usReserved2            ;
   int            m_nIndex                 ; //internal
};

typedef struct Cs_dis_ln_rsp : public SipLocalNodeDataBase_t
{
    int m_nNumber;
    SipNodeLocal_t m_stNodeLocal[E_LOC_MAXNUM=40];

    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    
} Cs_dis_ln_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_LN_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%dsHH%dsBb%dsBBHi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, SVC_RESERVED_SIZE))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_LOC_MAXNUM, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stNodeLocal m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_LN_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%dsHH%dsBb%dsBBHi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, SVC_RESERVED_SIZE))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szDomain m_usIPver m_usPort m_szIP m_ucProto m_cRCSOn m_ucReserved m_ucStatus m_ucUsed m_usReserved2 m_nIndex")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%ds%dsHH%dsBb%dsBBHi" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, SVC_RESERVED_SIZE), response.m_stNodeLocal[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stNodeLocal = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_LN_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_LN_REQ)

class MSG_EMS_CS_DEL_LN_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_LN_RSP)


###############################################################################################################################################

class SipNodeLocal_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%ds%dsHH%dsBb%dsBBHi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, SVC_RESERVED_SIZE)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_szDomain m_usIPver m_usPort m_szIP m_ucProto m_cRCSOn m_ucReserved m_ucStatus m_ucUsed m_usReserved2 m_nIndex"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, self.m_szDomain, self.m_usIPver, self.m_usPort, self.m_szIP, self.m_ucProto, self.m_cRCSOn, \
                    self.m_ucReserved, self.m_ucStatus, self.m_ucUsed, self.m_usReserved2, self.m_nIndex);

    """ 
typedef struct Cs_add_ln_rsp 
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    SipNodeLocal_t m_stNodeLocal;

} Cs_add_ln_rsp_t;
    """

class SipNodeLocal_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%dsHH%dsBb%dsBBHi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, SVC_RESERVED_SIZE))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stNodeLocal"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%dsHH%dsBb%dsBBHi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, SVC_RESERVED_SIZE))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szDomain m_usIPver m_usPort m_szIP m_ucProto m_cRCSOn m_ucReserved m_ucStatus m_ucUsed m_usReserved2 m_nIndex")
 
        new_list.append(StructInfo._make(unpack("I%ds%dsHH%dsBb%dsBBHi" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, SVC_RESERVED_SIZE), response.m_stNodeLocal)))
        response = response._replace(m_stNodeLocal = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_CS_ADD_LN_REQ(SipNodeLocal_t_REQ):

    '''
typedef SipNodeLocal_t Cs_add_ln_req_t;
    '''
    
    def __init__(self):
        SipNodeLocal_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_LN_REQ)

    '''
typedef Cs_add_ln_rsp_t Cs_chg_ln_rsp_t;
    '''

class MSG_EMS_CS_ADD_LN_RSP(SipNodeLocal_t_RSP):

    def __init__(self):
        SipNodeLocal_t_RSP.__init__(self, DEF_STYPE_CS_ADD_LN_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_LN_REQ(SipNodeLocal_t_REQ):
    
    '''
typedef SipNodeLocal_t Cs_chg_ln_req_t;
    '''
    
    def __init__(self):
        SipNodeLocal_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_LN_REQ)

    '''
typedef Cs_add_ln_rsp_t Cs_chg_ln_rsp_t;
    '''

class MSG_EMS_CS_CHG_LN_RSP(SipNodeLocal_t_RSP):
    
    def __init__(self):
        SipNodeLocal_t_RSP.__init__(self, DEF_STYPE_CS_CHG_LN_RSP)

###############################################################################################################################################

class SipLocCommand(IbcfCommand):
    
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
        print "\t" "%12s = %d" % ('LOC_ID', imsg.m_uiID)
        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szDesc))
        if imsg.m_szDomain != '':
            print "\t" "%12s = %s" % ('DOMAIN', self.reprName(imsg.m_szDomain))
        if imsg.m_usIPver != 0:
            print "\t" "%12s = %s" % ('IPV', self.reprIpVerIntToStr(imsg.m_usIPver))
        if imsg.m_szIP != '':
            print "\t" "%12s = %s" % ('IP', self.reprName(imsg.m_szIP))
        if imsg.m_usPort != 0:    
            print "\t" "%12s = %d" % ('PORT', imsg.m_usPort)
        if imsg.m_ucProto != 0:
            print "\t" "%12s = %s" % ('PROTOCOL', self.reprProctIntToStr(int(imsg.m_ucProto)))
        if imsg.m_cRCSOn != -1:
            print "\t" "%12s = %s" % ('RCS_ON', self.reprOnOffIntToStr(imsg.m_cRCSOn))    

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%7s %20s %20s %10s %30s %10s %10s %10s %10s" % ('LOC_ID', 'NAME', 'DOAMIN', 'IPV', 'IP', 'PORT', 'PROTOCOL', 'RCS_ON', 'STATUS')
           print "\t", " --------------------------------------------------------------------------------------------------------------------------------------"
                    
           for st in sorted(omsg.m_stNodeLocal) :

               print "\t", "%7d %20s %20s %10s %30s %10d %10s %10s %10s" % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 20, 15), self.reprNameShorter(st.m_szDomain, 20, 15),
                                                                            self.reprIpVerIntToStr(int(st.m_usIPver)), self.reprName(st.m_szIP), st.m_usPort,
                                                                            self.reprProctIntToStr(int(st.m_ucProto)), self.reprOnOffIntToStr(int(st.m_cRCSOn)),
                                                                            self.reprStsIntToStr(int(st.m_ucStatus)))
        
        elif self.isIdxSearch == 1:
           for st in omsg.m_stNodeLocal :
               print "\t"
               print "\t" "%12s = %d" % ('LOC_ID', st.m_uiID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szDesc))
               print "\t" "%12s = %s" % ('DOMAIN', self.reprName(st.m_szDomain))
               print "\t" "%12s = %s" % ('IPV', self.reprIpVerIntToStr(int(st.m_usIPver)))
               print "\t" "%12s = %s" % ('IP', self.reprName(st.m_szIP))
               print "\t" "%12s = %d" % ('PORT', st.m_usPort)
               print "\t" "%12s = %s" % ('PROTOCOL', self.reprProctIntToStr(int(st.m_ucProto)))
               print "\t" "%12s = %s" % ('RCS_ON', self.reprOnOffIntToStr(int(st.m_cRCSOn)))
               print "\t" "%12s = %s" % ('STATUS', self.reprStsIntToStr(int(st.m_ucStatus)))                
            
        if omsg.uiSubType == DEF_STYPE_CS_DIS_LN_RSP: 
           print ""
           print "%-10s = %s" % ('LOC_CNT', omsg.m_nNumber)

   
