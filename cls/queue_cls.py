
from mmi.ibcf import *
from cls.def_cls import *

TIMESPEC_SIZE = 16

class MSG_EMS_CS_DIS_CCM_ST_REQ(MSG_EMS_DEFAULT_DIS_REQ):
        
    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_CS_DIS_CCM_ST_REQ)
    
    
class MSG_EMS_CS_DIS_CCM_ST_RSP(IbcfResponseMsg):
    
    """
typedef struct QueueThreadInfo_t
{
   char m_szThreadName[32];
   unsigned int m_unThreadId;

   struct timespec m_stReqT; size:16
   struct timespec m_stRspT; size:16

   int inTemp;

   unsigned int m_unCurrentQ;
   unsigned int m_unMaxQ;

} QueueThreadInfo_t;

typedef struct ResourceRsp_t
{
   int m_nResult;
   int m_nReason;
   char m_szDesc[64];

   char m_szProcName[32];
   unsigned int m_unPid;

   struct timespec m_stBeginT; size:16
   int outTemp; 

   unsigned int m_unCurThreadNum;
   int outTemp2;

   QueueThreadInfo_t m_stInfo[DEF_MAX_MONITOR];

}ResourceRsp_t;

    """
    
    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_CS_DIS_CCM_ST_RSP)
    
    def getFormat(self):
        Struct_size = calcsize("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE))
        return FMT_UDP_HEADER + "ii%ds%dsi%dsiii%ds" % (64, 32, TIMESPEC_SIZE, Struct_size*DEF_MAX_MONITOR)
    
    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_szProcName m_unPid m_stBeginT outTemp m_unCurThreadNum outTemp2 m_stInfo"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_CS_DIS_CCM_ST_RSP unpack'
        print 'binary length : %d' % len(binary)
        
        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE))
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_szThreadName m_unThreadId m_stReqT inTemp m_stRspT m_unCurrentQ m_unMaxQ")

        for i in range(response.m_unCurThreadNum) :
            new_list.append(StructInfo._make(unpack("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE), response.m_stInfo[i*Struct_size:(i+1)*Struct_size])))

        response = response._replace(m_stInfo = new_list)
 
        print response
        return response

###################################################################################################################################################################

class MSG_EMS_PDE_DIS_PCDS_ST_REQ(MSG_EMS_DEFAULT_DIS_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_PDE_DIS_PCDS_ST_REQ)


class MSG_EMS_PDE_DIS_PCDS_ST_RSP(IbcfResponseMsg):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_PDE_DIS_PCDS_ST_RSP)

    def getFormat(self):
        Struct_size = calcsize("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE))
        return FMT_UDP_HEADER + "ii%ds%dsi%dsiii%ds" % (64, 32, TIMESPEC_SIZE, Struct_size*DEF_MAX_MONITOR)

    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_szProcName m_unPid m_stBeginT outTemp m_unCurThreadNum outTemp2 m_stInfo"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_PDE_DIS_PCDS_ST_RSP unpack'
        print 'binary length : %d' % len(binary)

        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE))
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_szThreadName m_unThreadId m_stReqT inTemp m_stRspT m_unCurrentQ m_unMaxQ")

        for i in range(response.m_unCurThreadNum) :
            new_list.append(StructInfo._make(unpack("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE), response.m_stInfo[i*Struct_size:(i+1)*Struct_size])))

        response = response._replace(m_stInfo = new_list)

        print response
        return response
    
###################################################################################################################################################################

class MSG_EMS_EMP_DIS_TGAS_ST_REQ(MSG_EMS_DEFAULT_DIS_REQ):

    def __init__(self):
        IbcfRequestMsg.__init__(self, SVC_MSG_MAGIC_COOKIE, self.getSize(), DEF_REQ_MSG_BASE, DEF_STYPE_EMP_DIS_TGAS_ST_REQ)


class MSG_EMS_EMP_DIS_TGAS_ST_RSP(IbcfResponseMsg):

    def __init__(self):
        IbcfResponseMsg.__init__(self, DEF_STYPE_EMP_DIS_TGAS_ST_RSP)

    def getFormat(self):
        Struct_size = calcsize("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE))
        return FMT_UDP_HEADER + "ii%ds%dsi%dsiii%ds" % (64, 32, TIMESPEC_SIZE, Struct_size*DEF_MAX_MONITOR)

    def getAttributes(self):
        return ATTR_UDP_HEADER + " " + "m_nResult m_nReason m_szReasonDesc m_szProcName m_unPid m_stBeginT outTemp m_unCurThreadNum outTemp2 m_stInfo"

    def getSize(self):
        return calcsize(self.getFormat())

    def unpack(self, binary):
        print '>> DEF_STYPE_EMP_DIS_TGAS_ST_RSP unpack'
        print 'binary length : %d' % len(binary)

        ResponseMsg = namedtuple("ResponseMsg", self.getAttributes())
        response = ResponseMsg._make(unpack(self.getFormat(), binary))

        Struct_size = calcsize("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE))
        new_list = []

        StructInfo = namedtuple("StructInfo", "m_szThreadName m_unThreadId m_stReqT inTemp m_stRspT m_unCurrentQ m_unMaxQ")

        for i in range(response.m_unCurThreadNum) :
            new_list.append(StructInfo._make(unpack("%dsi%dsi%dsii" % (32, TIMESPEC_SIZE, TIMESPEC_SIZE), response.m_stInfo[i*Struct_size:(i+1)*Struct_size])))

        response = response._replace(m_stInfo = new_list)

        print response
        return response    

###############################################################################################################################################

class QueueCommand(IbcfCommand):
    
    def __init__(self, request, response):
        IbcfCommand.__init__(self, request, response)
        
        self.request.m_ucReserved1 = ''
        self.request.m_nIndex = 0
        self.request.m_ucUsed = 0
        self.request.m_ucReserved = ''     

    def printInputMessage(self, imsg):
        print "\t"

    def printOutputMessage(self, omsg):
        #print "\t"
        #print "\t" "%12s = %s" % ('PROCESS_NAME', self.reprName(omsg.m_szProcName))
        print "\t"
        print "\t", "%17s %10s %10s" % ('THREAD_NAME', 'CUR_QUEUE', 'MAX_QUEUE')
        print "\t", " --------------------------------------"

        for st in omsg.m_stInfo :
            if st.m_unMaxQ !=0:
               print "\t", "%17s %10d %10d" % (self.reprNameShorter(st.m_szThreadName, 17, 15), st.m_unCurrentQ, st.m_unMaxQ)
            

