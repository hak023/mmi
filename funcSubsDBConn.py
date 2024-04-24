#!/bin/python3 -tt
# -*- coding: utf-8 -*-

# 가입자 DB Connection을 반환해주는 function
import jaydebeapi
import configparser
from Logger import funcGetLogger
logger=funcGetLogger()

def funcConnectDB():
    # config 파일을 읽어옵니다.
    config = configparser.ConfigParser()
    config.read('/home/vfras/mmi/conf/info.cfg')
    #config.read('./conf/info.cfg')

    # config 파일에서 데이터베이스 정보를 읽어옵니다.
    altibase_host = config.get('COMMON', 'altibase.host')
    altibase_port = config.getint('COMMON', 'altibase.port')
    altibase_account = config.get('COMMON', 'altibase.account')
    altibase_password = config.get('COMMON', 'altibase.password')
    altibase_database = config.get('COMMON', 'altibase.database')

    # JDBC사용을 위해 JDBC URL을 생성합니다.
    jdbc_url = f"jdbc:Altibase://{altibase_host}:{altibase_port}/{altibase_database}"

    # JDBC 드라이버의 경로를 지정합니다.
    jar_path = '/home/vfras/mmi/jdbc/altibase-jdbc-driver-7.3.0.0.1.jar'

    # JDBC 드라이버 클래스를 지정합니다.
    driver_class = "Altibase7_3.jdbc.driver.AltibaseDriver"

    # JDBC 드라이버를 사용하여 데이터베이스에 연결합니다.
    conn = jaydebeapi.connect(driver_class, jdbc_url, [altibase_account, altibase_password], jar_path)

    return conn

def funcDisConnectDB(_objDb):
    _objDb.close()

#db 연결을 테스트하기 위한 함수
def funcGet(_objDb):
    cursor = _objDb.cursor()
    cursor.execute("SELECT MSISDN, VIDEO_RING, URL FROM TB_MYVIEW_URL_DATA WHERE MSISDN LIKE ?", ('1020000121',));
    rows = cursor.fetchall()
    result_list = []
    for row in rows:
        result_list.append(row)

    return result_list

def main():
    objDb = funcConnectDB()
    result_list = funcGet(objDb)
    #logger.info(ha_status_result)
    print(result_list)

    funcDisConnectDB(objDb)

if __name__ == "__main__":
    main()

