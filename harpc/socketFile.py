import string, socket, select, sys

class CommunicationError(Exception): pass
class CommunicationTimeOut(Exception): pass

def Send(socket, string, flags=0, timeout=10):
    if timeout != None:
        ready = select.select([], [socket], [], timeout)
        if len(ready[1]) == 0:
            raise CommunicationTimeOut, (socket.getpeername()[0],
                                              socket.getsockname()[1])
    return socket.send(string, flags)

def Recv(socket, bufsize, flags=0, timeout=10):
    if timeout != None:
        ready = select.select([socket], [], [], timeout)
        if len(ready[0]) == 0:
            raise CommunicationTimeOut, "read timeout from %s:%d"%(socket.getpeername()[0], socket.getsockname()[1])
    return socket.recv(bufsize, flags)

readMode  = 0
writeMode = 1

class socketFile:
    def __init__(self, sock, mode, init_buffer="", timeout=10):
        self.socket  = sock
        self.buffer  = init_buffer
        self.mode    = mode
        self.timeout = timeout
        self.remainder = ''
        if mode == readMode: self.get()
        
    def write(self, s):
        self.buffer = self.buffer + s
        
    def send(self):
        Send(self.socket, str(len(self.buffer)) + '\0', timeout=self.timeout)
        Send(self.socket, self.buffer, timeout=self.timeout)
        
    def get(self):
        #print 'socketFile : get : buf(%d) : remain(%d)' % (len(self.buffer), len(self.remainder))

        if self.remainder:
            self.buffer = self.buffer + self.remainder
            self.remainder = ''
        length = 0

        while 1:
            if self.buffer:
                pos = string.find(self.buffer, '\0')
                if pos >= 0:
                    length = int(self.buffer[:pos])
                    if length + pos + 1 <= len(self.buffer):
                        self.buffer = self.buffer[pos+1:]
                        self.remainder = self.buffer[length:]
                        self.buffer = self.buffer[:length]
                        return

            data = Recv(self.socket, 1024, timeout=self.timeout)

            if data:
                self.buffer = self.buffer + data
            else:
                raise CommunicationError, "end of connection"
                
    def read(self, i):
        #print 'socketFile : read : %d' % i

        if self.buffer == '':
            self.get()

        val = self.buffer[:i]
        self.buffer = self.buffer[i:]
        #print '\t val(%d) : %s : buf(%d) : %s'     % (len(val), val, len(self.buffer), self.buffer)
        return val
    
    def readline(self):
        #print 'socketFile : readline'
        i = string.find(self.buffer, '\n')
        val = self.buffer[:i+1]
        self.buffer = self.buffer[i+1:]
        #print 'socketFile : val(%d) : %s' % (len(val), val)
        return val

