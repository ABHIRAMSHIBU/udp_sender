#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 17:45:19 2020

@author: Anandakrishnan P 
@secondary-author: Abhiram Shibu
"""

import hashlib


class CheckSum:
    def __init__(self, data):
        self.data = data

    def get_md5(self):
        data = self.data
        md5_hash = hashlib.md5()
        if type(data) is bytes:
            md5_hash.update(data)
        else:
            md5_hash.update(data.encode())
        return md5_hash.hexdigest()

    def verify_md5(self, hash):
        if hash == CheckSum.get_md5(self.data):
            return True
        else:
            return False
