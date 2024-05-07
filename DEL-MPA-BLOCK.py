#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcExecRemote
from funcHostName import funcGetMyServerName
import re
import importlib
import funcMmiPrint
from Logger import funcGetLogger

logger=funcGetLogger()

# 파일 경로
file_path = "/home/vfras/config/MPRM/mp_block.cmd"
data = []

def funcDataInitialize():
    nId = 1
    # 기초데이터. 서버명, MPA명, 코드를 포함합니다.
    for i in range(1, 9):
        for j in range(1, 9):
            data.append({"id": f"{nId}", "server": f"MS{i:02d}", "name": f"MPA{j}", "code": f"0x4{i-1:02d}{j-1}", "block": "UNBLOCKED"})
            nId += 1
    return

def funcReadMpBlockFile():
    try:
        # 파일을 열고 한 줄씩 읽습니다.
        with open(file_path, 'r') as file:
            for line in file:
                # 각 줄의 값을 변수로 저장합니다.
                mpa_code = line.strip()
                # mpa_code를 data 변수에 update함.
                funcDataBlockProcessForOneLine(mpa_code)
    except FileNotFoundError:
        print(f"{file_path} 파일을 찾을 수 없습니다.")
        #logger.error(f"{file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        print(f"{file_path} 파일을 읽을 권한이 없습니다.")
        #logger.error(f"{file_path} 파일을 읽을 권한이 없습니다.")
    except Exception as e:
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
        #logger.error(f"파일 처리 중 에러가 발생했습니다: {e}")
    return

# strId ex) 1,3,22
def funcAddMpUnBlockToFile(strId):
    try:
        # strId를 ','로 split하고 공백을 삭제하여 리스트로 만듭니다.
        id_list = [id.strip() for id in strId.split(',')]
        strMyServerName = funcGetMyServerName()

        # id_list를 data에 unblock 체크하여 업데이트합니다.
        for id in id_list:
            for item in data:
                if item['id'] == id:
                    print(f"SERVER = {strMyServerName}  ID = {item['id']}    {item['block']} -> UNBLOCKED")
                    item['block'] = 'UNBLOCKED'
                    break

        # 파일을 열고 data에서 block='BLOCKED' 인 code 값을 찾아 파일에 쓰기합니다.
        with open(file_path, 'w') as file:
            for item in data:
                if item['block'] == 'BLOCKED':
                    file.write(f"{item['code']}\n")

    except FileNotFoundError:
        print(f"{file_path} 파일을 찾을 수 없습니다.")
        #logger.error(f"{file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        print(f"{file_path} 파일을 작성할 권한이 없습니다.")
        #logger.error(f"{file_path} 파일을 작성할 권한이 없습니다.")
    except Exception as e:
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
        #logger.error(f"파일 처리 중 에러가 발생했습니다: {e}")
    return

def funcDataBlockProcessForOneLine(strMpaBlockConfigOneLine):
    # string 형태의 strMpaBlockConfigOneLine를 읽어서 data에 있는 딕셔너리의 'code' 키와 비교하여 같은 딕셔너리를 찾습니다.
    mpa_code = strMpaBlockConfigOneLine.strip()
    for item in data:
        if item['code'] == mpa_code:
            # 'block': 'BLCCKED' 필드를 추가합니다.
            item['block'] = 'BLOCKED'
            break
    return  

def funcDataBlockProcessForAllLine(strMpaBlockConfig):
    # string 형태의 strMpaBlockConfig을 line마다 읽어서 data에 있는 딕셔너리의 'code' 키와 비교하여 같은 딕셔너리를 찾습니다.
    for line in strMpaBlockConfig.splitlines():
        mpa_code = line.strip()
        for item in data:
            if item['code'] == mpa_code:
                # 'block': 'on' 필드를 추가합니다.
                item['block'] = 'BLOCKED'
                break
    return  

"""   
def funcMpaBlockPrint():
    # MPA BLOCK을 출력합니다.
    print("%-16s %-16s %-16s %-16s" % ("ID", "SERVER", "MPA", "STATUS"))
    print("------------------------------------------------------------------")
    for item in data:
        print("%-16s %-16s %-16s %-16s" % (item['id'], item['server'], item['name'], item['block']))
    return

def funcGetMpaBlockItem():
    # 'block'이 'on'인 딕셔너리를 찾습니다.
    block_on_items = [item for item in data if item.get('block') == 'BLOCKED']

    return block_on_items
"""

def funcExecMmiRemote(strServerName, strParameter):
    nTotal = 0
    nCurrent = 0
    result = ""
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DEL-MPA-BLOCK.py " + strParameter, "all")
        if "bash" in result:
            print(strServerName, " bash error occured! ", result)
            #logger.error("error: ", result)
        elif len(result) < 1:
            # nothing work.
            pass
        else:
            print(result)
            # nothing work.
            pass
    except Exception as e:
        print(f"error: {e}") 
        #logger.error(f"error: {e}") 
    return result

def funcDisMpaBlock():
    #call DIS-HA
    module_name = 'DIS-MPA-BLOCK'
    module = importlib.import_module(module_name)
    module.funcEmsRole()
    return

# strParameter ex) ID=1,3,22
def funcEmsRole(strParameter):
    # MPA BLOCK을 처리하기 위한 기초 데이터를 만든다.
    funcDataInitialize()
    
    # active/standby 모두 바꾸자. 그게 맞다.
    listServer = ["AS00", "AS01"]
    #listServer = ["AS00"]
    strMpaBlockConfig = ""
    for strServer in listServer: 
        funcExecMmiRemote(strServer, strParameter)

    #funcDataBlockProcessForAllLine(strMpaBlockConfig) 

    # 마지막에 DIS-MPA-BLOCK을 해서 작업이 잘 됐는지 확인하게 하자.
    funcDisMpaBlock()
    #funcMpaBlockPrint()

    return

# strId ex) 1,3,22
def funcServiceRole(strId):
    # MPA BLOCK을 처리하기 위한 기초 데이터를 만든다.
    funcDataInitialize()
    # MPA BLOCK을 읽어서 data에 update한다.
    funcReadMpBlockFile()

    # 입력받은 strId를 이용하여 파일을 읽어서 mp_block.cmd에 업데이트한다.
    funcAddMpUnBlockToFile(strId)
    #block이 on인 딕셔너리를 return한다.
    #dicMpaBlockItem = funcGetMpaBlockItem()
    #print("%s %s %s" % ("ID", "SERVER", "PROCESS"))
    #print("------------------------------------------------------------------")
    #print("test:", dicMpaBlockItem)
    return 


def funcHelpPrint():
    # Add the implementation of the funcHelpPrint function here
    print("Write Argument ID")
    print("ex) DEL-MPA-BLOCK ID=1")
    print("ex) DEL-MPA-BLOCK ID=1,3,22")
    print("ID LIST refer to DIS-MPA-BLOCK") 
    return

def main():
    strParameter = ""
    strId = ""
    num_args = len(sys.argv)

    # sys.argv에 py 문자열이 없을 경우 mmi print를 실행합니다.
    bMmiPrint = True
    if ".py" in sys.argv[0]:
        bMmiPrint = False
    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrint(sys.argv)
    if num_args < 2:
        pass
    else:
        strParameter = sys.argv[1]
    strParameter.upper()

    if "=" in strParameter:
        strParameterName, strParameterValue = strParameter.split('=')
        # strParameterValue를 ','로 split하고, 각 요소의 앞뒤 공백을 제거한 후, 그 결과를 list_values 변수에 저장합니다.
        list_values = [value.strip() for value in strParameterValue.split(',')]
        
        if strParameterName == "ID":
            strId = strParameterValue
        else:
            funcHelpPrint()
            if bMmiPrint == True:
                funcMmiPrint.funcMmiPrintComplete()
            return

        # list_value가 1개이며 숫자가 아닐 경우 도움말을 print하고, return하자. ex) ID=
        if len(list_values) == 1 and not list_values[0].isdigit():
            funcHelpPrint()
            if bMmiPrint == True:
                funcMmiPrint.funcMmiPrintComplete()
            return


    else:
        funcHelpPrint()
        if bMmiPrint == True:
            funcMmiPrint.funcMmiPrintComplete()
        return 

    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole(strParameter)
    else:
        funcServiceRole(strId)

    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrintComplete()

    return

if __name__ == "__main__":
    main()


