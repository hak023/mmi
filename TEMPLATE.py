#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json
from funcHostName import funcGetMyServerName
from Logger import funcGetLogger

logger=funcGetLogger()

def test():
    # 현재 시간을 가져옴
    now = datetime.datetime.now()

    # 현재 시간을 원하는 형식으로 포맷팅
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")

    # 고정값으로 설정된 데이터
    data = [
            {"server": "CP01", "total": 10000, "current": 9999},
            {"server": "CP02", "total": 10000, "current": 8888}
            ]

    # collectTime 필드 추가
    output_data = {"collectTime": formatted_time}
    output_data.update({"servers": data})

    # JSON 형식으로 출력
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


