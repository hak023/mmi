#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import json

# 입력 데이터 예시
test_data = """Recv End
-----------------------------------------

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[INPUT]
COMMAND    = DIS-SIP-RMT

             DISPLAY REMOTE SIP SERVER


[OUTPUT]
         RMT_ID                      NAME               DOAMIN   IPV                             IP    PORT   PROTOCOL  NAT_ON   DSCP     STATUS
         ---------------------------------------------------------------------------------------------------------------------------------------
          10111               SS_ICSCF_01           sktims.net  IPv4                220.103.220.210    5064        UDP     OFF      0      AVAIL
          10112              SS_OPTION_01           sktims.net  IPv4                220.103.220.210    3013        UDP     OFF      0      AVAIL

RMT_CNT    = 2

RESULT     = OK

COMPLETED - VIBCF61 2018-11-14 15:31:41.515

"""

print(test_data)
