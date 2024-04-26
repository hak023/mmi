
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_SCR_OP_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_SCR_OP_REQ)
    
    
class MSG_EMS_CS_DIS_SCR_OP_RSP(IbcfResponseMsg):
    
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
    
typedef struct LmScreenOp_t
{
    int m_nID;
    int m_iScreenActID;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];    

}LmScreenOp_t;
    
typedef struct Cs_dis_scr_op_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    int m_nNumber;

    LmScreenOp_t m_stScrOp[E_MAXNUM=100];

} Cs_dis_scr_op_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_SCR_OP_RSP)
    
    def getFormat(self):
        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("ii%dsI%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * E_MAXNUM)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stScrOp"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_SCR_OP_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))
        
        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("ii%dsI%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_iScreenActID m_szName m_unCnt m_arrRuleSet")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("ii%dsI%ds" %(DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ), response.m_stScrOp[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stScrOp = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_SCR_OP_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_SCR_OP_REQ)

class MSG_EMS_CS_DEL_SCR_OP_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_SCR_OP_RSP)


###############################################################################################################################################
'''
typedef struct LmScreenOp_t
{
    int m_nID;
    int m_iScreenActID;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];    

}LmScreenOp_t;
'''
class LmScreenOp_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        LmRuleSetParam_t_size = calcsize("ii")
        return FMT_UDP_HEADER + "ii%dsI%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size*DEF_LM_PARAM_MAX_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_iScreenActID m_szName m_unCnt m_arrRuleSet"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_iScreenActID, self.m_szName, self.m_unCnt, self.m_arrRuleSet
                    );

    """
typedef struct LmRuleSetParam_t
{
    int m_eCond;   //ERuleCond_t
    int m_nRuleID;

}LmRuleSetParam_t;
    
typedef struct LmScreenOp_t
{
    int m_nID;
    int m_iScreenActID;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];    

}LmScreenOp_t;
    
typedef struct Cs_add_scr_op_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    LmScreenOp_t m_stScrOp;

} Cs_add_scr_op_rsp_t;
    """

class LmScreenOp_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):    
        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("ii%dsI%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stScrOp"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        LmRuleSetParam_t_size = calcsize("ii")
        Struct_size = calcsize("ii%dsI%ds" % (DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_iScreenActID m_szName m_unCnt m_arrRuleSet")
        
        new_list.append(StructInfo._make(unpack("ii%dsI%ds" %(DEF_LM_RULE_STRING_SZ, LmRuleSetParam_t_size * DEF_LM_PARAM_MAX_SZ), response.m_stScrOp)))
        response = response._replace(m_stScrOp = new_list)
 
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_SCR_OP_REQ(LmScreenOp_t_REQ):

    '''
typedef LmScreenOp_t Cs_add_scr_op_req_t;
    '''
    
    def __init__(self):
        LmScreenOp_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_SCR_OP_REQ)


class MSG_EMS_CS_ADD_SCR_OP_RSP(LmScreenOp_t_RSP):

    def __init__(self):
        LmScreenOp_t_RSP.__init__(self, DEF_STYPE_CS_ADD_SCR_OP_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_SCR_OP_REQ(LmScreenOp_t_REQ):
    
    '''
typedef LmScreenOp_t Cs_chg_scr_op_req_t;
    '''
    
    def __init__(self):
        LmScreenOp_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_SCR_OP_REQ)


class MSG_EMS_CS_CHG_SCR_OP_RSP(LmScreenOp_t_RSP):
    
    def __init__(self):
        LmScreenOp_t_RSP.__init__(self, DEF_STYPE_CS_CHG_SCR_OP_RSP)

###############################################################################################################################################

'''
typedef struct LmScreenOp_t
{
    int m_nID;
    int m_iScreenActID;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    
    //LmRuleSet_t m_stRuleSet;
    
    unsigned int m_unCnt;
    LmRuleSetParam_t m_arrRuleSet[DEF_LM_PARAM_MAX_SZ=40];

}LmScreenOp_t;
'''
        
class LmScreenOpCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.rulestr = ''
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('SCR_OP_ID', imsg.m_nID)

        if imsg.m_szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))
            
        if imsg.m_iScreenActID != -1:
            print "\t" "%12s = %s" % ('SCR_ACT_ID', imsg.m_iScreenActID)
            
        if self.rulestr != '':
            print "\t" "%12s = %s" % ('RULESET', self.rulestr)


    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%10s %35s %12s %50s" % ('SCR_OP_ID', 'NAME', 'SCR_ACT_ID', 'RULESET')
           print "\t", " -------------------------------------------------------------------------------------------------------------"
           for st in sorted(omsg.m_stScrOp) : 
               Ruleset = self.reprRulesetHexIntToStr(st.m_arrRuleSet)
               print "\t", "%10d %35s %12d %50s" % \
                            (st.m_nID, self.reprNameShorter(st.m_szName, 35, 30), st.m_iScreenActID, self.reprNameShorter(Ruleset, 50, 45))
        
        elif self.isIdxSearch == 1:
           for st in omsg.m_stScrOp :
               Ruleset = self.reprRulesetHexIntToStr(st.m_arrRuleSet)
               print "\t"
               print "\t" "%12s = %d" % ('SCR_OP_ID', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %d" % ('SCR_ACT_ID', st.m_iScreenActID)
               print "\t" "%12s = %s" % ('RULESET', self.reprName(Ruleset))

        if omsg.uiSubType == DEF_STYPE_CS_DIS_SCR_OP_RSP: 
           print ""
           print "%-10s = %s" % ('SCR_OP_CNT', omsg.m_nNumber)
