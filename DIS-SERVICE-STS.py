#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcExecRemote
from funcHostName import funcGetMyServerName
from Logger import funcGetLogger

logger=funcGetLogger()

def test():
    now = datetime.datetime.now()

    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    data = [
            {"server": "AS01", "process": "ASFR", "total": 10000, "current": 9999},
            {"server": "AS02", "process": "ASFR", "total": 10000, "current": 9999}
            ]

    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    logger.info(json.dumps(output_data, indent=4))

#strServerName ex)CP01, CP02, AS01, AS ...
#strProcess ex) Myview, ASFR
#strStatus ex) active or all
def funcExecMmiRemote(strServerName, strService, strStatus):
    nTotal = 0
    nCurrent = 0
    strArgument = ""
    if len(strService) > 0:
        strArgument = "service=" + strService
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-SERVICE-STS.py " + strArgument, strStatus)
        if "bash" in result:
            logger.info(result)
            nTotal, nCurrent = 0, 0
        elif len(result) < 1:
            nTotal, nCurrent = 0, 0 
        else:
            dicResult = json.loads(result) 
            nTotal = dicResult['total']
            nCurrent = dicResult['current']
    except Exception as e:
        nTotal, nCurrent = 0, 0 

    nReturnValue = {"server": strServerName, "service": strService, "total": nTotal, "current": nCurrent}

    return nReturnValue 

def funcEmsRole():
    listServer = ["AS01", "AS02", "CP01", "CP02", "DS"]
    listAsService = ["ASFR", "Myview"]
    strServiceName = ""
    #listAsService = ["ASFR", "Myview"]
    data = []
    for strServer in listServer:
        #if AS server then, select Service.
        if "AS" in strServer:
            strServiceName = "ASFR"
            nServerExecResult = funcExecMmiRemote(strServer, strServiceName, "all")
        elif "CP" in strServer:
            strServiceName = "MYVIEW"
            nServerExecResult = funcExecMmiRemote(strServer, strServiceName, "all")
#            for strAsService in listAsService:
#                nServerExecResult = funcExecMmiRemote(strServer, strAsService, "all")
#                data.append(nServerExecResult)
        else:
            strServiceName = "IFSVR"
            nServerExecResult = funcExecMmiRemote(strServer, strServiceName, "active")
        data.append(nServerExecResult)

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    logger.info(output_json)

    return

def funcServiceRole(strRemoteServiceName):
    strMakeData = f'{{"service": "{strRemoteServiceName}", "total": 10000, "current": 9876}}'
 
    #for test.
    logger.info(strMakeData)
    return

def main():
    strParameter = ""
    strRemoteServiceName = ""
    num_args = len(sys.argv)
    if num_args < 2:
        #print("Usage: DIS-SERVICE-STS.py [service=ASFR]    << ex)ASFR, Myview ...")
        pass
    else:
        strParameter = sys.argv[1]

    if "=" in strParameter:
        strParameterName, strParameterValue = strParameter.split('=')
        if strParameterName == "service":
            strRemoteServiceName = strParameterValue
    elif "help" in strParameter:
        funcHelpPrint()
        return
    else:
        strRemoteServiceName = ""

    strMyServerName = funcGetMyServerName()
    if "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole(strRemoteServiceName)

if __name__ == "__main__":
    main()


