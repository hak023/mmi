
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_IGW_DIS_RTE_REQ(IbcfRequestMsg):
       
    """
typedef struct Cs_enum_dis_rte_req_t
{
   int m_nId;

}Cs_enum_dis_rte_req_t;
    """
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_IGW_RTE_REQ)
        
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
    
class MSG_EMS_IGW_DIS_RTE_RSP(IbcfResponseMsg):
    
    """ 
typedef struct EnumRoute_t
{
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN=32];
    int m_nArte;
    int m_nLocId;
    int m_nRmtId;
    int m_nRate;    // round-robin ratio
    int m_nMBlk;    // 0 avail, 1 = manual Block
    int m_nStatus;  // 0 avail, 1 = fault
}EnumRoute_t;
    
typedef struct Cs_enum_dis_rte_rsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

    int m_nCnt;
    EnumRoute_t m_arrrte[DEF_LM_NODE_LEN];
}Cs_enum_dis_rte_rsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_IGW_RTE_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%dsiiiiii" % (DEF_LM_NAME_LEN))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * DEF_LM_NODE_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nCnt m_arrrte"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_IGW_RTE_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%dsiiiiii" % (DEF_LM_NAME_LEN))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nId m_szName m_nArte m_nLocId m_nRmtId m_nRate m_nMBlk m_nStatus")
        for i in range(response.m_nCnt) :
            new_list.append(StructInfo._make(unpack("i%dsiiiiii" %(DEF_LM_NAME_LEN), response.m_arrrte[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_arrrte = new_list)
        
        print response
        return response

###############################################################################################################################################
  
'''
typedef struct Cs_enum_del_rte_rsp_t
{
    int m_nId;
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
}Cs_enum_del_rte_rsp_t;
'''

class MSG_EMS_IGW_DEL_RTE_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_IGW_RTE_REQ)

class MSG_EMS_IGW_DEL_RTE_RSP(IbcfResponseMsg):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_IGW_RTE_RSP)
    
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

class MSG_EMS_IGW_CON_RTE_REQ(IbcfRequestMsg):
    
    '''
typedef struct Cs_enum_con_req_t
{           
    int m_nId; // Rte_ID
    int m_eT;  // E_NONE = 0, E_CONNECT=1, E_DISCONNECT=2

}Cs_enum_con_req_t;

    '''
    
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CON_IGW_RTE_REQ)

    def getFormat(self):
        return FMT_UDP_HEADER + 'ii'
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nId m_eT"
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nId, self.m_eT)


class MSG_EMS_IGW_CON_RTE_RSP(IbcfResponseMsg):

    """
typedef struct Cs_enum_con_rsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN=128];
           
}Cs_enum_con_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_CON_IGW_RTE_RSP)
    
    def getFormat(self):
        return FMT_UDP_HEADER + "ii%ds" % (DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc"

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
typedef struct EnumRoute_t
{
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN = 32];
    int m_nArte;
    int m_nLocId;
    int m_nRmtId;
    int m_nRate;    // round-robin ratio
    int m_nMBlk;    // 0 avail, 1 = manual Block
    int m_nStatus;  // 0 avail, 1 = fault
}EnumRoute_t;

    """

class IgwRoute_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "i%dsiiiiii" % (DEF_LM_NAME_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nId m_szName m_nArte m_nLocId m_nRmtId m_nRate m_nMBlk m_nStatus"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nId, self.m_szName, self.m_nArte, self.m_nLocId, self.m_nRmtId, self.m_nRate, self.m_nMBlk, self.m_nStatus);

    """
typedef struct Cs_enum_crte_rte_rsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    EnumRoute_t m_arrrte;
}Cs_enum_crte_rte_rsp_t;

    """

class IgwRoute_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("i%dsiiiiii" % (DEF_LM_NAME_LEN))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_arrrte"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%dsiiiiii" % (DEF_LM_NAME_LEN))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nId m_szName m_nArte m_nLocId m_nRmtId m_nRate m_nMBlk m_nStatus")
 
        new_list.append(StructInfo._make(unpack("i%dsiiiiii" %(DEF_LM_NAME_LEN), response.m_arrrte)))
        response = response._replace(m_arrrte = new_list)
        
        print response
        return response

###############################################################################################################################################
        
class MSG_EMS_IGW_ADD_RTE_REQ(IgwRoute_t_REQ):

    def __init__(self):
        IgwRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CRTE_IGW_RTE_REQ)


class MSG_EMS_IGW_ADD_RTE_RSP(IgwRoute_t_RSP):

    def __init__(self):
        IgwRoute_t_RSP.__init__(self, DEF_STYPE_CS_CRTE_IGW_RTE_RSP)


class MSG_EMS_IGW_CHG_RTE_REQ(IgwRoute_t_REQ):
    
    def __init__(self):
        IgwRoute_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_IGW_RTE_REQ)

class MSG_EMS_IGW_CHG_RTE_RSP(IgwRoute_t_RSP):
    
    def __init__(self):
        IgwRoute_t_RSP.__init__(self, DEF_STYPE_CS_CHG_IGW_RTE_RSP)
        
###############################################################################################################################################
        
class IgwRteCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)

        self.request.m_ucReserved = ''
        self.request.m_ucStatus = 0
        self.request.m_ucUsed = 0
        self.request.m_usReserved2 = 0
        self.request.m_nIndex = 0
        
        self.isIdxSearch = 0

    '''
typedef struct EnumRoute_t
{
    int m_nId;
    char m_szName[DEF_LM_NAME_LEN = 32];
    int m_nArte;
    int m_nLocId;
    int m_nRmtId;
    int m_nRate;    // round-robin ratio
    int m_nMBlk;    // 0 avail, 1 = manual Block
    int m_nStatus;  // 0 avail, 1 = fault
}EnumRoute_t;
    '''

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RTE_ID', imsg.m_nId)
        if imsg.m_szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))
        if imsg.m_nArte != -1:
            print "\t" "%12s = %d" % ('ARTE', imsg.m_nArte)
        if imsg.m_nLocId != -1:    
            print "\t" "%12s = %d" % ('LOC_ID', imsg.m_nLocId)
        if imsg.m_nRmtId != -1:    
            print "\t" "%12s = %d" % ('RMT_ID', imsg.m_nRmtId)
        if imsg.m_nRate != -1:    
            print "\t" "%12s = %d" % ('RATE', imsg.m_nRate)
        if imsg.m_nMBlk != -1:    
            print "\t" "%12s = %s" % ('BLOCK', self.reprIgwNpdbBlkIntToStr(imsg.m_nMBlk))     

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
            print "\t", "%7s %20s %7s %7s %7s %7s %7s %7s" % ('RTE_ID', 'NAME', 'ARTE', 'LOC_ID', 'RMT_ID', 'RATE', 'BLOCK', 'STATUS')
            print "\t", " ---------------------------------------------------------------------------"

            for st in omsg.m_arrrte :
                print "\t", "%7d %20s %7d %7d %7d %7d %7s %7s" % (st.m_nId, self.reprNameShorter(st.m_szName, 20, 15), 
                                                                  st.m_nArte, st.m_nLocId, st.m_nRmtId, st.m_nRate,
                                                                  self.reprIgwNpdbBlkIntToStr(st.m_nMBlk),
                                                                  self.reprIgwNpdbStsIntToStr(st.m_nStatus)
                                                                 )

        elif self.isIdxSearch == 1:
            for st in omsg.m_arrrte :
               print "\t"
               print "\t" "%12s = %d" % ('RTE_ID', st.m_nId)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %d" % ('ARTE', st.m_nArte)
               print "\t" "%12s = %d" % ('LOC_ID', st.m_nLocId)
               print "\t" "%12s = %d" % ('RMT_ID', st.m_nRmtId)
               print "\t" "%12s = %d" % ('RATE', st.m_nRate)
               print "\t" "%12s = %s" % ('BLOCK', self.reprIgwNpdbBlkIntToStr(st.m_nMBlk))
               print "\t" "%12s = %s" % ('STATUS', self.reprIgwNpdbStsIntToStr(st.m_nStatus))
            
        if omsg.uiSubType == DEF_STYPE_CS_DIS_IGW_RTE_RSP: 
           print ""
           print "%-10s = %s" % ('RTE_CNT', omsg.m_nCnt)
