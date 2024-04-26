
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_FT_ACT_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_FT_ACT_REQ)
    
    
class MSG_EMS_CS_DIS_FT_ACT_RSP(IbcfResponseMsg):
    
    """
typedef struct LmFilterAct_t
{
    int m_nID;
    int m_nResponseCode;
    int m_nReasonCode;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szResponseDesc[DEF_LM_RULE_STRING_SZ];
    char m_szReasonText[DEF_LM_RULE_STRING_SZ];

}LmFilterAct_t;
    
typedef struct Cs_dis_ft_act_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    int m_nNumber;
    
    LmFilterAct_t m_stFtAct[E_MAXNUM=100];

} Cs_dis_ft_act_rsp_t;;

    """
    
    def __init__(self): 
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_FT_ACT_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iii%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * E_MAXNUM)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stFtAct"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> MSG_EMS_CS_DIS_FT_ACT_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))
        
        Struct_size = calcsize("iii%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_nResponseCode m_nReasonCode m_szName m_szResponseDesc m_szReasonText")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("iii%ds%ds%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.m_stFtAct[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stFtAct = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_FT_ACT_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_FT_ACT_REQ)

class MSG_EMS_CS_DEL_FT_ACT_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_FT_ACT_RSP)


###############################################################################################################################################
'''
typedef struct LmFilterAct_t
{
    int m_nID;
    int m_nResponseCode;
    int m_nReasonCode;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szResponseDesc[DEF_LM_RULE_STRING_SZ];
    char m_szReasonText[DEF_LM_RULE_STRING_SZ];

}LmFilterAct_t;
'''
class LmFilterAct_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iii%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_nResponseCode m_nReasonCode m_szName m_szResponseDesc m_szReasonText"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_nResponseCode, self.m_nReasonCode, self.m_szName, self.m_szResponseDesc, self.m_szReasonText
                    );

    """
typedef struct LmFilterAct_t
{
    int m_nID;
    int m_nResponseCode;
    int m_nReasonCode;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szResponseDesc[DEF_LM_RULE_STRING_SZ];
    char m_szReasonText[DEF_LM_RULE_STRING_SZ];

}LmFilterAct_t;
    
typedef struct Cs_add_ft_act_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    
    LmFilterAct_t m_stFtAct;

} Cs_add_ft_act_rsp_t;
    """

class LmFilterAct_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iii%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stFtAct"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iii%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_nResponseCode m_nReasonCode m_szName m_szResponseDesc m_szReasonText")
        
        new_list.append(StructInfo._make(unpack("iii%ds%ds%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.m_stFtAct)))
        response = response._replace(m_stFtAct = new_list)
 
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_FT_ACT_REQ(LmFilterAct_t_REQ):

    '''
typedef LmFilterAct_t Cs_add_ft_act_req_t;
    '''
    
    def __init__(self):
        LmFilterAct_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_FT_ACT_REQ)


class MSG_EMS_CS_ADD_FT_ACT_RSP(LmFilterAct_t_RSP):

    def __init__(self):
        LmFilterAct_t_RSP.__init__(self, DEF_STYPE_CS_ADD_FT_ACT_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_FT_ACT_REQ(LmFilterAct_t_REQ):
    
    '''
typedef LmFilterAct_t Cs_chg_ft_act_req_t;
    '''
    
    def __init__(self):
        LmFilterAct_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_FT_ACT_REQ)


class MSG_EMS_CS_CHG_FT_ACT_RSP(LmFilterAct_t_RSP):
    
    def __init__(self):
        LmFilterAct_t_RSP.__init__(self, DEF_STYPE_CS_CHG_FT_ACT_RSP)

###############################################################################################################################################

'''
typedef struct LmFilterAct_t
{
    int m_nID;
    int m_nResponseCode;
    int m_nReasonCode;
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szResponseDesc[DEF_LM_RULE_STRING_SZ];
    char m_szReasonText[DEF_LM_RULE_STRING_SZ];

}LmFilterAct_t;
'''
        
class LmFilterActCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('FT_ACT_ID', imsg.m_nID)

        if imsg.m_szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))
            
        if imsg.m_nResponseCode != -1:
            print "\t" "%12s = %s" % ('RSP_CODE', imsg.m_nResponseCode)
            
        if imsg.m_nReasonCode != -1:
            print "\t" "%12s = %s" % ('REA_CODE', imsg.m_nReasonCode)
            
        if imsg.m_szResponseDesc != '':
            print "\t" "%12s = %s" % ('RSP_DESC', self.reprName(imsg.m_szResponseDesc))
            
        if imsg.m_szReasonText != '':
            print "\t" "%12s = %s" % ('REA_TEXT', self.reprName(imsg.m_szReasonText))


    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%11s %25s %15s %15s %30s %30s" % ('FT_ACT_ID', 'NAME', 'RSP_CODE', 'REA_CODE', 'RSP_DESC', 'REA_TEXT')
           print "\t", " ----------------------------------------------------------------------------------------------------------------------------------"
           for st in sorted(omsg.m_stFtAct) : 
               print "\t", "%11d %25s %15d %15d %30s %30s" % \
                            (st.m_nID, self.reprNameShorter(st.m_szName, 25, 20), st.m_nResponseCode, st.m_nReasonCode,
                             self.reprNameShorter(st.m_szResponseDesc, 30, 25), self.reprNameShorter(st.m_szReasonText, 30, 25),
                            )
        
        elif self.isIdxSearch == 1:
           for st in omsg.m_stFtAct :
               print "\t"
               print "\t" "%12s = %d" % ('FT_ACT_ID', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %d" % ('RSP_CODE', st.m_nResponseCode)
               print "\t" "%12s = %d" % ('REA_CODE', st.m_nReasonCode)
               print "\t" "%12s = %s" % ('RSP_DESC', self.reprName(st.m_szResponseDesc))             
               print "\t" "%12s = %s" % ('REA_TEXT', self.reprName(st.m_szReasonText))
        
        if omsg.uiSubType == DEF_STYPE_CS_DIS_FT_ACT_RSP:
           print ""
           print "%-10s = %s" % ('FT_ACT_CNT', omsg.m_nNumber)

###############################################################################################################################################

   