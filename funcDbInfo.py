#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import MySQLdb
import configparser
from Logger import funcGetLogger

logger=funcGetLogger()

def funcConnectDB():
    # config 파일을 읽어옵니다.
    config = configparser.ConfigParser()
    config.read('/home/vfras/mmi/conf/info.cfg')

    # config 파일에서 데이터베이스 정보를 읽어옵니다.
    mysql_host = config.get('COMMON', 'mysql.host')
    mysql_port = config.getint('COMMON', 'mysql.port')
    mysql_account = config.get('COMMON', 'mysql.account')
    mysql_password = config.get('COMMON', 'mysql.password')
    mysql_database = config.get('COMMON', 'mysql.database')
    mysql_charset = config.get('COMMON', 'mysql.charset')

    # 데이터베이스에 연결합니다.
    db = MySQLdb.connect(host=mysql_host,
                         port=mysql_port,
                         user=mysql_account,
                         passwd=mysql_password,
                         db=mysql_database,
                         charset=mysql_charset)
    return db

def funcDisConnectDB(_objDb):
    _objDb.close()

def funcGetServerActiveAndStandby(_objDb, _strServerName):
    cursor = _objDb.cursor()
    cursor.execute("SELECT * FROM SAM_NETIF WHERE hostName LIKE %s AND netIfType = 'lan'", ('%-' + _strServerName + '%',))
    rows = cursor.fetchall()
    result_list = []
    for row in rows:
        result_list.append(row)

    # 첫 번째 쿼리의 결과가 없는 경우, 두 번째 쿼리를 실행합니다. 
    if not result_list:
        cursor.execute("SELECT * FROM SAM_NETIF WHERE hostName LIKE %s AND netIfType = 'vlan'", ('%-' + _strServerName + '%',))
        rows = cursor.fetchall()
        for row in rows:
            result_list.append(row)

    return result_list

# strServerName ex)AS01, AS02, AS03, AS04 ...
def funcGetServerActive(_objDb, _strServerName): 
    cursor = _objDb.cursor()
    query = "SELECT ipAddress \
    FROM SAM_NETIF \
    WHERE hostName LIKE '%-" + _strServerName + "%' \
    AND netIfType = 'lan' \
    AND systemId IN ( \
        SELECT systemId \
        FROM SAM_HA_SYSTEM \
        WHERE active = 1 \
    );"
    cursor.execute(query)
    rows = cursor.fetchall()
    result_list = []
    for row in rows:
        result_list.append(row)
    return result_list

# strServerName ex)AS01, AS02, AS03, AS04 ...
def funcGetHaStatus(_objDb):
    cursor = _objDb.cursor()
    query = "SELECT \
        n.hostName AS SERVER, \
        CASE s.active \
            WHEN 1 THEN 'ACTIVE' \
            ELSE 'STANDBY' \
        END AS STATUS \
    FROM \
        SAM_NETIF n \
    JOIN \
        SAM_HA_SYSTEM s ON n.systemId = s.systemId \
    WHERE \
        n.netIfType = 'lan' \
    ;"
    cursor.execute(query)
    rows = cursor.fetchall()
    result_list = []
    for row in rows:
        result_list.append(row)
    return result_list

def main():
    objDb = funcConnectDB()
    result_list = funcGetServerActiveAndStandby(objDb, "AS")
    active_result_list = funcGetServerActive(objDb, "AS")
    
    ha_status_result = funcGetHaStatus(objDb)
    #logger.info(ha_status_result)
    print(ha_status_result)    

    #logger.info("Number of items in result_list:", len(result_list))
    print("Number of items in result_list:", len(result_list))
    for item in result_list:
        #logger.info("IP:", item)
        print("IP:", item)
    #logger.info("Number of items in active_result_list:", len(active_result_list))
    print("Number of items in active_result_list:", len(active_result_list))
    for item in active_result_list:
        #logger.info("IP:", item)
        print("IP:", item)
    funcDisConnectDB(objDb)

if __name__ == "__main__":
    main()

