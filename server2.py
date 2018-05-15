import socket

MHOST, s1p1 = '123.207.161.147', 15002
HOST, s2p1 = '0.0.0.0', 16201
BUFFSIZE = 1024

class detectNatType():    
    def __init__(self):
        # detect server bind 1 port
        self.ds1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ds1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ds1.bind((HOST, s2p1))
    
    def run(self):
        while True:
            try:
                Data, _ = self.ds1.recvfrom(BUFFSIZE)
                print('s2p1: %s from %s' % (Data.decode(), str(_)))
                if _ == (MHOST,s1p1):
                    clientAddrData = Data.decode().split("'")
                    clientAddr = (clientAddrData[1], int(clientAddrData[2][2:-1]))
                    self.ds1.sendto(Data, clientAddr)
                else:
                    # return client's public address
                    self.ds1.sendto(str(_).encode(), _)
            except Exception as e:
                print("Error: ", str(e))

if __name__ == '__main__':
    s2 = detectNatType()
    s2.run()
