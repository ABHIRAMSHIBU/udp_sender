#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:46:28 2020

@author: Anjali Venugopal
@secondary-author: Abhiram Shibu
"""

from  Queue import Queue
testpass=True
myQueue = Queue(10)
if(myQueue.dequeue()!=None):
    testpass=False
if(myQueue.isEmpty()!=True):
    testpass=False
if(myQueue.isFull()!=False):
    testpass=False
if(myQueue.peek()!=None):
    testpass=False
myQueue.enqueue(1)
myQueue.enqueue(2)
myQueue.enqueue(3)
if(myQueue.dequeue()!=1):
    testpass=False
if(myQueue.dequeue()!=2):
    testpass=False
if(myQueue.dequeue()!=3):
    testpass=False
if(myQueue.dequeue()!=None):
    testpass=False
if(testPass==True):
    print("Test Passed!")
else:
    print("One or more of the tests failed!")