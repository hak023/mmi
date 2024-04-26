
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_RULE_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_RULE_REQ)
    
    
class MSG_EMS_CS_DIS_RULE_RSP(IbcfResponseMsg):
    
    """
    
typedef struct LmRule_t
{
    int m_nID;
    int m_eAtt;      // ERuleAttribute_t
    int m_ePos;      // EMsgPos_t
    int m_eMatch;    // ERuleMatch_t
    int m_eSave;     // ERuleSave_t
    int m_bExist;
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    char m_szVal1[DEF_LM_RULE_STRING_SZ];
    char m_szVal2[DEF_LM_RULE_STRING_SZ];
    char m_szVal3[DEF_LM_RULE_STRING_SZ];

}LmRule_t;
    
    
typedef struct Cs_dis_rule_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    int m_nNumber;
    LmRule_t m_stRule[E_RULE_MAXNUM=200];

} Cs_dis_rule_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_RULE_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_LM_DESC_LEN, Struct_size * E_RULE_MAXNUM)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stRule"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_RULE_REQ unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_eAtt m_ePos m_eMatch m_eSave m_bExist m_szName m_szVal1 m_szVal2 m_szVal3")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("iiiiii%ds%ds%ds%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.m_stRule[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stRule = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_RULE_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_RULE_REQ)

class MSG_EMS_CS_DEL_RULE_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_RULE_RSP)


###############################################################################################################################################

class LmRule_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiiii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nID m_eAtt m_ePos m_eMatch m_eSave m_bExist m_szName m_szVal1 m_szVal2 m_szVal3"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nID, self.m_eAtt, self.m_ePos, self.m_eMatch, self.m_eSave, self.m_bExist, self.m_szName, \
                    self.m_szVal1, self.m_szVal2, self.m_szVal3
                    );

    """
typedef struct Cs_add_rule_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    LmRule_t m_stRule;

} Cs_add_rule_rsp_t;

    """

class LmRule_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stRule"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiii%ds%ds%ds%ds" % (DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nID m_eAtt m_ePos m_eMatch m_eSave m_bExist m_szName m_szVal1 m_szVal2 m_szVal3")
        
        new_list.append(StructInfo._make(unpack("iiiiii%ds%ds%ds%ds" %(DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ, DEF_LM_RULE_STRING_SZ), response.m_stRule)))
        response = response._replace(m_stRule = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_RULE_REQ(LmRule_t_REQ):

    '''
typedef LmRule_t Cs_add_rule_req_t;
    '''
    
    def __init__(self):
        LmRule_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_RULE_REQ)


class MSG_EMS_CS_ADD_RULE_RSP(LmRule_t_RSP):

    def __init__(self):
        LmRule_t_RSP.__init__(self, DEF_STYPE_CS_ADD_RULE_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_RULE_REQ(LmRule_t_REQ):
    
    '''
typedef LmRule_t Cs_chg_rule_req_t;
    '''
    
    def __init__(self):
        LmRule_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_RULE_REQ)


class MSG_EMS_CS_CHG_RULE_RSP(LmRule_t_RSP):
    
    def __init__(self):
        LmRule_t_RSP.__init__(self, DEF_STYPE_CS_CHG_RULE_RSP)

###############################################################################################################################################

'''
typedef struct LmRule_t
{
    int m_nID;
    int m_eAtt;      // ERuleAttribute_t
    int m_ePos;      // EMsgPos_t
    int m_eMatch;    // ERuleMatch_t
    int m_eSave;     // ERuleSave_t
    int m_bExist;
    
    char m_szName[DEF_LM_RULE_STRING_SZ=128];
    char m_szVal1[DEF_LM_RULE_STRING_SZ];
    char m_szVal2[DEF_LM_RULE_STRING_SZ];
    char m_szVal3[DEF_LM_RULE_STRING_SZ];

}LmRule_t;
'''
        
class LmRuleCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        self.isIdxSearch = 0
        self.flagCrteOrChg = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RULE_ID', imsg.m_nID)

        if imsg.m_szName != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szName))

        if imsg.m_eAtt != 0:
            print "\t" "%12s = %s" % ('ATTRIBUTE', self.reprAttrIntToStr(imsg.m_eAtt))

        if imsg.m_ePos != 0:
            print "\t" "%12s = %s" % ('POS', self.reprPosIntToStr(imsg.m_ePos))

        if imsg.m_eMatch != 0:
            print "\t" "%12s = %s" % ('MATCH', self.reprMatchIntToStr(imsg.m_eMatch))

        if imsg.m_bExist != -1:
            print "\t" "%12s = %s" % ('EXIST', self.reprOnOffIntToStr(imsg.m_bExist))

        #if imsg.m_eSave != 0:
        #    print "\t" "%12s = %s" % ('SAVE', self.reprSaveIntToStr(imsg.m_eSave))

        if self.flagCrteOrChg == 1:
            if imsg.m_szVal1 != '':
               print "\t" "%12s = %s" % ('VALUE_1', self.reprName(imsg.m_szVal1))
      
            if imsg.m_szVal2 != '':
               print "\t" "%12s = %s" % ('VALUE_2', self.reprName(imsg.m_szVal2))
            
            if imsg.m_szVal3 != '':
               print "\t" "%12s = %s" % ('VALUE_3', self.reprName(imsg.m_szVal3))
                           
        elif self.flagCrteOrChg == 2:    
            if imsg.m_szVal1 != '-1':
               print "\t" "%12s = %s" % ('VALUE_1', self.reprName(imsg.m_szVal1))
      
            if imsg.m_szVal2 != '-1':
               print "\t" "%12s = %s" % ('VALUE_2', self.reprName(imsg.m_szVal2))
            
            if imsg.m_szVal3 != '-1':
               print "\t" "%12s = %s" % ('VALUE_3', self.reprName(imsg.m_szVal3))


    def printOutputMessage(self, omsg):
        if (self.isIdxSearch == 0) or (self.isIdxSearch == 2):
           print "\t", "%7s %25s %17s %15s %10s %10s %25s %25s %25s" % ('RULE_ID', 'NAME', 'ATTR', 'POS', 'MATCH', 'EXIST', 'VALUE_1', 'VALUE_2', 'VALUE_3')
           print "\t", " ----------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        
           for st in sorted(omsg.m_stRule) :
               print "\t", "%7d %25s %17s %15s %10s %10s %25s %25s %25s" % \
                           (st.m_nID, self.reprNameShorter(st.m_szName, 25, 20), self.reprAttrIntToStr(st.m_eAtt),
                            self.reprPosIntToStr(st.m_ePos), self.reprMatchIntToStr(st.m_eMatch), self.reprOnOffIntToStr(st.m_bExist),
                            self.reprNameShorter(st.m_szVal1, 25, 20), self.reprNameShorter(st.m_szVal2, 25, 20), self.reprNameShorter(st.m_szVal3, 25, 20))

        elif self.isIdxSearch == 1:
           for st in omsg.m_stRule :
               print "\t"
               print "\t" "%12s = %d" % ('RULE_ID', st.m_nID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szName))
               print "\t" "%12s = %s" % ('ATTR', self.reprAttrIntToStr(st.m_eAtt))
               print "\t" "%12s = %s" % ('POS', self.reprPosIntToStr(st.m_ePos))
               print "\t" "%12s = %s" % ('MATCH', self.reprMatchIntToStr(st.m_eMatch))
               print "\t" "%12s = %s" % ('EXIST', self.reprOnOffIntToStr(st.m_bExist))
               #print "\t" "%12s = %s" % ('SAVE', self.reprSaveIntToStr(st.m_eSave))
               print "\t" "%12s = %s" % ('VALUE_1', self.reprName(st.m_szVal1))
               print "\t" "%12s = %s" % ('VALUE_2', self.reprName(st.m_szVal2))
               print "\t" "%12s = %s" % ('VALUE_3', self.reprName(st.m_szVal3))

        if omsg.uiSubType == DEF_STYPE_CS_DIS_RULE_RSP: 
           print ""
           print "%-10s = %s" % ('RULE_CNT', omsg.m_nNumber)

   
