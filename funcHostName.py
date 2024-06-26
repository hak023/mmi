#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import subprocess
from Logger import funcGetLogger

logger=funcGetLogger()

def funcGetMyServerName():
    command_result = funcExecuteCommand("uname -n")
    #logger.info(command_result)
    #print(command_result)
    if command_result is not None:
        command_result = command_result.upper()
    return command_result

def funcExecuteCommand(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        output = result.stdout.strip()
        #logger.info(output)
        #print(output)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed with error: {e}")
        #logger.error(f"Command execution failed with error: {e}")
        return None
def main():
    command_result = funcGetMyServerName()
    if command_result:
        print("Command output:", command_result)
        #logger.info(f"Command output: {command_result}")
    else:
        print("Failed to execute command.")
        #logger.info("Failed to execute command.")

if __name__ == "__main__":
    main()



