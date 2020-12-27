class FileHash:
    def __init__(self, chunkSize, fileName=None, data=None, md5sum=None, generate=False):
        import MD5Sum
        if data == None and generate == False:
            print("Cannot proceed, data cannot be empty when in verify mode!")
            raise ValueError("Value Check Failed")
        if md5sum == None and generate == False:
            print("Cannot procced, no MD5sum found to verify")
            raise ValueError("MD5Sum required")
        self.MD5Sum = MD5Sum
        self.fileName = fileName
        self.chunkSize = chunkSize
        self.data = data
        self.md5sum = md5sum
        self.verified = False
        if (generate):
            self.MD5 = self.genMD5()
        else:
            self.verifyChunk()

    def genMD5(self):
        import math
        file = open(self.fileName, "ab")
        size = file.tell()
        file.close()
        file = open(self.fileName, "rb")
        l = []
        numberOfChunks = size / self.chunkSize
        for i in range(math.ceil(numberOfChunks)):
            oldloc = file.tell()
            data = file.read(self.chunkSize)
            checkSum = self.MD5Sum.CheckSum(data)
            newloc = file.tell()
            l.append([checkSum.get_md5(), oldloc, newloc])
        return l

    def getMD5(self):
        return self.MD5

    def verifyChunk(self):
        checkSum = self.MD5Sum.CheckSum(self.data)
        if checkSum.verify_md5(self.md5sum):
            self.verified = True
        return self.verified
