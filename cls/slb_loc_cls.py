
from mmi.ibcf import *

class MSG_EMS_SLB_DIS_LN_REQ(IbcfRequestMsg):

    """
typedef struct VNodeLocReq_t
{
    int m_nID;
    char m_szName[E_NAME_SZ=64];
    char m_szIp[E_IP_SZ=64];
    int m_nPort;
    int m_nReserved1;
    int m_nReserved2;
}VNodeLocReq_t;
    
typedef VNodeLocReq_t SlbDisLocReq_t

    """    

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_SLB_DIS_LN_REQ)
        
    def getFormat(self):
        return FMT_UDP_HEADER + 'i%ds%dsiii' % (E_NAME_SZ, E_IP_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_szName m_szIp m_nPort m_nReserved1 m_nReserved2"
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_szName, self.m_szIp, self.m_nPort, self.m_nReserved1, self.m_nReserved2);    
    
class MSG_EMS_SLB_DIS_LN_RSP(IbcfResponseMsg):
    
    """
typedef struct VNodeRsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    int m_nNumber;
}VNodeRsp_t;

typedef struct VNodeLocReq_t
{
    int m_nID;
    char m_szName[E_NAME_SZ=64];
    char m_szIp[E_IP_SZ=64];
    int m_nPort;
    int m_nReserved1;
    int m_nReserved2;
}VNodeLocReq_t;

typedef struct SlbDisLocRsp_t
{
    VNodeRsp_t m_stReason;
    VNodeLocReq_t m_arrLoc[E_DIS_NUMS=100];
}SlbDisLocRsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_SLB_DIS_LN_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%ds%dsiii" % (E_NAME_SZ, E_IP_SZ))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_DIS_NUMS)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_arrLoc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_SLB_DIS_LN_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%ds%dsiii" % (E_NAME_SZ, E_IP_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_szName m_szIp m_nPort m_nReserved1 m_nReserved2")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("i%ds%dsiii" %(E_NAME_SZ, E_IP_SZ), response.m_arrLoc[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_arrLoc = new_list)
        
        print response
        return response
    
###############################################################################################################################################

    """
typedef struct VNodeLocReq_t
{
    int m_nID;
    char m_szName[E_NAME_SZ=64];
    char m_szIp[E_IP_SZ=64];
    int m_nPort;
    int m_nReserved1;
    int m_nReserved2;
}VNodeLocReq_t;

typedef VNodeLocReq_t SlbDelLocReq_t;
   
    """

class MSG_EMS_SLB_DEL_LN_REQ(IbcfRequestMsg):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_SLB_DEL_LN_REQ)
        
    def getFormat(self):
        return FMT_UDP_HEADER + 'i%ds%dsiii' % (E_NAME_SZ, E_IP_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_szName m_szIp m_nPort m_nReserved1, m_nReserved2"
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_szName, self.m_szIp, self.m_nPort, self.m_nReserved1, self.m_nReserved2);

    """

typedef struct VNodeRsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    int m_nNumber;
}VNodeRsp_t;

typedef struct VNodeLocReq_t
{
    int m_nID;
    char m_szName[E_NAME_SZ=64];
    char m_szIp[E_IP_SZ=64];
    int m_nPort;
    int m_nReserved1;
    int m_nReserved2;
}VNodeLocReq_t;

typedef struct VNodeLocRsp_t
{
    VNodeRsp_t m_stRsp;
    VNodeLocReq_t m_stLoc;
}NodeMgrAddLocRsp_t;

typedef VNodeLocRsp_t SlbDelLocRsp_t;
    
    """

class MSG_EMS_SLB_DEL_LN_RSP(IbcfResponseMsg):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_SLB_DEL_LN_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%ds%dsiii" % (E_NAME_SZ, E_IP_SZ))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stLoc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_SLB_DEL_LN_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%ds%dsiii" % (E_NAME_SZ, E_IP_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_szName m_szIp m_nPort m_nReserved1 m_nReserved2")
        new_list.append(StructInfo._make(unpack("i%ds%dsiii" %(E_NAME_SZ, E_IP_SZ), response.m_stLoc)))
        
        response = response._replace(m_stLoc = new_list)
        
        print response
        return response        


###############################################################################################################################################

    """
typedef struct VNodeLocReq_t
{
    int m_nID;
    char m_szName[E_NAME_SZ=64];
    char m_szIp[E_IP_SZ=64];
    int m_nPort;
    int m_nReserved1;
    int m_nReserved2;
}VNodeLocReq_t;

typedef VNodeLocReq_t SlbAddLocReq_t;
    """
    
class VNodeLocReq_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "i%ds%dsiii" % (E_NAME_SZ, E_IP_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_szName m_szIp m_nPort m_nReserved1 m_nReserved2"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_szName, self.m_szIp, self.m_nPort, self.m_nReserved1, self.m_nReserved2);

    """
typedef struct VNodeRsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    int m_nNumber;
}VNodeRsp_t;

typedef struct VNodeLocReq_t
{
    int m_nID;
    char m_szName[E_NAME_SZ=64];
    char m_szIp[E_IP_SZ=64];
    int m_nPort;
    int m_nReserved1;
    int m_nReserved2;
}VNodeLocReq_t;

typedef struct VNodeLocRsp_t
{
    VNodeRsp_t m_stRsp;
    VNodeLocReq_t m_stLoc;
}NodeMgrAddLocRsp_t;
    
typedef VNodeLocRsp_t SlbAddLocRsp_t;
    """

class VNodeLocReq_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("i%ds%dsiii" % (E_NAME_SZ, E_IP_SZ))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stLoc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%ds%dsiii" % (E_NAME_SZ, E_IP_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_szName m_szIp m_nPort m_nReserved1 m_nReserved2")
 
        new_list.append(StructInfo._make(unpack("i%ds%dsiii" %(E_NAME_SZ, E_IP_SZ), response.m_stLoc)))
        response = response._replace(m_stLoc = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_SLB_ADD_LN_REQ(VNodeLocReq_t_REQ):

    def __init__(self):
        VNodeLocReq_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_SLB_ADD_LN_REQ)

class MSG_EMS_SLB_ADD_LN_RSP(VNodeLocReq_t_RSP):

    def __init__(self):
        VNodeLocReq_t_RSP.__init__(self, DEF_STYPE_SLB_ADD_LN_RSP)

###############################################################################################################################################

class SlbLocCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_nReserved1 = 0
        self.request.m_nReserved2 = 0
        
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('LOC_ID', imsg.m_nID)
        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))
        if imsg.m_szIP != '':
            print "\t" "%12s = %s" % ('IP', self.reprName(imsg.m_szIP))
        if imsg.m_usPort != 0:    
            print "\t" "%12s = %d" % ('PORT', imsg.m_nPort)   

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%7s %20s %30s %10s" % ('LOC_ID', 'NAME', 'IP', 'PORT')
           print "\t", " ---------------------------------------------------------------------"
                    
           for st in sorted(omsg.m_arrLoc) :
               print "\t", "%7d %20s %30s %10d" % (st.m_nID, self.reprNameShorter(st.m_szName, 20, 15),
                                                   self.reprName(st.m_szIp), st.m_nPort)
        
        elif self.isIdxSearch == 1:
           for st in omsg.m_arrLoc :
               print "\t"
               print "\t" "%12s = %d" % ('LOC_ID', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %s" % ('IP', self.reprName(st.m_szIP))
               print "\t" "%12s = %d" % ('PORT', st.m_nPort)                
            
        if omsg.uiSubType == DEF_STYPE_CS_DIS_LN_RSP: 
           print ""
           print "%-10s = %s" % ('LOC_CNT', omsg.m_nNumber)

   
