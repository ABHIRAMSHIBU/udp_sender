#!/usr/bin/env python3
import os
import sys
from datetime import datetime
class TimeIt:
    def __init__(self,command):
        self.command = command
    def timeDataTransfer(self,size):
        timenow = datetime.now()
        os.system(self.command)
        timeelapsed = datetime.now() - timenow
        print("Time elapsed = ",timeelapsed.seconds+(timeelapsed.microseconds/10**6))
        print("Data Transferred = ",size,"MB")
        print("Data MB/s = ",size/(timeelapsed.seconds+(timeelapsed.microseconds/10**6)))
args = sys.argv
command = args[1]
arguments = args[2:]
file = "testfiles/test.png" # Default
for i in arguments:
    if(i=="-f" or i=="--file"):
        pos = arguments.index(i)
        file = arguments[pos+1]
ti = TimeIt(command+" "+" ".join(arguments))
ti.timeDataTransfer(os.path.getsize(file)/(1000**2))