
from socket import *
import pickle
from harpc.result import *
from harpc import socketFile

_DEBUG = False

class HARPCClient(object):
    
    __MSG_FORMAT = '{"id":"omc", "name":"omc", "comment":"", "command":"%s", "args":"{\\\"what\\\":\\\"%s\\\", \\\"mode\\\":1}"}\r\n'

    _COMMAND_MAP= {"status":("monitor", "status"), "proc":("monitor", "proc"), "man":("monitor", "man"), "deact": ("deact", ""), "active":("mandatory", "active"), "standby":("mandatory", "standby"), "optional":("optional", "")}

    def __init__(self, host='127.0.0.1', port=12185):
        self._host = host
        self._port = port
        self._socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        if _DEBUG :
            print "Connecting to %s:%d"%(self._host, self._port)
            
        self._socket.connect((self._host, self._port))

        if _DEBUG :
            print "Connected"


    def sendMessage(self, command):
        #message = Format % ("monitor", "status")
        if HARPCClient._COMMAND_MAP.has_key(command) :
            _message = HARPCClient.__MSG_FORMAT % HARPCClient._COMMAND_MAP[command]
            if _DEBUG :
                print "Sending message : ", _message
            self._socket.send(_message)
        else :
            raise Exception("Unknown command : " + command)
            

    def readMessage(self, timeout=3):
        if _DEBUG :
            print "Reading message with timeout ", timeout
            
        _socketfile = socketFile.socketFile(self._socket, socketFile.readMode, timeout=timeout)
        _response = pickle.load(_socketfile)
        if not isinstance(_response, Result):
            raise Exception("Invalid response data : "+ _response)
        return _response
    
    def close(self):
        self._socket.close()

_HA_ACTIVE = 0x0400
_HA_STANDBY = 0x4000

def parseStatusCode(response):
    for _item in response:
        if _DEBUG :
            print "Parsing ", _item
            
        if _item[2] == "Own":
            if _DEBUG :
                print "Found Own"

            if _item[3] & _HA_ACTIVE == _HA_ACTIVE :
                return 1
            else :
                return 0
            break
        
    raise Exception("Not found Own element")



class HAAgentX():
        
    def __init__(self, host='127.0.1', port=12185):
        self._client = HARPCClient(host, port)

    def start(self):
        try :
            self._client.connect()
            while 1 : self.readStdin()
        finally :
            self._client.close()

    def readStdin(self) :
        (rr, wr, er) = select([sys.stdin], [], [])
        for fd in rr:
            try :
                line = fd.readline()
                self.processInput(line)
            except Exception:
                sys.exit(-1)

    def processInput (self, line) :
        if 'PING' in line :
            self.playPingPong()
        elif 'get' in line :
            target = sys.stdin.readline()
            self.doGet(target)
        elif 'set' in line :
            target = sys.stdin.readline()
            value = sys.stdin.readline()
            self.doSet(target, value)
        else:
            sys.exit(0)

    def playPingPong (self) :
        print 'PONG'

    def doGet(self, target) :
        _command = "status"
        self._client.sendMessage(_command)
        _response = self._client.readMessage()
        _result = parseStatusCode(_response)
        print target,
        print 'integer'
        print _result

    def doSet(self, target, value) :
        print "ok"
        _command = "deact"
        if string.find(value, _command) > 0 :
            self._client.sendMessage(_command)

def runAgentX():
    _agentx = HAAgentX("127.0.0.1", 22186)
    _agentx.start()
    return 0

