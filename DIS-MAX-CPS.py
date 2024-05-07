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
import configparser

logger=funcGetLogger()

# 파일 경로
myview_file_path = "/home/vfras/config/SVIF/SVIF_REFRESH.cfg"
ifsync_file_path = "/home/vfras/config/ifsync/IFSYNC_REFRESH.cfg"

# ifsync의 maxcps config를 읽어서 print한다.
def funcReadIfSyncMaxCps():
    max_count = 0
    strOnOff = ""
    try:
        # ConfigParser 객체를 생성합니다.
        config = configparser.ConfigParser()

        # 설정 파일을 읽습니다.
        config.read(ifsync_file_path)

        # 'OVERLOAD_CONTROL' 섹션의 'MAX_COUNT' 값을 가져옵니다.
        max_count = config.get('IFSYNC', 'MAX_CPS')
        if int(max_count.strip()) > 0:
            strOnOff = "ON"
        else:
            strOnOff = "OFF"
        #strOnOff = config.get('OVERLOAD_CONTROL', 'MAX_COUNT_ON')
    except configparser.NoSectionError:
        max_count = 0
        strOnOff = "OFF"
        print(f"'OVERLOAD_CONTROL' 섹션이 {ifsync_file_path} 파일에 없습니다.")
    except configparser.NoOptionError:
        max_count = 0
        strOnOff = "OFF"
        print(f"'MAX_COUNT' 옵션이 'OVERLOAD_CONTROL' 섹션에 없습니다.")
    except FileNotFoundError:
        max_count = 0
        strOnOff = "OFF"
        print(f"{ifsync_file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        max_count = 0
        strOnOff = "OFF"
        print(f"{ifsync_file_path} 파일을 읽을 권한이 없습니다.")
    except Exception as e:
        max_count = 0
        strOnOff = "OFF"
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
    return max_count, strOnOff



# myview의 maxcps config를 읽어서 print한다.
def funcReadMyviewMaxCps():
    max_count = 0
    strOnOff = ""
    try:
        # ConfigParser 객체를 생성합니다.
        config = configparser.ConfigParser()

        # 설정 파일을 읽습니다.
        config.read(myview_file_path)

        # 'OVERLOAD_CONTROL' 섹션의 'MAX_COUNT' 값을 가져옵니다.
        max_count = config.get('OVERLOAD_CONTROL', 'MAX_COUNT')
        if int(max_count.strip()) > 0:
            strOnOff = "ON"
        else:
            strOnOff = "OFF"
        #strOnOff = config.get('OVERLOAD_CONTROL', 'MAX_COUNT_ON')
    except configparser.NoSectionError:
        max_count = 0
        strOnOff = "OFF"
        print(f"'OVERLOAD_CONTROL' 섹션이 {myview_file_path} 파일에 없습니다.")
    except configparser.NoOptionError:
        max_count = 0
        strOnOff = "OFF"
        print(f"'MAX_COUNT' 옵션이 'OVERLOAD_CONTROL' 섹션에 없습니다.")
    except FileNotFoundError:
        max_count = 0
        strOnOff = "OFF"
        print(f"{myview_file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        max_count = 0
        strOnOff = "OFF"
        print(f"{myview_file_path} 파일을 읽을 권한이 없습니다.")
    except Exception as e:
        max_count = 0
        strOnOff = "OFF"
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
    return max_count, strOnOff


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

    #logger.info(json.dumps(output_data, indent=4))

# funcExecMmiRemote 함수는 주어진 서버 이름에 대해 원격으로 MMI 명령을 실행합니다.
def funcExecMmiRemote(strServerName, strParameter):
    strResult = ""
    try:
        if "IFSYNC" in strParameter:
            strResult = funcExecRemote.funcExecRemote(strServerName,"DIS-MAX-CPS.py " + strParameter,"active")
        else:
            strResult = funcExecRemote.funcExecRemote(strServerName,"DIS-MAX-CPS.py " + strParameter,"all")
        #if "bash" in strResult:
        #    strResult = "0"
        #elif len(strResult) < 1:
        #    strResult = "0"
        #nReturnValue = int(strResult)
    except Exception as e:
        #nReturnValue = 0
        strResult = {"type": "", "cps": 0, "on": "OFF"}
    return strResult 

# funcEmsRole 함수는 각 서버에 대해 MMI 명령을 실행하고 결과를 JSON 형식으로 출력합니다.
def funcEmsRole(strParameter):
    listServer = ["CP00", "CP01", "DS00"]
    data = []
    dicServerExecResult = {}
    strExecReturn = ""
    for strServer in listServer: 
        # strParameter 에 type이 SIP거나 MYVIEW이면, CP 서버에 대한 CPS 값을 가져옵니다.
        if "CP" in strServer:
            if "SIP" in strParameter or "MYVIEW" in strParameter:
                strExecReturn = funcExecMmiRemote(strServer, strParameter)
                try:
                    # strExecReturn json형태이다. 따라서 json.loads를 사용하여 dictionary로 변환한다.
                    dicServerExecResult = json.loads(str(strExecReturn))        
                    data.append(dicServerExecResult)
                except json.JSONDecodeError:
                    # strExecReturn 값이 JSON 형식이 아닐 경우 이 부분이 실행됩니다.
                    pass
        elif "DS" in strServer:
            if "IFSYNC" in strParameter:
                strExecReturn = funcExecMmiRemote(strServer, strParameter)
                try:
                    # strExecReturn json형태이다. 따라서 json.loads를 사용하여 dictionary로 변환한다.
                    dicServerExecResult = json.loads(str(strExecReturn))        
                    data.append(dicServerExecResult)
                except json.JSONDecodeError:
                    # strExecReturn 값이 JSON 형식이 아닐 경우 이 부분이 실행됩니다.
                    pass

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    print(output_json)
    #logger.info(output_json)

    return

# funcParseDisSipEnvCps 함수는 DIS-SIP-ENV.py 스크립트의 출력에서 CPS 값을 추출합니다.
def funcParseDisSipEnvCps(strDisSipEnvResult):
    strTotal = ""
    strCurrent = ""
    matchFindSession = re.search(r'CPS\(Number\)\s+(\d+)\s+(\d+)\s+(\S+)', strDisSipEnvResult)
    
    if matchFindSession:
        strCurrent = matchFindSession.group(1)
        strTotal = matchFindSession.group(2)
        strOnOff = matchFindSession.group(3)
    return strTotal, strOnOff

# funcGetSipSessionCps 함수는 DIS-SIP-ENV.py 스크립트를 실행하고 CPS 값을 반환합니다.
def funcGetSipMaxCps():
    strExcuteOutput = ""
    strOnOff = ""
    nCps = 0
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-SIP-ENV.py'])
        strExcuteOutput = output.decode('utf-8')
        strCps, strOnOff = funcParseDisSipEnvCps(strExcuteOutput)
        if strCps.strip():
            nCps = int(strCps)
        else:
            nCps = 0
            print("strResult is an empty string.")
            
    except subprocess.CalledProcessError as e:
        nCps = 0

    return nCps, strOnOff

def funcGetMyviewCps():
    # config 파일을 읽어서 max cps 값을 반환한다.
    nMaxCps, strOnOff = funcReadMyviewMaxCps()
    return nMaxCps, strOnOff

def funcGetIfSyncCps():
    # config 파일을 읽어서 max cps 값을 반환한다.
    nMaxCps, strOnOff = funcReadIfSyncMaxCps()
    return nMaxCps, strOnOff

# funcServiceRole 함수는 서버의 역할에 따라 CPS 값을 계산하고 출력합니다.
def funcServiceRole(dicParameter):
    strMakeResult = ""
    strMyServerName = funcGetMyServerName()
    nCps = 0
    strOnOff = ""

    #DIS-SIP-ENV.py check.
    if strMyServerName is not None and "CP" in strMyServerName and "SIP" in dicParameter["type"]:
        nCps, strOnOff = funcGetSipMaxCps()
    elif strMyServerName is not None and "CP" in strMyServerName and "MYVIEW" in dicParameter["type"]:
        nCps, strOnOff = funcGetMyviewCps()
    elif strMyServerName is not None and "DS" in strMyServerName and "IFSYNC" in dicParameter["type"]:
        nCps, strOnOff = funcGetIfSyncCps()
    else:
        #error
        nCps = -1 

    dicServerInfo = {"type": dicParameter["type"], "cps": nCps, "on": strOnOff}

    output_json = json.dumps(dicServerInfo, indent=4)

    print(output_json)
    #logger.info(nCps)
    return

def funcHelpPrint():
    print("help message")
    print("ex) DIS-MAX-CPS.py type=SIP")
    print("type의 종류는 SIP, MYVIEW, IFSYNC 입니다.")
    
    # Add the implementation of the funcHelpPrint function here
    pass

# main 함수는 프로그램의 주 실행 루틴입니다.
def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)

    # 입력받은 argument를 string 형태로 저장한다.
    for i in range(1, num_args):
        strParameter += sys.argv[i] + " "
    
    # 실행 예제.
    # DIS-MAX-CPS.py type=SIP
    # 입력받은 parameter를 dictionary 형태의 변수로 저장한다.
    dicParameter = {}
    for i in range(1, num_args):
        strArg = sys.argv[i]
        strArgList = strArg.split("=")
        dicParameter[strArgList[0]] = strArgList[1]


    if "help" in strParameter or len(strParameter) < 1:
        funcHelpPrint()
        return

    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole(strParameter)
    else:
        funcServiceRole(dicParameter)

# 스크립트가 직접 실행되는 경우 main 함수를 호출합니다.
if __name__ == "__main__":
    main()
