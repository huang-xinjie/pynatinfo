import socket
import threading

HOST, detectPort1, detectPort2 = '0.0.0.0', 15002, 12553
BUFFSIZE = 1024


class detectNatType():    
    def __init__(self):
        # detect server bind 2 ports
        self.ds1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ds2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ds1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ds2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ds1.bind((HOST, detectPort1))
        self.ds2.bind((HOST, detectPort2))
        # works in 2 thread
        threading.Thread(target=self.port1Run).start()
        threading.Thread(target=self.port2Run).start()
    

    def port1Run(self):
        # return client's public ip
        while True:
            _, addr = self.ds1.recvfrom(BUFFSIZE)
            print('detectPort1: %s %s' % (_.decode(), str(addr)))
            self.ds1.sendto(str(addr).encode(), addr)

    def port2Run(self):
        while True:
            _, addr = self.ds2.recvfrom(BUFFSIZE)
            print('detectPort2: %s %s' % (_.decode(), str(addr)))
            self.ds2.sendto(str(addr).encode(), addr)

if __name__ == '__main__':
    detectNatType()
