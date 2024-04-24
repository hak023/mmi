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
#myview_file_path = "/home/vfras/hak/SVIF_REFRESH.cfg"

# myview의 maxcps config를 변경한다.
def funcChangeMyviewMaxCps(dicParameter):
    strOnOff = dicParameter["on"]
    strMaxCps = dicParameter["max"]
    strResult = "NOK"
    try:
        # ConfigParser 객체를 생성합니다.
        config = configparser.ConfigParser()

        # 설정 파일을 읽습니다.
        config.read(myview_file_path)

        # 'OVERLOAD_CONTROL' 섹션의 'MAX_COUNT' 값을 변경합니다.
        if strOnOff == "ON":
            config.set('OVERLOAD_CONTROL', 'MAX_COUNT', strMaxCps)
        elif strOnOff == "OFF":
            config.set('OVERLOAD_CONTROL', 'MAX_COUNT', "0")

        # 변경된 설정을 파일에 씁니다.
        with open(myview_file_path, 'w') as configfile:
            config.write(configfile)

        #print(f"{myview_file_path} 파일의 'MAX_COUNT' 값을 변경했습니다.")
        strResult = "OK"
    except configparser.NoSectionError:
        print(f"'OVERLOAD_CONTROL' 섹션이 {myview_file_path} 파일에 없습니다.")
    except configparser.NoOptionError:
        print(f"'MAX_COUNT' 옵션이 'OVERLOAD_CONTROL' 섹션에 없습니다.")
    except FileNotFoundError:
        print(f"{myview_file_path} 파일을 찾을 수 없습니다.")
    except PermissionError:
        print(f"{myview_file_path} 파일을 쓸 권한이 없습니다.")
    except Exception as e:
        print(f"파일 처리 중 에러가 발생했습니다: {e}")
    return strResult

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
        strResult = funcExecRemote.funcExecRemote(strServerName,"CHG-MAX-CPS.py " + strParameter,"all")
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
    listServer = ["CP00", "CP01", "DS"]
    data = []
    dicServerExecResult = {}
    strExecReturn = ""
    for strServer in listServer: 
        # strParameter 에 type이 SIP거나 MYVIEW이면, CP 서버에 대한 CPS 값을 가져옵니다.
        if "CP" in strServer:
            if "SIP" in strParameter or "MYVIEW" in strParameter:
                strExecReturn = funcExecMmiRemote(strServer, strParameter)
                # strExecReturn json형태이다. 따라서 json.loads를 사용하여 dictionary로 변환한다.
                dicServerExecResult = json.loads(str(strExecReturn))        
                data.append(dicServerExecResult)
        elif "DS" in strServer:
            if "IFSVR" in strParameter:
                strExecReturn = funcExecMmiRemote(strServer, strParameter)
                # strExecReturn json형태이다. 따라서 json.loads를 사용하여 dictionary로 변환한다.
                dicServerExecResult = json.loads(str(strExecReturn))        
                data.append(dicServerExecResult)

    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    output_json = json.dumps(output_data, indent=4)
    print(output_json)
    #logger.info(output_json)

    return

# funcParseDisSipEnvCps 함수는 DIS-SIP-ENV.py 스크립트의 출력에서 RESULT 값을 추출합니다.
def funcParseDisSipEnvCps(strDisSipEnvResult):
    strResult = ""
    #strCurrent = ""
    matchFindSession = re.search(r'RESULT\s+(\S+)\s+(\S+)', strDisSipEnvResult)
    
    if matchFindSession:
        #strCurrent = matchFindSession.group(1)
        strResult = matchFindSession.group(2)
        #strOnOff = matchFindSession.group(3)
    return strResult

# funcGetSipSessionCps 함수는 DIS-SIP-ENV.py 스크립트를 실행하고 CPS 값을 반환합니다.
def funcChgSipMaxCps(dicParameter):
    strExcuteOutput = ""
    strOnOff = dicParameter["on"]
    nMaxCps = int(dicParameter["max"])
    strResult = ""
    try:
        # ex) /home/vfras/mmi/DIS-SIP-ENV.py CPS_CHK_ON=ON, MAX_CPS=100
        command = ["/home/vfras/mmi/CHG-SIP-ENV.py", f"CPS_CHK_ON={strOnOff},", f"MAX_CPS={nMaxCps}"]
        output = subprocess.check_output(command)
        strExcuteOutput = output.decode('utf-8')
        strResult = funcParseDisSipEnvCps(strExcuteOutput)
        if "NOK" in strResult.strip():
            strResult = "NOK"
        else:
            strResult = "OK"
            
    except subprocess.CalledProcessError as e:
        strResult = "NOK"

    return strResult

def funcChgMyviewCps(dicParameter):
    # config 파일을 읽어서 max cps 값을 변경한다.
    strResult = funcChangeMyviewMaxCps(dicParameter)
    return strResult

def funcChgIfsvrCps(dicParameter):

    # 담당자가 규격을 안준다....
    nCps = 44
    strOnOff = "OFF"
    strResult = "OK"
    return strResult

# funcServiceRole 함수는 서버의 역할에 따라 CPS 값을 계산하고 출력합니다.
def funcServiceRole(dicParameter):
    strMakeResult = ""
    strMyServerName = funcGetMyServerName()
    nCps = int(dicParameter["max"])
    strOnOff = dicParameter["on"]
    strResult = ""

    #DIS-SIP-ENV.py check.
    if strMyServerName is not None and "CP" in strMyServerName and "SIP" in dicParameter["type"]:
        strResult = funcChgSipMaxCps(dicParameter)
    elif strMyServerName is not None and "CP" in strMyServerName and "MYVIEW" in dicParameter["type"]:
        strResult = funcChgMyviewCps(dicParameter)
    elif strMyServerName is not None and "DS" in strMyServerName and "IFSVR" in dicParameter["type"]:
        strResult = funcChgIfsvrCps(dicParameter)
    else:
        #error
        nCps = -1 
    dicServerInfo = {"type": dicParameter["type"], "cps": nCps, "on": strOnOff, "result": strResult}

    output_json = json.dumps(dicServerInfo, indent=4)

    print(output_json)
    #logger.info(nCps)
    return

def funcHelpPrint():
    print("help message")
    print("ex) DIS-MAX-CPS.py type=SIP")
    print("type의 종류는 SIP, MYVIEW, IFSVR 입니다.")
    
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


    if "help" in strParameter:
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
