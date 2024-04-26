#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcDbInfo
from funcHostName import funcGetMyServerName
import funcMmiPrint
from Logger import funcGetLogger
import funcIpcShm
import funcExecRemote

logger=funcGetLogger()

def test():
    now = datetime.datetime.now()

    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    data = [
            ]

    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    json_dumps=json.dumps(output_data, indent=4)
    #logger.info(json_dumps)
    print(json_dumps)

    return

def funcServiceRole(strMyServerName):
    dictionary = {}
    strMakeData = {}
    nTotal, nSuccess = 0, 0
    # strMyServerName 이 AS 인 경우
    if "AS" in strMyServerName:
        dictionary = funcIpcShm.funcReadAsAsfrStatusShm()
        # dictionary 형태의 데이터를 추출하여 strMakeData를 만든다.
        # dictionary 중 Audio_Total 를 가져온다.
        nTotal  = dictionary['Audio_Total'] + dictionary['Video_Total']
        nSuccess = dictionary['Audio_Success'] + dictionary['Video_Success']
    # strMyServerName 이 MYVIEW 인 경우
    elif "CP" in strMyServerName:
        dictionary = funcIpcShm.funcReadCpSvifStatusShm()
        # dictionary 형태의 데이터를 추출하여 strMakeData를 만든다.
        # dictionary 중 Audio_Total 를 가져온다.
        nTotal  = dictionary['Total']
        nSuccess = dictionary['Success']
    # strMyServerName 이 DS 인 경우
    elif "DS" in strMyServerName:
        dictionary = funcIpcShm.funcReadDsIfsyncStatusShm()
        # dictionary 형태의 데이터를 추출하여 strMakeData를 만든다.
        # dictionary 중 Audio_Total 를 가져온다.
        nTotal  = dictionary['Total']
        nSuccess = dictionary['Success']

    strMakeData = f'{{"server": "{strMyServerName}", "total": {nTotal}, "success": {nSuccess}}}'
    #strMakeData = f'{{"server": "{strMyServerName}", "total": 444, "current": 333}}'
 
    #for test.
    #logger.info(strMakeData)
    print(strMakeData)
    return

def funcHelpPrint():
    #nothing work.
    return

# RSTAT 파일을 제공 안한다고 해서 결국 not use. 바로 shm을 봐야함.
# 해당 파일을 실행하여 결과를 리턴함.
def funcExecRstat():
    strExcuteOutput = ""
    strResult = ""
    try:
        output = subprocess.check_output(['/home/vfras/bin/RSTAT'])
        strExcuteOutput = output.decode('utf-8')
        print(strExcuteOutput)
        #logger.info(strExcuteOutput)
        strResult = "success"
    except subprocess.CalledProcessError as e:
        strResult = "fail"
        print(e, " ", strExcuteOutput)
        #logger.error(e, " ", strExcuteOutput)

    return strResult

#strServerName ex)CP01, CP02, AS01, AS ...
#strProcess ex) Myview, ASFR
#strStatus ex) active or all
def funcExecMmiRemote(strServerName, strService, strStatus):
    nTotal = 0
    nSuccess = 0
    strArgument = ""
    if len(strService) > 0:
        strArgument = "service=" + strService
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-RSTAT.py " + strArgument, strStatus)
        if "bash" in result:
            #logger.info(result)
            print(result)
            nTotal, nSuccess = 0, 0
        elif len(result) < 1:
            nTotal, nSuccess = 0, 0 
        else:
            dicResult = json.loads(result) 
            nTotal = dicResult['total']
            nSuccess = dicResult['success']
    except Exception as e:
        nTotal, nSuccess = 0, 0 

    nReturnValue = {"server": strServerName, "service": strService, "total": nTotal, "success": nSuccess}

    return nReturnValue 

def funcEmsRole():
    listServer = ["AS00", "AS01", "CP00", "CP01", "DS00"]
    #listAsService = ["ASFR", "Myview"]
    strServiceName = ""
    strServerAndService = ""
    data = []
    nSuccessRate = 0.0
    print("%s %s %s" % ("FRAS", "SERVICE", "STATISTICS"))
    print("----------------------------")
    for strServer in listServer:
        now = datetime.datetime.now()
        #if AS server then, select Service.
        if "AS" in strServer:
            strServiceName = "ASFR"
            dicServerExecResult = funcExecMmiRemote(strServer, strServiceName, "all")
        elif "CP" in strServer:
            strServiceName = "MYVIEW"
            dicServerExecResult = funcExecMmiRemote(strServer, strServiceName, "all")
        elif "DS" in strServer:
            strServiceName = "IFSVR"
            dicServerExecResult = funcExecMmiRemote(strServer, strServiceName, "active")
        strServerAndService = strServer + "-" + strServiceName
        # 성공율을 %로 계산하자.
        if dicServerExecResult['total'] > 0:
            nSuccessRate = round((dicServerExecResult['success'] / dicServerExecResult['total']) * 100, 1)
        else:
            nSuccessRate = 0
        #formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
        formatted_time = now.strftime("%Y%m%d%H%M%S")
        #print("%-16s, REQUEST=%-8d, SUCCESS=%-8d, SUCCESSRATE=%-8.1f, TIME=%-16s" % (strServerAndService, dicServerExecResult['total'], dicServerExecResult['success'], nSuccessRate, formatted_time))
        print("%-16s, REQUEST=%d, SUCCESS=%d, SUCCESSRATE=%.1f, TIME=%-16s" % (strServerAndService, dicServerExecResult['total'], dicServerExecResult['success'], nSuccessRate, formatted_time))

    return

def main():
    strParameter = ""
    strRemoteServiceName = ""
    num_args = len(sys.argv)

    # sys.argv에 py 문자열이 없을 경우 mmi print를 실행합니다.
    bMmiPrint = True
    if ".py" in sys.argv[0]:
        bMmiPrint = False
    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrint(sys.argv)

    if num_args < 2:
        #print("Usage: DIS-SERVICE-STS.py [service=ASFR]    << ex)ASFR, Myview ...")
        pass
    else:
        strParameter = sys.argv[1]

    if "help" in strParameter:
        funcHelpPrint()

        if bMmiPrint == True:
            funcMmiPrint.funcMmiPrintComplete()
        return

    strMyServerName = funcGetMyServerName()
    if "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole(strMyServerName)

    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrintComplete()

    return

if __name__ == "__main__":
    main()


