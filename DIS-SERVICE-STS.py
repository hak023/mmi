#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcExecRemote
from funcHostName import funcGetMyServerName
from Logger import funcGetLogger
import funcIpcShm

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

    json_dumps=json.dumps(output_data, indent=4)
    #logger.info(json_dumps)
    print(json_dumps)

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
            #logger.info(result)
            print(result)
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
    listServer = ["AS00", "AS01", "CP00", "CP01", "DS"]
    #listAsService = ["ASFR", "Myview"]
    strServiceName = ""
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
        elif "DS" in strServer:
            strServiceName = "IFSVR"
            nServerExecResult = funcExecMmiRemote(strServer, strServiceName, "active")
        data.append(nServerExecResult)

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    #logger.info(output_json)
    print(output_json)

    return

def funcServiceRole(strRemoteServiceName):
    dictionary = {}
    strMakeData = {}
    nTotal, nSuccess = 0, 0
    # strRemoteServiceName 이 ASFR 인 경우
    if "ASFR" in strRemoteServiceName:
        dictionary = funcIpcShm.funcReadAsAsfrStatusShm()
        # dictionary 형태의 데이터를 추출하여 strMakeData를 만든다.
        # dictionary 중 Audio_Total 를 가져온다.
        nTotal  = dictionary['Audio_Total'] + dictionary['Video_Total']
        nSuccess = dictionary['Audio_Success'] + dictionary['Video_Success']
    # strRemoteServiceName 이 MYVIEW 인 경우
    elif "MYVIEW" in strRemoteServiceName:
        dictionary = funcIpcShm.funcReadCpSvifStatusShm()
        # dictionary 형태의 데이터를 추출하여 strMakeData를 만든다.
        # dictionary 중 Audio_Total 를 가져온다.
        nTotal  = dictionary['Total']
        nSuccess = dictionary['Success']
    # strRemoteServiceName 이 IFSVR 인 경우
    elif "IFSVR" in strRemoteServiceName:
        dictionary = funcIpcShm.funcReadDsIfsyncStatusShm()
        # dictionary 형태의 데이터를 추출하여 strMakeData를 만든다.
        # dictionary 중 Audio_Total 를 가져온다.
        nTotal  = dictionary['Total']
        nSuccess = dictionary['Success']

    strMakeData = f'{{"service": "{strRemoteServiceName}", "total": {nTotal}, "current": {nSuccess}}}'
 
    #for test.
    #logger.info(strMakeData)
    print(strMakeData)
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


