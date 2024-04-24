#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import subprocess
import json
from funcHostName import funcGetMyServerName
import funcExecRemote
import sys
from Logger import funcGetLogger

logger=funcGetLogger()

#not use.
def run_DIS_SIP_RMT():
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-SIP-RMT.py'])
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Error running DIS-SIP-RMT.py:", e)
        #logger.error("Error running DIS-SIP-RMT.py:", e)
        return None

#not use.
def run_DIS_RTE():
    try:
        output = subprocess.check_output(['/home/vfras/mmi/DIS-RTE.py'])
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print("Error running DIS-SIP-RMT.py:", e)
        #logger.error("Error running DIS-SIP-RMT.py:", e)
        return None

def parse_loc_output(output):
    lines = output.split('\n')
    data = []
    headers = []
    loc_count = None
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
                    else:
                        continue 
                    print("test hak. headers:", headers, ", header:", header, ", i:", i, ", values:", values)
                    #logger.debug("test hak. headers:", headers, ", header:", header, ", i:", i, ", values:", values)
                    entry[header] = values[i]
                data.append(entry)
    return data, rmt_count, rmt_result


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

def merge_rte_and_rmt_data(rte_data, rmt_data):
    merged_data = []
    for rte_entry in rte_data:
        for rmt_entry in rmt_data:
            if rte_entry["RTE"] == rmt_entry["RMT_ID"]:
                merged_entry = rte_entry.copy()
                merged_entry.update(rmt_entry)
                merged_data.append(merged_entry)
    return merged_data

#not use.
def main_pre():
    rmt_output = run_DIS_SIP_RMT()
    rte_output = run_DIS_RTE()
    result_data = {}  # »õ·Î¿î µñ¼Å³Ê¸® »ý¼º
    if rmt_output:
        rmt_data, rmt_count, rmt_result = parse_rmt_output(rmt_output)
        if rmt_data:
            merged_rmt_data = {}
            for entry in rmt_data:
                merged_rmt_data.update(entry)  # °¢ µñ¼Å³Ê¸®¸¦ º´ÇÕ
            rmt_output_data = {"RMT_RESULT": rmt_result, "data": merged_rmt_data, "RMT_CNT": rmt_count}
            result_data.update(rmt_output_data)  # ÇÕÄ¥ µñ¼Å³Ê¸®¿¡ Ãß°¡
        else:
            error_message = {"RMT_RESULT": "NOK"}
            result_data.update(error_message)  # ÇÕÄ¥ µñ¼Å³Ê¸®¿¡ Ãß°¡
    if rte_output:
        rte_data, rte_count, rte_result = parse_rte_output(rte_output)
        if rte_data:
            rte_output_data = {"RTE_RESULT": rte_result, "data": rte_data, "RTE_CNT": rte_count}
            result_data.update(rte_output_data)  # ÇÕÄ¥ µñ¼Å³Ê¸®¿¡ Ãß°¡
    else:
        error_message = {"RTE_RESULT": "NOK"}
        result_data.update(error_message)  # ÇÕÄ¥ µñ¼Å³Ê¸®¿¡ Ãß°¡
    
    merged_data = merge_rte_and_rmt_data(rte_data, rmt_data)
    result_data["data"] = merged_data
    
    result_json = json.dumps(result_data, indent=4)
    print(result_json)
    #logger.info(result_json)

def funcParseRmtAndRte(strDisSipRmtResult, strDisRteResult):
    result_data = {}
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
    merged_data = merge_rte_and_rmt_data(rte_data, rmt_data)
    result_data["data"] = merged_data

    #sort to "STATUS UNAVAIL First."
    sorted_data = sorted(result_data["data"], key=lambda x: x["STATUS"], reverse=True)
 
    #result_json = json.dumps(result_data, indent=4)
    result_json = json.dumps(sorted_data, indent=4)
    print(result_json)
    #logger.info(result_json)
    return


# not use.
def funcParseRmtResult(strDisRteResult):
    if rte_output:
        rte_data, rte_count, rte_result = parse_rte_output(strDisRteResult)
        if rte_data:
            rte_output_data = {"RTE_RESULT": rte_result, "data": rte_data, "RTE_CNT": rte_count}
            #result_data.update(rte_output_data)  # ÇÕÄ¥ µñ¼Å³Ê¸®¿¡ Ãß°¡
    else:
        rte_output_data = {"RTE_RESULT": "NOK"}
        #result_data.update(error_message)
    return rte_output_data 

def funcExecMmiDisSipRmt(strServerName):
    result = funcExecRemote.funcExecRemote(strServerName,"DIS-SIP-RMT.py","all")
    #print(result)
    return result

def funcExecMmiDisRte(strServerName):
    result = funcExecRemote.funcExecRemote(strServerName,"DIS-RTE.py","all")
    #print(result)
    return result

def funcEmsRole(strRemoteServerName):
    strRmtResult = funcExecMmiDisSipRmt(strRemoteServerName)
    strRteResult = funcExecMmiDisRte(strRemoteServerName) 
    funcParseRmtAndRte(strRmtResult, strRteResult)
    return

def funcServiceRole():
    #nothing.
    return

def main():
    num_args = len(sys.argv)
    if num_args < 2:
        strRemoteServerName = "CP"
        #print("Usage: DIS-SIP-NODE.py [servername]    << ex)CP, CP01, AS, AS01, AS02 ...")
    else:
        strRemoteServerName = sys.argv[1]

    strMyServerName = funcGetMyServerName()
    if "EMS" in strMyServerName:
        funcEmsRole(strRemoteServerName)
    else:
        funcServiceRole()

if __name__ == "__main__":
    main()

