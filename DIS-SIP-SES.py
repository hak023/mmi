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
            {"server": "CP01", "total": 10000, "current": 9999},
            {"server": "CP02", "total": 10000, "current": 8888}
            ]

    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    logger.info(json.dumps(output_data, indent=4))


def funcExecMmiRemote(strServerName):
    nTotal = 0
    nCurrent = 0
    try:
        #result = funcExecRemote.funcExecRemote(strServerName,"sam_ps.sh","all")
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-SIP-SES.py","all")
        if "bash" in result:
            nTotal, nCurrent = 0, 0
        elif len(result) < 1:
            nTotal, nCurrent = 0, 0 
        else:
            dicResult = json.loads(result) 
            nTotal = dicResult['total']
            nCurrent = dicResult['current']
    except Exception as e:
        nTotal, nCurrent = 0, 0

    nReturnValue = {"server": strServerName, "total": nTotal, "current": nCurrent}

    return nReturnValue 

def funcEmsRole():
    listServer = ["CP01", "CP02"]
    data = []
    for strServer in listServer: 
        nServerExecResult = funcExecMmiRemote(strServer)
        data.append(nServerExecResult)
        #strCpServerResult = funcExecMmiRemote(strServer)
        #data.append({"server": strServer, "cps": strCpServerResult.strip("\n")})

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    logger.info(output_json)

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
 
    logger.info(strMakeResult)
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


