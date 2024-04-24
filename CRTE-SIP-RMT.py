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
COMMAND    = CRTE-SIP-RMT

             CREATE REMOTE SIP SERVER


[OUTPUT]
         RMT_ID                      NAME               DOAMIN   IPV                             IP    PORT   PROTOCOL  NAT_ON   DSCP     STATUS
         ---------------------------------------------------------------------------------------------------------------------------------------
          10111               SS_ICSCF_01           sktims.net  IPv4                220.103.220.210    5064        UDP     OFF      0      AVAIL

RMT_CNT    = 1

RESULT     = OK

COMPLETED - VIBCF61 2018-11-14 15:31:41.515

"""

print(test_data)
#logger.info(test_data)
