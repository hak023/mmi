#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
import paramiko
import funcDbInfo
import configparser
import sys
from Logger import funcGetLogger

logger=funcGetLogger()

#parameter info
#target : choose "active" or "all"
#server : choose server name. ex) "AS", "CP"...
def funcExecRemote(server, script_file_name, target):
    config = configparser.ConfigParser()
    config.read('conf/info.cfg')
    strRemoteTagetList = []
    strReturn = "" 

    #ssl config load
    ssl_port = config.getint('COMMON', 'ssh.port')
    ssl_account = config.get('COMMON', 'ssh.username')
    ssl_password = config.get('COMMON', 'ssh.password')

    #script path
    path_homedir = config.get('COMMON', 'mmi.homedir')
    script = path_homedir + script_file_name 

    #get IP from DB    
    objDb = funcDbInfo.funcConnectDB()
    if target == "active":
        result_tuple = funcDbInfo.funcGetServerActive(objDb, server)
        if len(result_tuple) > 0:
            result_str = str(result_tuple[0])
            strIP = result_str.replace("'", "").replace("(", "").replace(")", "").replace(",", "") 
            strRemoteTagetList.append(strIP)
    else:
        result_list = funcDbInfo.funcGetServerActiveAndStandby(objDb, server)
        for listServerInfo in result_list:
            strRemoteTagetList.append(listServerInfo[5])
            #print(listServerInfo[5])

    for strRemoteIp in strRemoteTagetList:
        strReturn += str(execute_remote_script(strRemoteIp, ssl_port, ssl_account, ssl_password, script))
        #print("funcExecRemote : ", strRemoteIp, " / ", ssl_port, " / ",ssl_account, " / ", ssl_password, " / ", script)
        #print("strReturn:",strReturn) 
    return strReturn


def execute_remote_script(server, port, username, password, script_path):
    try:
        ssh = paramiko.SSHClient()

        # ���� ��� ���� �ʽ
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # SSH ���������
        ssh.connect(server, port, username, password, timeout=1)
        #ssh.connect(server, port=port, username=username, password=password, timeout=1)

        # ������� ��������
        stdin, stdout, stderr = ssh.exec_command(script_path, timeout=1)

        # ���� ��n�1�       
        result = stdout.read().decode('utf-8')
        errmsg = stderr.read().decode('utf-8')

        # �� ÷�        
        #print("Script input test:", server, port, username, password, script_path)
        #print("Script execution result:",result)
        if len(errmsg) > 0 :
            result = errmsg
        return result

    except Exception as e:
        result = e
        return result 
    finally:
        ssh.close()

def test():
    # ��� d��
    server = '121.134.202.235'
    port = 10022  # SSH ƿ
    username = 'vfras'
    password = '!core0908'
    script_path = '/home/vfras/mmi/DIS-RTE.py'
    #script_path = '/home/vfras/mmi/hak_test.sh'
    #script_path = '/home/vfras/mmi/DIS-SIP-NODE.py'

    # ������� ���   execut
    #execute_remote_script(server, port, username, password, script_path)
    result = funcExecRemote("CP","DIS-SIP-RMT.py","active")
    logger.info(result) 

def main():
    test()

if __name__ == "__main__":
    main()

