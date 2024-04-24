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
import importlib

logger=funcGetLogger()


def funcExecMmiRemote(strServerName, strParameter):
    nTotal = 0
    nCurrent = 0
    result = ""
    try:
        strParameter = " " + strParameter
        result = funcExecRemote.funcExecRemote(strServerName, 'DEL-SIP-NODE.py' + strParameter, "all")
    except subprocess.TimeoutExpired as e:
        #logger.error("Command execution timed out : ", e)
        result = "Failed"
    except Exception as e:
        #logger.error("error:", e)
        result = "Failed"

    if "bash" in result:
        result = "Failed"
    elif len(result) < 1:
        result = "Failed"

    nReturnValue = {"server": strServerName, "result": result}

    return nReturnValue 

def funcEmsRole(strParameter):
    listServer = ["CP01", "CP02"]
    data = []
    bExecRemoteResult = False
    strExecRemoteResult = ""
    for strServer in listServer: 
        strServerExecResult = funcExecMmiRemote(strServer, strParameter)
        if "Failed" in strServerExecResult["result"]:
            bExecRemoteResult = False
        else:
            bExecRemoteResult = True
        data.append(strServerExecResult)
        #strCpServerResult = funcExecMmiRemote(strServer)
        #data.append({"server": strServer, "cps": strCpServerResult.strip("\n")})
    print(strExecRemoteResult)
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

def funcCheckValidationRte(dicParameter):

    bResult = True
    listRteId = []
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-RTE.py'], timeout=1)
        strExcuteOutput = output.decode('utf-8')
        listRteId = funcParseDisRte(strExcuteOutput)
        for rte_id in listRteId:
            if rte_id == dicParameter["ID"]:
                return True
    except subprocess.CalledProcessError as e:
        bResult = False
    except subprocess.TimeoutExpired:
        bResult = False

    return bResult

def funcParseDisRmt(strDisRmtResult):
    # 결과를 줄 단위로 분할합니다.
    lines = strDisRmtResult.split('\n')

    # RMT_ID 필드 값을 저장할 리스트를 초기화합니다.
    listRmtId = []

    # 각 줄에서 RMT_ID 필드 값을 찾습니다.
    for line in lines:
        match = re.search(r'\s+(\d+)\s+(\S+)\s', line)
        if match:
            # match.group(1)은 RMT_ID 필드 값을 포함합니다.
            rmt_id_value = match.group(1)
            listRmtId.append(rmt_id_value)

    # RMT_ID 필드 값을 포함하는 리스트를 반환합니다.
    return listRmtId

def funcCheckValidationRmt(dicParameter):
    bResult = True
    listRmtId = []
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-SIP-RMT.py'], timeout=1)
        strExcuteOutput = output.decode('utf-8')
        listRmtId = funcParseDisRmt(strExcuteOutput)
        for rmt_id in listRmtId:
            if rmt_id == dicParameter["ID"]:
                return True

    except subprocess.CalledProcessError as e:
        bResult = False
    except subprocess.TimeoutExpired:
        bResult = False

    return bResult

# not use... DEL 시에는 필요없음.
# DIS-SIP-LOC.py 파일을 실행하여 LOC_ID 값을 리턴한다. 하나만 리턴한다. LOC_ID 두개두지 말것...
def funcGetSipLocId():
    nSipLocId = 0
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-SIP-LOC.py'], timeout=1)
        strExcuteOutput = output.decode('utf-8')
        lines = strExcuteOutput.split('\n')
        for line in lines:
            match = re.search(r'\s+(\d+)\s+(\S+)\s', line)
            if match:
                nSipLocId = match.group(1)
                break
    except subprocess.CalledProcessError as e:
        nSipLocId = 0
    except subprocess.TimeoutExpired:
        nSipLocId = 0

    return nSipLocId


"""
    CRTE-SIP-RMT RMT_ID=13511, NAME=SS_ICSCF_35, DOMAIN=sktims.net, IPV=IP4, IP=172.28.109.145, PORT=5164, PROTOCOL=UDP, NAT_ON=OFF, DSCP=0
    CRTE-RTE RTE=13511, NAME=SS_ICSCF_35, LOC_ID=10001, RMT_ID=13511, TRTE=1, TYPE=MINE, MEDIA=ROUTED, OPT_TIME=5, RETRY=3, ACTION=ACT, SES_TIME=0, GROUP_ID=1, MAX_CNT=100000, DEACT_RSP=SEND
    CRTE-RTE-SEQ RSEQ=13511, NAME=SS_ICSCF_35, DRTE=13511

    listRteId = []
    bResult = False
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-RTE.py'], timeout=1)
        strExcuteOutput = output.decode('utf-8')
        listRteId = funcParseDisRte(strExcuteOutput)
        for rte_id in listRteId:
            logger.info(rte_id)
            subprocess.check_output(['/home/vfras/mmi/CHG-RTE.py', f'RTE={rte_id}, ACTION=DEACT'], timeout=1)
        bResult = True
    except subprocess.CalledProcessError as e:
        bResult = False
    except subprocess.TimeoutExpired:
        bResult = False

    return bResult
"""

def funcExecDelSipRmt(strDelSipRmtParameter):
    bResult = False
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DEL-SIP-RMT.py', strDelSipRmtParameter], timeout=1)
        strExcuteOutput = output.decode('utf-8')

        """ 할 필요 없을듯? GUI는 자동으로 DIS 명령어를 내린다. 따라서 확인할 필요 없다.
        # DIS-SIP-NODE를 import하여 parse_rmt_output함수를 실행한다.
        module_name = 'DIS-SIP-NODE'
        module = importlib.import_module(module_name)
        rmt_data, rmt_count, rmt_result = module.parse_rmt_output(strExcuteOutput)
        # 결과값을 확인한다.
        if "NOK" in rmt_result:
            bResult = False
        else:
            bResult = True
        """
        bResult = True

    except subprocess.CalledProcessError as e:
        bResult = False
    except subprocess.TimeoutExpired:
        bResult = False

    return bResult

def funcExecDelRte(strDelRteParameter):
    bResult = False
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DEL-RTE.py', strDelRteParameter], timeout=1)
        strExcuteOutput = output.decode('utf-8')

        """ 할 필요 없을듯? GUI는 자동으로 DIS 명령어를 내린다. 따라서 확인할 필요 없다.

        # DIS-SIP-NODE를 import하여 parse_rte_output함수를 실행한다.
        module_name = 'DIS-SIP-NODE'
        module = importlib.import_module(module_name)
        rte_data, rte_count, rte_result = module.parse_rte_output(strExcuteOutput)
        
        # 결과값을 확인한다.
        if "NOK" in rte_result:
            bResult = False
        else:
            bResult = True
        """
        bResult = True

    except subprocess.CalledProcessError as e:
        bResult = False
    except subprocess.TimeoutExpired:
        bResult = False

    return bResult
    

# dictionary 형태의 parameter를 받아서 맞는 값인지 validation을 체크하자.
def funcCheckParameterValidation(dicParameter):
    bReturn = True
    # ID, NAME, IP, PORT, PERIOD
    if "ID" not in dicParameter:
        bReturn = False
        print("ID is not in dicParameter")
    """
    if "NAME" not in dicParameter:
        bReturn = False
        print("NAME is not in dicParameter")
    if "IP" not in dicParameter:
        bReturn = False
        print("IP is not in dicParameter")
    if "PORT" not in dicParameter:
        bReturn = False
        print("PORT is not in dicParameter")
    if "PERIOD" not in dicParameter:
        bReturn = False
        print("PERIOD is not in dicParameter")
    # ID는 숫자만 가능하다.
    if not dicParameter["ID"].isdigit():
        return False
    # PORT는 숫자만 가능하다.
    if not dicParameter["PORT"].isdigit():
        return False
    # PERIOD는 숫자만 가능하다.
    if not dicParameter["PERIOD"].isdigit():
        return False
    # NAME은 문자만 가능하다.
    if not dicParameter["NAME"].isalpha():
        return False
    # IP는 숫자와 .만 가능하다.
    if not all(c.isdigit() or c == '.' for c in dicParameter["IP"]):
        return False
    """
    return bReturn

def funcMakeDelSipRmtParameter(dicParameter):
    # 입력예시) DEL-SIP-RMT RMT_ID=13511
    strParameter = f"RMT_ID={dicParameter['ID']}"
    return strParameter

def funcMakeDelRteParameter(dicParameter):
    # 입력예시) DEL-RTE RTE=13511
    strParameter = f"RTE={dicParameter['ID']}"
    return strParameter

def funcServiceRole(dicParameter):
    bServiceRoleFunctionResult = True
    bReturn = False
    strMyServerName = funcGetMyServerName()

    if strMyServerName is not None and "CP" in strMyServerName:
        # DIS-RTE.py 파일을 실행하여 RTE 값과 dicParameter의 ID값이 일치하는지 확인한다.
        bReturn = funcCheckValidationRte(dicParameter)
        if bReturn == False:
            bServiceRoleFunctionResult = False
        
        # DIS-SIP-RMT.py 파일을 실행하여 RMT_ID 값과 dicParameter의 ID값이 일치하는지 확인한다.
        bReturn = funcCheckValidationRmt(dicParameter)
        if bReturn == False:
            bServiceRoleFunctionResult = False
        
        """ DELETE 시에는 확인할 필요 없어서 삭제.
        # DIS-SIP-LOC.py 파일을 실행하여 LOC_ID 값을 확인한다.
        nSipLocId = funcGetSipLocId()
        if int(nSipLocId) < 1:
            bServiceRoleFunctionResult = False
        """

        if (bServiceRoleFunctionResult == True):
            # dicParameter의 값을 이용하여 DEL-SIP-RMT.py 명령어의 parameter String을 만든다.
            strDelSipRmtParameter = funcMakeDelSipRmtParameter(dicParameter)
            # CRTE-SIP-RMT.py 파일을 실행하여 SIP RMT를 생성한다.
            bReturn = funcExecDelSipRmt(strDelSipRmtParameter)
            if bReturn == False:
                bServiceRoleFunctionResult = False
            
            # dicParameter의 값을 이용하여 CRTE-RTE.py 명령어의 parameter String을 만든다.
            strDelSipRteParameter = funcMakeDelRteParameter(dicParameter)
            # DEL-RTE.py 파일을 실행하여 RTE 를 생성한다.
            bReturn = funcExecDelRte(strDelSipRteParameter)
            #print("aaa", strCrteSipRteParameter, bReturn)
            if bReturn == False:
                bServiceRoleFunctionResult = False
    else:
        bServiceRoleFunctionResult = False

    # 결과를 Print하여 EMS 서버에서 알 수 있도록 한다.
    if bServiceRoleFunctionResult == True:
        print("Success")
    else:
        print("Failed")
    return

def funcHelpPrint():
    print("help message")
    print("ex) DEL-SIP-NODE.py ID=10001")
    print("ID는 DIS-RTE.py와 DIS-SIP-RMT.py에서 확인한 ID 값을 입력해야 합니다.")
    
    # Add the implementation of the funcHelpPrint function here
    pass

def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)

    # 입력받은 argument를 string 형태로 저장한다.
    for i in range(1, num_args):
        strParameter += sys.argv[i] + " "
    
    # 실행 예제.
    # DEL-SIP-NODE.py ID=10111 
    # 입력받은 parameter를 dictionary 형태의 변수로 저장한다.
    dicParameter = {}
    for i in range(1, num_args):
        strArg = sys.argv[i]
        strArgList = strArg.split("=")
        dicParameter[strArgList[0]] = strArgList[1]

    # argument 내용을 validation 체크한다.
    bCheckArgument = funcCheckParameterValidation(dicParameter)
    if bCheckArgument == False:
        funcHelpPrint()
        return
    
    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole(strParameter)
    else:
        funcServiceRole(dicParameter)

if __name__ == "__main__":
    main()


