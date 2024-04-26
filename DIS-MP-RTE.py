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
def funcGetIdAndCode(strServer, strModule):
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

                # 변수를 출력합니다.
                print(mp_route_config)
    except FileNotFoundError:
        print(f"{file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        print(f"{file_path} 파일을 읽을 권한이 없습니다.")
    except Exception as e:
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
    return

# config를 읽어서 내부 data에 저장한다.
def funcMpRouteProcess(strMpaBlockConfig):
    id = 1
    # string 형태의 strMpaBlockConfig을 line마다 읽어서 data에 있는 딕셔너리의 'code' 키와 비교하여 같은 딕셔너리를 찾습니다.
    for line in strMpaBlockConfig.splitlines():
        strOneLineConfig = line.strip()
        try:
            # strOneLineConfig를 ,로 split하여 각각의 변수에 저장한다.
            mdn, server, module, mpa_code = strOneLineConfig.split(',')
            # 분리된 각 부분을 딕셔너리로 만든다.
            dicItem = {"mdn": mdn, "server": server, "module": module}
            mpa_code = funcGetIdAndCode(dicItem['server'], dicItem['module'])
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
   
def funcMpRtePrint():
    # data를 json 형태로 출력한다.
    print(json.dumps(data, indent=4))



    
    #print("%-16s %-16s %-16s %-16s" % ("ID", "MDN", "SERVER", "MPA", "MPA_ID"))
    #print("------------------------------------------------------------------")
    #for item in data:
    #    print("%-16s %-16s %-16s %-16s" % (item['id'], item['server'], item['name'], item['block']))
    return

def funcExecMmiRemote(strServerName):
    result = ""
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-MP-RTE.py","active")
        if "bash" in result:
            print("error: ", result)
        else:
            # nothing work.
            pass
    except Exception as e:
        print("error: ", e)

    return result

def funcEmsRole():
    # MPA BLOCK을 처리하기 위한 기초 데이터를 만든다.
    #funcDataInitialize()
    

    listServer = ["AS"]
    strMpRouteConfig = ""
    for strServer in listServer: 
        strMpRouteConfig = funcExecMmiRemote(strServer)

    funcMpRouteProcess(strMpRouteConfig) 
    
    funcMpRtePrint()
    

    return

def funcServiceRole():
    # MPA BLOCK 파일을 읽어서 기초 데이터에 업데이트한다.
    funcReadMpRouteFile()
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

    # sys.argv에 py 문자열이 없을 경우 mmi print를 실행합니다.
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


