#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import posix_ipc
import mmap
import struct
from Logger import funcGetLogger
import configparser

logger=funcGetLogger()

COMMON_CONFIG_FILE = "/home/vfras/config/COMMON.cfg"

TEST_SHARED_MEMORY_KEY = "0x00fb0019"
TEST_SHARED_MEMORY_SIZE = 24  # 4 (int) + 16 (char) + 4 (int) = 24 bytes

def funcFindShmKeyFromCommonConfig(strType):
    strSection = ""
    strKey = ""
    if "SVIF" in strType:
        strSection = "CP_SHM"
        strKey = "SVIF_STAT"
    elif "ASFR" in strType:
        strSection = "AS_SHM"
        strKey = "ASFR_STAT"
    elif "IFSYNC" in strType:
        strSection = "AS_SHM"
        strKey = "IFSYNC_STAT"

    # not use.
    elif "IFAFR" in strType:
        strSection = "AS_SHM"
        strKey = "IFAFR_STAT"
    elif "MPRM" in strType:
        strSection = "AS_SHM"
        strKey = "MPRM_STAT"
    elif "MPA" in strType:
        strSection = "MS_SHM"
        strKey = "MPA_STAT"
    elif "DB" in strType:
        strSection = "DS_SHM"
        strKey = "DB"
        
    config = configparser.ConfigParser()
    config.read(COMMON_CONFIG_FILE) 
    strShmKey = config.get(strSection, strKey)
    
    return strShmKey

# AS 서버의 ASFR 서버의 정보를 읽어온다. 
def funcReadAsAsfrStatusShm():
    # 변수 초기화 및 선언.
    cps, audio_total, audio_success, audio_fail, video_total, video_success, video_fail = 0, 0, 0, 0, 0, 0, 0
    dictAsfr = {}
    try:
        # shm key는 COMMON_CONFIG_FILE 에 [CP_SHM] 로 적혀져 있는 섹터에 SVIF_STAT 의 값을 읽어온다.
        strSvifShmKey = funcFindShmKeyFromCommonConfig("ASFR")
        
        shm = posix_ipc.SharedMemory(strSvifShmKey, flags=posix_ipc.O_RDONLY)

        # shm에 기록되어있는 내용을 읽어오자.
        with mmap.mmap(shm.fd, shm.size) as mapped_memory:
            #int nCPS;
            #int nAtt_A ;
            #int nSucc_A ;
            #int nFail_A;
            #int nAtt_V;
            #int nSucc_V;
            #int nFail_V;

            # for 반복문으로 2번 반복되도록. 앞 28 byte에 작성될지, 뒤 28 byte에 작성될지 모른다.
            for i in range(2):
                # int 형 7개의 데이터 존재. 차례대로 CPS, audio 시도수, audio 성공수, audio 실패수, video 시도수, video 성공수, video 실패수
                temp_cps = struct.unpack("i", mapped_memory.read(4))[0]
                temp_audio_total = struct.unpack("i", mapped_memory.read(4))[0]
                temp_audio_success = struct.unpack("i", mapped_memory.read(4))[0]
                temp_audio_fail = struct.unpack("i", mapped_memory.read(4))[0]
                temp_video_total = struct.unpack("i", mapped_memory.read(4))[0]
                temp_video_success = struct.unpack("i", mapped_memory.read(4))[0]
                temp_video_fail = struct.unpack("i", mapped_memory.read(4))[0]

                if temp_cps != 0 :
                    cps = temp_cps
                if temp_audio_total != 0 :
                    audio_total = temp_audio_total
                    audio_success = temp_audio_success
                    audio_fail = temp_audio_fail
                if temp_video_total != 0 :
                    video_total = temp_video_total
                    video_success = temp_video_success
                    video_fail = temp_video_fail

        # shm close
        shm.close_fd()

        # 받은 데이터를 dictionary 형태로 가공한다.
        dictAsfr = {"CPS": cps, "Audio_Total": audio_total, "Audio_Success": audio_success, "Audio_Fail": audio_fail, "Video_Total": video_total, "Video_Success": video_success, "Video_Fail": video_fail}

    except Exception as e:
        # dictionary 형태에 모두 0을 기록한다.
        dictAsfr = {"CPS": 0, "Audio_Total": 0, "Audio_Success": 0, "Audio_Fail": 0, "Video_Total": 0, "Video_Success": 0, "Video_Fail": 0}
    
    return dictAsfr

# CP서버의 Svif 서버의 정보를 읽어온다. myview 정보.
def funcReadCpSvifStatusShm():
    dictSvif = {}
    try:
        # shm key는 COMMON_CONFIG_FILE 에 [CP_SHM] 로 적혀져 있는 섹터에 SVIF_STAT 의 값을 읽어온다.
        strSvifShmKey = funcFindShmKeyFromCommonConfig("SVIF")
        
        shm = posix_ipc.SharedMemory(strSvifShmKey, flags=posix_ipc.O_RDONLY)

        # shm에 기록되어있는 내용을 읽어오자.
        with mmap.mmap(shm.fd, shm.size) as mapped_memory:
            # 처음 2400 byte를 건너뛰고 계산 시작.
            mapped_memory.seek(2400)
            # int 형 4개의 데이터 존재. 차례대로, CPS, 총 시도수, 성공수, 실패수
            cps = struct.unpack("i", mapped_memory.read(4))[0]
            total = struct.unpack("i", mapped_memory.read(4))[0]
            success = struct.unpack("i", mapped_memory.read(4))[0]
            fail = struct.unpack("i", mapped_memory.read(4))[0]

        # shm close
        shm.close_fd()

        # 받은 데이터를 dictionary 형태로 가공한다.
        dictSvif = {"CPS": cps, "Total": total, "Success": success, "Fail": fail}

    except Exception as e:
        # dictionary 형태에 모두 0을 기록한다.
        dictSvif = {"CPS": 0, "Total": 0, "Success": 0, "Fail": 0}
        # logger.error(f"funcReadCpSvifShm() error : {str(e)}")
    
    return dictSvif

# DS서버의 Ifsync 서버의 정보를 읽어온다. 가입 정보.
def funcReadDsIfsyncStatusShm():
    dictIfSync = {}
    try:
        # shm key는 COMMON_CONFIG_FILE 에 [CP_SHM] 로 적혀져 있는 섹터에 SVIF_STAT 의 값을 읽어온다.
        strSvifShmKey = funcFindShmKeyFromCommonConfig("IFSYNC")
        
        shm = posix_ipc.SharedMemory(strSvifShmKey, flags=posix_ipc.O_RDONLY)

        # shm에 기록되어있는 내용을 읽어오자.
        with mmap.mmap(shm.fd, shm.size) as mapped_memory:
            # 처음 2400 byte를 건너뛰고 계산 시작.
            mapped_memory.seek(2400)
            # int 형 4개의 데이터 존재. 차례대로, CPS, 총 시도수, 성공수, 실패수
            cps = struct.unpack("i", mapped_memory.read(4))[0]
            total = struct.unpack("i", mapped_memory.read(4))[0]
            success = struct.unpack("i", mapped_memory.read(4))[0]
            fail = struct.unpack("i", mapped_memory.read(4))[0]

        # shm close
        shm.close_fd()

        # 받은 데이터를 dictionary 형태로 가공한다.
        dictIfSync = {"CPS": cps, "Total": total, "Success": success, "Fail": fail}

    except Exception as e:
        # dictionary 형태에 모두 0을 기록한다.
        dictIfSync = {"CPS": 0, "Total": 0, "Success": 0, "Fail": 0}
        # logger.error(f"funcReadCpSvifShm() error : {str(e)}")
    
    return dictIfSync

# DS서버의 IFSYNC 서버의 정보를 읽어온다. 가입자 정보.
def funcReadDsIfSyncConnectShm():
    dictIfSync = {}
    nCount = 0
    strConnect = ""
    try:
        # shm key는 COMMON_CONFIG_FILE 에 [CP_SHM] 로 적혀져 있는 섹터에 SVIF_STAT 의 값을 읽어온다.
        strSvifShmKey = funcFindShmKeyFromCommonConfig("IFSYNC")
        shm = posix_ipc.SharedMemory(strSvifShmKey, flags=posix_ipc.O_RDONLY)

        # shm에 기록되어있는 내용을 읽어오자.
        with mmap.mmap(shm.fd, shm.size) as mapped_memory:
            # 100번 반복.
            for i in range(100):
                # 3개의 데이터 존재. 차례대로, 16 byte의 IP, 4 byte의 Port, 4 byte의 Status
                ip = struct.unpack("16s", mapped_memory.read(16))[0]
                port = struct.unpack("i", mapped_memory.read(4))[0]
                status = struct.unpack("i", mapped_memory.read(4))[0]

                # ip의 값이 유효하다면,
                if ip != b'\x00':
                    if (status == 1) :
                        strConnect = "AVAIL"
                    else :
                        strConnect = "UNAVAIL"

                    # ip, port, status를 dictIfSync 중 nCount의 배열에 저장한다. 
                    dictIfSync[nCount] = {"IP": ip.decode(), "PORT": port, "STATUS": strConnect}
                    nCount += 1
    except Exception as e:
        # 초기화 값을 기록한다.
        dictIfSync = {"IP": "", "PORT": 0, "STATUS": ""}
    return dictIfSync


# CP서버의 Svif 서버의 정보를 읽어온다. myview 정보.
def funcReadCpSvifConnectShm():
    dictSvif = {}
    nCount = 0
    strConnect = ""
    try:
        # shm key는 COMMON_CONFIG_FILE 에 [CP_SHM] 로 적혀져 있는 섹터에 SVIF_STAT 의 값을 읽어온다.
        strSvifShmKey = funcFindShmKeyFromCommonConfig("SVIF")
        shm = posix_ipc.SharedMemory(strSvifShmKey, flags=posix_ipc.O_RDONLY)

        # shm에 기록되어있는 내용을 읽어오자.
        with mmap.mmap(shm.fd, shm.size) as mapped_memory:
            # 100번 반복.
            for i in range(100):
                # 3개의 데이터 존재. 차례대로, 16 byte의 IP, 4 byte의 Port, 4 byte의 Status
                ip = struct.unpack("16s", mapped_memory.read(16))[0]
                port = struct.unpack("i", mapped_memory.read(4))[0]
                status = struct.unpack("i", mapped_memory.read(4))[0]

                # ip의 값이 유효하다면,
                if ip != b'\x00':
                    if (status == 1) :
                        strConnect = "AVAIL"
                    else :
                        strConnect = "UNAVAIL"

                    # ip, port, status를 dictIfSync 중 nCount의 배열에 저장한다. 
                    dictSvif[nCount] = {"IP": ip.decode(), "PORT": port, "STATUS": strConnect}
                    nCount += 1
    except Exception as e:
        # 초기화 값을 기록한다.
        dictSvif = {"IP": "", "PORT": 0, "STATUS": ""}
    return dictSvif



def test_write_shared_memory():
    # ���� �޸� ����
    shm = posix_ipc.SharedMemory(TEST_SHARED_MEMORY_KEY, flags=posix_ipc.O_CREAT, mode=0o666, size=TEST_SHARED_MEMORY_SIZE)

    # ������ ����
    int_value = 123
    str_value = "Hello, Shared Memory!"
    temp_value = 456

    # ������ ��ŷ
    packed_data = struct.pack("i16si", int_value, str_value.encode(), temp_value)

    # ���� �޸𸮿� ������ ����
    with mmap.mmap(shm.fd, shm.size) as mapped_memory:
        mapped_memory.write(packed_data)

    # ���� ��ũ���� �ݱ�
    shm.close_fd()

def test_read_shared_memory():
    # ���� �޸� ����
    shm = posix_ipc.SharedMemory(TEST_SHARED_MEMORY_KEY, flags=posix_ipc.O_RDONLY)

    # ���� �޸𸮿��� ������ �б�
    with mmap.mmap(shm.fd, shm.size) as mapped_memory:
        # ������ ����ŷ
        packed_data = mapped_memory.read(24)  # 4 (int) + 16 (char) + 4 (int)
        int_value, str_value, temp_value = struct.unpack("i16si", packed_data)

    # ���� ��ũ���� �ݱ�
    shm.close_fd()

    # ���ڿ� ���ڵ�
    str_value = str_value.decode().rstrip(b'\x00'.decode())

    return int_value, str_value, temp_value

if __name__ == "__main__":
    # ������ ����
    test_write_shared_memory()

    # ������ �б�
    int_value, str_value, temp_value = test_read_shared_memory()
    print("Read from shared memory:")
    print("Integer:", int_value)
    print("String:", str_value)
    print("Temporary Integer:", temp_value)
    logger.info(f"Read from shared memory: Intger: {int_value}, String: {str_value}, Temporary Integer: {temp_value}")
