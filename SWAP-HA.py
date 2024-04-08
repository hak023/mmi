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
        result = funcExecRemote.funcExecRemote(strServerName,"SWAP-HA.py","active")
        if "bash" in result:
            print(result)
        else:
            nReturnValue = "success"
    except Exception as e:
        print("error : ", e) 

    return nReturnValue 

def funcHaSelfDeact():
    strExcuteOutput = ""
    strResult = "" 
    try:
        output = subprocess.check_output(['/home/vfras/mmi/sam_hactl.py'])
        strExcuteOutput = output.decode('utf-8')
        strResult = "success"
    except subprocess.CalledProcessError as e:
        strResult = "fail" 

    return strResult 

def funcServiceRole():
    print("SEND MESSAGE SWAP COMMAND...")       
    strResult = funcHaSelfDeact()
    if "success" in strResult: 
        time.sleep(1) 
        print("SWAP COMMAND SEND SUCCESS")
    else:
        print("SWAP COMMAND SEND FAIL")
    return

def funcHelpPrint():
    print("Write Argument Server Name")
    print("ex) SWAP-HA SERVER=XX")
    print("SERVER LIST [CP, DS, EMS, AS, MS]") 
    return

def funcEmsRole(strRemoteServerName):
    nServerExecResult = funcExecMmiRemote(strRemoteServerName)

    #call DIS-HA
    module_name = 'DIS-HA'
    module = importlib.import_module(module_name)
    module.funcEmsRole()
    #DIS-HA.funcEmsRole()
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


