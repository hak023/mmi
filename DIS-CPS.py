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

    logger.info(json.dumps(output_data, indent=4))

# funcExecMmiRemote 함수는 주어진 서버 이름에 대해 원격으로 MMI 명령을 실행합니다.
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

# funcEmsRole 함수는 각 서버에 대해 MMI 명령을 실행하고 결과를 JSON 형식으로 출력합니다.
def funcEmsRole():
    listServer = ["CP01", "CP02", "AS01", "AS02", "DS"]
    data = []
    for strServer in listServer: 
        nServerExecResult = funcExecMmiRemote(strServer)
        data.append({"server": strServer, "cps": nServerExecResult})

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    logger.info(output_json)

    return

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
def funcServiceRole():
    strMakeResult = ""
    strMyServerName = funcGetMyServerName()
    nCps = 0

    #DIS-SIP-ENV.py check.
    if strMyServerName is not None and "CP" in strMyServerName:
        nCps = funcGetSipSessionCps()
    #shm check. temporary
    else:
        #for test.
        nCps = 88

    logger.info(nCps)
    return

# main 함수는 프로그램의 주 실행 루틴입니다.
def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)
    if num_args < 2:
        pass
    else:
        strParameter = sys.argv[1]

    if "help" in strParameter:
        funcHelpPrint()
        return

    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole()

# 스크립트가 직접 실행되는 경우 main 함수를 호출합니다.
if __name__ == "__main__":
    main()
