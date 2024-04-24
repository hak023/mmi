#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import json
import sys
import funcSubsDBConn
from Logger import funcGetLogger
logger=funcGetLogger()

def funcGetMyViewData(_objDb, param):
    cursor = _objDb.cursor()
    cursor.execute("SELECT MSISDN, VIDEO_RING, URL FROM TB_MYVIEW_URL_DATA WHERE MSISDN LIKE ?", (param,));
    rows = cursor.fetchall()
    result_list = []
    for row in rows:
        result_list.append(row)

    return result_list

def funcDataInitialize(result_list):
    data=[]
    for row in result_list:
        data.append({"MSISDN": '0'+row[0], "VIDEO_RING": row[1], "URL": row[2]})

    print(data)

    return

def main():
    objDb = funcSubsDBConn.funcConnectDB()
    strParameter = sys.argv[1]

    if "=" in strParameter:
        strParameterName, strParameterValue = strParameter.split('=')
        if strParameterName == "msisdn":
            strParameter = strParameterValue
        else:
            print("Usage: DIS-MYVIEW.py [MSISDN=01012345678]    << ex)01012345678")
            return

    result_list = funcGetMyViewData(objDb, strParameter)
    funcDataInitialize(result_list)
    funcSubsDBConn.funcDisConnectDB(objDb)

if __name__ == "__main__":
    main()

