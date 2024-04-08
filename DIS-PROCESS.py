#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import subprocess
import funcDbInfo
from funcHostName import funcGetMyServerName
import funcMmiPrint
import time
import importlib
import funcExecRemote

def test():
    return

#strServerName ex)CP01, CP02, AS01, AS ...
#strProcess ex) Myview, ASFR
#strStatus ex) active or all
def funcExecMmiRemote(strServerName):
    nReturnValue = "fail"
    try:
        result = funcExecRemote.funcExecRemote(strServerName,"DIS-PROCESS.py","all")
        if "bash" in result:
            print(result)
        else:
            nReturnValue = "success"
    except Exception as e:
        print("error : ", e) 

    return nReturnValue 

def funcCheckProcess():
    strExcuteOutput = ""
    strResult = "" 
    try:
        output = subprocess.check_output(['/home/vfras/bin/chk'])
        strExcuteOutput = output.decode('utf-8')
        print(strExcuteOutput)
        strResult = "success"
    except subprocess.CalledProcessError as e:
        strResult = "fail"
        print(e, " ", strExcuteOutput) 

    return strResult 

def funcServiceRole():
    print("DIS PROCESS COMMAND...")       
    strResult = funcCheckProcess()
    return

def funcHelpPrint():
    print("Write Argument Server Name")
    print("ex) DIS-PROCESS SERVER=XX")
    print("SERVER LIST [CP, DS, EMS, AS, MS]") 
    return

def funcEmsRole(strRemoteServerName):
    nServerExecResult = funcExecMmiRemote(strRemoteServerName)

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
    strParameter.upper()

    if "=" in strParameter:
        strParameterName, strParameterValue = strParameter.split('=')
        if strParameterName == "SERVER":
            strRemoteServerName = strParameterValue
        else:
            funcHelpPrint()
            return
    else:
        funcHelpPrint()
        return

    if "EMS" in strRemoteServerName:
        funcServiceRole()

    strMyServerName = funcGetMyServerName()
    if "EMS" in strMyServerName:
        funcEmsRole(strRemoteServiceName)
    else:
        funcServiceRole()

    funcMmiPrint.funcMmiPrintComplete()

    return

if __name__ == "__main__":
    main()


