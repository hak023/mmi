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
from Logger import funcGetLogger

logger=funcGetLogger()

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
            #logger.info(result)
        else:
            pass
    except Exception as e:
        print("error : ", e) 
        #logger.error("error : ", e)

    return result 

def funcCheckProcess():
    strExcuteOutput = ""
    strResult = "" 
    try:
        output = subprocess.check_output(['/home/vfras/bin/chk'])
        strExcuteOutput = output.decode('utf-8')
        print(strExcuteOutput)
        #logger.info(strExcuteOutput)
        strResult = "success"
    except subprocess.CalledProcessError as e:
        strResult = "fail"
        print(e, " ", strExcuteOutput) 
        #logger.error(e, " ", strExcuteOutput)

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
    print (nServerExecResult)
    return

def main():
    strParameter = ""
    strRemoteServerName = ""
    num_args = len(sys.argv)
    funcMmiPrint.funcMmiPrint(sys.argv)
    if num_args < 2:
        #print("Usage: DIS-SERVICE-STS.py [service=ASFR]    << ex)ASFR, Myview ...")
        pass
    else:
        strParameter = sys.argv[1]
    strParameter.upper()
    strMyServerName = funcGetMyServerName()

    if "=" in strParameter:
        strParameterName, strParameterValue = strParameter.split('=')
        if strParameterName == "SERVER":
            strRemoteServerName = strParameterValue
        else:
            funcHelpPrint()
            funcMmiPrint.funcMmiPrintComplete()
            return
        
        # strParameterValue 에 아무것도 없을때.
        if len(strParameterValue) < 1 and "EMS" in strMyServerName: # type: ignore
            funcHelpPrint()
            funcMmiPrint.funcMmiPrintComplete()
            return
    else:
        if strRemoteServerName and "EMS" in strRemoteServerName:
            funcHelpPrint()
            return
        else:
            pass

    if strRemoteServerName and "EMS" in strRemoteServerName:
        funcServiceRole()

    if strMyServerName and "EMS" in strMyServerName:
        funcEmsRole(strRemoteServerName)
    else:
        funcServiceRole()

    funcMmiPrint.funcMmiPrintComplete()

    return

if __name__ == "__main__":
    main()


