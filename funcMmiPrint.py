#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import sys
import datetime
import os

def funcMmiDisHa(listArgv):
    strInputCommand = " ".join(listArgv)
    strMakeUpCommand = os.path.basename(strInputCommand)
    print("[INPUT]")
    #command
    print("COMMAND : ", strMakeUpCommand)
    print("")
    #command comment
    print("DISPLAY HA STATE")
    print("")
    print("[OUTPUT]")
    return 

def funcMmiSwapHa(listArgv):
    strInputCommand = " ".join(listArgv)
    strMakeUpCommand = os.path.basename(strInputCommand)
    print("[INPUT]")
    #command
    print("COMMAND : ", strMakeUpCommand)
    print("")
    #command comment
    print("SWAP HA STATE")
    print("")
    print("[OUTPUT]")
    return 

def funcMmiDisRstat(listArgv):
    strInputCommand = " ".join(listArgv)
    strMakeUpCommand = os.path.basename(strInputCommand)
    print("[INPUT]")
    #command
    print("COMMAND : ", strMakeUpCommand)
    print("")
    #command comment
    print("DISPLAY CURRENT SERVICE STATISTICS")
    print("")
    print("[OUTPUT]")
    return 

def funcMmiDisProcess(listArgv):
    strInputCommand = " ".join(listArgv)
    strMakeUpCommand = os.path.basename(strInputCommand)
    print("[INPUT]")
    #command
    print("COMMAND : ", strMakeUpCommand)
    print("")
    #command comment
    print("DISPLAY SERVER PROCESS")
    print("")
    print("[OUTPUT]")
    return 

def funcMmiDisMpaBlock(listArgv):
    strInputCommand = " ".join(listArgv)
    strMakeUpCommand = os.path.basename(strInputCommand)
    print("[INPUT]")
    #command
    print("COMMAND : ", strMakeUpCommand)
    print("")
    #command comment
    print("DISPLAY MPA BLOCK")
    print("")
    print("[OUTPUT]")
    return

def funcMmiSetMpaBlock(listArgv):
    strInputCommand = " ".join(listArgv)
    strMakeUpCommand = os.path.basename(strInputCommand)
    print("[INPUT]")
    #command
    print("COMMAND : ", strMakeUpCommand)
    print("")
    #command comment
    print("SETTING MPA BLOCK")
    print("")
    print("[OUTPUT]")
    return

def funcMmiDelMpaBlock(listArgv):
    strInputCommand = " ".join(listArgv)
    strMakeUpCommand = os.path.basename(strInputCommand)
    print("[INPUT]")
    #command
    print("COMMAND : ", strMakeUpCommand)
    print("")
    #command comment
    print("DELETE MPA BLOCK")
    print("")
    print("[OUTPUT]")
    return


def funcMmiPrint(listArgv):
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print("%-16s %-16s" % ("START - ", current_time))
    print("")
    if "DIS-HA" in listArgv[0]:
        funcMmiDisHa(listArgv)
    elif "SW-HA" in listArgv[0]:
        funcMmiSwapHa(listArgv)
    elif "DIS-RSTAT" in listArgv[0]:
        funcMmiDisRstat(listArgv)
    elif "DIS-PROCESS" in listArgv[0]:
        funcMmiDisProcess(listArgv)
    elif "DIS-MPA-BLOCK" in listArgv[0]:
        funcMmiDisMpaBlock(listArgv)
    elif "SET-MPA-BLOCK" in listArgv[0]:
        funcMmiSetMpaBlock(listArgv)
    elif "DEL-MPA-BLOCK" in listArgv[0]:
        funcMmiDelMpaBlock(listArgv)
    return 

def funcMmiPrintComplete():
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print("")
    print("%-16s %-16s" % ("COMPLETE - ", current_time))
    return 

def main():
    listArgumentTest = []
    listArgumentTest.append("DIS-HA")
    #listArgumentTest.append("SWAP-HA")
    #listArgumentTest.append("DIS-PROCESS")
    #listArgumentTest.append("DIS-RSTAT")
    funcMmiPrint(listArgumentTest)

    return

if __name__ == "__main__":
    main()



