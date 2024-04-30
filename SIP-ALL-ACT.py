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

    json_dumps = json.dumps(output_data, indent=4)
    #logger.info(json_dumps)
    print(json_dumps)


def funcExecMmiRemote(strServerName):
    nTotal = 0
    nCurrent = 0
    result = ""
    strParameter = " SERVER=" + strServerName
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"SIP-ALL-ACT.py" + strParameter,"all")
    except subprocess.TimeoutExpired as e:
        #logger.error("Command execution timed out : ", e)
        print("Command execution timed out : ", e)
        result = "Failed"
    except Exception as e:
        #logger.error(e)
        print(e)
        result = "Failed"

    if "bash" in result:
        result = "Failed"
    elif len(result) < 1:
        result = "Failed"

    nReturnValue = {"server": strServerName, "result": result}

    return nReturnValue 

def funcEmsRole(strRemoteServerName):
    listServer = ["CP00", "CP01"]

    #listServer 에서 문자열 검색하여 strRemoteServerName가 존재하는지 확인한다.
    if strRemoteServerName not in listServer:
        #logger.error(f"impossible server name : {strRemoteServerName}")
        print(f"impossible server name : {strRemoteServerName}")
        return


    data = []
    bExecRemoteResult = False
    strExecRemoteResult = ""
    strServerExecResult = funcExecMmiRemote(strRemoteServerName)
    if "Failed" in strServerExecResult["result"]:
        bExecRemoteResult = False
    else:
        bExecRemoteResult = True
    data.append(strServerExecResult)

    if bExecRemoteResult == True:
        strExecRemoteResult = "Success"
    else:
        strExecRemoteResult = "Failed"

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"result": strExecRemoteResult})

    output_json = json.dumps(output_data, indent=4)
    #logger.info(output_json)
    print(output_json)

    return

def funcParseDisRte(strDisRteResult):
    # 결과를 줄 단위로 분할합니다.
    lines = strDisRteResult.split('\n')

    # RTE 필드 값을 저장할 리스트를 초기화합니다.
    listRteId = []

    # 각 줄에서 RTE 필드 값을 찾습니다.
    for line in lines:
        match = re.search(r'\s+(\d+)\s+(\S+)\s', line)
        if match:
            # match.group(1)은 RTE 필드 값을 포함합니다.
            rte_value = match.group(1)
            listRteId.append(rte_value)

    # RTE 필드 값을 포함하는 리스트를 반환합니다.
    return listRteId

def funcRteSetAllDeact():
    listRteId = []
    bResult = False
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-RTE.py'], timeout=1)
        strExcuteOutput = output.decode('utf-8')
        listRteId = funcParseDisRte(strExcuteOutput)
        for rte_id in listRteId:
            subprocess.check_output(['/home/vfras/mmi/CHG-RTE.py', f'RTE={rte_id}, ACTION=ACT'], timeout=1)
        bResult = True
    except subprocess.CalledProcessError as e:
        bResult = False
    except subprocess.TimeoutExpired:
        bResult = False

    return bResult

def funcServiceRole():
    bReturn = False
    strMyServerName = funcGetMyServerName()

    # DIS-SIP-ENV.py check.
    if strMyServerName is not None and "CP" in strMyServerName:
        bReturn = funcRteSetAllDeact()
    if bReturn:
        print("Success")
    else:
        print("Failed")
    return

def funcHelpPrint():
    print("SIP-ALL-ACT.py help page.")
    print("Usage ex) SIP-ALL-ACT.py SERVER=CP01")
    # Add the implementation of the funcHelpPrint function here
    pass

def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)

    if num_args < 2:
        #print("Usage: DIS-SERVICE-STS.py [service=ASFR]    << ex)ASFR, Myview ...")
        pass
    else:
        strParameter = sys.argv[1]
    strParameter.upper()

    if "=" in strParameter:
        strParameterName, strParameterValue = strParameter.split('=')
        if strParameterName == "SERVER":
            strRemoteServerName = strParameterValue
        else:
            funcHelpPrint()
            return
        
        # strParameterValue 에 아무것도 없을때.
        if len(strParameterValue) < 1 :
            funcHelpPrint()
            return
    else:
        funcHelpPrint()
        return
    
    if "help" in strParameter:
        funcHelpPrint()
        return

    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole(strRemoteServerName)
    else:
        funcServiceRole()

if __name__ == "__main__":
    main()


