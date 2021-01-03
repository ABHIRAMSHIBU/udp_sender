import subprocess as sp
import time
from threading import Thread


def doAction(data, action):
    if type(data) is type(b""):
        data = data.decode()
    if action is None:
        return False
    else:
        if action == 1:
            if "Hello" in data:
                print("Hello was found")
            else:
                print("Hello was not found")
        else:
            if action is not None:
                action(data)

        return True


class ncTCPServer:
    def __init__(self, port=5006):
        # GLOBAL VARIABLES
        self.process = sp.Popen("nc -lp " + str(port), shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        self.t = Thread(target=self.watchForData)
        self.action = None
        self.run = True
        self.port = port
        self.start()


    def watchForData(self):
        count = 0
        try:
            while self.run:
                z = self.process.stdout.readline()
                if z:
                    if self.action is not None:
                        doAction(z, self.action)
                        self.action = None
                    print("Got message", count, z)
                else:
                    break
                count += 1
        except KeyboardInterrupt:
            self.run = False
            z = self.process.stderr.read()
            print("Printing error")
            print(z)
            print("Bye...")

    def start(self):
        # PROCEDURE
        self.t.start()

    def join(self):
        self.t.join()

    def write(self, data):
        self.process.stdin.write(data)

    def test(self):
        if self.process.poll() is None:
            return True  # alive
        else:
            return False  # dead

    def setAction(self, action):
        self.action = action


ncTS = ncTCPServer()
ncTS.action = 1
ncTS.join()
