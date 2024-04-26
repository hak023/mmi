
from mmi.cmd import MMICommandException, MMI_COMMAND_RESULT_FAILURE,\
    MMI_COMMAND_RESULT_SUCCESS, MMIOutputMessage, MMI_COMMAND_TYPE_OAM,\
    MMICommand, MMICommandParamException
from mysql import connector
import datetime


STAT_TIMEUNIT_5MIN = "5MIN"
STAT_TIMEUNIT_HOUR = "HOUR"
STAT_TIMEUNIT_DAY = "DAY"
STAT_TIMEUNIT_WEEK = "WEEK"
STAT_TIMEUNIT_MON = "MON"
STAT_TIMEUNIT_YEAR = "YEAR"

TIMEUNIT_24 = "24HOUR"

TIMEUNIT_ONE_HOUR = "ONE_HOUR"

STAT_TIMEUNITS = [STAT_TIMEUNIT_5MIN, STAT_TIMEUNIT_HOUR, STAT_TIMEUNIT_DAY, STAT_TIMEUNIT_WEEK, STAT_TIMEUNIT_MON, STAT_TIMEUNIT_YEAR]

_COLUMN_LEN_MIN = 8
_DATETIME_INPUT_FORMAT = '%y%m%d%H%M'

STAT_LIMIT_DEFAULT = '50'

class MysqlCommandException(MMICommandException):
    pass


class MysqlOutputMessage(MMIOutputMessage):
    def __init__(self, result=MMI_COMMAND_RESULT_FAILURE, reason=None):
        MMIOutputMessage.__init__(self, result, reason)
        self.updated = 0
        self.rows = None


class MysqlCommand(MMICommand):

    def __init__(self):
        MMICommand.__init__(self)
        self.labels = ()
        self.query = ''
        self.queryParameters = ()
        self.omsg = MysqlOutputMessage(MMI_COMMAND_RESULT_FAILURE, 0)

    def printType(self):
        print MMI_COMMAND_TYPE_OAM

    def getQuery(self):
        return self.query
    
    def getQueryParameters(self):
        return self.queryParameters
    
    def getLabels(self):
        return self.labels
    
    def printInputMessage(self, args):
        pass

    def printOutputMessage(self, omsg):
        if omsg.rows is not None :
            _labels = self.getLabels()

            # The length of Korean character must be 2
            # So we need str object rows instead of unicode object row
            # Now we will print with not omsg.rows but _strrows
            _strrows = list()

            for _row in omsg.rows:
                _strrow = list()
                _strrows.append(_strrow)
                for _i in range(len(_row)):
                    _strrow.append(str(_row[_i]))

            columns =len(_labels)

            # Find char length of each column name
            _columnLens = [_COLUMN_LEN_MIN for _x in range(columns)]
            for _i in range(columns):
                _len = len(_labels[_i])
                if _len > _columnLens[_i]:
                    _columnLens[_i] = _len
                    
            # Find char length of each column data
            for _row in _strrows:
                for _i in range(len(_row)):
                    _len = len(_row[_i])
                    if _len > _columnLens[_i]:
                        _columnLens[_i] = _len
            
            
            _row_format = ' '.join(['%%%ds'%_columnLens[_i] for _i in range(columns)])
            _total_colum_len = sum([_columnLens[_i] for _i in range(columns)])
            _total_colum_len += (columns -1)  # division spaces
            
            print ''.rjust(_total_colum_len, '-') #row deliminator
            print _row_format % self.getLabels()
            print ''.rjust(_total_colum_len, '-') #row deliminator

            for row in _strrows:
                print _row_format % tuple(row[0:columns])

            print ''.rjust(_total_colum_len, '-') #row deliminator
        
        elif omsg.updated >= 0:
            pass
            #print '%-10s : %s'%('UPDATED', omsg.updated)
        
        else:
            print 'PRINT ERROR : SELECT or UPDATE'
            
    
    def openConnection(self):
        return connector.connect(host=self.config.getCommon('mysql.host', '127.0.0.1')
                                       ,port=self.config.getintCommon('mysql.port', 3306)
                                       ,user=self.config.getCommon('mysql.account')
                                       ,password=self.config.getCommon('mysql.password')
                                       ,charset=self.config.getCommon('mysql.charset', 'euckr')
                                       ,use_unicode=self.config.getbooleanCommon('mysql.use_unicode', False)
                                       ,database=self.config.getCommon('mysql.database'))

    def findSystem(self, systemName):
        try:
            conn = self.openConnection()
            
        except connector.Error, e:
            print "Error %d, SQLState %s, %s" % (e.errno, e.sqlstate, e.msg)
            raise MMICommandException((e.errno, e.msg))
        
        isystem = None
        
        try:
            cursor = conn.cursor()
            _updated = cursor.execute (""" SELECT SYSTEMID FROM SERVER WHERE SYSTEMNAME = %s """, (systemName,))
        
            row = cursor.fetchone()
        
            if row is None :
                raise MMICommandException(("Not found server : %s"%(systemName)))
        
            isystem = SystemInfo()
            isystem.systemId = row[0]
        
        except connector.Error, e:
            print "Error %d, SQLState %s, %s" % (e.errno, e.sqlstate, e.msg)
            raise MMICommandException(e.errno, e.msg)
        
        return isystem
     

    def findServer(self, systemName, serverName):
        try:
            conn = self.openConnection()
        except connector.Error, e:
            print "Error %d, SQLState %s, %s" % (e.errno, e.sqlstate, e.msg)
            raise MMICommandException((e.errno, e.msg))

        server = None
        
        try:
            cursor = conn.cursor()
            _updated = cursor.execute ("""SELECT SYSTEMID,SYSTEMNAME,SERVERID,SERVERNAME,
                SERVERTYPE,SERVERINDEX,SERVERIP,SERVEROS,OMAPORT,TELNETPORT,FTPPORT,HAPORT,DESCRIPTION,
                SEQ,DBID,DATECREATED,VALIDSTATE 
                FROM SERVER
                WHERE SYSTEMNAME=%s AND SERVERNAME=%s""", (systemName, serverName))

            row = cursor.fetchone()
            
            if row is None :
                raise MMICommandException(("Not found server : %s, %s"%(systemName, serverName)))
            
            server = ServerInfo()
            server.systemId = row[0]
            server.systemName = row[1]
            server.serverId = row[2]
            server.serverName = row[3]
            server.serverType = row[4]
            server.serverInex = row[5]
            server.serverIP = row[6]
            server.serverOS = row[7]
            server.omaPort = row[8]
            server.telentPort = row[9]
            server.ftpPort = row[10]
            server.haPort = row[11]
            server.description = row[12]
            server.seq = row[13]
            server.dbId = row[14]
            server.dateCreated = row[15]
            server.validState = row[16]
            
        except connector.Error, e:
            print "Error %d, SQLState %s, %s" % (e.errno, e.sqlstate, e.msg)
            raise MMICommandException(e.errno, e.msg)
            
        return server
    
    def execute(self):
        
        _omsg = MysqlOutputMessage(MMI_COMMAND_RESULT_FAILURE, 0)
        
        try:
            conn = self.openConnection()
            conn.set_autocommit('ON')
                      
        except connector.Error, e:
            raise MMICommandException((e.errno, e.msg))

        try:
            cursor = conn.cursor()
            
            self.omsg.updated = cursor.execute (self.getQuery(), self.getQueryParameters())

            if self.omsg.updated < 0 :
                self.omsg.result = MMI_COMMAND_RESULT_SUCCESS
                self.omsg.rows = cursor.fetchall()
            
            elif self.omsg.updated > 0 :
                self.omsg.result = MMI_COMMAND_RESULT_SUCCESS

            else :
                raise MysqlCommandException('No data affected')
                
            cursor.close()

        except connector.Error, e:
            self.exception = e
            self.omsg.result = MMI_COMMAND_RESULT_FAILURE
            self.omsg.reason = e.sqlstate
            
        conn.close()
        
        self.printMessage(self.queryParameters, self.omsg)

    def printExcecption(self, e):
        if type(e) is MMICommandParamException: #Deprecated
            self.printUsage()
        else :
            self.exception = e
            self.printMessage(self.queryParameters, self.omsg)
    
    def findFromTimeToTime(self, timeunit, fromTime=None, toTime=None):
        
        if fromTime is not None and not isinstance(fromTime, datetime.datetime) :
            if fromTime is '':
                fromTime = None
            else :
                fromTime = datetime.datetime.strptime(fromTime, _DATETIME_INPUT_FORMAT)

        if toTime is not None and not isinstance(toTime, datetime.datetime) :
            if toTime is '':
                toTime = None
            else :
                toTime = datetime.datetime.strptime(toTime, _DATETIME_INPUT_FORMAT)
        
        if fromTime is None and toTime is None:
            toTime = datetime.datetime.now()
            
            if timeunit == STAT_TIMEUNIT_5MIN:

                toTime = toTime - datetime.timedelta(minutes=(toTime.minute % 5)+5, 
                                                     seconds=toTime.second, microseconds=toTime.microsecond)
                
                fromTime = toTime - datetime.timedelta(minutes=5)
                
            elif timeunit == STAT_TIMEUNIT_HOUR:
                
                toTime = toTime.replace(minute=0, second=0, microsecond=0)
                
                fromTime = toTime - datetime.timedelta(hours=1)
                
            elif timeunit == STAT_TIMEUNIT_DAY:
                toTime = toTime.replace(hour=0, minute=0, second=0, microsecond=0)
                fromTime = toTime - datetime.timedelta(days=1)
                
            elif timeunit == STAT_TIMEUNIT_WEEK:
                toTime = toTime.replace(hour=0, minute=0, second=0, microsecond=0)
                toTime = toTime - datetime.timedelta(days=toTime.weekday()) # Monday
                fromTime = toTime - datetime.timedelta(days=7)

            elif timeunit == STAT_TIMEUNIT_MON:
                toTime = toTime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                if toTime.month == 1:
                    fromTime = toTime.replace(year=toTime.year-1, month=12)
                else :
                    fromTime = toTime.replace(month=toTime.month-1)
                    
            elif timeunit == STAT_TIMEUNIT_YEAR:
                toTime = toTime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                fromTime = toTime.replace(year=toTime.year-1)

            elif timeunit == TIMEUNIT_24:
                fromTime = toTime - datetime.timedelta(days=1)

            elif timeunit == TIMEUNIT_ONE_HOUR:
                fromTime = toTime - datetime.timedelta(hours=1)


        elif fromTime is None:
            if timeunit == STAT_TIMEUNIT_5MIN:
                fromTime = toTime - datetime.timedelta(minutes=5)
                
            elif timeunit == STAT_TIMEUNIT_HOUR:
                fromTime = toTime - datetime.timedelta(hours=1)
                
            elif timeunit == STAT_TIMEUNIT_DAY:
                fromTime = toTime - datetime.timedelta(days=1)
                
            elif timeunit == STAT_TIMEUNIT_WEEK:
                fromTime = toTime - datetime.timedelta(days=7)

            elif timeunit == STAT_TIMEUNIT_MON:
                if toTime.month == 1:
                    fromTime = toTime.replace(year=toTime.year-1, month=12)
                else :
                    fromTime = toTime.replace(month=toTime.month-1)

            elif timeunit == STAT_TIMEUNIT_YEAR:
                fromTime = toTime.replace(year=toTime.year-1)

            elif timeunit == TIMEUNIT_24:
                fromTime = toTime - datetime.timedelta(days=1)

            elif timeunit == TIMEUNIT_ONE_HOUR:
                fromTime = toTime - datetime.timedelta(hours=1)

            
        elif toTime is None:
            toTime = datetime.datetime.now()

            if timeunit == STAT_TIMEUNIT_5MIN:
                toTime = toTime - datetime.timedelta(minutes=(toTime.minute % 5)+5,
                                                     seconds=toTime.second, microseconds=toTime.microsecond)

            elif timeunit == STAT_TIMEUNIT_HOUR:
                toTime = toTime.replace(minute=0, second=0, microsecond=0)

            elif timeunit == STAT_TIMEUNIT_DAY:
                toTime = toTime.replace(hour=0, minute=0, second=0, microsecond=0)

            elif timeunit == STAT_TIMEUNIT_WEEK:
                toTime = toTime.replace(hour=0, minute=0, second=0, microsecond=0)
                toTime = toTime - datetime.timedelta(days=toTime.weekday()) # Monday

            elif timeunit == STAT_TIMEUNIT_MON:
                toTime = toTime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            elif timeunit == STAT_TIMEUNIT_YEAR:
                toTime = toTime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        return (fromTime, toTime)

class ServerInfo(object):
    def __init__(self):
        self.systemId = None
        self.systemName = None
        self.serverId = None
        self.serverName = None
        self.serverType = None
        self.serverInex = None
        self.serverIP = None
        self.serverOS = None
        self.omaPort = None
        self.telentPort = None
        self.ftpPort = None
        self.haPort = None
        self.description = None
        self.seq = None
        self.dbId = None
        self.dateCreated = None
        self.validState = None

class SystemInfo(object):
    def __init__(self):
        self.systemId = None

