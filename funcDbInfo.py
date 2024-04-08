#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import MySQLdb
import configparser

def funcConnectDB():
    # ¼³d ÆÀ À±â   c
    config = configparser.ConfigParser()
    config.read('conf/info.cfg')

    # MySQL ¿¬°á³d
    mysql_host = config.get('COMMON', 'mysql.host')
    mysql_port = config.getint('COMMON', 'mysql.port')
    mysql_account = config.get('COMMON', 'mysql.account')
    mysql_password = config.get('COMMON', 'mysql.password')
    mysql_database = config.get('COMMON', 'mysql.database')
    mysql_charset = config.get('COMMON', 'mysql.charset')

    # MySQL ¿¬°á   d
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
    cursor.execute("SELECT * FROM SAM_NETIF WHERE hostName LIKE %s", ('%-' + _strServerName + '%',))
    rows = cursor.fetchall()
    result_list = []
    for row in rows:
        result_list.append(row)
    return result_list

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
    print(ha_status_result)

    print("Number of items in result_list:", len(result_list))
    for item in result_list:
        print("IP:", item)
    print("Number of items in active_result_list:", len(active_result_list))
    for item in active_result_list:
        print("IP:", item)
    funcDisConnectDB(objDb)

if __name__ == "__main__":
    main()

