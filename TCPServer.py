class tcpServerHandler:
    def __init__(self,connection,address):
        self.data=b""
        self.connection=connection
        self.address=address
    def recieve(self):
        from threading import Thread
        self.connection.settimeout(1)
        def run():
            import socket
            self.run=True
            while(self.run):
                try:
                    data = self.connection.recv(1024)
                    self.data+=data
                except socket.timeout:
                    pass
        self.t=Thread(target=run)
        self.t.start()
    def read(self):
        data=self.data
        self.data=b""
        return data
    def send(self,data):
        self.connection.send(data)
    def available(self):
        return len(self.data)
    def stop(self):
        self.run=False
    def __del__(self):
        self.run=False
class tcpServer:
    def __init__(self,host="localhost",port=7011):
        self.host=host
        self.port=port
        self.handlerList=[]
    def start(self):
        import socket
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen()
    def acceptConnection(self,*args):
        connection, address = self.s.accept()
        handler = tcpServerHandler(connection,address)
        handler.recieve()
        self.handlerList.append(handler)
        return(handler)
    def destroyConnection(self,handler):
        if(type(handler)==type(1)):
            handler=handlerList[handler]
        handler.stop()
        handlerList.pop(handlerList.index(handler))
    def close(self):
        self.s.close()