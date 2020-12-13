
class packect:
    def __init__(self):
        pass
    def generator(self,l):
        n=[]
        for i in range (l):
            print(b"1011")
            n.append(b"1011")
        data=b''
        for i in n:
            data+=i
        return data

            

s=packect()

                
import UDPServer
u=UDPServer.udp()
d=u.recieve()
if(d==s.generator(len(d))):
    from TCPClient import tcpClient
    tc=tcpClient("127.0.0.1", 7011)
    tc.send(b"1")
    tc.close()










