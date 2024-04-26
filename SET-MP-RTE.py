#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcExecRemote
from funcHostName import funcGetMyServerName
import re

import funcMmiPrint

# 파일 경로
file_path = "/home/vfras/config/MPRM/mp_routing.cmd"
data = []


# server와 module을 넣으면 code를 return한다.
def funcGetCode(strServer, strModule):
    listMpRouteStructure = []
    # 기초데이터. 서버명, MPA명, 코드를 포함합니다.
    for i in range(1, 9):
        for j in range(1, 9):
            listMpRouteStructure.append({"server": f"MS{i:02d}", "module": f"MPA{j}", "code": f"0x4{i-1:02d}{j-1}"})

    # listMpRouteStructure에서 server와 name이 일치하는 객체를 찾는다.
    for item in listMpRouteStructure:
        if item['server'] == strServer and item['module'] == strModule:
            return item['code']
    return ""


def funcReadMpRouteFile():
    strMpRouteFile = ""
    try:
        # 파일을 열고 한 줄씩 읽습니다.
        with open(file_path, 'r') as file:
            for line in file:
                # 각 줄의 값을 변수로 저장합니다.
                mp_route_config = line.strip()

                # 만약 mp_route_config가 #으로 시작한다면.
                if mp_route_config.startswith("#"):
                    # 주석이므로 출력하지 않습니다.
                    continue
                #strMpRouteFile에 mp_route_config를 추가합니다.
                strMpRouteFile += mp_route_config + "\n"
    except FileNotFoundError:
        print(f"{file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        print(f"{file_path} 파일을 읽을 권한이 없습니다.")
    except Exception as e:
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
    return strMpRouteFile

# config를 읽어서 내부 data에 저장한다.
def funcMpRouteProcess(strMpRouteConfig):
    id = 1
    # string 형태의 strMpaBlockConfig을 line마다 읽어서 data에 있는 딕셔너리의 'code' 키와 비교하여 같은 딕셔너리를 찾습니다.
    for line in strMpRouteConfig.splitlines():
        strOneLineConfig = line.strip()
        try:
            # strOneLineConfig를 ,로 split하여 각각의 변수에 저장한다.
            mdn, server, module, mpa_code = strOneLineConfig.split(',')
            # 분리된 각 부분을 딕셔너리로 만든다.
            dicItem = {"mdn": mdn, "server": server, "module": module}
            mpa_code = funcGetCode(dicItem['server'], dicItem['module'])
            # 딕셔너리에 id와 code를 추가한다.
            dicItem.update({"id": id, "code": mpa_code})
            # id는 고유하게 1개씩 증가. 
            id = id + 1
            
            # 딕셔너리를 data 리스트에 추가한다.
            data.append(dicItem)
        except ValueError:
            # strOneLineConfig에 ,가 부족하여 분리된 부분의 수가 변수의 수보다 적을 경우 이 부분이 실행됩니다.
            print(f"'{strOneLineConfig}'는 올바른 형식이 아닙니다.")

    return  
def funcMpRouteAdd(dicParameter):
    strResult = "OK"
    # dicParameter를 읽어서 변수에 저장한다.
    strMdn = dicParameter['MDN']
    strServer = dicParameter['SERVER']
    strMpa = dicParameter['MPA']
    mpa_code = funcGetCode(strServer, strMpa)
    id = len(data) + 1    

    # dictionary item을 만든다.
    dicParameter = {"mdn": strMdn, "server": strServer, "module": strMpa, "id": id, "code": mpa_code}

    data.append(dicParameter)
    return strResult

def funcMpRouteWriteFile():
    strResult = "OK"
    try:
        with open(file_path, 'w') as file:
            #mdn,server,module 기본 표시 주석을 작성해준다.
            file.write("#mdn,server,module,code\n")
            for item in data:
                # item을 파일에 쓴다.
                file.write(f"{item['mdn']},{item['server']},{item['module']},{item['code']}\n")
    except FileNotFoundError:
        strResult = f"{file_path} 파일을 찾을 수 없습니다."
    except PermissionError:
        strResult = f"{file_path} 파일을 쓸 권한이 없습니다."
    except Exception as e:
        strResult = f"파일 처리 중 에러가 발생했습니다: {e}"

    return strResult

def funcExecMmiRemote(strServerName, strParameter):
    result = ""
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"SET-MP-RTE.py " + strParameter, "active")
        if "bash" in result:
            print("error: ", result)
        elif len(result) < 1:
            print("error: ", result)
        else:
            # nothing work.
            pass
    except Exception as e:
        print("error: ", e)

    return result

def funcEmsRole(strParameter):
    # MP-RTE을 처리하기 위한 기초 데이터를 만든다.
    #funcDataInitialize()
    dicResult = {}
    listServer = ["AS"]
    strExecMmiRemoteResult = ""
    for strServer in listServer: 
        strExecMmiRemoteResult = funcExecMmiRemote(strServer, strParameter)
    # strExecMmiRemoteResult변수가 정확하게 OK 문자열과 일치한다면
    if "OK" == strExecMmiRemoteResult.strip() :
        dicResult["result"] = "OK"
    else:
        dicResult["result"] = "NOK"
        dicResult["cause"] = strExecMmiRemoteResult.strip()

    #dicResult를 json으로 변환한 후 print한다.
    print(json.dumps(dicResult, indent=4))

    return

def funcServiceRole(dicParameter):
    # 먼저 기존의 파일을 읽어들여 기초 data를 만든다.
    strMpRouteConfig = funcReadMpRouteFile()
    funcMpRouteProcess(strMpRouteConfig)

    # validation check.
    if dicParameter["MDN"] in strMpRouteConfig:
        print("error: already exist.")
        return

    # dicParameter 내용을 반영한다.
    #dicParameter ex) -> MDN=01012345678 SERVER=MS01 MPA=MPA1
    strResult = funcMpRouteAdd(dicParameter)

    # 기초 data를 기반으로 파일을 작성한다.
    strResult = funcMpRouteWriteFile()
    # 작성한 결과를 프린트한다.
    print(strResult)
    
    return 


def funcHelpPrint():
    print("ex) SET-MP-RTE.py MDN=01012345678 SERVER=MS01 MPA=MPA1")
    # Add the implementation of the funcHelpPrint function here
    pass

def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)

    # sys.argv에 py 문자열이 없을 경우 mmi print를 실행합니다.
    bMmiPrint = True
    if ".py" in sys.argv[0]:
        bMmiPrint = False
    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrint(sys.argv)
    
    # 입력받은 argument를 string 형태로 저장한다.
    for i in range(1, num_args):
        strParameter += sys.argv[i] + " "

    # 실행 예제.
    # CRTE-MP-RTE.py MDN=01012345678 SERVER=MS01 MPA=MPA01
    # 입력받은 parameter를 dictionary 형태의 변수로 저장한다.
    dicParameter = {}
    for i in range(1, num_args):
        strArg = sys.argv[i]
        strArgList = strArg.split("=")
        dicParameter[strArgList[0]] = strArgList[1]

    if "help" in strParameter:
        funcHelpPrint()

        if bMmiPrint == True:
            funcMmiPrint.funcMmiPrintComplete()
        return
    
    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole(strParameter)
    else:
        funcServiceRole(dicParameter)

    if bMmiPrint == True:
        funcMmiPrint.funcMmiPrintComplete()

if __name__ == "__main__":
    main()


