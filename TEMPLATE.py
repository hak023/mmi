#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
from funcHostName import funcGetMyServerName
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
    print(json.dumps(output_data, indent=4))
    logger.info(json.dumps(output_data, indent=4))

def funcEmsRole():
    return

def funcServiceRole():
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


