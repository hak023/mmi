#!/bin/python3 -tt
# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
import datetime
import json
import sys
import subprocess
import funcExecRemote
from funcHostName import funcGetMyServerName
import re
from Logger import funcGetLogger
import funcIpcShm

logger=funcGetLogger()

# test 함수는 현재 시간을 가져와서 서버의 cps 값을 포함하는 JSON 객체를 출력합니다.
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

# funcExecMmiRemote 함수는 주어진 서버 이름에 대해 원격으로 MMI 명령을 실행합니다.
def funcExecMmiRemote(strServerName, strParameter):
    nReturnValue = 0
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-CPS.py " + strParameter, "active")
        if "bash" in result:
            result = "0"
        elif len(result) < 1:
            result = "0"
        nReturnValue = int(result)
    except Exception as e:
        nReturnValue = 0
    return nReturnValue 

# funcEmsRole 함수는 각 서버에 대해 MMI 명령을 실행하고 결과를 JSON 형식으로 출력합니다.
def funcEmsRole():
    listServer = ["CP00", "CP01", "DS00"]
    listCpServerType = ["SIP", "MYVIEW"]
    listDsServerType = ["IFSYNC"]
    data = []
    strParameter = ""
    for strServer in listServer: 
        if "CP" in strServer:
            for strType in listCpServerType:
                strParameter = "type=" + strType
                nServerExecResult = funcExecMmiRemote(strServer, strParameter)
                data.append({"server": strServer, "type": strType, "cps": nServerExecResult})
        elif "DS" in strServer:
            for strType in listDsServerType:
                strParameter = "type=" + strType
                nServerExecResult = funcExecMmiRemote(strServer, strParameter)
                data.append({"server": strServer, "type": strType, "cps": nServerExecResult})

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    #logger.info(output_json)
    print(output_json)

    #return output_json

# funcParseDisSipEnvCps 함수는 DIS-SIP-ENV.py 스크립트의 출력에서 CPS 값을 추출합니다.
def funcParseDisSipEnvCps(strDisSipEnvResult):
    strTotal = ""
    strCurrent = ""
    matchFindSession = re.search(r'CPS\(Number\)\s+(\d+)\s+(\d+)', strDisSipEnvResult)
    if matchFindSession:
        strCurrent = matchFindSession.group(1)
        strTotal = matchFindSession.group(2)
    return strCurrent

# funcGetSipSessionCps 함수는 DIS-SIP-ENV.py 스크립트를 실행하고 CPS 값을 반환합니다.
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

# funcServiceRole 함수는 서버의 역할에 따라 CPS 값을 계산하고 출력합니다.
def funcServiceRole(strParameter):
    strMakeResult = ""
    strMyServerName = funcGetMyServerName()
    nCps = 0

    #DIS-SIP-ENV.py check.
    if strMyServerName is not None and "CP" in strMyServerName and "SIP" in strParameter:
        nCps = funcGetSipSessionCps()
    elif strMyServerName is not None and "CP" in strMyServerName and "MYVIEW" in strParameter:
        dictSvif = funcIpcShm.funcReadCpSvifStatusShm()
        nCps = int(dictSvif["cps"])
    elif strMyServerName is not None and "DS" in strMyServerName and "IFSYNC" in strParameter:
        dictIfsync = funcIpcShm.funcReadDsIfsyncStatusShm()
        nCps = int(dictIfsync["cps"])

    #logger.info(nCps)
    print(nCps)
    return

def funcHelpPrint():
    print("DIS-CPS.py is a script that calculates the CPS value of the server.")
    print("If EMS Excute, no parameter")
    print("If other Excute, please write parameter TYPE.")
    print("ex) DIS-CPS.py type=SIP / DIS-CPS.py type=MYVIEW / DIS-CPS.py type=IFSYNC")
    return

# main 함수는 프로그램의 주 실행 루틴입니다.
def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)

    # 입력받은 argument를 string 형태로 저장한다.
    for i in range(1, num_args):
        strParameter += sys.argv[i] + " "
    strParameter.upper()

    if "help" in strParameter:
        funcHelpPrint()
        return

    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole(strParameter)

# 스크립트가 직접 실행되는 경우 main 함수를 호출합니다.
if __name__ == "__main__":
    main()
