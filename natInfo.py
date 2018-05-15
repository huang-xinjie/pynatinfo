import json
import time
import socket

HOST1, s1p1, s1p2 = '123.207.161.147', 15002, 12553
HOST2, s2p1 = '139.199.194.49', 16201
BUFFSIZE = 1024

def getNatInfo():
    Type, ip, port = '', '', ''
    dc1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dc1.settimeout(0.5)     # 500ms
    # FC detect
    retry = 0
    while not Type and retry < 3:
        dc1.sendto("FC detect".encode(), (HOST1, s1p1))
        try:
            _, addr = dc1.recvfrom(BUFFSIZE)
            if addr == (HOST2, s2p1):
                Type = 'FC Nat'
                _, ip, port = _.decode().split("'")
        except socket.timeout:
            retry += 1   # Not FC Nat
        # ARC detect
    retry = 0
    while not Type and retry < 3:
        dc1.sendto("ARC detect".encode(), (HOST1, s1p1))
        try:
            _, addr = dc1.recvfrom(BUFFSIZE)
            if addr == (HOST1, s1p2):
                Type = 'ARC Nat'
                _, ip, port = _.decode().split("'")
        except socket.timeout:
            retry += 1  # Not ARC Nat
    # Sym detect
    retry = 0
    while not Type and retry < 3:
        try:
            dc1.sendto("Sym detect".encode(), (HOST1, s1p1))
            s1Data1, _ = dc1.recvfrom(BUFFSIZE)
            dc1.sendto("Sym detect".encode(), (HOST2, s2p1))
            s2Data1, _ = dc1.recvfrom(BUFFSIZE)
            if s1Data1 != s2Data1:
                Type = 'Sym Nat'
            else:
                Type = 'PRC Nat'
            _, ip, port = s1Data1.decode().split("'")
        except socket.timeout:
            if retry >= 2:
                print('Timeout: something error!')
            retry += 1
    
    print('Nat Type: ', Type)
    print('Public IP: ', ip)
    print('Public Port: ', port[2:-1])

getNatInfo()