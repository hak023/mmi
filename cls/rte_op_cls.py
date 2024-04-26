
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_RTE_OP_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_RTE_OP_REQ)
    
    
class MSG_EMS_CS_DIS_RTE_OP_RSP(IbcfResponseMsg):
    
    """
    
typedef struct LmRuleSetParam_t
{
    int m_eCond;   //ERuleCond_t
    int m_nRuleID;

}LmRuleSetParam_t;
    
typedef struct LmRuleSet_t
{
    unsigned int m_unCnt;    
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];

}LmRuleSet_t;
    
typedef struct LmRouteOp_t
{
    int m_nID;
    int m_eRoute;   // ERouteOp_t 
    int m_nPriority;
    int m_nSeq;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;    
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];    
    
    int m_nServiceOPS[DEF_LM_PARAM_MAX_SZ=40];
}LmRouteOp_t;
    
typedef struct Cs_dis_rte_op_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    int m_nNumber;
    LmRouteOp_t m_stRteOp[E_MAXNUM=100];

} Cs_dis_rte_op_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_RTE_OP_RSP)
    
    def getFormat(self):
        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("iiii%dsI%ds%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ, DEF_LM_PARAM_MAX_SZ*4))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * E_MAXNUM)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stRteOp"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_RTE_OP_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))
        
        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("iiii%dsI%ds%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ, DEF_LM_PARAM_MAX_SZ*4))
       
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_eRoute m_nPriority m_nSeq m_szName m_unCnt m_arrRuleSet m_nServiceOPS")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("iiii%dsI%ds%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ, DEF_LM_PARAM_MAX_SZ*4), response.m_stRteOp[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stRteOp = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_RTE_OP_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_RTE_OP_REQ)

class MSG_EMS_CS_DEL_RTE_OP_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_RTE_OP_RSP)


###############################################################################################################################################
'''
typedef struct LmRouteOp_t
{
    int m_nID;
    int m_eRoute;   // ERouteOp_t 
    int m_nPriority;
    int m_nSeq;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;    
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];    
    
    int m_nServiceOPS[DEF_LM_PARAM_MAX_SZ=40];
}LmRouteOp_t;
'''
class LmRouteOp_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        LmRuleSetParam_t_size = calcsize("ii")
        return FMT_UDP_HEADER + "iiii%dsI%ds%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ, DEF_LM_PARAM_MAX_SZ*4)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_eRoute m_nPriority m_nSeq m_szName m_unCnt m_arrRuleSet m_nServiceOPS"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_eRoute, self.m_nPriority, self.m_nSeq, self.m_szName, self.m_unCnt, self.m_arrRuleSet, self.m_nServiceOPS
                    );

    """
typedef struct LmRuleSetParam_t
{
    int m_eCond;   //ERuleCond_t
    int m_nRuleID;

}LmRuleSetParam_t;
    
typedef struct LmRouteOp_t
{
    int m_nID;
    int m_eRoute;   // ERouteOp_t 
    int m_nPriority;
    int m_nSeq;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;    
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];    
    
    int m_nServiceOPS[DEF_LM_PARAM_MAX_SZ=40];
}LmRouteOp_t;
    
typedef struct Cs_add_rte_op_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    LmRouteOp_t m_stRteOp;

} Cs_add_rte_op_rsp_t;
    """

class LmRouteOp_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):    
        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("iiii%dsI%ds%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ, DEF_LM_PARAM_MAX_SZ*4))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stRteOp"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("iiii%dsI%ds%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ, DEF_LM_PARAM_MAX_SZ*4))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_eRoute m_nPriority m_nSeq m_szName m_unCnt m_arrRuleSet m_nServiceOPS")
        
        new_list.append(StructInfo._make(unpack("iiii%dsI%ds%ds" %(DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ, DEF_LM_PARAM_MAX_SZ*4), response.m_stRteOp)))
        response = response._replace(m_stRteOp = new_list)
 
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_RTE_OP_REQ(LmRouteOp_t_REQ):

    '''
typedef LmScreenOp_t Cs_add_scr_op_req_t;
    '''
    
    def __init__(self):
        LmRouteOp_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_RTE_OP_REQ)


class MSG_EMS_CS_ADD_RTE_OP_RSP(LmRouteOp_t_RSP):

    def __init__(self):
        LmRouteOp_t_RSP.__init__(self, DEF_STYPE_CS_ADD_RTE_OP_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_RTE_OP_REQ(LmRouteOp_t_REQ):
    
    '''
typedef LmScreenOp_t Cs_chg_scr_op_req_t;
    '''
    
    def __init__(self):
        LmRouteOp_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_RTE_OP_REQ)


class MSG_EMS_CS_CHG_RTE_OP_RSP(LmRouteOp_t_RSP):
    
    def __init__(self):
        LmRouteOp_t_RSP.__init__(self, DEF_STYPE_CS_CHG_RTE_OP_RSP)

###############################################################################################################################################

'''
typedef struct LmRouteOp_t
{
    int m_nID;
    int m_eRoute;   // ERouteOp_t 
    int m_nPriority;
    int m_nSeq;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;    
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];    
    
    int m_nServiceOPS[DEF_LM_PARAM_MAX_SZ=40];
}LmRouteOp_t;
'''
        
class LmRteOpCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.scr_scr_ops = 0
        self.scr_dst_ops = 0
        self.ft_ops = 0
        self.rulestr = ''
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RTE_OP_ID', imsg.m_nID)

        if imsg.m_szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))
         
        if imsg.m_eRoute != 0:
            print "\t" "%12s = %s" % ('ROUTE_TYPE', self.reprRteopTypeIntToStr(imsg.m_eRoute))

        if imsg.m_nPriority != -1:
            print "\t" "%12s = %d" % ('PRIORITY', imsg.m_nPriority)
            
        if imsg.m_nSeq != -1:
            print "\t" "%12s = %d" % ('SEQ', imsg.m_nSeq)

        if self.scr_scr_ops != -1:
            print "\t" "%12s = %d" % ('SRC_SCR_OPS', self.scr_scr_ops)

        if self.scr_dst_ops != -1:
            print "\t" "%12s = %d" % ('SRC_DST_OPS', self.scr_dst_ops)
            
        if self.ft_ops != -1:
            print "\t" "%12s = %d" % ('FT_OPS', self.ft_ops)         
            
        if self.rulestr != '':
            print "\t" "%12s = %s" % ('RULESET', self.rulestr)             

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%10s %25s %10s %10s %10s %12s %12s %12s %50s" % ('RTE_OP_ID', 'NAME', 'RTE_TYPE', 'PRIORITY', 'SEQ', 'SRC_SCR_OPS', 'DST_SCR_OPS', 'FT_OPS', 'RULESET')
           print "\t", " --------------------------------------------------------------------------------------------------------------------------------------------------------------"
           
           for st in sorted(omsg.m_stRteOp) :
               Ruleset = self.reprRulesetHexIntToStr(st.m_arrRuleSet)
               OpsList = self.reprRteOpHexIntToIntAry(st.m_nServiceOPS)

               Scr_scr_ops = 0
               Dst_scr_ops = 0
               Ft_ops = 0

               if len(OpsList):
                  Scr_scr_ops = OpsList[0]
                  Dst_scr_ops = OpsList[1]
                  Ft_ops = OpsList[2]

               print "\t", "%10d %25s %10s %10d %10d %12s %12s %12s %50s" % \
                           (st.m_nID, self.reprNameShorter(st.m_szName, 25, 20), self.reprRteopTypeIntToStr(st.m_eRoute), st.m_nPriority, st.m_nSeq,
                            Scr_scr_ops, Dst_scr_ops, Ft_ops,
                            self.reprNameShorter(Ruleset, 50, 45)
                            )

        elif self.isIdxSearch == 1:
           for st in omsg.m_stRteOp :
               Ruleset = self.reprRulesetHexIntToStr(st.m_arrRuleSet)
               OpsList = self.reprRteOpHexIntToIntAry(st.m_nServiceOPS)

               Scr_scr_ops = 0
               Dst_scr_ops = 0
               Ft_ops = 0

               if len(OpsList):
                  Scr_scr_ops = OpsList[0]
                  Dst_scr_ops = OpsList[1]
                  Ft_ops = OpsList[2]
                  
               print "\t"
               print "\t" "%12s = %d" % ('RTE_OP_ID', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %s" % ('RTE_TYPE', self.reprRteopTypeIntToStr(st.m_eRoute))
               print "\t" "%12s = %d" % ('PRIORITY', st.m_nPriority)
               print "\t" "%12s = %d" % ('SEQ', st.m_nSeq)
               print "\t" "%12s = %s" % ('SRC_SCR_OPS', Scr_scr_ops)
               print "\t" "%12s = %s" % ('DST_SCR_OPS', Dst_scr_ops)
               print "\t" "%12s = %s" % ('FT_OPS', Ft_ops)
               print "\t" "%12s = %s" % ('RULESET', self.reprName(Ruleset))
        
        if omsg.uiSubType == DEF_STYPE_CS_DIS_RTE_OP_RSP: 
           print ""
           print "%-10s = %s" % ('RTE_OP_CNT', omsg.m_nNumber)

   
