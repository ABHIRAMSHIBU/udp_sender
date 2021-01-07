import subprocess as sp
import time
from threading import Thread


def doAction(data, action):
    if type(data) is type(""):
        data = data.encode()
    if action is None:
        return False
    else:
        if action == 1:
            if b"Hello" in data:
                print("Hello was found")
                return True
            else:
                print("Hello was not found")
                return False
        else:
            if action is not None:
                return action(data)

        return True


class ncTCPServer:
    def __init__(self, port=5006):
        import os
        if os.path.exists("/usr/bin/nc") is not True:
            print("Warning: NETCAT binary not found in usual place, if not there in your ENVIRONMENT, things are "
                  "going to go sideways!")
        else:
            print("MESSAGE: Found netcat binary at /usr/bin/nc, continuing with ENVIRONMENT Path.")
        # GLOBAL VARIABLES
        self.process = sp.Popen("nc -lp " + str(port), shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        self.t = Thread(target=self.watchForData)
        self.action = None
        self.run = True
        self.z = b""
        self.port = port
        self.start()

    def watchForData(self):
        count = 0
        try:
            while self.run:
                old = self.z
                self.z += self.process.stdout.read(1)
                if old != self.z:
                    if self.action is not None:
                        returnValue = doAction(self.z, self.action)
                        if returnValue is True:
                            self.z=b""
                            self.action = None
                        elif returnValue is None:
                            self.z=b""
                    print("Got message", count, self.z)
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
        self.process.stdin.flush()

    def test(self):
        if self.process.poll() is None:
            return True  # alive
        else:
            return False  # dead

    def setAction(self, action):
        self.action = action

    def stop(self):
        self.run=False