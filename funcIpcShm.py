#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import posix_ipc
import mmap
import struct

from Logger import funcGetLogger

logger=funcGetLogger()

# 공유 메모리의 키와 크기 정의
SHARED_MEMORY_KEY = "0x00fb0019"
SHARED_MEMORY_SIZE = 24  # 4 (int) + 16 (char) + 4 (int) = 24 bytes

def write_shared_memory():
    # 공유 메모리 열기
    shm = posix_ipc.SharedMemory(SHARED_MEMORY_KEY, flags=posix_ipc.O_CREAT, mode=0o666, size=SHARED_MEMORY_SIZE)

    # 데이터 생성
    int_value = 123
    str_value = "Hello, Shared Memory!"
    temp_value = 456

    # 데이터 패킹
    packed_data = struct.pack("i16si", int_value, str_value.encode(), temp_value)

    # 공유 메모리에 데이터 쓰기
    with mmap.mmap(shm.fd, shm.size) as mapped_memory:
        mapped_memory.write(packed_data)

    # 파일 디스크립터 닫기
    shm.close_fd()

def read_shared_memory():
    # 공유 메모리 열기
    shm = posix_ipc.SharedMemory(SHARED_MEMORY_KEY, flags=posix_ipc.O_RDONLY)

    # 공유 메모리에서 데이터 읽기
    with mmap.mmap(shm.fd, shm.size) as mapped_memory:
        # 데이터 언패킹
        packed_data = mapped_memory.read(24)  # 4 (int) + 16 (char) + 4 (int)
        int_value, str_value, temp_value = struct.unpack("i16si", packed_data)

    # 파일 디스크립터 닫기
    shm.close_fd()

    # 문자열 디코딩
    str_value = str_value.decode().rstrip(b'\x00'.decode())

    return int_value, str_value, temp_value

if __name__ == "__main__":
    # 데이터 쓰기
    write_shared_memory()

    # 데이터 읽기
    int_value, str_value, temp_value = read_shared_memory()
    print("Read from shared memory:")
    print("Integer:", int_value)
    print("String:", str_value)
    print("Temporary Integer:", temp_value)
    logger.info(f"Read from shared memory: Intger: {int_value}, String: {str_value}, Temporary Integer: {temp_value}")
