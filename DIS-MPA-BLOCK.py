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

import funcMmiPrint

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

                # 변수를 출력합니다.
                logger.info(mpa_code)
    except FileNotFoundError:
        logger.info(f"{file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        logger.info(f"{file_path} 파일을 읽을 권한이 없습니다.")
    except Exception as e:
        logger.info(f"파일 처리 중 에러가 발생했습니다: {e}")
    return

def funcDataBlockProcess(strMpaBlockConfig):
    # string 형태의 strMpaBlockConfig을 line마다 읽어서 data에 있는 딕셔너리의 'code' 키와 비교하여 같은 딕셔너리를 찾습니다.
    for line in strMpaBlockConfig.splitlines():
        mpa_code = line.strip()
        for item in data:
            if item['code'] == mpa_code:
                # 'block': 'on' 필드를 추가합니다.
                item['block'] = 'BLOCKED'
                break
    return  
   
def funcMpaBlockPrint():
    # MPA BLOCK을 출력합니다.
    logger.info("%-16s %-16s %-16s %-16s" % ("ID", "SERVER", "MPA", "STATUS"))
    logger.info("------------------------------------------------------------------")
    for item in data:
        logger.info("%-16s %-16s %-16s %-16s" % (item['id'], item['server'], item['name'], item['block']))
    return

def funcGetMpaBlockItem():
    # 'block'이 'on'인 딕셔너리를 찾습니다.
    block_on_items = [item for item in data if item.get('block') == 'BLOCKED']

    return block_on_items

def funcExecMmiRemote(strServerName):
    nTotal = 0
    nCurrent = 0
    result = ""
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-MPA-BLOCK.py","active")
        if "bash" in result:
            logger.error("error: ", result)
        elif len(result) < 1:
            logger.error("error: ", result)
        else:
            # nothing work.
            pass
    except Exception as e:
        logger.error("error: ", e)

    return result

def funcEmsRole():
    # MPA BLOCK을 처리하기 위한 기초 데이터를 만든다.
    funcDataInitialize()
    

    listServer = ["AS01"]
    strMpaBlockConfig = ""
    for strServer in listServer: 
        strMpaBlockConfig = funcExecMmiRemote(strServer)

    funcDataBlockProcess(strMpaBlockConfig) 
    
    funcMpaBlockPrint()
    

    return

def funcServiceRole():
    # MPA BLOCK 파일을 읽어서 기초 데이터에 업데이트한다.
    funcReadMpBlockFile()
    #block이 on인 딕셔너리를 return한다.
    #dicMpaBlockItem = funcGetMpaBlockItem()
    #print("%s %s %s" % ("ID", "SERVER", "PROCESS"))
    #print("------------------------------------------------------------------")
    #print("test:", dicMpaBlockItem)
    return 


def funcHelpPrint():
    # Add the implementation of the funcHelpPrint function here
    pass

def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)

    # sys.argv에 py 문자열이 있을 경우만 mmi 관련 내용을 print하지 말자.
    bMmiPrint = True
    if ".py" in sys.argv[0]:
        bMmiPrint = False
    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrint(sys.argv)
    
    if num_args < 2:
        #print("Usage: DIS-CPS.py [servername=CP]    << ex)CP, CP01, AS, AS01, AS02 ...")
        pass
    else:
        strParameter = sys.argv[1]

    if "help" in strParameter:
        funcHelpPrint()

        if bMmiPrint == True:
            funcMmiPrint.funcMmiPrintComplete()
        return

    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole()

    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrintComplete()

if __name__ == "__main__":
    main()


