#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import json
from Logger import funcGetLogger

logger=funcGetLogger()

# 입력 데이터 예시
test_data = """Recv End
-----------------------------------------

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[INPUT]
COMMAND    = DIS-SIP-ENV

             DISPLAY SIP ENVIRONMENT


[OUTPUT]
                     ITEM           CURRENT               MAX    OVERLOAD_CHECK
        -----------------------------------------------------------------------
              SES(Number)                33             90000               N/A
              CPS(Number)                44               500               OFF
              TPS(Number)                 0               100               OFF
                   CPU(%)                19                80               OFF
                   MEM(%)                19                10               OFF
                MSG(byte)               N/A              4000    CTRL_RELAY_TCP

                     ITEM              EMER             AUDIO             VIDEO    OVERLOAD_CHECK
        -----------------------------------------------------------------------------------------
        CPS_CLASS(Number)                 1                 3                 2               OFF

RESULT     = OK

COMPLETED - IBC53 2024-03-27 11:31:49.794

"""

#logger.info(test_data)
print(test_data)
