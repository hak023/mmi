#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
from funcHostName import funcGetMyServerName
from funcIpcShm import test_read_shared_memory
from Logger import funcGetLogger

logger=funcGetLogger()

def test():
    # ���� �ð��� ������
    now = datetime.datetime.now()

    # ���� �ð��� ���ϴ� �������� ������
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")

    # ���������� ������ ������
    data = [
            {"server": "CP01", "total": 10000, "current": 9999},
            {"server": "CP02", "total": 10000, "current": 8888}
            ]

    # collectTime �ʵ� �߰�
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    # JSON �������� ���
    json_dump = json.dumps(output_data, indent=4)
    print(json_dump)
    #logger.info(json_dump)

def funcEmsRole():
    #strResult = funcExecRemote("AS","DIS-SIP-SES.py","all")
    return

def funcServiceRole():
    int_value, str_value, temp_value = test_read_shared_memory()

    #make json

    return

def main():
    test()
    strMyServerName = funcGetMyServerName()
    if "EMS" in strMyServerName:
        funcEmsRole()
    else:
        funcServiceRole()
 
    #print(strMyServerName)

if __name__ == "__main__":
    main()


