
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_SCR_ACT_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_SCR_ACT_REQ)
    
    
class MSG_EMS_CS_DIS_SCR_ACT_RSP(IbcfResponseMsg):
    
    """
typedef struct LmScreenAct_t
{
    int m_nID;
    int m_eAct;      // EScreenAct_t
    int m_ePos;      // EMsgPos_t
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szVal1[DEF_LM_RULE_STRING_SZ];
    char m_szVal2[DEF_LM_RULE_STRING_SZ];
    char m_szVal3[DEF_LM_RULE_STRING_SZ];

}LmScreenAct_t;
    
typedef struct Cs_dis_scr_act_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    int m_nNumber;
    
    LmScreenAct_t m_stScrAct[E_MAXNUM=100];

} Cs_dis_scr_act_rsp_t;

    """
    
    def __init__(self): 
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_SCR_ACT_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * E_MAXNUM)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stScrAct"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_SCR_ACT_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))
        
        Struct_size = calcsize("iii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_eAct m_ePos m_szName m_szVal1 m_szVal2 m_szVal3")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("iii%ds%ds%ds%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.m_stScrAct[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stScrAct = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_SCR_ACT_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_SCR_ACT_REQ)

class MSG_EMS_CS_DEL_SCR_ACT_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_SCR_ACT_RSP)


###############################################################################################################################################
'''
typedef struct LmScreenAct_t
{
    int m_nID;
    int m_eAct;      // EScreenAct_t
    int m_ePos;      // EMsgPos_t
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szVal1[DEF_LM_RULE_STRING_SZ];
    char m_szVal2[DEF_LM_RULE_STRING_SZ];
    char m_szVal3[DEF_LM_RULE_STRING_SZ];

}LmScreenAct_t;
'''
class LmScreenAct_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_eAct m_ePos m_szName m_szVal1 m_szVal2 m_szVal3"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_eAct, self.m_ePos, self.m_szName, self.m_szVal1, self.m_szVal2, self.m_szVal3
                    );

    """
typedef struct LmScreenAct_t
{
    int m_nID;
    int m_eAct;      // EScreenAct_t
    int m_ePos;      // EMsgPos_t
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szVal1[DEF_LM_RULE_STRING_SZ];
    char m_szVal2[DEF_LM_RULE_STRING_SZ];
    char m_szVal3[DEF_LM_RULE_STRING_SZ];

}LmScreenAct_t;
    
typedef struct Cs_add_scr_act_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    
    LmScreenAct_t m_stScrAct;

} Cs_add_scr_act_rsp_t;
    """

class LmScreenAct_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stScrAct"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_eAct m_ePos m_szName m_szVal1 m_szVal2 m_szVal3")
        
        new_list.append(StructInfo._make(unpack("iii%ds%ds%ds%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.m_stScrAct)))
        response = response._replace(m_stScrAct = new_list)
 
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_SCR_ACT_REQ(LmScreenAct_t_REQ):

    '''
typedef LmScreenAct_t Cs_add_scr_act_req_t;
    '''
    
    def __init__(self):
        LmScreenAct_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_SCR_ACT_REQ)


class MSG_EMS_CS_ADD_SCR_ACT_RSP(LmScreenAct_t_RSP):

    def __init__(self):
        LmScreenAct_t_RSP.__init__(self, DEF_STYPE_CS_ADD_SCR_ACT_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_SCR_ACT_REQ(LmScreenAct_t_REQ):
    
    '''
typedef LmScreenAct_t Cs_chg_scr_act_req_t;
    '''
    
    def __init__(self):
        LmScreenAct_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_SCR_ACT_REQ)


class MSG_EMS_CS_CHG_SCR_ACT_RSP(LmScreenAct_t_RSP):
    
    def __init__(self):
        LmScreenAct_t_RSP.__init__(self, DEF_STYPE_CS_CHG_SCR_ACT_RSP)

###############################################################################################################################################

'''
typedef struct LmScreenAct_t
{
    int m_nID;
    int m_eAct;      // EScreenAct_t
    int m_ePos;      // EMsgPos_t
    char m_szName[DEF_LM_RULE_STRING_SZ];
    char m_szVal1[DEF_LM_RULE_STRING_SZ];
    char m_szVal2[DEF_LM_RULE_STRING_SZ];
    char m_szVal3[DEF_LM_RULE_STRING_SZ];

}LmScreenAct_t;
'''
        
class LmScreenActCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.isIdxSearch = 0
        self.flagCrteOrChg = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('SCR_ACT_ID', imsg.m_nID)

        if imsg.m_szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))
            
        if imsg.m_eAct != 0:
            print "\t" "%12s = %s" % ('ACT', self.reprActIntToStr(imsg.m_eAct))
            
        if imsg.m_ePos != 0:
            print "\t" "%12s = %s" % ('POS', self.reprPosIntToStr(imsg.m_ePos))
        
        if self.flagCrteOrChg == 1:    
           if self.reprName(imsg.m_szVal1) != '':
              print "\t" "%12s = %s" % ('VALUE_1', self.reprName(imsg.m_szVal1))
 
           if self.reprName(imsg.m_szVal2) != '':
              print "\t" "%12s = %s" % ('VALUE_2', self.reprName(imsg.m_szVal2))
            
           if self.reprName(imsg.m_szVal2) != '':
              print "\t" "%12s = %s" % ('VALUE_3', self.reprName(imsg.m_szVal3))
              
        elif self.flagCrteOrChg == 2:
           if self.reprName(imsg.m_szVal1) != '-1':
              print "\t" "%12s = %s" % ('VALUE_1', self.reprName(imsg.m_szVal1))
 
           if self.reprName(imsg.m_szVal2) != '-1':
              print "\t" "%12s = %s" % ('VALUE_2', self.reprName(imsg.m_szVal2))
            
           if self.reprName(imsg.m_szVal2) != '-1':
              print "\t" "%12s = %s" % ('VALUE_3', self.reprName(imsg.m_szVal3))                 


    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%11s %25s %20s %13s %30s %30s %30s" % ('SCR_ACT_ID', 'NAME', 'ACT', 'POS', 'VALUE_1', 'VALUE_2', 'VALUE_3')
           print "\t", " --------------------------------------------------------------------------------------------------------------------------------------------------------------------"
           for st in sorted(omsg.m_stScrAct) : 
               print "\t", "%11d %25s %20s %13s %30s %30s %30s" % \
                            (st.m_nID, self.reprNameShorter(st.m_szName, 25, 20), self.reprActIntToStr(st.m_eAct), self.reprPosIntToStr(st.m_ePos),
                             self.reprNameShorter(st.m_szVal1, 30, 25), self.reprNameShorter(st.m_szVal2, 30, 25), self.reprNameShorter(st.m_szVal3, 30, 25)
                            )
        
        elif self.isIdxSearch == 1:
           for st in omsg.m_stScrAct :
               print "\t"
               print "\t" "%12s = %d" % ('SCR_ACT_ID', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %s" % ('ACT', self.reprActIntToStr(st.m_eAct))
               print "\t" "%12s = %s" % ('POS', self.reprPosIntToStr(st.m_ePos))
               print "\t" "%12s = %s" % ('VALUE_1', self.reprName(st.m_szVal1))
               print "\t" "%12s = %s" % ('VALUE_2', self.reprName(st.m_szVal2))
               print "\t" "%12s = %s" % ('VALUE_3', self.reprName(st.m_szVal3))
        
        if omsg.uiSubType == DEF_STYPE_CS_DIS_SCR_ACT_RSP:
           print ""
           print "%-10s = %s" % ('SCR_ACT_CNT', omsg.m_nNumber)

###############################################################################################################################################

   
