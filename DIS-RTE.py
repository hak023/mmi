#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import json

# �Է� ������ ����
test_data = """Recv End
-----------------------------------------

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[INPUT]
COMMAND    = DIS-RTE

             DISPLAY ROUTE


[OUTPUT]
            RTE                      NAME     LOC_ID     RMT_ID       TRTE       TYPE      MEDIA OPT_TIME   RETRY  ACTION  SES_TIME  GROUP_ID  PROTOCOL  MAX_CNT  DEACT_RSP        STATUS
         --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          10111               SS_ICSCF_01      10001      10111          1       MINE     ROUTED        5       3     ACT         0         1       UDP   100000       SEND         AVAIL
          10112              SS_OPTION_01      10001      10112          1       MINE     ROUTED        5       3  BYPASS         0         1       UDP   100000       SEND         AVAIL

RTE_CNT    = 2

RESULT     = OK

COMPLETED - VIBCF61 2018-11-14 15:31:41.515

"""

print(test_data)
