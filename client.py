import json
import time
import socket

HOST1, PORT, s1p1, s1p2 = '123.207.161.147', 23333, 15002, 12553
HOST2, s2p1 = '123.207.161.147', 6201
BUFFSIZE = 1024

# get lan ip
def getLanIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def getNatInfo():
    ip = getLanIp()
    dc1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dc2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dc1.sendto("Hi".encode(), (HOST1, s1p1))
    s1Data1, _ = dc1.recvfrom(BUFFSIZE)
    print('public ip: ', s1Data1.decode().split("'")[1])
    # 所获得ip与返回ip一致 则 处于公网
    if s1Data1.decode().split("'")[1] == ip:
        return 'NoNat'
    # 同一公网ip, 相同端口, 不同会话   ## 不同 则 对称型
    dc2.sendto("Hi".encode(), (HOST1, s1p1))
    s1Data2, _ = dc2.recvfrom(BUFFSIZE)
    if s1Data1 != s1Data2:
        return 'SymNat'
    # 同一公网ip, 不同端口   ## 不同 则 端口受限锥型
    dc1.sendto("Hi".encode(), (HOST1, s1p2))
    s1Data3, _ = dc1.recvfrom(BUFFSIZE)
    if s1Data1 != s1Data3:
        return 'PRCNat'
    # 不同公网ip          ## 不同 则 受限锥型, 相同 则 全锥型
    dc1.sendto("Hi".encode(), (HOST2, s2p1))
    s1Data4, _ = dc1.recvfrom(BUFFSIZE)
    if s1Data1 != s1Data4:
        return 'RCNat'
    else:
        return 'FCNat'

print('Nat Type: ', getNatInfo())