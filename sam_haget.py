#!/bin/python2.7

import sys
from harpc.client import *
from Logger import funcGetLogger

logger=funcGetLogger()

_DEBUG = False

def main(argv=None):

    if argv is None:
            argv = sys.argv

    _command = "status"

    if len(argv) == 5 and argv[1] == "-s":
        _command = argv[4]

    _client = HARPCClient("localhost", 22186)

    try :
        _client.connect()
        
        if _DEBUG :
            #logger.info( "Processing command : ", _command)
            print( "Processing command : ", _command)

        _client.sendMessage(_command)
        
        if _command == "status" or _command == "proc" or _command == "man" :
            _response = _client.readMessage()
            
            if _DEBUG :
                #logger.info( "Response is ", _response)
                print( "Response is ", _response)
                
            if _command == "status" :
                #logger.info(parseStatusCode(_response))
                print(parseStatusCode(_response))
            else :
                _command _response
        
        return 0
    except Exception as e:
        #logger.error( e)
        print(e)
	return -1
        
    finally :
        if _DEBUG :
            #logger.info( "Closing socket...")
            print( "Closing socket...")
            
        _client.close()
        
        if _DEBUG :
            #logger.info( "Closed")
            print( "Closed")

if __name__ == "__main__":
    sys.exit(main())
    #sys.exit(runAgentX())
