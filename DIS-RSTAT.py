#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcDbInfo
from funcHostName import funcGetMyServerName
import funcMmiPrint

def test():
    now = datetime.datetime.now()

    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    data = [
            ]

    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    print(json.dumps(output_data, indent=4))
    return

def funcServiceRole(strRemoteServiceName):
    #nothing work.
    return

def funcHelpPrint():
    #nothing work.
    return

# 해당 파일을 실행하여 결과를 리턴함.
def funcExecRstat():
    strExcuteOutput = ""
    strResult = ""
    try:
        output = subprocess.check_output(['/home/vfras/bin/RSTAT'])
        strExcuteOutput = output.decode('utf-8')
        print(strExcuteOutput)
        strResult = "success"
    except subprocess.CalledProcessError as e:
        strResult = "fail"
        print(e, " ", strExcuteOutput)

    return strResult

def funcEmsRole():
    #print("%-16s %-16s %-16s" % ("FRAS", "SERVICE", "STATISTICS"))
    print("%s %s %s" % ("FRAS", "SERVICE", "STATISTICS"))
    print("------------------------------------------------------------------")
    result = funcExecRstat()
    return

def main():
    strParameter = ""
    strRemoteServiceName = ""
    num_args = len(sys.argv)
    funcMmiPrint.funcMmiPrint(sys.argv)
    if num_args < 2:
        #print("Usage: DIS-SERVICE-STS.py [service=ASFR]    << ex)ASFR, Myview ...")
        pass
    else:
        strParameter = sys.argv[1]

    if "help" in strParameter:
        funcHelpPrint()
        return

    strMyServerName = funcGetMyServerName()
    if "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole(strRemoteServiceName)

    funcMmiPrint.funcMmiPrintComplete()

    return

if __name__ == "__main__":
    main()


