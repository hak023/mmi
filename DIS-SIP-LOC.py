#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import json

test_data = """Recv End
-----------------------------------------

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[INPUT]
COMMAND    = DIS-SIP-LOC

             DISPLAY LOCAL SIP SERVER


[OUTPUT]
         LOC_ID                 NAME               DOAMIN        IPV                             IP       PORT   PROTOCOL     RCS_ON     STATUS
         --------------------------------------------------------------------------------------------------------------------------------------
          10001                 CP02           sktims.net       IPv4                 223.39.134.206       5060        UDP        OFF      AVAIL
          10002              SKT-TCP           sktims.net       IPv4                 223.39.134.206       5060        TCP        OFF      AVAIL

LOC_CNT    = 2

RESULT     = OK

COMPLETED - IBC55 2023-10-24 02:18:46.449

"""

print(test_data)
