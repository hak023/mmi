#!/bin/python2.7

import sys
from harpc.client import *
from Logger import funcGetLogger

logger=funcGetLogger()

_DEBUG = False

def main(argv=None):

    if argv is None:
        argv = sys.argv

    _command = "deact"

    if len(argv) == 5 and argv[1] == "-s":
        _command = argv[4]

    _client = HARPCClient("127.0.0.1", 22186)

    try :
        _client.connect()
        
        if _DEBUG :
            logger.debug(f"Processing command : '{_command}'")

        _client.sendMessage(_command)
        

        if _command == "status" or _command == "proc" or _command == "man" :
            _response = _client.readMessage()
            
            if _DEBUG :
                logger.info(f"Response is '{_response}'")
                
            if _command == "status" :
                logger.info(parseStatusCode(_response))
            else :
                logger.info(f"'{_response}'")
        
        return 0
    except Exception as e:
        logger.erro(e)
	return -1
        
    finally :
        if _DEBUG :
            logger.debug("Closing socket...")
            
        _client.close()
        
        if _DEBUG :
            logger.debug("Closed")

if __name__ == "__main__":
    sys.exit(main())
    #sys.exit(runAgentX())
