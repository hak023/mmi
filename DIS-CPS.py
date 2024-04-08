#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcExecRemote
from funcHostName import funcGetMyServerName
import re

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

    print(json.dumps(output_data, indent=4))


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
    print(output_json)

    return

def funcParseDisSipEnvCps(strDisSipEnvResult):
    strTotal = ""
    strCurrent = ""
    matchFindSession = re.search(r'CPS\(Number\)\s+(\d+)\s+(\d+)', strDisSipEnvResult)
    if matchFindSession:
        strCurrent = matchFindSession.group(1)
        strTotal = matchFindSession.group(2)
    #dicResult = {"total": int(strTotal), "current": int(strCurrent)}
    #output_json = json.dumps(dicResult, indent=4)
    #return output_json
    return strCurrent

def funcGetSipSessionCps():
    strExcuteOutput = ""
    nCps = 0
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-SIP-ENV.py'])
        strExcuteOutput = output.decode('utf-8')
        strResult = funcParseDisSipEnvCps(strExcuteOutput)
        nCps = int(strResult)
    except subprocess.CalledProcessError as e:
        nCps = 0

    return nCps 

def funcServiceRole():
    strMakeResult = ""
    strMyServerName = funcGetMyServerName()
    nCps = 0

    #DIS-SIP-ENV.py check.
    if "CP" in strMyServerName:
        nCps = funcGetSipSessionCps()
    #shm check. temporary
    else:
        #for test.
        nCps = 88

    print(nCps)
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


