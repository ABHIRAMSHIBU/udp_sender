class udp:
    def __init__(self,UDP_PORT= 5005,UDP_IP= "127.0.0.1"):
        import socket
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.UDP_PORT=UDP_PORT
        self.UDP_IP=UDP_IP

        
        
    def send(self,MESSAGE):
        self.socket.sendto(MESSAGE, (self.UDP_IP,self.UDP_PORT))