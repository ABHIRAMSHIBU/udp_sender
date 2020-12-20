import sys
sys.path.append("../")

import TCPServer
import TCPClient
import os
import unittest
import multiprocessing
import time



def create_server_connection_thread():
    # print("Creating Server Connection")
    server_thread = TCPServer.tcpServer()
    server_thread.start()
    server_handler = server_thread.acceptConnection()
    # print("Server Handler = ", server_handler)
    while(server_handler.available() == 0):
        time.sleep(1)
        # print("Nothing available")
    else:
        data = server_handler.read()
        with open("tcp_output.txt", "w") as f:
            f.write(data.decode())
            server_handler.stop()
            server_thread.close()


def send_client_data():
    # print("Creating Client Connection")
    time.sleep(1)
    client_thread = TCPClient.tcpClient("127.0.0.1", 7011)
    client_thread.send("Hello World!")
    # print("Something here")
    client_thread.close()


class TCPClientServerClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        if(os.path.exists("tcp_output.txt")):
            os.remove("tcp_output.txt")
        self.p1 = multiprocessing.Process(
            target=create_server_connection_thread)
        self.p1.start()
        self.p2 = multiprocessing.Process(target=send_client_data)
        self.p2.start()

    @classmethod
    def tearDownClass(self):
        if(os.path.exists("tcp_output.txt")):
            os.remove("tcp_output.txt")

    def testconnection(self):
        self.p2.join()
        self.p1.join()
        data = None
        with open("tcp_output.txt") as f:
            data = f.read()
        self.assertEqual(data, "Hello World!")


if __name__ == "__main__":
    unittest.main()
