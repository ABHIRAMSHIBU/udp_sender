#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 19:20:03 2020

@author: Abhiram Shibu

Copyleft 2020 Project SSAL
"""
class tcpClient:
    '''This class is going to be an ascii interface layer of SSAL Test Suit'''
    def __init__(self,ip,port,timeout=0.5):
        from telnetlib import Telnet
        self.telnet=Telnet(host=ip,port=port,timeout=timeout)
        self.ip=ip
        self.port=port
        self.timeout=timeout
        self.data=b""
    def send(self,data):
        '''Will raise Broken pipe error if connection closed, otherwise will send ascii data over telnet'''
        self.telnet.write(data.encode())
    def sendLine(self,data):
        '''Will raise Broken pipe error if connection closed, otherwise will send ascii data new line terminated over telnet'''
        self.telnet.write((data+"\n").encode())
    def sendCRLF(self,data):
        '''Will raise Broken pipe error if connection closed, otherwise will send ascii data new line terminated over telnet'''
        self.telnet.write((data+"\r\n").encode())
    def readLine(self):
        '''Will raise EOFError if connection closed, otherwise will return ascii data'''
        return self.telnet.read_until(b"\n",timeout=self.timeout)
    def readAvailable(self):
        '''Will raise EOFError if connection closed, otherwise will return ascii data'''
        return self.telnet.read_eager()
    def asyncRead(self,delay=0.1):
        import time
        from threading import Thread
        def run():
            self.run=True
            while(self.run):
                data=self.readLine()
                self.data+=data
                time.sleep(delay)
        t=Thread(target=run)
        t.start()
    def avilable(self):
        return len(self.data)
    def read(self):
        data=self.data
        self.data=b""
        return data
    def close(self):
        self.run=False
        self.telnet.close()
    def stop(self):
        self.run=False
    def __del__(self):
        self.stop()