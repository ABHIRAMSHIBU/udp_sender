import UDPServer
u=UDPServer.udp()
u.recieve()
while(True):
    c=input("1 available \n2 read data\n0 exit\nenterchoice:")
    if (int(c)==1):
        print(u.available())
    elif(int(c)==2):
        print(u.read())
    else:
        break
