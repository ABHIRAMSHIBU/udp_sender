
class packect:
    def __init__(self):
        pass
    def generator(self,l):
        n=[]
        for i in range (l):
            print(b"1011")
            n.append(b"1011")
        return n
    def test(self):
        for i in range (1024*2*2,131030):
            i=i*2
            self.generator(i)
            #send&check
            

s=packect()

                
import UDPServer
u=UDPServer.udp()
d=u.recieve()
if(d==s.generator(len(d))):
    from TCPClient import tcpClient
    tc=tcpClient("127.0.0.1", 7011)
    tc.send(b"1")
    tc.close()










