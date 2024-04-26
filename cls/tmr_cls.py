
from mmi.ibcf import *
from cls.def_cls import *


class MSG_EMS_CS_DIS_TMR_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_TMR_REQ)
    
    
class MSG_EMS_CS_DIS_TMR_RSP(IbcfResponseMsg):
    
    """
struct SipCoreTimer_t
{
   int            m_nTimeT2                   ; // 1. M, T2 (1 ~ 10000)
   int            m_nTimeTA                   ; // 2. M, TA (1 ~ 180000)
   int            m_nTimeTB                   ; // 3. M, TB (1 ~ 180000)
   int            m_nTimeTC                   ; // 4. M, TC (1 ~ 180000)
   int            m_nTimeTD                   ; // 5. M, TD (1 ~ 180000)
   int            m_nTimeTE                   ; // 6. M, TE (1 ~ 180000)
   int            m_nTimeTF                   ; // 7. M, TF (1 ~ 180000)
   int            m_nTimeTG                   ; // 8. M, TG (1 ~ 180000)
   int            m_nTimeTH                   ; // 9. M, TH (1 ~ 180000)
   int            m_nTimeTI                   ; //10. M, TI (1 ~ 180000)
   int            m_nTimeTJ                   ; //11. M, TJ (1 ~ 180000)
   int            m_nTimeTK                   ; //12. M, TK (1 ~ 180000)
   int            m_nTimeTL                   ; //13. M, TL (1 ~ 180000)
   int            m_nTimeTM                   ; //14. M, TM (1 ~ 180000)
   int            m_nTimeDAlive               ; //15. M, DIAL_ALIVE  (1 ~ 300)   . sec
   int            m_nTimeDTerm                ; //16. M, DIAL_TERMINATED (1 ~ 300). sec
   int            m_nTimeTrGW                 ; //17. M, TRGW_ALIVE (1 ~ 10). sec
   unsigned char  m_ucReserved1[12]           ;
   ////////the below api set ////////////////
   int            m_nIndex        ; //internal index
   unsigned char  m_ucUsed        ; //used flag
   unsigned char  m_ucReserved[3] ;
};

// CS_DIS_TMR_RSP
typedef struct Cs_dis_tmr_rsp 
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_LM_DESC_LEN];

    SipCoreTimer_t m_stTmr;

} Cs_dis_tmr_rsp_t;
    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_TMR_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiiiiiiiiiiii%dsiB%ds" % (12, 3))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stTmr"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_TMR_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiiiiiiiiiiii%dsiB%ds" % (12, 3))
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_nTimeT2 m_nTimeTA m_nTimeTB m_nTimeTC m_nTimeTD m_nTimeTE m_nTimeTF m_nTimeTG m_nTimeTH m_nTimeTI m_nTimeTJ m_nTimeTK m_nTimeTL m_nTimeTM m_nTimeDAlive m_nTimeDTerm m_nTimeTrGW  m_ucReserved1 m_nIndex m_ucUsed m_ucReserved")
        
        new_list.append(StructInfo._make(unpack("iiiiiiiiiiiiiiiii%dsiB%ds" %(12, 3), response.m_stTmr)))
        response = response._replace(m_stTmr = new_list)
        
        print response
        return response

###############################################################################################################################################

class SipCoreTimer_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "iiiiiiiiiiiiiiiii%dsiB%ds" % (12, 3)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " m_nTimeT2 m_nTimeTA m_nTimeTB m_nTimeTC m_nTimeTD m_nTimeTE m_nTimeTF m_nTimeTG m_nTimeTH m_nTimeTI m_nTimeTJ m_nTimeTK m_nTimeTL m_nTimeTM m_nTimeDAlive m_nTimeDTerm m_nTimeTrGW m_ucReserved1 m_nIndex m_ucUsed m_ucReserved"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.m_nTimeT2, self.m_nTimeTA, self.m_nTimeTB, self.m_nTimeTC, self.m_nTimeTD, self.m_nTimeTE, self.m_nTimeTF, self.m_nTimeTG, self.m_nTimeTH, self.m_nTimeTI, self.m_nTimeTJ, self.m_nTimeTK, self.m_nTimeTL, self.m_nTimeTM, self.m_nTimeDAlive, self.m_nTimeDTerm, self.m_nTimeTrGW, \
                    self.m_ucReserved1, self.m_nIndex, self.m_ucUsed, self.m_ucReserved);



class SipCoreTimer_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("iiiiiiiiiiiiiiiii%dsiB%ds" % (12, 3))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_LM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stTmr"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("iiiiiiiiii%dsiB%ds" % (16, 3))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "m_nTimeT2 m_nTimeTA m_nTimeTB m_nTimeTC m_nTimeTD m_nTimeTE m_nTimeTF m_nTimeTG m_nTimeTH m_nTimeTI m_nTimeTJ m_nTimeTK m_nTimeTL m_nTimeTM m_nTimeDAlive m_nTimeDTerm m_nTimeTrGW  m_ucReserved1 m_nIndex m_ucUsed m_ucReserved")
 
        new_list.append(StructInfo._make(unpack("iiiiiiiiiiiiiiiii%dsiB%ds" %(12, 3), response.m_stTmr)))
        response = response._replace(m_stTmr = new_list)
        
        print response
        return response

###############################################################################################################################################

class MSG_EMS_CS_CHG_TMR_REQ(SipCoreTimer_t_REQ):
    
    def __init__(self):
        SipCoreTimer_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_CHG_TMR_REQ)

class MSG_EMS_CS_CHG_TMR_RSP(SipCoreTimer_t_RSP):
    
    def __init__(self):
        SipCoreTimer_t_RSP.__init__(self, DEF_STYPE_CS_CHG_TMR_RSP)

###############################################################################################################################################

class TmrCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved1 = ''
        self.request.m_nIndex = 0
        self.request.m_ucUsed = 0
        self.request.m_ucReserved = ''
        
        self.flagSipOrCs = -1

    def printInputMessage(self, imsg):        
        print "\t"
        if imsg.m_nTimeT2 != 0:
            print "\t" "%16s = %d" % ('T2', imsg.m_nTimeT2)
  
        if imsg.m_nTimeTA != 0:
            print "\t" "%16s = %d" % ('T_A', imsg.m_nTimeTA)

        if imsg.m_nTimeTB != 0:
            print "\t" "%16s = %d" % ('T_B', imsg.m_nTimeTB)

        if imsg.m_nTimeTC !=0:
            print "\t" "%16s = %d" % ('T_C', imsg.m_nTimeTC)

        if imsg.m_nTimeTD !=0:
            print "\t" "%16s = %d" % ('T_D', imsg.m_nTimeTD)
            
        if imsg.m_nTimeTE !=0:
            print "\t" "%16s = %d" % ('T_E', imsg.m_nTimeTE)
            
        if imsg.m_nTimeTF !=0:
            print "\t" "%16s = %d" % ('T_F', imsg.m_nTimeTF)
            
        if imsg.m_nTimeTG !=0:
            print "\t" "%16s = %d" % ('T_G', imsg.m_nTimeTG)
            
        if imsg.m_nTimeTH !=0:
            print "\t" "%16s = %d" % ('T_H', imsg.m_nTimeTH)
            
        if imsg.m_nTimeTI !=0:
            print "\t" "%16s = %d" % ('T_I', imsg.m_nTimeTI)
            
        if imsg.m_nTimeTJ !=0:
            print "\t" "%16s = %d" % ('T_J', imsg.m_nTimeTJ)
            
        if imsg.m_nTimeTK !=0:
            print "\t" "%16s = %d" % ('T_K', imsg.m_nTimeTK)
            
        if imsg.m_nTimeTL !=0:
            print "\t" "%16s = %d" % ('T_L', imsg.m_nTimeTL)

        if imsg.m_nTimeDAlive !=0:
            print "\t" "%16s = %d" % ('DIAL_ALIVE', imsg.m_nTimeDAlive) 

        if imsg.m_nTimeDTerm !=0:
            print "\t" "%16s = %d" % ('DIAL_TERMIT', imsg.m_nTimeDTerm) 


    def printOutputMessage(self, omsg):
        for st in omsg.m_stTmr :
            if self.flagSipOrCs == 1:
               print "\t", "%10s = %6d(ms)  %s" % ('T2',  st.m_nTimeT2, ' - The MAX retransmit interval for non-INVITE request and INVITE response')
               print "\t", "%10s = %6d(ms)  %s" % ('T_A', st.m_nTimeTA, ' - INVITE request retransmit interval, UDP only')
               print "\t", "%10s = %6d(ms)  %s" % ('T_B', st.m_nTimeTB, ' - INVITE transaction timeout timer') 
               print "\t", "%10s = %6d(ms)  %s" % ('T_C', st.m_nTimeTC, ' - proxy INVITE transaction timeout')
               print "\t", "%10s = %6d(ms)  %s" % ('T_D', st.m_nTimeTD, ' - Wait time for Response retransmits')
               print "\t", "%10s = %6d(ms)  %s" % ('T_E', st.m_nTimeTE, ' - non-INVITE request retransmit interval, UDP only')
               print "\t", "%10s = %6d(ms)  %s" % ('T_F', st.m_nTimeTF, ' - non-INVITE transaction timeout timer')
               print "\t", "%10s = %6d(ms)  %s" % ('T_G', st.m_nTimeTG, ' - INVITE response retransmit interval')
               print "\t", "%10s = %6d(ms)  %s" % ('T_H', st.m_nTimeTH, ' - Wait time for ACK receipt')
               print "\t", "%10s = %6d(ms)  %s" % ('T_I', st.m_nTimeTI, ' - Wait time for ACK retransmits')
               print "\t", "%10s = %6d(ms)  %s" % ('T_J', st.m_nTimeTJ, ' - Wait time for non-INVITE request retransmits')
               print "\t", "%10s = %6d(ms)  %s" % ('T_K', st.m_nTimeTK, ' - Wait time for response retransmits')
               print "\t", "%10s = %6d(ms)  %s" % ('T_L', st.m_nTimeTL, ' - Wait time for accepted INVITE request retransmits')
            elif self.flagSipOrCs == 2:
               print "\t", "%15s = %6d(ms)" % ('DIAL_ALIVE', st.m_nTimeDAlive)
               print "\t", "%15s = %6d(ms)" % ('DIAL_TERMIT', st.m_nTimeDTerm)

   
