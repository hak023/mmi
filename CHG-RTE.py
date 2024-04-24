#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import json
from Logger import funcGetLogger

logger=funcGetLogger()

# �Է� ������ ����
test_data = """Recv End
-----------------------------------------
binary length : 336
ResponseMsg(uiMagicCookie=0, uiMsgLen=336, uiType=33554432, uiSubType=570429476, uiCompId=2, uiCompSesId=0, uiAsId=0, uiAsSesId=0, szSesDesc='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', uiReasonCode=0, union_Reserved='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', m_nResult=0, m_nReason=0, m_szReasonDesc='Msync_SUCCESS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', m_stRte=[StructInfo(m_uiID=50001, m_szDesc='LocalTest1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', m_uiLID=50001, m_uiRID=50001, m_uiTRTE=1, m_ucType=1, m_ucDoRouteMedia=1, m_sOptTime=5, m_sOptRetry=3, m_sOptAction=0, m_sSesRefreshTime=0, m_nRouteGroup=1, m_nMAXCnt=100000, m_nDeactRsp=1, m_ucReserved='\x00\x00\x00\x00', m_ucStatus=1, m_ucProto=3, m_ucUsed=1, m_usReserved2=0, m_uiBusyCnt=0, m_uiICCnt=0, m_uiOGCnt=0, m_nCurRetry=1, m_nIndex=31)])

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[INPUT]
COMMAND    = CHG-RTE

             CHANGE ROUTE

                 RTE = 50001
                NAME = LocalTest1

[OUTPUT]
            RTE                      NAME     LOC_ID     RMT_ID       TRTE       TYPE      MEDIA OPT_TIME   RETRY  ACTION  SES_TIME  GROUP_ID  PROTOCOL  MAX_CNT  DEACT_RSP        STATUS
         --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          10111                LocalTest1      50001      50001          1       MINE     ROUTED        5       3     ACT         0         1       UDP   100000       SEND       UNAVAIL

RESULT     = OK
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

"""

#logger.info(test_data)
print(test_data)
