#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import subprocess
import json
from funcHostName import funcGetMyServerName
import funcExecRemote
import sys
from Logger import funcGetLogger
import funcIpcShm

logger=funcGetLogger()

#not use.
def run_DIS_SIP_RMT():
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-SIP-RMT.py'])
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running DIS-SIP-RMT.py '{e}'")
        #logger.error(f"Error running DIS-SIP-RMT.py '{e}'")
        return None

#not use.
def run_DIS_RTE():
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-RTE.py'])
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running DIS-SIP-RMT.py:'{e}'")
        #logger.error(f"Error running DIS-SIP-RMT.py:'{e}'")
        return None

def parse_loc_output(output):
    lines = output.split('\n')
    data = []
    headers = []
    loc_count = None
    loc_result = ""
    for line in lines:
        line = line.strip()
        if line.startswith("LOC_ID"):
            headers = line.split()
        elif line.startswith("LOC_CNT"):
            loc_count = int(line.split("=")[-1].strip())
        elif line.startswith("RESULT"):
            loc_result = line.split("=")[-1].strip()
        elif headers and line:
            values = line.split()
            if len(values) == len(headers):
                entry = {}
                for i, header in enumerate(headers):
                    if header == "IP":
                        header = "LOC_IP"
                    elif header == "PORT":
                        header = "LOC_PORT"
                    elif header == "NAME":
                        header = "LOC_NAME"
                    elif header == "LOC_ID":
                        header = "LOC_ID"
                    else:
                        continue 
                    #print("test hak loc. headers:", headers, ", header:", header, ", i:", i, ", values:", values)
                    entry[header] = values[i]
                data.append(entry)
    return data, loc_count, loc_result


def parse_rmt_output(output):
    lines = output.split('\n')
    data = []
    headers = []
    rmt_count = None  
    for line in lines:
        line = line.strip()
        if line.startswith("RMT_ID"):
            headers = line.split()
        elif line.startswith("RMT_CNT"):
            rmt_count = int(line.split("=")[-1].strip())  
        elif line.startswith("RESULT"):
            rmt_result = line.split("=")[-1].strip()  
        elif headers and line:
            values = line.split()
            if len(values) == len(headers):
                entry = {}
                for i, header in enumerate(headers):
                    #print("test hak. headers:", headers, ", header:", header, ", i:", i, ", values:", values) 
                    entry[header] = values[i]
                data.append(entry)
    return data, rmt_count, rmt_result

def parse_rte_output(output):
    lines = output.split('\n')
    data = []
    headers = []
    rte_count = None
    rte_result = None
    for line in lines:
        line = line.strip()
        if line.startswith("RTE_CNT"):
           rte_count_str = line.split("=")[-1].strip()
           if rte_count_str.lower() == 'null':
                rte_count = None
           else:
                rte_count = int(rte_count_str)
        elif line.startswith("RTE"):
            headers = line.split()
        elif line.startswith("RESULT"):
            rte_result = line.split("=")[-1].strip().upper()
        elif headers and line:
            values = line.split()
            if len(values) == len(headers):
                entry = {}
                for i, header in enumerate(headers):
                    entry[header] = values[i]
                data.append(entry)
    return data, rte_count, rte_result

# 3 merge from rte, loc, rmt.
def funcDataMerge(rte_data, loc_data, rmt_data, strServer):
    merged_data = []
    listCheckDuplicationValue = []
    for rte_entry in rte_data:
        for rmt_entry in rmt_data:
            if rte_entry["RMT_ID"] == rmt_entry["RMT_ID"]:
                #print("rte_entry_RMT_ID: ", rte_entry["RMT_ID"], ", rmt_entry_RMT_ID: ", rmt_entry["RMT_ID"])
                for loc_entry in loc_data:
                    strCheckDuplicationKey = rte_entry["RTE"] + rte_entry["LOC_ID"] + loc_entry["LOC_NAME"] + rmt_entry["RMT_ID"]
                    if rte_entry["LOC_ID"] == loc_entry["LOC_ID"] and strCheckDuplicationKey not in listCheckDuplicationValue:
                        merged_entry = rte_entry.copy()
                        merged_entry.update(rmt_entry)
                        merged_entry.update(loc_entry)
                        # merged_entry에 "TYPE": "SIP" 를 추가하자.
                        merged_entry["TYPE"] = "SIP"
                        merged_entry["SERVER"] = strServer
                        merged_data.append(merged_entry)
                        listCheckDuplicationValue.append(strCheckDuplicationKey)
                        #print("KEY: ", strCheckDuplicationKey, "rte_RMT_ID: ", rte_entry["RMT_ID"], "rte_LOC_ID: ", rte_entry["LOC_ID"], "loc_LOC_NAME: ", loc_entry["LOC_NAME"] )
   
    return merged_data

def funcParseLocAndRmtAndRte(strDisSipLocResult, strDisSipRmtResult, strDisRteResult, strServer):
    result_data = {}
    if strDisSipLocResult:
        loc_data, loc_count, loc_result = parse_loc_output(strDisSipLocResult)
        if loc_data:
            merged_loc_data = {}
            for entry in loc_data:
                merged_loc_data.update(entry)
            loc_output_data = {"LOC_RESULT": loc_result, "data": merged_loc_data, "LOC_CNT": loc_count}
            result_data.update(loc_output_data)
        else:
            loc_output_data = {"LOC_RESULT": "NOK"}
            result_data.update(loc_output_data)

    if strDisSipRmtResult:
        rmt_data, rmt_count, rmt_result = parse_rmt_output(strDisSipRmtResult)
        if rmt_data:
            merged_rmt_data = {}
            for entry in rmt_data:
                merged_rmt_data.update(entry) 
            rmt_output_data = {"RMT_RESULT": rmt_result, "data": merged_rmt_data, "RMT_CNT": rmt_count}
            result_data.update(rmt_output_data)
        else:
            rmt_output_data = {"RMT_RESULT": "NOK"}
            result_data.update(rmt_output_data)

    if strDisRteResult:
        rte_data, rte_count, rte_result = parse_rte_output(strDisRteResult)
        if rte_data:
            rte_output_data = {"RTE_RESULT": rte_result, "data": rte_data, "RTE_CNT": rte_count}
            result_data.update(rte_output_data) 
    else:
        rte_output_data = {"RTE_RESULT": "NOK"}
        result_data.update(rte_output_data)
    merged_data = funcDataMerge(rte_data, loc_data, rmt_data, strServer)
    #result_data["data"] = merged_data

    return merged_data



def funcExecMmiDisSipLoc(strServerName):
    result = funcExecRemote.funcExecRemote(strServerName,"DIS-SIP-LOC.py","all")
    #print(result)
    return result

def funcExecMmiDisSipRmt(strServerName):
    result = funcExecRemote.funcExecRemote(strServerName,"DIS-SIP-RMT.py","all")
    return result

def funcExecMmiDisRte(strServerName):
    result = funcExecRemote.funcExecRemote(strServerName,"DIS-RTE.py","all")
    return result

# funcExecMmiRemote 함수는 주어진 서버 이름에 대해 원격으로 MMI 명령을 실행합니다.
def funcExecMmiRemote(strServerName):
    strResult = ""
    try:
        strResult = funcExecRemote.funcExecRemote(strServerName,"DIS-ALL-NODE.py", "all")
    except Exception as e:
        strResult = ""
    return strResult 

def funcEmsRole(strRemoteServerName):
    listServer = ["CP00", "CP01", "DS00"] # 추후 DS00 -> DS로 바꿔주세요. 현재 TB 상황상 테스트 함.
    sorted_data = []
    # SIP 서버에 대한 정보를 가져옵니다.
    for strServer in listServer: 
        # DS 서버는 skip.
        if "DS" in strServer:
            continue
        strLocResult = funcExecMmiDisSipLoc(strServer)
        strRmtResult = funcExecMmiDisSipRmt(strServer)
        strRteResult = funcExecMmiDisRte(strServer)
        merged_data = funcParseLocAndRmtAndRte(strLocResult, strRmtResult, strRteResult, strServer)
        
        for data in merged_data:
            sorted_data.append(data)
    
    # shm 봐야하는 애들. DS서버의 IFSYNC와 CP서버의 SVIF 프로세스.
    # 동일한 python을 실행해서 서버 이름에 맞는 job을 수행한다.
    for strServer in listServer: 
        strExecReturn = funcExecMmiRemote(strServer)
        try:
            # strExecReturn는 json형태의 string이다. 따라서 json으로 읽어들이자.
            dicServerExecResult = json.loads(str(strExecReturn))
            print("dicServerExecResult: ", dicServerExecResult)
            sorted_data.append(dicServerExecResult)
        except json.JSONDecodeError:
            # strExecReturn 값이 JSON 형식이 아닐 경우 이 부분이 실행됩니다.
            pass

    #sort to "STATUS UNAVAIL First."
    #sorted_data = sorted(sorted_data, key=lambda x: x["STATUS"], reverse=True)

    result_json = json.dumps(sorted_data, indent=4)

    print(result_json)

    return

def funcServiceRole(strMyServerName):
    dicServerExecResult = {}
    if "DS" in strMyServerName:
        # shm 를 확인해서 json 형태로 print하자.
        dicServerExecResult = funcIpcShm.funcReadDsIfSyncConnectShm()
        # dicServerExecResult에 일부 값을 추가하자.
        dicServerExecResult["TYPE"] = "IFSYNC"
        dicServerExecResult["SERVER"] = strMyServerName
        dicServerExecResult["NAME"] = strMyServerName + "-IFSYNC"
        dicServerExecResult["ACTION"] = "ACT"
        #dictionary를 json으로 변환하여 출력한다.
        result_json = json.dumps(dicServerExecResult, indent=4)
        print(result_json)
    elif "CP" in strMyServerName:
        # shm 를 확인해서 json 형태로 print하자.
        dicServerExecResult = funcIpcShm.funcReadCpSvifConnectShm()
        # dicServerExecResult에 일부 값을 추가하자.
        dicServerExecResult["TYPE"] = "MYVIEW"
        dicServerExecResult["SERVER"] = strMyServerName
        dicServerExecResult["NAME"] = strMyServerName + "-IFSYNC"
        dicServerExecResult["ACTION"] = "ACT"
        #dictionary를 json으로 변환하여 출력한다.
        result_json = json.dumps(dicServerExecResult, indent=4)
        print(result_json)

    return

def funcHelpPrint():
    print("help message nothing.")
    return

def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)
    if num_args < 2:
        #print("Usage: DIS-SIP-NODE.py [servername=CP]    << ex)CP, CP01, AS, AS01, AS02 ...")
        pass 
    else:
        strParameter = sys.argv[1]

    if "=" in strParameter:
        strParameterName, strParameterValue = strParameter.split('=')
        if strParameterName == "servername":
            strRemoteServerName = strParameterValue
    elif "help" in strParameter:
        funcHelpPrint()
        return
    else:
        strRemoteServerName = "CP"
    
    strMyServerName = funcGetMyServerName()
    if strMyServerName is not None and "EMS" in strMyServerName:
        funcEmsRole(strRemoteServerName)
    else:
        funcServiceRole(strMyServerName)

if __name__ == "__main__":
    main()

