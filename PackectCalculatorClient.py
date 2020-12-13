class packect:
    def __init__(self):
        pass
    def generator(self,l):
        n=[]
        for i in range (l):
           
            n.append(b"1011")
            return n
    def test(self):
        for i in range (1024*2*2,131030):
            
            n=self.generator(i)
            import UDPClient
            jer=UDPClient.udp()
            jer.send(n)
            #send&check
            import TCPServer
            ts=None
            ts = TCPServer.tcpServer()
            ts.start()
            u = ts.acceptConnection()
            if(u.read()==1):
                i=i*2
            else:
                print(i)
                break


s=packect()
s.test()