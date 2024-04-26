
import sys
import time
import re
from struct import *
from collections import namedtuple
import socket
from mmi.cmd import *

#from binascii import unhexlify

TYPE_TRGW_AS   = 1
TYPE_TRGW_RM   = 2
TYPE_TRGW_MSRP = 3

TRGW_AS_PKT_SIZE = 68
TRGW_RM_PKT_SIZE = 132

MSG_FUNC_MAINT_TGAS   = 0x400
MSG_FUNC_MAINT_TGRM   = 0x600
MSG_FUNC_MAINT_MSRPRM = 0x700

MSG_SDP_PTGR_ADD_REQ  =   0x411
MSG_SDP_PTGR_ADD_RES  =   0x412
MSG_SDP_PTGR_DEL_REQ  =   0x413
MSG_SDP_PTGR_DEL_RES  =   0x414
MSG_SDP_PTGR_MOD_REQ  =   0x415
MSG_SDP_PTGR_MOD_RES  =   0x416

MSG_SDP_CODEC_ADD_REQ =   0x421
MSG_SDP_CODEC_ADD_RES =   0x422
MSG_SDP_CODEC_DEL_REQ =   0x423
MSG_SDP_CODEC_DEL_RES =   0x424
MSG_SDP_CODEC_MOD_REQ =   0x425
MSG_SDP_CODEC_MOD_RES =   0x426

MSG_SDP_RULE_ADD_REQ  =   0x431
MSG_SDP_RULE_ADD_RES  =   0x432
MSG_SDP_RULE_DEL_REQ  =   0x433
MSG_SDP_RULE_DEL_RES  =   0x434
MSG_SDP_RULE_MOD_REQ  =   0x435
MSG_SDP_RULE_MOD_RES  =   0x436

######################################

MSG_RTE_BLK_REQ    = 0x601
MSG_RTE_BLK_RES    = 0x602
MSG_RTE_UNBLK_REQ  = 0x603
MSG_RTE_UNBLK_RES  = 0x604

MSG_BD_BLK_REQ     = 0x611
MSG_BD_BLK_RES     = 0x612
MSG_BD_UNBLK_REQ   = 0x613
MSG_BD_UNBLK_RES   = 0x614

MSG_POOL_BLK_REQ   = 0x621
MSG_POOL_BLK_RES   = 0x622
MSG_POOL_UNBLK_REQ = 0x623
MSG_POOL_UNBLK_RES = 0x624

MSG_RSC_BLK_REQ    = 0x631
MSG_RSC_BLK_RES    = 0x632
MSG_RSC_UNBLK_REQ  = 0x633
MSG_RSC_UNBLK_RES  = 0x634

MSG_RTE_ADD_REQ    = 0x651 
MSG_RTE_ADD_RES    = 0x652 
MSG_RTE_MOD_REQ    = 0x653 
MSG_RTE_MOD_RES    = 0x654 
MSG_RTE_DEL_REQ    = 0x655 
MSG_RTE_DEL_RES    = 0x656 

MSG_RSC_ADD_REQ    = 0x681 
MSG_RSC_ADD_RES    = 0x682 
MSG_RSC_MOD_REQ    = 0x683 
MSG_RSC_MOD_RES    = 0x684 
MSG_RSC_DEL_REQ    = 0x685 
MSG_RSC_DEL_RES    = 0x686 

######################################

MSG_MSRP_RTE_ADD_REQ    = 0x651
MSG_MSRP_RTE_ADD_RES    = 0x652
MSG_MSRP_RTE_MOD_REQ    = 0x653
MSG_MSRP_RTE_MOD_RES    = 0x654
MSG_MSRP_RTE_DEL_REQ    = 0x655
MSG_MSRP_RTE_DEL_RES    = 0x656

MSG_MSRP_RTE_BLK_REQ    = 0x601
MSG_MSRP_RTE_BLK_RES    = 0x602
MSG_MSRP_RTE_UNBLK_REQ  = 0x603
MSG_MSRP_RTE_UNBLK_RES  = 0x604

MSG_MSRP_BD_BLK_REQ     = 0x611
MSG_MSRP_BD_BLK_RES     = 0x612
MSG_MSRP_BD_UNBLK_REQ   = 0x613
MSG_MSRP_BD_UNBLK_RES   = 0x614

MSG_MSRP_POOL_BLK_REQ   = 0x621
MSG_MSRP_POOL_BLK_RES   = 0x622
MSG_MSRP_POOL_UNBLK_REQ = 0x623
MSG_MSRP_POOL_UNBLK_RES = 0x624

MSG_BD_SWITCH_REQ  = 0x641
MSG_BD_SWITCH_RES  = 0x642

######################################

MAX_NAME_LEN = 128
MAX_NUM_NAME = 24
MAX_NUM_FMTP = 128
MAX_NUM_VALUE = 128
MAX_NUM_FS = 16
MAX_LIST = 20
MAX_CNT = 3
RULE_MAX_CNT = 8

DEFAULT_AUDIO_RATE = 8000
DEFAULT_VIDEO_RATE = 90000

########################################

# connection states
_CS_IDLE = 'Idle'
_CS_REQ_STARTED = 'Request-started'
_CS_REQ_SENT = 'Request-sent'

e_tga_status_ok           = 0x00
e_tga_status_ng           = 0x01
e_tga_status_block        = 0x02
e_tga_status_connect_fail = 0x04
e_tga_status_not_active   = 0x08
e_tga_status_hw_fail      = 0x10
e_tga_status_nic_fail     = 0x20
e_tga_status_init_fail    = 0x40

'''
typedef struct {

   unsigned int     nMagicCookie;
   int              nMsgLen;

   unsigned short   usRecvZoneId;
   unsigned short   usRecvSysId;
   unsigned short   usRecvParentId;
   unsigned short   usRecvChildId;
   unsigned int     ulRecvTmpPid;

   unsigned short   usSendZoneId;
   unsigned short   usSendSysId;
   unsigned short   usSendParentId;
   unsigned short   usSendChildId;
   unsigned int     ulSendTmpPid;

   short            snHopCnt;
   unsigned short   usTransactionId;
   short            snSerNo;
   unsigned short   reserved;
   unsigned short   usType;
   unsigned short   usSubType;
   
   # ARSLINE
   unsigned short   usAreaId;
   unsigned short   usSystemId;
   unsigned short   usBoardId;
   unsigned short   usTrunkId;
   unsigned short   usChannelId;
   unsigned short   usReserved_1
   unsigned short   usReserved_2;
   unsigned short   usReserved_3
   
} EVENTINFO; (26count 60size)

//////////////////////////////////////////////////////
// TGAS
typedef struct st_as_base {

    unsigned int uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucID;
    unsigned char ucStatus;

} st_as_base, *pst_as_base;

//////////////////////////////////////////////////////

typedef struct st_tg_base 
{
    unsigned int  uReason;
    unsigned char ucEnabled;
    unsigned char ucValid;
    unsigned char ucStatus;
    unsigned char ucID;
    char szName[64];

} st_tg_base, *pst_tg_base;

//////////////////////////////////////////////////////
'''

# common header
FMT_TCP_HEADER = '=IiHHHHIHHHHIhHhHHHHHHHHHHH'
ATTR_TCP_HEADER = 'nMagicCookie nMsgLen usRecvZoneId usRecvSysId usRecvParentId usRecvChildId ulRecvTmpPid usSendZoneId usSendSysId usSendParentId usSendChildId ulSendTmpPid snHopCnt usTransactionId snSerNo reserved usType usSubType usAreaId usSystemId usBoardId usTrunkId usChannelId usReserved_1 usReserved_2 usReserved_3'

FMT_AS_HEADER = 'IBBBB'
ATTR_AS_HEADER = 'uReason ucEnabled ucValid ucID ucStatus'

FMT_RM_HEADER = 'IBBBB%ds' % (64)
ATTR_RM_HEADER = 'uReason ucEnabled ucValid ucStatus ucID szName'


class EventInfoException(MMICommandException):
    pass

class NotConnected(EventInfoException):
    pass


class EventInfoConnection:

    def __init__(self, host, port, recv_port):
        self._set_hostport(host, port)
        self.send_sock = None
        self.__state = _CS_IDLE
        
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listen_addr = ('', recv_port)

        self.send_sock.bind(listen_addr)
    
    def setMsgType(self, type):
        self._type = type
             
    def _set_hostport(self, host, port):
        self.host = host
        self.port = port
        
        
    def sendRequestUDP(self, data):          
        try:
            self.send_sock.sendto(data, (self.host, self.port))
        
        except socket.error, e:
            raise EventInfoException(e)
             
            
    def recvResponse(self, responseMsg):
        if self._type == TYPE_TRGW_AS:
            
            packet, addr = self.send_sock.recvfrom(TRGW_AS_PKT_SIZE)
            
            TCP_MSG_HDR = namedtuple("TCP_MSG_HDR", ATTR_TCP_HEADER + " " + ATTR_AS_HEADER)
            tcp_header = TCP_MSG_HDR._make(unpack(FMT_TCP_HEADER + FMT_AS_HEADER, packet))        
        
            if tcp_header.usType != MSG_FUNC_MAINT_TGAS : 
                return -1;
            
        elif self._type == TYPE_TRGW_RM:
            
            packet, addr = self.send_sock.recvfrom(TRGW_RM_PKT_SIZE)
            
            TCP_MSG_HDR = namedtuple("TCP_MSG_HDR", ATTR_TCP_HEADER + " " + ATTR_RM_HEADER)
            tcp_header = TCP_MSG_HDR._make(unpack(FMT_TCP_HEADER + FMT_RM_HEADER, packet))        
        
            if tcp_header.usType != MSG_FUNC_MAINT_TGRM :
                return -1;
            
        elif  self._type == TYPE_TRGW_MSRP:   
            
            packet, addr = self.send_sock.recvfrom(TRGW_RM_PKT_SIZE)
            
            TCP_MSG_HDR = namedtuple("TCP_MSG_HDR", ATTR_TCP_HEADER + " " + ATTR_RM_HEADER)
            tcp_header = TCP_MSG_HDR._make(unpack(FMT_TCP_HEADER + FMT_RM_HEADER, packet))        

            #if tcp_header.usType != MSG_FUNC_MAINT_TGRM :
            #    return -1;            

        return responseMsg.unpack(packet)

    
    def close(self):
        if self.send_sock:
            self.send_sock.close()
            self.send_sock = None

        self.__state = _CS_IDLE    
        
          
class EventInfoMsg:
           
    def __init__(self, nMsgLen=0, usType=0, usSubType=0, nMagicCookie=0, usRecvZoneId=0, usRecvSysId=0, usRecvParentId=0, usRecvChildId=0, ulRecvTmpPid=0, 
                 usSendZoneId=0, usSendSysId=0, usSendParentId=0, usSendChildId=0, ulSendTmpPid=0, snHopCnt=0, usTransactionId=0, snSerNo=0, reserved=0, 
                 usAreaId=0, usSystemId=0, usBoardId=0, usTrunkId=0, usChannelId=0, usReserved_1=0, usReserved_2=0, usReserved_3=0):
        
        self.nMagicCookie = nMagicCookie
        self.nMsgLen = nMsgLen
        
        self.usRecvZoneId = usRecvZoneId 
        self.usRecvSysId = usRecvSysId
        self.usRecvParentId = usRecvParentId 
        self.usRecvChildId = usRecvChildId 
        self.ulRecvTmpPid = ulRecvTmpPid
        
        self.usSendZoneId = usSendZoneId 
        self.usSendSysId = usSendSysId 
        self.usSendParentId = usSendParentId 
        self.usSendChildId = usSendChildId 
        self.ulSendTmpPid = ulSendTmpPid
        
        self.snHopCnt = snHopCnt 
        self.usTransactionId = usTransactionId  
        self.snSerNo = snSerNo 
        self.reserved = reserved  
        self.usType = usType 
        self.usSubType = usSubType 
        self.usAreaId = usAreaId
        self.usSystemId = usSystemId 
        self.usBoardId = usBoardId 
        self.usTrunkId = usTrunkId 
        self.usChannelId = usChannelId
        self.usReserved_1 = usReserved_1 
        self.usReserved_2 = usReserved_2 
        self.usReserved_3 = usReserved_3
               
    def getFormat(self):
        return FMT_TCP_HEADER
    
    def getSize(self):
        return calcsize(self.getFormat())
    
    def pack(self):
        return pack(self.getFormat(), \
                    self.nMagicCookie, self.nMsgLen, self.usRecvZoneId, self.usRecvSysId, self.usRecvParentId, self.usRecvChildId, self.ulRecvTmpPid, \
                    self.usSendZoneId, self.usSendSysId, self.usSendParentId, self.usSendChildId, self.ulSendTmpPid, \
                    self.snHopCnt, self.usTransactionId, self.snSerNo, self._reserved, self.usType, self.usSubType, self.usAreaId, self.usSystemId, \
                    self.usBoardId, self.usTrunkId, self.usChannelId, self.usReserved_1, self.usReserved_2, self.usReserved_3)
        
    def printMessage(self, msg):
        print ''    

class EventInfoRequestMsg(EventInfoMsg):
    def __init__(self, nMsgLen, usType, usSubType):
        EventInfoMsg.__init__(self, nMsgLen, usType, usSubType)


class EventInfoResponseMsg(EventInfoMsg):
    def getAttributes(self):
        return ATTR_TCP_HEADER
    
    def unpack(self, binary):
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        return ResponseMsg._make(unpack(self.getForamt(), binary))     
    
        
class EventInfoCommand(MMICommand):

    def __init__(self, request, response, type):
        MMICommand.__init__(self)
        self.setEventInfoRequestMsg(request)
        self.setEventInfoResponseMsg(response)
        self.setMsgType(type)
        
    def setMsgType(self, type):
        self.type = type    
    
    def setEventInfoRequestMsg(self, request):
        self.request = request

    def getEventInfoRequestMsg(self):
        return self.request

    def setEventInfoResponseMsg(self, response):
        self.response = response

    def getEventInfoResponseMsg(self):
        return self.response
        
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
                self.printOutputMessage(omsg)
            except Exception:
                pass
            
            print ""           
            
        else :
            print "%-10s = %s" % ('RESULT', 'FAILURE')
            print "%-10s = %s" % ('REASON', self.exception)
            #traceback.print_exc(file=sys.stdout)
        self.printTail()


    def getAsReason(self, reason):
        
        resultMap = {                                      
            0:"OK",
            0x20020001:"AS - MakeSdpFail",
            0x20020002:"AS - SessionFindFail",
            0x20020003:"AS - ConnectFailTGRM",
            0x20020004:"AS - InvalidNode",
            0x20020005:"AS - SessionFull",
            0x20020006:"AS - InternalError",
            0x20020007:"AS - NegoFail",
            0x20020008:"AS - NotFoundAudio",
            0x20020009:"AS - NotFoundVideo",
            0x2002000A:"AS - NotFoundCodec",
            0x2002000B:"AS - GarbageCollect", 
            0x2002000C:"AS - ConnectFailTCRM", 
            0x2002000D:"AS - ConnectFailMSRPRM", 
            0x2002000E:"AS - SessionBusy", 
            0x2002000F:"AS - SdpParseError", 
            0x20020010:"AS - NotFoundMsrp",
            0x20020011:"AS - NetfailKill",
            0x20020012:"AS - NetfailKill",
            0x20020013:"AS - NetfailKill",
            0x20020014:"AS - NetfailKill",
            0x20020015:"AS - NetfailKill",
            
            0x20021000:"AS - Timeout", 
            0x20021001:"AS - AddTimeout", 
            0x20021002:"AS - ModTimeout", 
            0x20021003:"AS - DelTimeout", 
            0x20021004:"AS - CallDurationTimeout", 
            0x20021005:"AS - AddRspTimeout",   
                 
            0x20022000:"AS - NotFoundPTGroup", 
            0x20022001:"AS - NotFoundCodecList", 
            0x20022002:"AS - AlreadyExistPTList", 
            0x20022003:"AS - NotFoundPTList", 
            0x20022004:"AS - AlreadyExistPTGroup",
            0x20022005:"AS - AlreadyExistCodecList", 
            0x20022006:"AS - AlreadyExistCodecName", 
            0x20022007:"AS - AlreadyExistRuleList", 
            0x20022008:"AS - NotFoundRuleList", 
            0x20022009:"AS - ExistDID", 
            0x2002200A:"AS - ExistCID", 
            0x2002200B:"AS - ExistPID", 
            0x2002200C:"AS - RuleMaxCntOver", 
            
            0x20023001:"AS - SwitchBDStatusFail",
            0x20023002:"AS - ASIPAllocFail"
        }
        
        return resultMap.get(reason)


    def getRmReason(self, reason):
        
        resultMap = {                                      
            0:"OK",                                                        
            0x20031001:"RM - Session Alloc Fail",             
            0x20031002:"RM - Session Busy",                  
            0x20031003:"RM - Session Full",                  
            0x20031004:"RM - Session Idle",                  
            0x20031005:"RM - Insufficient Resource",         
            0x20031006:"RM - Not Enabled",                   
            0x20031007:"RM - Already Enabled",               
            0x20031008:"RM - Invalid Status",                
                                                       
            0x20032001:"RM - Not Found Route",                
            0x20032002:"RM - Not Found Board",                
            0x20032003:"RM - Not Found Tga",                  
            0x20032004:"RM - Not Found Pool",                 
            0x20032005:"RM - Not Found Rsc",                  
            0x20032006:"RM - Not Found Port",                 
            0x20032007:"RM - Not Found AppId",                   
            0x20032008:"RM - Not Found Session",              
            0x20032009:"RM - Not Found Addr",                 
            0x2003200A:"RM - Exist Route",                   
            0x2003200B:"RM - Exist Board",                   
            0x2003200C:"RM - Exist Pool",                    
            0x2003200D:"RM - Exist Rsc",                     
            0x2003200E:"RM - Duplicate Route",               
            0x2003200F:"RM - Duplicate Board",               
            0x20032010:"RM - DuplicateIP",            
            0x20032011:"RM - DuplicateRsc",
            0x20032012:"RM - AlreadyExistRoute",               
                                                       
            0x20033001:"RM - TGAAddrSetFail",               
            0x20033002:"RM - TGABoardNotActive",            
            0x20033003:"RM - GarbageCollect",               
            0x20033004:"RM - AlreadyRecvAddReq",            
            0x20033005:"RM - InvalidIPVersion",             
            0x20033006:"RM - FileSaveFail",                 
            0x20033007:"RM - LongCallDel",                  
                                              
            0x20034001:"RM - RouteFullAlloc",      
            0x20034002:"RM - BoardFullAlloc",      
            0x20034003:"RM - PoolFullAlloc",       
            0x20034004:"RM - RscFullAlloc",        
            0x20034005:"RM - InvalidRoute",        
            0x20034006:"RM - InvalidBoard",        
            0x20034007:"RM - InvalidPool",         
            0x20034008:"RM - InvalidRsc",          
            0x20034009:"RM - ModRouteFail",        
            0x2003400A:"RM - DelRouteFail",        
            0x2003400B:"RM - ModBoardFail",        
            0x2003400C:"RM - DelBoardFail",        
            0x2003400D:"RM - ModPoolFail",         
            0x2003400E:"RM - DelPoolFail",         
            0x2003400F:"RM - ModRscFail",          
            0x20034010:"RM - DelRscFail",
            0x20034011:"RM - SwitchBDStatusFail", 
            0x20034012:"RM - AddRouteFail", 
            0x20034013:"RM - ExistTRTE", 
            0x20034014:"RM - BlockRoute", 
            0x20034015:"RM - BlockBoard", 
            0x20034016:"RM - BlockPool", 
            0x20034017:"RM - BlockRsc",     
                                              
            0x20035000:"RM - Timeout",             
            0x20035001:"RM - DelReqTimeout",       
            0x20035002:"RM - StopReqTimeout",      
            0x20035003:"RM - TgaInitTimeout",      
            0x20035004:"RM - TgaDownTimeout"
        }
        
        return resultMap.get(reason)


    
    def getMsrpReason(self, reason):
        
        resultMap = {                                      
            0:"OK",
            0x20040001:"InsufficientResource",
            0x20040002:"DuplicateCh",
            0x20040003:"NotFoundCh",
            0x20040004:"NotFoundMsrpa",
            0x20040005:"ConnectFailMsrpa",
            0x20040006:"ConnectFailTgas",
            0x20040007:"InternalError",
            0x20040008:"SessionFindFail",
            0x20040009:"MsrpaDown",
            0x2004000A:"SessionBusy",
            0x2004000B:"AlreadyRecvInit",
            0x2004000C:"GarbageCollect",
            0x2004000D:"CloseReqTimeout",
                      
            0x20040010:"NotFoundBoard",
            0x20040011:"SwitchBDStatusFail",
            0x20040012:"AllocFail",
            0x20040013:"AlreadyExistRoute",
            0x20040014:"NotFoundRoute",
            0x20040015:"BlockRoute",
            0x20040016:"BlockBoard",
            0x20040017:"BlockPool",
            0x20040018:"BlockRsc",
            0x20040019:"NotFoundPool",
            0x2004001A:"NotFoundRsc",
            0x2004001B:"SwitchBDModeFail",
            0x2004001C:"ExistTRTE"
        }
        
        return resultMap.get(reason)

    def execute(self):
        
        if(self.response is None) :
            raise EventInfoException()

        if self.type == TYPE_TRGW_AS:
            conn = EventInfoConnection(self.config.get('COMMON', 'as.host'), self.config.getint('COMMON', 'as.port'), self.config.getint('COMMON', 'mmi.port'))
            
        elif self.type == TYPE_TRGW_RM:
            conn = EventInfoConnection(self.config.get('COMMON', 'rm.host'), self.config.getint('COMMON', 'rm.port'), self.config.getint('COMMON', 'mmi.port'))   

        elif self.type == TYPE_TRGW_MSRP:
            conn = EventInfoConnection(self.config.get('COMMON', 'msrp.host'), self.config.getint('COMMON', 'msrp.port'), self.config.getint('COMMON', 'mmi.port'))
            
        self.exception = None
        
        try :
            conn.setMsgType(self.type)      
            conn.sendRequestUDP(self.request.pack())
            self.response = conn.recvResponse(self.response)
            
        except Exception, e:
            print '>>> EventInfoCommand exception...'
            self.exception = e
        
        conn.close()
    
        self.printMessage(self.request, self.response)
        
    def printExcecption(self, e):
        if type(e) is MMICommandParamException:
            self.printUsage()
        else :
            self.exception = e
            self.printMessage(self.request, self.response)          
          
    ###################################################################
    
    def reprName(self, name):
        tempName = []
        for i in range(len(name)):
            if name[i] != '\x00':
                tempName.append(name[i])
            else:
                break

        fixname = "".join(tempName)
        return fixname

    def reprNameShorter(self, name, chklen, cutlen):
        value = self.reprName(name)
        if len(value) > int(chklen):
           value = value[0:int(cutlen)]
           value = value + " ...."
        return value    
    
    ###################################################################
      
    def reprTypeIntToStr(self, type):
        if   type == 0 : return "OTHER"
        elif type == 1 : return "MINE"
        else: return "NONE"

    def reprTypeToStrToInt(self, type):
        if   type == "MINE"  : return 1
        elif type == "OTHER" : return 0
        else: return "UNKNOWN"
    
    def reprOnOffIntToStr(self, type):
        if   type == 1 : return "ON"
        elif type == 0 : return "OFF"
        else: return "UNKNOWN"
    
    def reprOnOffStrToInt(self, type):
        if   type == "ON"  : return 1
        elif type == "OFF" : return 0
        else: return 0    
        
    def reprTgEncTypeIntToStr(self, enctype):
        if   enctype == 0 : return "OFF"
        elif enctype == 1 : return "AES"
        elif enctype == 2 : return "ARIA"
        else: return "UNKNOWN"
        
    def reprTgEncTypeStrToInt(self, type):
        if   type == "OFF"  : return 0
        elif type == "AES"  : return 1
        elif type == "ARIA" : return 2
        else: return 0        
     
    def reprIpverIntToStr(self, ver):
        strVer = ''
        if   ver == 4: strVer = "IPv4"
        elif ver == 6: strVer = "IPv6"
        elif ver == 0: strVer = "RecvDefault"    
        else: strVer = "NONE"
        return strVer
        
    def reprIpTypeStrToInt(self, type):
        if   type == "IP4" : return 4
        elif type == "IP6" : return 6
        elif type == "RECV_DEFAULT" : return 0
        else: return -1
        
    ###################################################################        

    def reprCodecTypeIntToStr(self, type):
        if   type == 1 : return "AUDIO"
        elif type == 2 : return "VIDEO"
        else : return "UNKNOWN"
        
    def reprCodecTypeStrToInt(self, type):
        if   type == "AUDIO": return 1
        elif type == "VIDEO": return 2
        else: return 0
        
    def reprDtmfIntToStr(self, dtmf):
        if   dtmf == 0 : return "FALSE"
        elif dtmf == 1 : return "TRUE"
        else : return "UNKNOWN"         
        
    def reprDtmfStrToInt(self, dtmf):
        if   dtmf == "FALSE" : return 0
        elif dtmf == "TRUE"  : return 1
        else: return 0
        
    ###################################################################
    
    def reprSetupIntToStr(self, setup):
        strSetup = ""
        if setup == 1:
           strSetup = "ACTPASS"
        elif setup == 2:
           strSetup = "ACTIVE"
        elif setup == 3:
           strSetup = "PASSIVE"
        else:
           strSetup = "UNKNOWN"  

        return strSetup
    
    def reprSetupStrToInt(self, setup):
        if   setup == "ACTPASS" : return 1
        elif setup == "ACTIVE"  : return 2
        elif setup == "PASSIVE" : return 3
        else: return 0

    def reprStatusIntToStr(self, status):
        strSts = ''
        
        if status == e_tga_status_ok:
            strSts = "NORMAL"
        else:
            if status & e_tga_status_block:
                if str(strSts): strSts += " & "
                strSts += "BLK"
                
            if status & e_tga_status_ng:
                if str(strSts): strSts += " & "
                strSts += "NG"
                
            if status & e_tga_status_connect_fail:
                if str(strSts): strSts += " & "
                strSts += "CONN_FAIL"
                
            if status & e_tga_status_not_active:
                if str(strSts): strSts += " & "
                strSts += "NOT_ACTIVE"

            if status & e_tga_status_hw_fail:
                if str(strSts): strSts += " & "
                strSts += "HW_FAIL"

            if status & e_tga_status_nic_fail:
                if str(strSts): strSts += " & "
                strSts += "NIC_FAIL"
                
            if status & e_tga_status_init_fail:
                if str(strSts): strSts += " & "
                strSts += "INIT_FAIL"
                
        return strSts
    
    ###################################################################    

            
