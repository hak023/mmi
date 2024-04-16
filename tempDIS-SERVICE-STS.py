#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
from funcHostName import funcGetMyServerName
from funcIpcShm import read_shared_memory
from Logger import funcGetLogger

logger=funcGetLogger()

def test():
    # ���� �ð��� ������
    now = datetime.datetime.now()

    # ���� �ð��� ���ϴ� �������� ������
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")

    # ���������� ������ ������
    data = [
           {"server": "AS01","process": "ASFR","total": 10000,"current": 9999},
           {"server": "AS01","process": "Myview","total": 10000,"current": 8888},
           {"server": "AS02","process": "ASFR","total": 10000,"current": 6666},
           {"server": "AS02","process": "Myview","total": 10000,"current": 2222},
           {"server": "DS","process": "IFSVR","total": 10000,"current": 7777} 
           ]

    # collectTime �ʵ� �߰�
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    # JSON �������� ���
    print(json.dumps(output_data, indent=4))
    logger.info(json.dumps(output_data, indent=4))

def funcEmsRole():
    #strResult = funcExecRemote("AS","DIS-SIP-SES.py","all")
    return

def funcServiceRole():
    int_value, str_value, temp_value = read_shared_memory()

    #make json

    return

def main():
    test()


if __name__ == "__main__":
    main()
