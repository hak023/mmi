
from mmi.ibcf import *

class MSG_EMS_VNODE_DIS_SLB_REQ(IbcfRequestMsg):

    """
typedef struct VNodeInfo_t
{
    int m_nIdx;
    char m_szVmName[DEF_LM_NAME_LEN=32];
    char m_szLocalIp[E_CONST_MAX_IPADDR_LEN=50];
    char m_szRemoteIp[E_CONST_MAX_IPADDR_LEN=50];
    int m_nLocalPort;
    int m_nRemotePort;
    int m_nFBlock;
    int m_nMBlock;
    int m_nRate;
    int m_nUsingSession;

}VNodeInfo_t;
    
typedef VNodeInfo_t VNode_Dis_Slb_Req_t;

    """    

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_VNODE_DIS_SLB_REQ)
        
    def getFormat(self):
        return FMT_UDP_HEADER + 'i%ds%ds%dsiiiiii' % (DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_szVmName m_szLocalIp m_szRemoteIp m_nLocalPort m_nRemotePort m_nFBlock m_nMBlock m_nRate m_nUsingSession"
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_szVmName, self.m_szLocalIp, self.m_szRemoteIp, self.m_nLocalPort, self.m_nRemotePort, \
                    self.m_nFBlock, self.m_nMBlock, self.m_nRate, self.m_nUsingSession);    
    
class MSG_EMS_VNODE_DIS_SLB_RSP(IbcfResponseMsg):
    
    """
typedef struct VNodeRsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN=128];
    int m_nNumber;
}VNodeRsp_t;

typedef struct VNodeInfo_t
{
    int m_nIdx;
    char m_szVmName[DEF_LM_NAME_LEN=32];
    char m_szLocalIp[E_CONST_MAX_IPADDR_LEN=50];
    char m_szRemoteIp[E_CONST_MAX_IPADDR_LEN=50];
    int m_nLocalPort;
    int m_nRemotePort;
    int m_nFBlock;
    int m_nMBlock;
    int m_nRate;
    int m_nUsingSession;

}VNodeInfo_t;

typedef struct Dis_VNode_Rsp_t
{
    VNodeRsp_t m_stRsp;
    VNodeInfo_t m_arrInfo[E_CONST_MAX_VM_NODE=100];
}Dis_VNode_Rsp_t;

typedef Dis_VNode_Rsp_t VNode_Dis_Slb_Rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_VNODE_DIS_SLB_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%ds%ds%dsiiiiii" % (DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_CONST_MAX_VM_NODE)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_arrInfo"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_VNODE_DIS_SLB_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%ds%ds%dsiiiiii" % (DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_szVmName m_szLocalIp m_szRemoteIp m_nLocalPort m_nRemotePort m_nFBlock m_nMBlock m_nRate m_nUsingSession")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("i%ds%ds%dsiiiiii" %(DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN), response.m_arrInfo[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_arrInfo = new_list)
        
        print response
        return response
    
###############################################################################################################################################

    """
typedef struct VNodeInfo_t
{
    int m_nIdx;
    char m_szVmName[DEF_LM_NAME_LEN=32];
    char m_szLocalIp[E_CONST_MAX_IPADDR_LEN=50];
    char m_szRemoteIp[E_CONST_MAX_IPADDR_LEN=50];
    int m_nLocalPort;
    int m_nRemotePort;
    int m_nFBlock;
    int m_nMBlock;
    int m_nRate;
    int m_nUsingSession;

}VNodeInfo_t;

typedef VNodeInfo_t VNode_Chg_Slb_Req_t;
    """
    
class VNodeInfo_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "i%ds%ds%dsiiiiii" % (DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_szVmName m_szLocalIp m_szRemoteIp m_nLocalPort m_nRemotePort m_nFBlock m_nMBlock m_nRate m_nUsingSession"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_szVmName, self.m_szLocalIp, self.m_szRemoteIp, self.m_nLocalPort, self.m_nRemotePort, \
                    self.m_nFBlock, self.m_nMBlock, self.m_nRate, self.m_nUsingSession);

    """
typedef struct VNodeRsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    int m_nNumber;
}VNodeRsp_t;

typedef struct VNodeInfo_t
{
    int m_nIdx;
    char m_szVmName[DEF_LM_NAME_LEN=32];
    char m_szLocalIp[E_CONST_MAX_IPADDR_LEN=50];
    char m_szRemoteIp[E_CONST_MAX_IPADDR_LEN=50];
    int m_nLocalPort;
    int m_nRemotePort;
    int m_nFBlock;
    int m_nMBlock;
    int m_nRate;
    int m_nUsingSession;

}VNodeInfo_t;

typedef struct Chg_VNode_Rsp_t
{
    VNodeRsp_t m_stRsp;
    VNodeInfo_t m_arrInfo;
}Chg_VNode_Rsp_t;
    
typedef Chg_VNode_Rsp_t VNode_Chg_Slb_Rsp_t;
    """

class VNodeInfo_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("i%ds%ds%dsiiiiii" % (DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_arrInfo"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%ds%ds%dsiiiiii" % (DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_szVmName m_szLocalIp m_szRemoteIp m_nLocalPort m_nRemotePort m_nFBlock m_nMBlock m_nRate m_nUsingSession")
 
        new_list.append(StructInfo._make(unpack("i%ds%ds%dsiiiiii" %(DEF_LM_NAME_LEN, E_CONST_MAX_IPADDR_LEN, E_CONST_MAX_IPADDR_LEN), response.m_arrInfo)))
        response = response._replace(m_arrInfo = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_EMS_VNODE_CHG_SLB_REQ(VNodeInfo_t_REQ):

    def __init__(self):
        VNodeInfo_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_VNODE_CHG_SLB_REQ)

class MSG_EMS_VNODE_CHG_SLB_RSP(VNodeInfo_t_RSP):

    def __init__(self):
        VNodeInfo_t_RSP.__init__(self, DEF_STYPE_VNODE_CHG_SLB_RSP)

###############################################################################################################################################

class VNodeSlbCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)

        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('CM_INDEX', imsg.m_nID)
        if imsg.m_nMBlock != -1:
            print "\t" "%12s = %s" % ('MBLK', self.reprOnOffIntToStr(imsg.m_nMBlock))
        if imsg.m_nRate != -1:
            print "\t" "%12s = %d" % ('RATE', imsg.m_nRate)   

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%8s %20s %30s %9s %30s %9s %7s %7s %7s %7s" % ('CM_INDEX', 'NAME', 'LB_IP', 'LB_PORT', 'CM_IP', 'CM_PORT', 'FBLK', 'MBLK', 'RATE', 'SES')
           print "\t", " ----------------------------------------------------------------------------------------------------------------------------------------------"
                    
           for st in sorted(omsg.m_arrInfo) :
               print "\t", "%8d %20s %30s %9d %30s %9d %7s %7s %7d %7d" % (st.m_nID, self.reprNameShorter(st.m_szVmName, 20, 15), 
                                                                           self.reprName(st.m_szLocalIp), st.m_nLocalPort,
                                                                           self.reprName(st.m_szRemoteIp), st.m_nRemotePort, 
                                                                           self.reprOnOffIntToStr(st.m_nFBlock), 
                                                                           self.reprOnOffIntToStr(st.m_nMBlock),
                                                                           st.m_nRate, st.m_nUsingSession
                                                                          )

        elif self.isIdxSearch == 1:
           for st in omsg.m_arrInfo :
               print "\t"
               print "\t" "%12s = %d" % ('CM_INDEX', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szVmName))
               print "\t" "%12s = %s" % ('LB_IP', self.reprName(st.m_szLocalIp))
               print "\t" "%12s = %d" % ('LB_PORT', st.m_nLocalPort)
               print "\t" "%12s = %s" % ('CM_IP', self.reprName(st.m_szRemoteIp))
               print "\t" "%12s = %d" % ('CM_PORT', st.m_nRemotePort)
               print "\t" "%12s = %s" % ('FBLK', self.reprOnOffIntToStr(st.m_nFBlock))
               print "\t" "%12s = %s" % ('MBLK', self.reprOnOffIntToStr(st.m_nMBlock))
               print "\t" "%12s = %d" % ('RATE', st.m_nRate)
               print "\t" "%12s = %d" % ('SES', st.m_nUsingSession)               
            
        if omsg.uiSubType == DEF_STYPE_VNODE_DIS_SLB_RSP:
           print ""
           print "%-10s = %s" % ('SLB_CNT', omsg.m_nNumber)

   
