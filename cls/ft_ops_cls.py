
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_FT_OPS_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_FT_OPS_REQ)
    
    
class MSG_EMS_CS_DIS_FT_OPS_RSP(IbcfResponseMsg):
    
    """
typedef struct LmServiceOPList_t
{
    unsigned int m_unCnt;
    int m_arrServiceOp[DEF_LM_PARAM_MAX_SZ];

}LmServiceOPList_t;

typedef struct LmFilterOpSet_t
{    
    int m_nID;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    
    //LmServiceOPList_t m_stOPList;
    
    unsigned int m_unCnt;
    int m_arrServiceOp[DEF_LM_PARAM_MAX_SZ];        

}LmFilterOpSet_t;

typedef struct Cs_dis_ft_ops_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    int m_nNumber;
    
    LmFilterOpSet_t m_stFtOps[E_MAXNUM=100];

} Cs_dis_ft_ops_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_FT_OPS_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("i%dsI%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_PARAM_MAX_SZ * 4))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * E_MAXNUM)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stFtOps"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_FT_OPS_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))
        
        Struct_size = calcsize("i%dsI%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_PARAM_MAX_SZ * 4))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_szName m_unCnt m_arrServiceOp")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("i%dsI%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_PARAM_MAX_SZ * 4), response.m_stFtOps[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stFtOps = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_FT_OPS_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_FT_OPS_REQ)

class MSG_EMS_CS_DEL_FT_OPS_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_FT_OPS_RSP)


###############################################################################################################################################
'''
typedef struct LmFilterOpSet_t
{    
    int m_nID;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    
    //LmServiceOPList_t m_stOPList;
    
    unsigned int m_unCnt;
    int m_arrServiceOp[DEF_LM_PARAM_MAX_SZ];        

}LmFilterOpSet_t;
'''
class LmFilterOpSet_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "i%dsI%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_PARAM_MAX_SZ*4)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_szName m_unCnt m_arrServiceOp"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_szName, self.m_unCnt, self.m_arrServiceOp
                    );

    """
typedef struct LmFilterOpSet_t
{    
    int m_nID;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    
    //LmServiceOPList_t m_stOPList;
    
    unsigned int m_unCnt;
    int m_arrServiceOp[DEF_LM_PARAM_MAX_SZ];        

}LmFilterOpSet_t;

typedef struct Cs_add_ft_ops_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    
    LmFilterOpSet_t m_stFtOps;

} Cs_add_ft_ops_rsp_t;
    """

class LmFilterOpSet_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):    
        Struct_size = calcsize("i%dsI%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_PARAM_MAX_SZ * 4))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stFtOps"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("i%dsI%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_PARAM_MAX_SZ * 4))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_szName m_unCnt m_arrServiceOp")
        
        new_list.append(StructInfo._make(unpack("i%dsI%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_PARAM_MAX_SZ * 4), response.m_stFtOps)))
        response = response._replace(m_stFtOps = new_list)
 
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_FT_OPS_REQ(LmFilterOpSet_t_REQ):

    '''
typedef LmFilterOpSet_t Cs_add_ft_ops_req_t;
    '''
    
    def __init__(self):
        LmFilterOpSet_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_FT_OPS_REQ)


class MSG_EMS_CS_ADD_FT_OPS_RSP(LmFilterOpSet_t_RSP):

    def __init__(self):
        LmFilterOpSet_t_RSP.__init__(self, DEF_STYPE_CS_ADD_FT_OPS_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_FT_OPS_REQ(LmFilterOpSet_t_REQ):
    
    '''
typedef LmFilterOpSet_t Cs_chg_ft_ops_req_t;
    '''
    
    def __init__(self):
        LmFilterOpSet_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_FT_OPS_REQ)


class MSG_EMS_CS_CHG_FT_OPS_RSP(LmFilterOpSet_t_RSP):
    
    def __init__(self):
        LmFilterOpSet_t_RSP.__init__(self, DEF_STYPE_CS_CHG_FT_OPS_RSP)

###############################################################################################################################################

'''
typedef struct LmFilterOpSet_t
{    
    int m_nID;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    
    //LmServiceOPList_t m_stOPList;
    
    unsigned int m_unCnt;
    int m_arrServiceOp[DEF_LM_PARAM_MAX_SZ];        

}LmFilterOpSet_
'''
        
class LmFilterOpSetCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.isIdxSearch = 0
        self.opstr = ''

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%14s = %d" % ('FT_OPS_ID', imsg.m_nID)

        if imsg.m_szName != '':
            print "\t" "%14s = %s" % ('NAME', self.reprName(imsg.m_szName))
            
        if self.opstr != '':
            print "\t" "%14s = %s" % ('FT_OP_ID_LIST', self.opstr)
            

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%10s %25s %95s" % ('FT_OPS_ID', 'NAME', 'FT_OP_ID_LIST')
           print "\t", " -----------------------------------------------------------------------------------------------------------------------------------"
           for st in sorted(omsg.m_stFtOps) : 
               SvcOpSet = self.reprScrOpsHexIntToIntAry(st.m_arrServiceOp)
               print "\t", "%10d %25s %95s" % \
                            (st.m_nID, self.reprNameShorter(st.m_szName, 25, 20), self.reprNameShorter(SvcOpSet, 95, 90))
        
        elif self.isIdxSearch == 1:
           for st in omsg.m_stFtOps :
               SvcOpSet = self.reprScrOpsHexIntToIntAry(st.m_arrServiceOp)
               print "\t"
               print "\t" "%12s = %d" % ('FT_OPS_ID', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %s" % ('FT_OP_ID_LIST', self.reprName(SvcOpSet))
        
        if omsg.uiSubType == DEF_STYPE_CS_DIS_FT_OPS_RSP: 
           print ""
           print "%-10s = %s" % ('FT_OPS_CNT', omsg.m_nNumber)

