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

def funcEmsRole():
    objDb = funcDbInfo.funcConnectDB()
    ha_status_result = funcDbInfo.funcGetHaStatus(objDb)
    
    print("%-16s %-16s" % ("SERVER", "STATUS"))
    print("----------------------------")
    for result_one_line in ha_status_result:
        print("%-16s %-16s" % (result_one_line[0], result_one_line[1]))
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

    "help" in strPar= funcGetMyServerName()
    if funcHelpPrint()
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


