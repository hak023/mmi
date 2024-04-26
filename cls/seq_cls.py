
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_RSQ_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_RSQ_REQ)
    
    
class MSG_EMS_CS_DIS_RSQ_RSP(IbcfResponseMsg):
    
    """
struct SipRouteSeq_t
{

   unsigned int   m_uiID                        ; //RSEQ
   char           m_szDesc[DEF_RTE_MAXLEN_DESC] ; //NAME
   unsigned int   m_uiDRTE                      ; //DRTE, 1 ~ 9999999
   unsigned int   m_uiARTE[E_MAX_ARTE=20]       ; //ARTE, 0 ~ 9999999
   unsigned char  m_ucReserved[16]              ; //nothing.
   ////////the below api set ////////////////
   unsigned char  m_ucUsed                      ; //used flag
   unsigned char  m_ucReserved2[3]              ; 
   int            m_nIndex                      ; //internal index

};

typedef struct Cs_dis_rsq_rsp : public SipRouteSeqDataBase_t
{
    int m_nNumber;
    SipRouteSeq_t m_stRteSeq[E_SEQ_MAXNUM=300];
   
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_rsq_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_RSQ_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%dsIIIIIIIIIIIIIIIIIIIII%dsB%dsi" % (DEF_RTE_MAXLEN_DESC, 16, 3))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_RTE_SEQ_MAXNUM, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stRteSeq m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%dsIIIIIIIIIIIIIIIIIIIII%dsB%dsi" % (DEF_RTE_MAXLEN_DESC, 16, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_uiDRTE m_uiARTE_1 m_uiARTE_2 m_uiARTE_3 m_uiARTE_4 m_uiARTE_5 m_uiARTE_6 m_uiARTE_7 m_uiARTE_8 m_uiARTE_9 m_uiARTE_10 m_uiARTE_11 m_uiARTE_12 m_uiARTE_13 m_uiARTE_14 m_uiARTE_15 m_uiARTE_16 m_uiARTE_17 m_uiARTE_18 m_uiARTE_19 m_uiARTE_20 m_ucReserved m_ucUsed m_ucReserved2 m_nIndex")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%dsIIIIIIIIIIIIIIIIIIIII%dsB%dsi" %(DEF_RTE_MAXLEN_DESC, 16, 3), response.m_stRteSeq[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stRteSeq = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_RSQ_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_RSQ_REQ)

class MSG_EMS_CS_DEL_RSQ_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_RSQ_RSP)


###############################################################################################################################################

class SipRouteSeq_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%dsiiiiiiiiiiiiiiiiiiiii%dsB%dsi" % (DEF_RTE_MAXLEN_DESC, 16, 3)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_uiDRTE m_uiARTE_1 m_uiARTE_2 m_uiARTE_3 m_uiARTE_4 m_uiARTE_5 m_uiARTE_6 m_uiARTE_7 m_uiARTE_8 m_uiARTE_9 m_uiARTE_10 m_uiARTE_11 m_uiARTE_12 m_uiARTE_13 m_uiARTE_14 m_uiARTE_15 m_uiARTE_16 m_uiARTE_17 m_uiARTE_18 m_uiARTE_19 m_uiARTE_20 m_ucReserved m_ucUsed m_ucReserved2 m_nIndex"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, \
                    self.m_uiDRTE, \
                    self.m_uiARTE_1, self.m_uiARTE_2, self.m_uiARTE_3, self.m_uiARTE_4, self.m_uiARTE_5, \
                    self.m_uiARTE_6, self.m_uiARTE_7, self.m_uiARTE_8, self.m_uiARTE_9, self.m_uiARTE_10, \
                    self.m_uiARTE_11, self.m_uiARTE_12, self.m_uiARTE_13, self.m_uiARTE_14, self.m_uiARTE_15, \
                    self.m_uiARTE_16, self.m_uiARTE_17, self.m_uiARTE_18, self.m_uiARTE_19, self.m_uiARTE_20, \
                    self.m_ucReserved, self.m_ucUsed, self.m_ucReserved2, self.m_nIndex);

    """
typedef struct Cs_add_rsp_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];
    SipRouteSeq_t m_stRteSeq;

} Cs_add_rsq_rsp_t;
    """

class SipRouteSeq_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%dsiiiiiiiiiiiiiiiiiiiii%dsB%dsi" % (DEF_RTE_MAXLEN_DESC, 16, 3))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stRteSeq"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%dsiiiiiiiiiiiiiiiiiiiii%dsB%dsi" % (DEF_RTE_MAXLEN_DESC, 16, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_uiDRTE m_uiARTE_1 m_uiARTE_2 m_uiARTE_3 m_uiARTE_4 m_uiARTE_5 m_uiARTE_6 m_uiARTE_7 m_uiARTE_8 m_uiARTE_9 m_uiARTE_10 m_uiARTE_11 m_uiARTE_12 m_uiARTE_13 m_uiARTE_14 m_uiARTE_15 m_uiARTE_16 m_uiARTE_17 m_uiARTE_18 m_uiARTE_19 m_uiARTE_20 m_ucReserved m_ucUsed m_ucReserved2 m_nIndex")
 
        new_list.append(StructInfo._make(unpack("I%dsiiiiiiiiiiiiiiiiiiiii%dsB%dsi" %(DEF_RTE_MAXLEN_DESC, 16, 3), response.m_stRteSeq)))
        response = response._replace(m_stRteSeq = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_RSQ_REQ(SipRouteSeq_t_REQ):

    def __init__(self):
        SipRouteSeq_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_RSQ_REQ)


class MSG_EMS_CS_ADD_RSQ_RSP(SipRouteSeq_t_RSP):

    def __init__(self):
        SipRouteSeq_t_RSP.__init__(self, DEF_STYPE_CS_ADD_RSQ_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_RSQ_REQ(SipRouteSeq_t_REQ):
       
    def __init__(self):
        SipRouteSeq_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_RSQ_REQ)


class MSG_EMS_CS_CHG_RSQ_RSP(SipRouteSeq_t_RSP):
    
    def __init__(self):
        SipRouteSeq_t_RSP.__init__(self, DEF_STYPE_CS_CHG_RSQ_RSP)

###############################################################################################################################################

'''
struct SipRouteSeq_t
{
   unsigned int   m_uiID                        ; //RSEQ
   char           m_szDesc[DEF_RTE_MAXLEN_DESC] ; //NAME
   unsigned int   m_uiDRTE                      ; //DRTE, 1 ~ 9999999
   unsigned int   m_uiARTE[E_MAX_ARTE=20]       ; //ARTE, 0 ~ 9999999
   unsigned char  m_ucReserved[16]              ; //nothing.
   
   ////////the below api set ////////////////
   
   unsigned char  m_ucUsed                 ; //used flag
   unsigned char  m_ucReserved2[3]         ; 
   int            m_nIndex                 ; //internal index
};
'''
class SipRteSeqCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved = ''
        self.request.m_ucUsed = 0
        self.request.m_ucReserved2 = ''
        self.request.m_nIndex = 0
        
        self.isIdxSearch = 0
        self.seqcnt = 0
        self.printSeqCnt = 0
        self.rangeCntStart = 0
        self.rangeCntEnd = 0        

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('RSEQ', imsg.m_uiID)
        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szDesc))
        if imsg.m_uiDRTE != 0:
            print "\t" "%12s = %d" % ('DRTE', imsg.m_uiDRTE)
        if imsg.m_uiARTE_1 != -1:
            print "\t" "%12s = %d" % ('ARTE01', imsg.m_uiARTE_1)
        if imsg.m_uiARTE_2 != -1:
            print "\t" "%12s = %d" % ('ARTE02', imsg.m_uiARTE_2)
        if imsg.m_uiARTE_3 != -1:
            print "\t" "%12s = %d" % ('ARTE03', imsg.m_uiARTE_3)
        if imsg.m_uiARTE_4 != -1:
            print "\t" "%12s = %d" % ('ARTE04', imsg.m_uiARTE_4)
        if imsg.m_uiARTE_5 != -1:
            print "\t" "%12s = %d" % ('ARTE05', imsg.m_uiARTE_5)
        if imsg.m_uiARTE_6 != -1:
            print "\t" "%12s = %d" % ('ARTE06', imsg.m_uiARTE_6)
        if imsg.m_uiARTE_7 != -1:
            print "\t" "%12s = %d" % ('ARTE07', imsg.m_uiARTE_7)
        if imsg.m_uiARTE_8 != -1:
            print "\t" "%12s = %d" % ('ARTE08', imsg.m_uiARTE_8)
        if imsg.m_uiARTE_9 != -1:
            print "\t" "%12s = %d" % ('ARTE09', imsg.m_uiARTE_9) 
        if imsg.m_uiARTE_10 != -1:
            print "\t" "%12s = %d" % ('ARTE10', imsg.m_uiARTE_10)
        if imsg.m_uiARTE_11 != -1:
            print "\t" "%12s = %d" % ('ARTE11', imsg.m_uiARTE_11)
        if imsg.m_uiARTE_12 != -1:
            print "\t" "%12s = %d" % ('ARTE12', imsg.m_uiARTE_12)
        if imsg.m_uiARTE_13 != -1:
            print "\t" "%12s = %d" % ('ARTE13', imsg.m_uiARTE_13)
        if imsg.m_uiARTE_14 != -1:
            print "\t" "%12s = %d" % ('ARTE14', imsg.m_uiARTE_14)                                                
        if imsg.m_uiARTE_15 != -1:
            print "\t" "%12s = %d" % ('ARTE15', imsg.m_uiARTE_15)
        if imsg.m_uiARTE_16 != -1:
            print "\t" "%12s = %d" % ('ARTE16', imsg.m_uiARTE_16)
        if imsg.m_uiARTE_17 != -1:
            print "\t" "%12s = %d" % ('ARTE17', imsg.m_uiARTE_17)
        if imsg.m_uiARTE_18 != -1:
            print "\t" "%12s = %d" % ('ARTE18', imsg.m_uiARTE_18)
        if imsg.m_uiARTE_19 != -1:
            print "\t" "%12s = %d" % ('ARTE19', imsg.m_uiARTE_19)
        if imsg.m_uiARTE_20 != -1:
            print "\t" "%12s = %d" % ('ARTE20', imsg.m_uiARTE_20)  


    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", "%7s %20s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s %7s" % \
                      ('RSEQ', 'NAME', 'DRTE', 'ARTE01', 'ARTE02', 'ARTE03', 'ARTE04', 'ARTE05', 'ARTE06', 'ARTE07', 'ARTE08', 'ARTE09', 'ARTE10', 'ARTE11', 'ARTE12', 'ARTE13', 'ARTE14', 'ARTE15', 'ARTE16', 'ARTE17', 'ARTE18', 'ARTE19', 'ARTE20')
           print "\t", "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
         
           for st in sorted(omsg.m_stRteSeq) :
               
               if self.rangeCntStart != 0:
                  if self.rangeCntEnd != 0:
                     self.seqcnt = self.seqcnt + 1
               
               if self.rangeCntStart <= self.seqcnt:
                  if self.rangeCntEnd >= self.seqcnt:
                     self.printSeqCnt = self.printSeqCnt + 1
                     print "\t", "%7d %20s %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d %7d" \
                                  % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 20, 15), st.m_uiDRTE,
                                     st.m_uiARTE_1, st.m_uiARTE_2, st.m_uiARTE_3, st.m_uiARTE_4, st.m_uiARTE_5,
                                     st.m_uiARTE_6, st.m_uiARTE_7, st.m_uiARTE_8, st.m_uiARTE_9, st.m_uiARTE_10,
                                     st.m_uiARTE_11, st.m_uiARTE_12, st.m_uiARTE_13, st.m_uiARTE_14, st.m_uiARTE_15,
                                     st.m_uiARTE_16, st.m_uiARTE_17, st.m_uiARTE_18, st.m_uiARTE_19, st.m_uiARTE_20)

        elif self.isIdxSearch == 1:
           for st in omsg.m_stRteSeq :
               print "\t"
               print "\t" "%12s = %d" % ('RSEQ', st.m_uiID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szDesc))
               print "\t" "%12s = %d" % ('DRTE', st.m_uiDRTE)
               print "\t" "%12s = %d" % ('ARTE01', st.m_uiARTE_1)
               print "\t" "%12s = %d" % ('ARTE02', st.m_uiARTE_2)
               print "\t" "%12s = %d" % ('ARTE03', st.m_uiARTE_3)
               print "\t" "%12s = %d" % ('ARTE04', st.m_uiARTE_4)
               print "\t" "%12s = %d" % ('ARTE05', st.m_uiARTE_5)
               print "\t" "%12s = %d" % ('ARTE06', st.m_uiARTE_6)
               print "\t" "%12s = %d" % ('ARTE07', st.m_uiARTE_7)
               print "\t" "%12s = %d" % ('ARTE08', st.m_uiARTE_8)
               print "\t" "%12s = %d" % ('ARTE09', st.m_uiARTE_9)
               print "\t" "%12s = %d" % ('ARTE10', st.m_uiARTE_10)
               print "\t" "%12s = %d" % ('ARTE11', st.m_uiARTE_11)
               print "\t" "%12s = %d" % ('ARTE12', st.m_uiARTE_12)
               print "\t" "%12s = %d" % ('ARTE13', st.m_uiARTE_13)
               print "\t" "%12s = %d" % ('ARTE14', st.m_uiARTE_14)
               print "\t" "%12s = %d" % ('ARTE15', st.m_uiARTE_15)
               print "\t" "%12s = %d" % ('ARTE16', st.m_uiARTE_16)
               print "\t" "%12s = %d" % ('ARTE17', st.m_uiARTE_17)
               print "\t" "%12s = %d" % ('ARTE18', st.m_uiARTE_18)
               print "\t" "%12s = %d" % ('ARTE19', st.m_uiARTE_19)
               print "\t" "%12s = %d" % ('ARTE20', st.m_uiARTE_20)

        if omsg.uiSubType == DEF_STYPE_CS_DIS_RSQ_RSP: 
           print ""
           if self.rangeCntStart != 0:
              if self.rangeCntEnd != 0:
                 print "%-10s = %s" % ('SEQ_CNT', self.printSeqCnt)
           else:
              print "%-10s = %s" % ('SEQ_CNT', omsg.m_nNumber)

   
