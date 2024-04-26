
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_NPDB_DIS_RMT_REQ(MSG_EMS_DEFAULT_DIS_REQ):
       
    """
typedef struct Cs_enum_dis_rmt_req_t
{
    int m_nId;

}Cs_enum_dis_rmt_req_t;
    """
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_NPDB_RMT_REQ)

    def getFormat(self):
        return FMT_UDP_HEADER + 'i'
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nId"
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nId);
    
class MSG_EMS_NPDB_DIS_RMT_RSP(IbcfResponseMsg):
    
    """ 
typedef struct EnumRemote_t
{
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN];
    char m_szIP[DEF_LM_IP_LEN];
    int m_nPort;
}EnumRemote_t;
    
typedef struct Cs_enum_dis_rmt_rsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN = 128];

    int m_nCnt;
    EnumRemote_t m_stRmt[DEF_LM_NODE_LEN = 20];
}Cs_enum_dis_rmt_rsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_NPDB_RMT_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%ds%dsi" % (DEF_LM_NAME_LEN, DEF_LM_IP_LEN))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * DEF_LM_NODE_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nCnt m_stRmt"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_NPDB_RMT_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%ds%dsi" % (DEF_LM_NAME_LEN, DEF_LM_IP_LEN))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nId m_szName m_szIP m_nPort")
        for i in range(response.m_nCnt) :
            new_list.append(StructInfo._make(unpack("i%ds%dsi" %(DEF_LM_NAME_LEN, DEF_LM_IP_LEN), response.m_stRmt[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stRmt = new_list)
        
        print response
        return response

###############################################################################################################################################
  
'''
typedef struct Cs_enum_del_rmt_rsp_t
{
    int m_nId;
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
}Cs_enum_del_Rmt_rsp_t;
'''

class MSG_EMS_NPDB_DEL_RMT_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_NPDB_RMT_REQ)

class MSG_EMS_NPDB_DEL_RMT_RSP(IbcfResponseMsg):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_NPDB_RMT_RSP)
    
    def getFormat(self):
        return FMT_UDP_HEADER + "iii%ds" % (DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nId m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())
    
    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))     
        
        print response
        return response

###############################################################################################################################################

    """
typedef struct EnumRemote_t
{
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN];
    char m_szIP[DEF_LM_IP_LEN];
    int m_nPort;
}EnumRemote_t;

typedef struct Cs_enum_crte_rmt_req_t
{
    EnumRemote_t m_stRmt;
}Cs_enum_crte_rmt_req_t;

    """

class NpdbRemote_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "i%ds%dsi" % (DEF_LM_NAME_LEN, DEF_LM_IP_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nId m_szName m_szIP m_nPort"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nId, self.m_szName, self.m_szIP, self.m_nPort);

    """
    
typedef struct EnumRemote_t
{
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN];
    char m_szIP[DEF_LM_IP_LEN];
    int m_nPort;
}EnumRemote_t;

typedef struct Cs_enum_crte_rmt_rsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

    EnumRemote_t m_stRmt;
}Cs_enum_crte_Rmt_rsp_t;

    """

class NpdbRemote_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("i%ds%dsi" % (DEF_LM_NAME_LEN, DEF_LM_IP_LEN))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stRmt"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%ds%dsi" % (DEF_LM_NAME_LEN, DEF_LM_IP_LEN))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nId m_szName m_szIP m_nPort")
 
        new_list.append(StructInfo._make(unpack("i%ds%dsi" %(DEF_LM_NAME_LEN, DEF_LM_IP_LEN), response.m_stRmt)))
        response = response._replace(m_stRmt = new_list)
        
        print response
        return response

###############################################################################################################################################
        
class MSG_EMS_NPDB_ADD_RMT_REQ(NpdbRemote_t_REQ):

    def __init__(self):
        NpdbRemote_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CRTE_NPDB_RMT_REQ)


class MSG_EMS_NPDB_ADD_RMT_RSP(NpdbRemote_t_RSP):

    def __init__(self):
        NpdbRemote_t_RSP.__init__(self, DEF_STYPE_CS_CRTE_NPDB_RMT_RSP)


class MSG_EMS_NPDB_CHG_RMT_REQ(NpdbRemote_t_REQ):
    
    def __init__(self):
        NpdbRemote_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_NPDB_RMT_REQ)

class MSG_EMS_NPDB_CHG_RMT_RSP(NpdbRemote_t_RSP):
    
    def __init__(self):
        NpdbRemote_t_RSP.__init__(self, DEF_STYPE_CS_CHG_NPDB_RMT_RSP)
        
###############################################################################################################################################
        
class NpdbRmtCommand(IbcfCommand):
    
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
        print "\t" "%12s = %d" % ('RMT_ID', imsg.m_nId)
        if imsg.m_szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))
        if imsg.m_szIP != '':
            print "\t" "%12s = %s" % ('IP', self.reprName(imsg.m_szIP))
        if imsg.m_nPort != -1:    
            print "\t" "%12s = %d" % ('PORT', imsg.m_nPort)


    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
            print "\t", "%7s %20s %30s %7s" % ('RMT_ID', 'NAME', 'IP', 'PORT')
            print "\t", " ------------------------------------------------------------------"

            for st in omsg.m_stRmt :
                print "\t", "%7d %20s %30s %7d" % (st.m_nId, self.reprNameShorter(st.m_szName, 20, 15), self.reprName(st.m_szIP), st.m_nPort)

        elif self.isIdxSearch == 1:
            for st in omsg.m_stRmt :
               print "\t"
               print "\t" "%12s = %d" % ('RMT_ID', st.m_nId)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %s" % ('IP', self.reprName(st.m_szIP))
               print "\t" "%12s = %d" % ('PORT', st.m_nPort)
            
        if omsg.uiSubType == DEF_STYPE_CS_DIS_NPDB_RMT_RSP: 
           print ""
           print "%-10s = %s" % ('RMT_CNT', omsg.m_nCnt)
