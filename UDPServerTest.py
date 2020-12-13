import UDPServer
u=UDPServer.udp()
u.recieve()
try:
    while(True):
        c=input("1) Check Available Data \n2) Read Available Data\n0) Exit\nenterchoice:")
        if (int(c)==1):
            print(u.available())
        elif(int(c)==2):
            print(u.read())
        else:
            break
    u.stop()
except KeyboardInterrupt:
    u.stop()
    print("Keyboard interrupt! Exiting")