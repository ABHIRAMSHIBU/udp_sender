#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:13:57 2020

@author: Vishnu
@secondary-author: Abhiram Shibu
"""
from Stack import stack
testPass=True
s=stack()
s.push(5)
if(s.peek()!=5):
    testPass=False
s.push(5)
s.push(64)
s.push(777)
if(s.size()!=4):
    testPass=False
if(s.pop()!=777):
    testPass=False
if(s.peek()!=64):
    testPass=False
if(s.pop()!=64):
    testPass=False
if(s.pop()!=5):
    testPass=False
if(s.pop()!=5):
    testPass=False
if(s.pop(handle=True)!=None):
    testPass=False
if(testPass==True):
    print("Test Passed!")
else:
    print("One or more of the tests failed!")
    
    