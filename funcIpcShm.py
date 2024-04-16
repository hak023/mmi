#!/bin/python3 -tt
# -*- coding: utf-8 -*-

import posix_ipc
import mmap
import struct

from Logger import funcGetLogger

logger=funcGetLogger()

# ���� �޸��� Ű�� ũ�� ����
SHARED_MEMORY_KEY = "0x00fb0019"
SHARED_MEMORY_SIZE = 24  # 4 (int) + 16 (char) + 4 (int) = 24 bytes

def write_shared_memory():
    # ���� �޸� ����
    shm = posix_ipc.SharedMemory(SHARED_MEMORY_KEY, flags=posix_ipc.O_CREAT, mode=0o666, size=SHARED_MEMORY_SIZE)

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

def read_shared_memory():
    # ���� �޸� ����
    shm = posix_ipc.SharedMemory(SHARED_MEMORY_KEY, flags=posix_ipc.O_RDONLY)

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
    write_shared_memory()

    # ������ �б�
    int_value, str_value, temp_value = read_shared_memory()
    print("Read from shared memory:")
    print("Integer:", int_value)
    print("String:", str_value)
    print("Temporary Integer:", temp_value)
    logger.info(f"Read from shared memory: Intger: {int_value}, String: {str_value}, Temporary Integer: {temp_value}")
