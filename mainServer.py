import socket
import threading

HOST, detectPort1, detectPort2 = '0.0.0.0', 15002, 12553
HOST2, s2p1 = '139.199.194.49', 16201
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

    def run(self):
        # return client's public address
        while True:
            try:
                _, addr = self.ds1.recvfrom(BUFFSIZE)
                data = _.decode()
                print('detectPort1: %s from %s' % (data, str(addr)))
                if data == 'FC detect':
                    self.ds1.sendto(str(addr).encode(), (HOST2, s2p1))
                elif data == 'ARC detect':
                    self.ds2.sendto(str(addr).encode(), addr)
                else:
                    self.ds1.sendto(str(addr).encode(), addr)
            except Exception as e:
                print("Error: ", str(e))

if __name__ == '__main__':
    s1 = detectNatType()
    s1.run()