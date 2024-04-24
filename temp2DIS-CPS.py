#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcExecRemote
from funcHostName import funcGetMyServerName
import re
from Logger import funcGetLogger

logger=funcGetLogger()

def test():
    now = datetime.datetime.now()

    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")

    data = [
            {"server": "CP01", "cps": 9},
            {"server": "CP02", "cps": 88},
            {"server": "AS01", "cps": 77},
            {"server": "AS02", "cps": 33},
            {"server": "DS", "cps": 66}
            ]

    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    json_dumps = json.dumps(output_data, indent=4)
    #logger.info(json_dumps)
    print(json_dumps)

def funcExecMmiRemote(strServerName):
    nReturnValue = 0
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-CPS.py","active")
        if "bash" in result:
            result = "0"
        elif len(result) < 1:
            result = "0"
        nReturnValue = int(result)
    except Exception as e:
        nReturnValue = 0
    return nReturnValue 

def funcEmsRole():
    listServer = ["CP01", "CP02", "AS01", "AS02", "DS"]
    data = []
    for strServer in listServer: 
        nServerExecResult = funcExecMmiRemote(strServer)
        data.append({"server": strServer, "cps": nServerExecResult})
        #strCpServerResult = funcExecMmiRemote(strServer)
        #data.append({"server": strServer, "cps": strCpServerResult.strip("\n")})

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    #logger.info(output_json)
    print(output_json)

    return

def funcParseDisSipEnv(strDisSipEnvResult):
    strTotal = ""
    strCurrent = ""
    matchFindSession = re.search(r'SES\(Number\)\s+(\d+)\s+(\d+)', strDisSipEnvResult)
    if matchFindSession:
        strCurrent = matchFindSession.group(1)
        strTotal = matchFindSession.group(2)
    dicResult = {"total": int(strTotal), "current": int(strCurrent)}
    output_json = json.dumps(dicResult, indent=4)
    return output_json

def funcGetSipSession():
    strExcuteOutput = ""
    dicMakeResult = {}
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-SIP-ENV.py'])
        strExcuteOutput = output.decode('utf-8')
        dicMakeResult = funcParseDisSipEnv(strExcuteOutput)
    except subprocess.CalledProcessError as e:
        dicMakeResult = '{"total": 0, "current": 0, "error": e}'

    return dicMakeResult

def funcServiceRole():
    strMakeResult = ""
    strMyServerName = funcGetMyServerName()

    #DIS-SIP-ENV.py check.
    if "CP" in strMyServerName:
        strMakeResult = funcGetSipSession()
    #shm check. temporary
    else:
        #for test.
        strMakeResult = '{"total": 10000, "current": 9876}'

    #logger.info(strMakeResult)
    print(strMakeResult)
    return

    #for test.
    print(88)
    return

def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)
    if num_args < 2:
        #print("Usage: DIS-CPS.py [servername=CP]    << ex)CP, CP01, AS, AS01, AS02 ...")
        pass
    else:
        strParameter = sys.argv[1]

    if "help" in strParameter:
        funcHelpPrint()
        return

    strMyServerName = funcGetMyServerName()
    if "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole()

if __name__ == "__main__":
    main()


