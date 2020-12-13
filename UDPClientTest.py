import UDPClient
jer=UDPClient.udp()

for i in range(10):
    jer.send(b"hello")