class udp:
    def __init__(self,UDP_PORT = 5005,UDP_IP = "127.0.0.1"):
        import socket
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.UDP_PORT=UDP_PORT
        self.UDP_IP=UDP_IP
        self.data=b""
    def recieve(self):
        import threading
        self.socket.settimeout(1)
        self.socket.bind((self.UDP_IP,self.UDP_PORT))
        def continuous():
            import socket
            self.run=True
            while self.run :
                try:
                    data, addr = self.socket.recvfrom(1024,) # buffer size is 1024 bytes
                    #print("received message: %s" % data)
                    self.data += data
                except socket.timeout:
                    pass
        t=threading.Thread(target=continuous)
        self.t=t
        self.t.start()
    def read(self):
        data=self.data
        self.data=b""
        return data
    def available(self):
        return len(self.data)
    def __del__(self):
        self.run=False
    def stop(self):
        self.run=False
