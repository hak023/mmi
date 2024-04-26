
from mmi.ibcf import *

class MSG_EMS_VNODE_DIS_EMP_REQ(IbcfRequestMsg):

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
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_VNODE_DIS_EMP_REQ)
        
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
    
class MSG_EMS_VNODE_DIS_EMP_RSP(IbcfResponseMsg):
    
    """
typedef struct VNodeEmpSubList_t
{
    int m_nVmIdx;
    char m_szVmName[DEF_LM_NAME_LEN];
    int m_nRscIdx;
    char m_szRscName[DEF_LM_NAME_LEN];
    int m_nTrte;
    char m_szRscIP[E_CONST_MAX_EMP_IPADDR_LEN=64];
    int m_nStartPort;
    int m_nMaxSession;
    int m_nBusyCnt;
    int m_nTcBusyCnt;
    int m_nTcMaxSession;

}VNodeEmpSubList_t;

typedef struct VNodeEmpListRsp_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN=128];
    int m_nNumber;
    VNodeEmpSubList_t m_stData[E_CONST_MAX_DIS_ENUM=100];

}VNodeEmpListRsp_t;

typedef VNodeEmpListRsp_t VNode_Dis_Emp_Rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_VNODE_DIS_EMP_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%dsi%dsi%dsiiiii" % (DEF_LM_NAME_LEN, DEF_LM_NAME_LEN, E_CONST_MAX_EMP_IPADDR_LEN))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * E_CONST_MAX_DIS_ENUM)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_VNODE_DIS_EMP_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%dsi%dsi%dsiiiii" % (DEF_LM_NAME_LEN, DEF_LM_NAME_LEN, E_CONST_MAX_EMP_IPADDR_LEN))
        new_list = []
              
        StructInfo = namedtuple("StructInfo", "m_nVmIdx m_szVmName m_nRscIdx m_szRscName m_nTrte m_szRscIP m_nStartPort m_nMaxSession m_nBusyCnt m_nTcBusyCnt m_nTcMaxSession")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("i%dsi%dsi%dsiiiii" %(DEF_LM_NAME_LEN, DEF_LM_NAME_LEN, E_CONST_MAX_EMP_IPADDR_LEN), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################

class VNodeEmpCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)

        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('EMP_ID', imsg.m_nID)

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%7s %20s %7s %20s %7s %30s %7s %9s %9s %11s %11s" % ('VM_ID', 'NAME', 'RSC_ID', 'RSC_NAME', 'TRTE', 'RSC_IP', 'PORT', 'BUSY_CNT', 'MAX_CNT', 'TC_BUSY_CNT', 'TC_MAX_CNT')
           print "\t", " -------------------------------------------------------------------------------------------------------------------------------------------------"

           for st in sorted(omsg.m_stData) :
               print "\t", "%7d %20s %7d %20s %7d %30s %7d %9s %9d %11d %11d" % (st.m_nVmIdx, self.reprNameShorter(st.m_szVmName, 20, 15), st.m_nRscIdx, 
                                                                                 self.reprName(st.m_szRscName), st.m_nTrte, self.reprName(st.m_szRscIP),
                                                                                 st.m_nStartPort, st.m_nBusyCnt, st.m_nMaxSession,
                                                                                 st.m_nTcBusyCnt, st.m_nTcMaxSession)

        elif self.isIdxSearch == 1:
           for st in omsg.m_stData :
               print "\t"
               print "\t" "%12s = %d" % ('VM_ID', st.m_nVmIdx)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szVmName))
               print "\t" "%12s = %s" % ('RSC_ID', st.m_nRscIdx)
               print "\t" "%12s = %s" % ('RSC_NAME', self.reprName(st.m_szRscName))
               print "\t" "%12s = %d" % ('TRTE', st.m_nTrte)
               print "\t" "%12s = %s" % ('RSC_IP', self.reprName(st.m_szRscIP))
               print "\t" "%12s = %d" % ('PORT', st.m_nStartPort)
               print "\t" "%12s = %s" % ('BUSY_CNT', st.m_nBusyCnt)
               print "\t" "%12s = %d" % ('MAX_CNT', st.m_nMaxSession)
               print "\t" "%12s = %s" % ('TC_BUSY_CNT', st.m_nTcBusyCnt)
               print "\t" "%12s = %d" % ('TC_MAX_CNT', st.m_nTcMaxSession)            
            
        if omsg.uiSubType == DEF_STYPE_VNODE_DIS_EMP_RSP:
           print ""
           print "%-10s = %s" % ('EMP_CNT', omsg.m_nNumber)

   
