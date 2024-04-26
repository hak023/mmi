
from mmi.ibcf import *
from cls.def_cls import *


class MSG_SUBF_RTE_DIS_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_RTE_REQ)
    
    
class MSG_SUBF_RTE_DIS_RSP(IbcfResponseMsg):
    
    """
typedef struct st_tg_route : public st_tg_base 
{
    unsigned int  uiReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucStatus;       // e_tga_status
    unsigned char ucID;
    char szName[64];
    
    unsigned int uiTRTE;          // TRTE
    unsigned char ucLMT_RT;       // LMT_RT
    unsigned char ucOOS_LMT_RT;   // OOS_LMT_RT
    char cDefIPVer;               // Default IP Ver
    unsigned char ucML_BLK; 

    unsigned char ucF_BLK; 
    char cOwn;  
    unsigned char ucReserved[6];

    // tg only
    char cSRTP;  
    char cRemoteNATCnt;
    char cChkIPPort;
    char cUseAuth;                // SHA-1
    char cUseEnc;                 // 0:Off 1:AES 2:ARIA
    char cChkPT;
    char cChkSSRC;                // not use
    char cChgPT;

    char cChgSSRC;                // not use
    char cChkSeq;
    char cChkTS;
    char cOMRAdd;
    char cUseImgAttr;
    char cPID;                    // PT Group ID
    char cReserved[2];

    char cEncKey[128];            // 128byte 
    ////////////

    // msrp only
    unsigned char ucSetup;        // msrp. active, passive, actpass
    unsigned char ucReserved2[7];
    ////////////

    unsigned int uiUsedSes;
    unsigned int uiAvailSes;
    unsigned int uiTotalSes;
    unsigned int uiTotalRsc;


    char cChkCodec;               // codecList used
    char cCodecList[64];          // codecList ex) 1/2/3/4 
    char cReserved2[7];

} st_tg_route, *pst_tg_route;    
    
typedef struct Emp_dis_rte_rsp
{
    int m_nResult;
    int m_nReason;
    char m_szReasonDesc[DEF_VLM_DESC_LEN];
    int m_nNumber;
    st_tg_route m_stData[EMG_MAX_TG_ROUTE];

} Emp_dis_rte_rsp_t;

    """
    
    def __init__(self):       
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_RTE_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBB%dsIBBbBBb%dsbbbbbbbbbbbbbb%ds%dsB%dsIIIIb%ds%ds" % (64, 6, 2, 128, 7, 64, 7))
        return FMT_UDP_HEADER + "ii%dsi%ds" % (DEF_VLM_DESC_LEN, Struct_size * EMG_MAX_TG_ROUTE)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_nNumber m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_RTE_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBB%dsIBBbBBb%dsbbbbbbbbbbbbbb%ds%dsB%dsIIIIb%ds%ds" % (64, 6, 2, 128, 7, 64, 7))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucStatus ucID szName uiTRTE ucLMT_RT ucOOS_LMT_RT cDefIPVer ucML_BLK ucF_BLK cOwn ucReserved cSRTP cRemoteNATCnt cChkIPPort cUseAuth cUseEnc cChkPT cChkSSRC cChgPT cChgSSRC cChkSeq cChkTS cOMRAdd cUseImgAttr cPID cReserved cEncKey ucSetup ucReserved2 uiUsedSes uiAvailSes uiTotalSes uiTotalRsc cChkCodec cCodecList cReserved2")
        for i in range(response.m_nNumber) :
            new_list.append(StructInfo._make(unpack("IBBBB%dsIBBbBBb%dsbbbbbbbbbbbbbb%ds%dsB%dsIIIIb%ds%ds" %(64, 6, 2, 128, 7, 64, 7), response.m_stData[i*Struct_size:(i+1)*Struct_size])))
        
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################


class MSG_SUBF_RTE_DEL_REQ(MSG_EMS_DEFAULT_DEL_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DEL_RTE_REQ)

class MSG_SUBF_RTE_DEL_RSP(MSG_EMS_DEFAULT_DEL_RSP):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DEL_RTE_RSP)


###############################################################################################################################################

class TgRte_t_REQ(IbcfRequestMsg):

    def __init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType):
        self.uReason = 0
        self.ucEnabled = 0
        self.ucValid = 0
        self.ucID = 0
        self.ucStatus = 0        
        IbcfRequestMsg.__init__(self, uiMagicCookie, uiMsgLen, uiType, uiSubType)

    def getFormat(self):
        return FMT_UDP_HEADER + "IBBBB%dsIBBbBBb%dsbbbbbbbbbbbbbb%ds%dsB%dsIIIIb%ds%ds" % (64, 6, 2, 128, 7, 64, 7)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " uReason ucEnabled ucValid ucStatus ucID szName uiTRTE ucLMT_RT ucOOS_LMT_RT cDefIPVer ucML_BLK ucF_BLK cOwn ucReserved cSRTP cRemoteNATCnt cChkIPPort cUseAuth cUseEnc cChkPT cChkSSRC cChgPT cChgSSRC cChkSeq cChkTS cOMRAdd cUseImgAttr cPID cReserved cEncKey ucSetup ucReserved2 uiUsedSes uiAvailSes uiTotalSes uiTotalRsc cChkCodec cCodecList cReserved2"

    def getSize(self):
        return calcsize(self.getFormat())

    def pack(self):  
        return pack(self.getFormat(), \
                    self.uiMagicCookie, self.uiMsgLen, self.uiType, self.uiSubType, \
                    self.uiCompId, self.uiCompSesId, self.uiAsId, self.uiAsSesId, self.szSesDesc, self.uiReasonCode, \
                    self.union_Reserved, \
                    self.uReason, self.ucEnabled, self.ucValid, self.ucStatus, self.ucID, self.szName, \
                    self.uiTRTE, self.ucLMT_RT, self.ucOOS_LMT_RT, self.cDefIPVer, self.ucML_BLK, self.ucF_BLK, self.cOwn, self.ucReserved, \
                    self.cSRTP, self.cRemoteNATCnt, self.cChkIPPort, self.cUseAuth, self.cUseEnc, \
                    self.cChkPT, self.cChkSSRC, self.cChgPT, self.cChgSSRC, self.cChkSeq, self.cChkTS, self.cOMRAdd, self.cUseImgAttr, self.cPID, \
                    self.cReserved, self.cEncKey, \
                    self.ucSetup, self.ucReserved2, \
                    self.uiUsedSes, self.uiAvailSes, self.uiTotalSes, self.uiTotalRsc, \
                    self.cChkCodec, self.cCodecList, self.cReserved2
                    )

class TgRte_t_RSP(IbcfResponseMsg):

    def __init__(self, uiSubType):
        IbcfResponseMsg.__init__(self, uiSubType)
    
    def getFormat(self):
        Struct_size = calcsize("IBBBB%dsIBBbBBb%dsbbbbbbbbbbbbbb%ds%dsB%dsIIIIb%ds%ds" % (64, 6, 2, 128, 7, 64, 7))
        return FMT_UDP_HEADER + "ii%ds%ds" % (DEF_VLM_DESC_LEN, Struct_size)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_stData"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("IBBBB%dsIBBbBBb%dsbbbbbbbbbbbbbb%ds%dsB%dsIIIIb%ds%ds" % (64, 6, 2, 128, 7, 64, 7))
        new_list = []
        
        StructInfo = namedtuple("StructInfo", "uReason ucEnabled ucValid ucStatus ucID szName uiTRTE ucLMT_RT ucOOS_LMT_RT cDefIPVer ucML_BLK ucF_BLK cOwn ucReserved cSRTP cRemoteNATCnt cChkIPPort cUseAuth cUseEnc cChkPT cChkSSRC cChgPT cChgSSRC cChkSeq cChkTS cOMRAdd cUseImgAttr cPID cReserved cEncKey ucSetup ucReserved2 uiUsedSes uiAvailSes uiTotalSes uiTotalRsc cChkCodec cCodecList cReserved2")
 
        new_list.append(StructInfo._make(unpack("IBBBB%dsIBBbBBb%dsbbbbbbbbbbbbbb%ds%dsB%dsIIIIb%ds%ds" %(64, 6, 2, 128, 7, 64, 7), response.m_stData)))
        response = response._replace(m_stData = new_list)
        
        print response
        return response
    
###############################################################################################################################################
         
class MSG_SUBF_RTE_ADD_REQ(TgRte_t_REQ):

    def __init__(self):
        TgRte_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_ADD_RTE_REQ)

class MSG_SUBF_RTE_ADD_RSP(TgRte_t_RSP):

    def __init__(self):
        TgRte_t_RSP.__init__(self, DEF_STYPE_EMP_ADD_RTE_RSP)

###############################################################################################################################################

class MSG_SUBF_RTE_CHG_REQ(TgRte_t_REQ):
    
    def __init__(self):
        TgRte_t_REQ.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_CHG_RTE_REQ)

class MSG_SUBF_RTE_CHG_RSP(TgRte_t_RSP):
    
    def __init__(self):
        TgRte_t_RSP.__init__(self, DEF_STYPE_EMP_CHG_RTE_RSP)

###############################################################################################################################################

class TgRteCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved = ''
        self.request.m_ucStatus = 0
        self.request.m_ucUsed = 0
        self.request.m_usReserved2 = 0
        self.request.m_nIndex = 0
        
        self.isIdxSearch = 0

    def printInputMessage(self, imsg):
        print ""
        print "\t" "%10s : %d" % ('ID', imsg.uiTRTE)
        if imsg.cDefIPVer != -1:
            print "\t" "%10s : %s" % ('IPVER', self.reprTgRteIpverIntToStr(imsg.cDefIPVer))
        if imsg.ucLMT_RT != 0:
            print "\t" "%10s : %d" % ('LMT', imsg.ucLMT_RT)
        if imsg.ucOOS_LMT_RT != 0:
            print "\t" "%10s : %d" % ('OOS-LMT', imsg.ucOOS_LMT_RT)
        if imsg.szName !='':
            print "\t" "%10s : %s" % ('NAME', self.reprName(imsg.szName))
        if imsg.cOwn != -1:
            print "\t" "%10s : %s" % ('TYPE', self.reprTgRteTypeIntToStr(imsg.cOwn))
        if imsg.cRemoteNATCnt != -1:
            print "\t" "%10s : %d" % ('RMT_NAT', imsg.cRemoteNATCnt)
        if imsg.cChkIPPort != -1:
            print "\t" "%10s : %s" % ('CHK_IPPORT', self.reprOnOffIntToStr(imsg.cChkIPPort))
        if imsg.cChkSeq != -1:
            print "\t" "%10s : %s" % ('CHK_SEQ', self.reprOnOffIntToStr(imsg.cChkSeq))
        if imsg.cChkTS != -1:
            print "\t" "%10s : %s" % ('CHK_TS', self.reprOnOffIntToStr(imsg.cChkTS))
        if imsg.cChkPT != -1:
            print "\t" "%10s : %s" % ('CHK_PT', self.reprOnOffIntToStr(imsg.cChkPT))

    def printOutputMessage(self, omsg):
        if self.isIdxSearch == 0:
           print "\t", " %5s %15s %7s %4s %8s %12s %8s %11s %8s %8s %8s %10s" \
                            % ('TRTE', 'NAME', 'TYPE', 'LMT', 'OOS-LMT', 'IPVER', 'RMT_NAT', 'CHK_IPPORT', 'CHK_SEQ', 'CHK_TS', 'CHK_PT', 'STATUS')

           print "\t", "--------------------------------------------------------------------------------------------------------------------"

           for rte in sorted(omsg.m_stData) :
               print "\t", " %5d %15s %7s %4d %8d %12s %8d %11s %8s %8s %8s %10s" % \
                              (rte.uiTRTE, self.reprNameShorter(rte.szName, 15, 10), self.reprTgRteTypeIntToStr(rte.cOwn),
                               rte.ucLMT_RT, rte.ucOOS_LMT_RT,
                               self.reprTgRteIpverIntToStr(rte.cDefIPVer),
                               rte.cRemoteNATCnt, self.reprOnOffIntToStr(rte.cChkIPPort),
                               self.reprOnOffIntToStr(rte.cChkSeq), self.reprOnOffIntToStr(rte.cChkTS),
                               self.reprOnOffIntToStr(rte.cChkPT), 
                               self.reprStatusIntToStr(rte.ucStatus)
                              )

        elif self.isIdxSearch == 1:
           for rte in omsg.m_stData :
               print "\t" "%10s : %d" % ('ID', rte.uiTRTE)
               print "\t" "%10s : %s" % ('NAME', self.reprName(rte.szName))
               print "\t" "%10s : %s" % ('TYPE', self.reprTgRteTypeIntToStr(rte.cOwn))
               print "\t" "%10s : %d" % ('LMT', rte.ucLMT_RT)
               print "\t" "%10s : %d" % ('OOS-LMT', rte.ucOOS_LMT_RT)
               print "\t" "%10s : %s" % ('IPVER', self.reprTgRteIpverIntToStr(rte.cDefIPVer))
               print "\t" "%10s : %d" % ('RMT_NAT', rte.cRemoteNATCnt)
               print "\t" "%10s : %s" % ('CHK_IPPORT', self.reprOnOffIntToStr(rte.cChkIPPort))
               print "\t" "%10s : %s" % ('CHK_SEQ', self.reprOnOffIntToStr(rte.cChkSeq))
               print "\t" "%10s : %s" % ('CHK_TS', self.reprOnOffIntToStr(rte.cChkTS))
               print "\t" "%10s : %s" % ('CHK_PT', self.reprOnOffIntToStr(rte.cChkPT))
               print "\t" "%10s : %s" % ('STATUS', self.reprStatusIntToStr(rte.ucStatus))                          
            
        if omsg.uiSubType == DEF_STYPE_EMP_DIS_RTE_REQ: 
           print ""
           print "%-10s = %s" % ('RTE_CNT', omsg.m_nNumber)

   
