#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import datetime
import json

# ���� �ð��� ������
now = datetime.datetime.now()

# ���� �ð��� ���ϴ� �������� ������
formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")

# ���������� ������ ������
data = [
        {"server": "CP01", "cps": 9},
        {"server": "CP02", "cps": 88},
        {"server": "AS01", "cps": 77},
        {"server": "AS02", "cps": 33},
        {"server": "DS", "cps": 66}
        ]

# collectTime �ʵ� �߰�
output_data = {"collectTime": formatted_time}
output_data.update({"servers": data})

# JSON �������� ���
print(json.dumps(output_data, indent=4))

