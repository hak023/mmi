#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json

# 현재 시간을 가져옴
now = datetime.datetime.now()

# 현재 시간을 원하는 형식으로 포맷팅
formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")

# 고정값으로 설정된 데이터
data = [
        {"server": "CP01", "cps": 9},
        {"server": "CP02", "cps": 88},
        {"server": "AS01", "cps": 77},
        {"server": "AS02", "cps": 33},
        {"server": "DS", "cps": 66}
        ]

# collectTime 필드 추가
output_data = {"collectTime": formatted_time}
output_data.update({"servers": data})

# JSON 형식으로 출력
print(json.dumps(output_data, indent=4))

