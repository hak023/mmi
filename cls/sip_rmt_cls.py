
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_RMT_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_RMT_REQ)
    
    
class MSG_EMS_CS_DIS_RMT_RSP(IbcfResponseMsg):
    
    """
struct SipNodeRemote_t
{
   unsigned int   m_uiID                   ; //0. M, RMT_ID, 1~9999999
   char m_szDesc[DEF_RTE_MAXLEN_DESC]      ; //1. M, NAME,  
   char m_szDomain[DEF_RTE_MAXLEN_DOMAIN]  ; //2. M, DOMAIN, 
   unsigned short m_usIPver                ; //3. M, IPV, IP4/IP6, No Modify
   unsigned short m_usPort                 ; //4. M, PORT, 1 ~ 65535, No Modify
   char m_szIP[DEF_RTE_MAXLEN_IP]          ; //5. M, IP, No Modify
   unsigned char m_ucProto                 ; //6. M, PROTOCOL, UDP/TCP/TLS, No Modify
   unsigned char m_ucReserved              ; //nothing
   
   short         m_sNATOn                  ; //7. M, NAT_ON, 
   int           m_nDSCP                   ; //8. O, DSCP,
   
   ////////the below api set ////////////////
   
   char m_szNATIP[DEF_RTE_MAXLEN_IP]       ; //9.  O, REAL_IP, print
   unsigned short m_usNATPort              ; //10. O, REAL_PORT, 1 ~ 65535, print
   unsigned char  m_ucStatus               ; //11. O, status, see eum EIPNodeStatus_t, print
   unsigned char  m_ucUsed                 ; //O, used flag
   unsigned char  m_ucInterDel             ; //internal delete
   unsigned char  m_ucReserved2[3]         ; //reserved   
   int            m_nIndex                 ; //internal
};

typedef struct Cs_dis_rmt_rsp : public SipRemoteNodeDataBase_t
{
    int m_nNumber;
    SipNodeRemote_t m_stNodeRmt[E_RMT_MAXNUM=300];
    
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_rmt_rsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_RMT_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%dsHH%dsBBhi%dsHBBB%dsi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_RMT_MAXNUM, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stNodeRmt m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_RMT_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%dsHH%dsBBhi%dsHBBB%dsi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szDomain m_usIPver m_usPort m_szIP m_ucProto m_ucReserved m_sNATOn m_nDSCP m_szNATIP m_usNATPort m_ucStatus m_ucUsed m_ucInterDel m_ucReserved2 m_nIndex")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%ds%dsHH%dsBBhi%dsHBBB%dsi" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3), response.m_stNodeRmt[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stNodeRmt = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_RMT_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_RMT_REQ)

class MSG_EMS_CS_DEL_RMT_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_RMT_RSP)


###############################################################################################################################################

class SipNodeRemote_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%ds%dsHH%dsBBhi%dsHBBB%dsi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_szDomain m_usIPver m_usPort m_szIP m_ucProto m_ucReserved m_sNATOn m_nDSCP m_szNATIP m_usNATPort m_ucStatus m_ucUsed m_ucInterDel m_ucReserved2 m_nIndex"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, self.m_szDomain, self.m_usIPver, self.m_usPort, self.m_szIP, self.m_ucProto, \
                    self.m_ucReserved, \
                    self.m_sNATOn, self.m_nDSCP, self.m_szNATIP, self.m_usNATPort, \
                    self.m_ucStatus, self.m_ucUsed, self.m_ucInterDel, self.m_ucReserved2, self.m_nIndex);

    """
typedef struct Cs_add_rmt_rsp 
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    SipNodeRemote_t m_stNodeRmt;

} Cs_add_rmt_rsp_t;
    """

class SipNodeRemote_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%dsHH%dsBBhi%dsHBBB%dsi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stNodeRmt"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%dsHH%dsBBhi%dsHBBB%dsi" % (DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_szDomain m_usIPver m_usPort m_szIP m_ucProto m_ucReserved m_sNATOn m_nDSCP m_szNATIP m_usNATPort m_ucStatus m_ucUsed m_ucInterDel m_ucReserved2 m_nIndex")
 
        new_list.append(StructInfo._make(unpack("I%ds%dsHH%dsBBhi%dsHBBB%dsi" %(DEF_RTE_MAXLEN_DESC, DEF_RTE_MAXLEN_DOMAIN, DEF_RTE_MAXLEN_IP, DEF_RTE_MAXLEN_IP, 3), response.m_stNodeRmt)))
        response = response._replace(m_stNodeRmt = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_RMT_REQ(SipNodeRemote_t_REQ):

    '''
typedef SipNodeRemote_t Cs_add_rmt_req_t;
    '''
    
    def __init__(self):
        SipNodeRemote_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_RMT_REQ)


class MSG_EMS_CS_ADD_RMT_RSP(SipNodeRemote_t_RSP):

    def __init__(self):
        SipNodeRemote_t_RSP.__init__(self, DEF_STYPE_CS_ADD_RMT_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_RMT_REQ(SipNodeRemote_t_REQ):
    
    '''
typedef SipNodeRemote_t Cs_chg_rmt_req_t;
    '''
    
    def __init__(self):
        SipNodeRemote_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_RMT_REQ)

    '''
typedef Cs_add_rmt_rsp_t Cs_chg_rmt_rsp_t;
    '''

class MSG_EMS_CS_CHG_RMT_RSP(SipNodeRemote_t_RSP):
    
    def __init__(self):
        SipNodeRemote_t_RSP.__init__(self, DEF_STYPE_CS_CHG_RMT_RSP)

###############################################################################################################################################

class SipRmtCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved = 0
        self.request.m_ucStatus = 0
        self.request.m_ucUsed = 0
        self.request.m_nIndex = 0
        self.request.m_ucInterDel = 0
        self.request.m_ucReserved2 = ''
        
        self.isIdxSearch = 0
        self.rmtcnt = 0
        self.printRmtCnt = 0
        self.rangeCntStart = 0
        self.rangeCntEnd = 0         

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RMT_ID', imsg.m_uiID)
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
        if imsg.m_sNATOn != -1:
            print "\t" "%12s = %s" % ('NAT_ON', self.reprOnOffIntToStr(imsg.m_sNATOn))
        if imsg.m_nDSCP != -1:
            print "\t" "%12s = %d" % ('DSCP', imsg.m_nDSCP)
        '''
        if imsg.m_szNATIP != '':
            print "\t" "%12s = %s" % ('REAL_IP', self.reprName(imsg.m_szNATIP))
        if imsg.m_usNATPort != 0:
            print "\t" "%12s = %d" % ('REAL_PORT', imsg.m_usNATPort)
        '''    

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%7s %25s %20s %5s %30s %7s %10s %7s %6s %10s" % ('RMT_ID', 'NAME', 'DOAMIN', 'IPV', 'IP', 'PORT', 'PROTOCOL', 'NAT_ON', 'DSCP', 'STATUS')
           print "\t", " ---------------------------------------------------------------------------------------------------------------------------------------"
        
           for st in sorted(omsg.m_stNodeRmt) :
               
               if self.rangeCntStart != 0:
                  if self.rangeCntEnd != 0: 
                     self.rmtcnt = self.rmtcnt + 1
               
               if self.rangeCntStart <= self.rmtcnt:
                  if self.rangeCntEnd >= self.rmtcnt:
                     self.printRmtCnt = self.printRmtCnt + 1              
                     print "\t", "%7d %25s %20s %5s %30s %7d %10s %7s %6d %10s" % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 25, 20), self.reprNameShorter(st.m_szDomain, 20, 15),
                                                                             self.reprIpVerIntToStr(int(st.m_usIPver)), self.reprName(st.m_szIP), st.m_usPort,
                                                                             self.reprProctIntToStr(int(st.m_ucProto)), self.reprOnOffIntToStr(st.m_sNATOn), st.m_nDSCP,
                                                                             self.reprStsIntToStr(int(st.m_ucStatus)))
               
        elif self.isIdxSearch == 1:
           for st in omsg.m_stNodeRmt :
               print "\t"
               print "\t" "%12s = %d" % ('RMT_ID', st.m_uiID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szDesc))
               print "\t" "%12s = %s" % ('IPV', self.reprIpVerIntToStr(int(st.m_usIPver)))
               print "\t" "%12s = %s" % ('IP', self.reprName(st.m_szIP))
               print "\t" "%12s = %d" % ('PORT', st.m_usPort)
               print "\t" "%12s = %s" % ('PROTOCOL', self.reprProctIntToStr(int(st.m_ucProto)))
               print "\t" "%12s = %s" % ('NAT_ON', self.reprOnOffIntToStr(st.m_sNATOn))
               print "\t" "%12s = %d" % ('DSCP', st.m_nDSCP)
               print "\t" "%12s = %s" % ('STATUS', self.reprStsIntToStr(int(st.m_ucStatus)))
                   
        if omsg.uiSubType == DEF_STYPE_CS_DIS_RMT_RSP: 
           print ""
           if self.rangeCntStart != 0:
              if self.rangeCntEnd != 0:
                 print "%-10s = %s" % ('RMT_CNT', self.printRmtCnt)
           else:
              print "%-10s = %s" % ('RMT_CNT', omsg.m_nNumber)    

###############################################################################################################################################

   
