
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_SRSQ_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_SRSQ_REQ)
    
    
class MSG_EMS_CS_DIS_SRSQ_RSP(IbcfResponseMsg):
    
    """
    
struct SipSpecialRouteSeq_t
{
   unsigned int   m_uiID                        ; //SSEQ
   char           m_szDesc[DEF_RTE_MAXLEN_DESC] ; //NAME
   unsigned int   m_uiRSEQ[E_MAX_RSEQ=100]      ; //RSEQ, 0 ~ 9999999
   int            m_nRATE[E_MAX_RSEQ=100]       ; //RATE, 0 ~ 99999999 
   unsigned char  m_ucReserved[16]              ; //nothing.
   
   ////////the below api set ////////////////
   
   unsigned char  m_ucUsed                  ; //used flag
   unsigned char  m_ucReserved2[3]          ;
   int            m_nIndex                  ; //internal index
   int            m_nCurRATE[E_MAX_RSEQ=100]; //internal
   int            m_nRNum                   ; //internal
   int            m_nCurPos                 ; //internal
};

typedef struct Cs_dis_rsq_rsp : public SipRouteSeqDataBase_t
{
    int m_nNumber;
    SipSpecialRouteSeq_t m_stSpecialRteSeq[E_SPC_SEQ_MAXNUM=100];
   
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

} Cs_dis_rsq_rsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_SRSQ_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%ds%ds%dsB%dsi%dsii" % (DEF_RTE_MAXLEN_DESC, E_MAX_RSEQ*4, E_MAX_RSEQ*4, 16, 3, E_MAX_RSEQ*4))
        return FMT_UDP_HEADER + "i%dsii%ds" % (Struct_size * E_SPC_SEQ_MAXNUM, DEF_LM_DESC_LEN)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nNumber m_stSpecialRteSeq m_nResult m_nReason m_szReasonDesc"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%ds%ds%dsB%dsi%dsii" % (DEF_RTE_MAXLEN_DESC, E_MAX_RSEQ*4, E_MAX_RSEQ*4, 16, 3, E_MAX_RSEQ*4))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_uiRSEQ m_nRATE m_ucReserved m_ucUsed m_ucReserved2 m_nIndex m_nCurRATE m_nRNum m_nCurPos")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("I%ds%ds%ds%dsB%dsi%dsii" % (DEF_RTE_MAXLEN_DESC, E_MAX_RSEQ*4, E_MAX_RSEQ*4, 16, 3, E_MAX_RSEQ*4), response.m_stSpecialRteSeq[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stSpecialRteSeq = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_EMS_CS_DEL_SRSQ_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DEL_SRSQ_REQ)

class MSG_EMS_CS_DEL_SRSQ_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DEL_SRSQ_RSP)


###############################################################################################################################################

class SipSpcRouteSeq_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "I%ds%ds%ds%dsB%dsi%dsii" % (DEF_RTE_MAXLEN_DESC, E_MAX_RSEQ*4, E_MAX_RSEQ*4, 16, 3, E_MAX_RSEQ*4)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_uiID m_szDesc m_uiRSEQ m_nRATE m_ucReserved m_ucUsed m_ucReserved2 m_nIndex m_nCurRATE m_nRNum m_nCurPos"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_uiID, self.m_szDesc, \
                    self.m_uiRSEQ, self.m_nRATE, \
                    self.m_ucReserved, self.m_ucUsed, self.m_ucReserved2, self.m_nIndex, self.m_nCurRATE, self.m_nRNum, self.m_nCurPos);

    """

typedef struct Cs_dis_srsq_rsp : public SipSpecialRouteSeqDataBase_t
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

   int m_nNumber;
   SipSpecialRouteSeq_t m_stSpecialRteSeq[E_SEQ_MAXNUM];

} Cs_dis_srsq_rsp_t;
    """

class SipSpcRouteSeq_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("I%ds%ds%ds%dsB%dsi%dsii" % (DEF_RTE_MAXLEN_DESC, E_MAX_RSEQ*4, E_MAX_RSEQ*4, 16, 3, E_MAX_RSEQ*4))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stSpecialRteSeq"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("I%ds%ds%ds%dsB%dsi%dsii" % (DEF_RTE_MAXLEN_DESC, E_MAX_RSEQ*4, E_MAX_RSEQ*4, 16, 3, E_MAX_RSEQ*4))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_uiID m_szDesc m_uiRSEQ m_nRATE m_ucReserved m_ucUsed m_ucReserved2 m_nIndex m_nCurRATE m_nRNum m_nCurPos")
 
        new_list.append(StructInfo._make(unpack("I%ds%ds%ds%dsB%dsi%dsii" %(DEF_RTE_MAXLEN_DESC, E_MAX_RSEQ*4, E_MAX_RSEQ*4, 16, 3, E_MAX_RSEQ*4), response.m_stSpecialRteSeq)))
        response = response._replace(m_stSpecialRteSeq = new_list)
        
        print response
        return response
    
###############################################################################################################################################
        
class MSG_EMS_CS_ADD_SRSQ_REQ(SipSpcRouteSeq_t_REQ):

    def __init__(self):
        SipSpcRouteSeq_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_ADD_SRSQ_REQ)


class MSG_EMS_CS_ADD_SRSQ_RSP(SipSpcRouteSeq_t_RSP):

    def __init__(self):
        SipSpcRouteSeq_t_RSP.__init__(self, DEF_STYPE_CS_ADD_SRSQ_RSP)

###############################################################################################################################################

class MSG_EMS_CS_CHG_SRSQ_REQ(SipSpcRouteSeq_t_REQ):
       
    def __init__(self):
        SipSpcRouteSeq_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_SRSQ_REQ)


class MSG_EMS_CS_CHG_SRSQ_RSP(SipSpcRouteSeq_t_RSP):
    
    def __init__(self):
        SipSpcRouteSeq_t_RSP.__init__(self, DEF_STYPE_CS_CHG_SRSQ_RSP)

###############################################################################################################################################

'''
struct SipSpecialRouteSeq_t
{

   unsigned int   m_uiID                        ; //SSEQ
   char           m_szDesc[DEF_RTE_MAXLEN_DESC] ; //NAME
   unsigned int   m_uiRSEQ[E_MAX_RSEQ=100]      ; //RSEQ, 0 ~ 9999999
   int            m_nRATE[E_MAX_RSEQ=100]       ; //RATE, 0 ~ 99999999 
   unsigned char  m_ucReserved[16]              ; //nothing.

   ////////the below api set ////////////////

   unsigned char  m_ucUsed                  ; //used flag
   unsigned char  m_ucReserved2[3]          ;
   int            m_nIndex                  ; //internal index
   int            m_nCurRATE[E_MAX_RSEQ=100]; //internal
   int            m_nRNum                   ; //internal
   int            m_nCurPos                 ; //internal
};
'''
class SipSpcRteSeqCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved = ''
        self.request.m_ucUsed = 0
        self.request.m_ucReserved2 = ''
        self.request.m_nIndex = 0
        self.request.m_nCurRATE = ''
        self.request.m_nRNum = 0
        self.request.m_nCurPos = 0
        
        self.isIdxSearch = 0
        
        self.rseqList = [0 for _ in range(E_MAX_RSEQ)]
        self.rateList = [0 for _ in range(E_MAX_RSEQ)]

    def printMessage(self, imsg, omsg):
        self.printHeader()
        print "[INPUT]"
        print "%-10s = %s" % ('COMMAND', self.getCommandName())
        print ""
        print "%-12s %s" % ('', self.getCommandDesc())
        try:
            self.printInputMessage(imsg)
        except Exception:
            print "     %-5s = %s" % ('ARGS', repr(sys.argv[1:]))

        print ""
        print "[OUTPUT]"
        if(self.exception is None) :
            try:
                if omsg.m_nResult == IBCF_COMMAND_RESULT_SUCCESS :
                   self.printOutputMessage(omsg)
            except Exception:
                pass

            print ""

            if omsg.m_nResult == IBCF_COMMAND_RESULT_SUCCESS :
               if omsg.uiSubType == DEF_STYPE_CS_DIS_SRSQ_RSP:
                  if omsg.m_nNumber != 0:
                     print "%-10s = %s" % ('RESULT', "OK")
                  elif omsg.m_nNumber == 0:
                     if self.isIdxSearch == 1:
                        print "%-10s = %s" % ('RESULT', "NOK")
                        print "%-10s = %s" % ('REASON', "CheckSRouteSeq_NotFoundID");
               else:
                  print "%-10s = %s" % ('RESULT', "OK")

            elif omsg.m_nResult == IBCF_COMMAND_RESULT_FAILURE :
               print "%-10s = %s" % ('RESULT', "NOK")

            if omsg.m_nResult == IBCF_COMMAND_RESULT_FAILURE :
                print "%-10s = %s" % ('REASON', omsg.m_szReasonDesc)

        else :
            print "%-10s = %s" % ('RESULT', 'NOK')
            print "%-10s = %s" % ('REASON', self.exception)
        self.printTail()

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%12s = %d" % ('SSEQ', imsg.m_uiID)
        if imsg.m_szDesc != '':
            print "\t" "%12s = %s" % ('NAME', self.reprName(imsg.m_szDesc))
      
        for i in range(0, E_MAX_RSEQ):
            if self.rseqList[i] > 0:
               print "\t" "%12s = %s" % ('RSEQ' + str(i+1).zfill(2), self.rseqList[i])
            if self.rateList[i] > 0:
               print "\t" "%12s = %s" % ('RATE' + str(i+1).zfill(2), self.rateList[i])

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:

           count_list = {'0': '1-20', '20': '21-40', '40':'41-60', '60':'61-80', '80':'81-100'}
            
           print "\t", "%6s %25s %7s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s" \
                        % ('SSEQ', 'NAME', 'COUNT', '   ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')

           print "\t %s" % ('-'*186)
           
           for st in omsg.m_stSpecialRteSeq :
               
               routeseq_list = self.reprSpcSeqHextoStrInt(st.m_uiRSEQ)
               rate_list = self.reprSpcSeqHextoStrInt(st.m_nRATE)

               print "\t", "%6d %25s %7s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s" \
                           % (st.m_uiID, self.reprNameShorter(st.m_szDesc, 25, 20), count_list['0'], "RSEQ", 
                              routeseq_list[0], routeseq_list[1], routeseq_list[2], routeseq_list[3], routeseq_list[4], routeseq_list[5], 
                              routeseq_list[6], routeseq_list[7], routeseq_list[8], routeseq_list[9], routeseq_list[10], routeseq_list[11],
                              routeseq_list[12], routeseq_list[13], routeseq_list[14], routeseq_list[15], routeseq_list[16], routeseq_list[17],
                              routeseq_list[18], routeseq_list[19]
                              )

               print "\t", "%6s %25s %7s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s" \
                           % (" ", " ", " ", "RRATE", 
                              rate_list[0], rate_list[1], rate_list[2], rate_list[3], rate_list[4], rate_list[5], 
                              rate_list[6], rate_list[7], rate_list[8], rate_list[9], rate_list[10], rate_list[11],
                              rate_list[12], rate_list[13], rate_list[14], rate_list[15], rate_list[16], rate_list[17],
                              rate_list[18], rate_list[19]
                              )

               print "\t %s %s" % (' '*31, '-'*155)
                           
               for i in range(20, E_MAX_RSEQ-1):  
                   if i % 20 == 0:
                      if routeseq_list[i] != '0':
                         print "\t", "%6s %25s %7s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s" \
                              % (" ", " ", count_list[str(i)], "RSEQ",
                              routeseq_list[i], routeseq_list[i+1], routeseq_list[i+2], routeseq_list[i+3], routeseq_list[i+4], routeseq_list[i+5], 
                              routeseq_list[i+6], routeseq_list[i+7], routeseq_list[i+8], routeseq_list[i+9], routeseq_list[i+10], routeseq_list[i+11],
                              routeseq_list[i+12], routeseq_list[i+13], routeseq_list[i+14], routeseq_list[i+15], routeseq_list[i+16], routeseq_list[i+17],
                              routeseq_list[i+18], routeseq_list[i+19]
                              )

                      if routeseq_list[i] != '0':
                         print "\t", "%6s %25s %7s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s" \
                              % (" ", " ", " ", "RRATE",
                              rate_list[i], rate_list[i+1], rate_list[i+2], rate_list[i+3], rate_list[i+4], rate_list[i+5],
                              rate_list[i+6], rate_list[i+7], rate_list[i+8], rate_list[i+9], rate_list[i+10], rate_list[i+11],
                              rate_list[i+12], rate_list[i+13], rate_list[i+14], rate_list[i+15], rate_list[i+16], rate_list[i+17],
                              rate_list[i+18], rate_list[i+19]
                              )
                      else:
                         if rate_list[i] != '0':                           
                            print "\t", "%6s %25s %7s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s" \
                              % (" ", " ", " ", "RRATE",
                              rate_list[i], rate_list[i+1], rate_list[i+2], rate_list[i+3], rate_list[i+4], rate_list[i+5], 
                              rate_list[i+6], rate_list[i+7], rate_list[i+8], rate_list[i+9], rate_list[i+10], rate_list[i+11],
                              rate_list[i+12], rate_list[i+13], rate_list[i+14], rate_list[i+15], rate_list[i+16], rate_list[i+17],
                              rate_list[i+18], rate_list[i+19]
                              )

                   if i % 20 == 10:
                      if i != 20:
                         if routeseq_list[i-9] != '0':
                            print "\t %s %s" % (' '*31, '-'*155)

        elif self.isIdxSearch == 1:
           for st in omsg.m_stSpecialRteSeq :
               
               routeseq_list = self.reprSpcSeqHextoStrInt(st.m_uiRSEQ)
               rate_list = self.reprSpcSeqHextoStrInt(st.m_nRATE)
               
               print "\t"
               print "\t" "%12s = %d" % ('SSEQ', st.m_uiID)
               print "\t" "%12s = %s" % ('NAME', self.reprName(st.m_szDesc))
               
               for i in range(0, E_MAX_RSEQ):
                   if routeseq_list[i] != '0':
                      print "\t" "%12s = %s" % ('RSEQ' + str(i+1).zfill(2), routeseq_list[i])
                   if rate_list[i] != '0':
                      print "\t" "%12s = %s" % ('RATE' + str(i+1).zfill(2), rate_list[i])


        if omsg.uiSubType == DEF_STYPE_CS_DIS_SRSQ_RSP:
           print ""

           if omsg.m_nNumber != 0:
              print "%-10s = %s" % ('SPC_SEQ_CNT', omsg.m_nNumber)

           elif omsg.m_nNumber == 0:
              if self.isIdxSearch == 1:
                 print ""

