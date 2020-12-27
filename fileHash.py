class FileHash:
    def __init__(self,fileName,chunkSize):
        import MD5Sum
        self.MD5Sum = MD5Sum
        self.fileName = fileName
        self.chunkSize = chunkSize
        self.MD5=self.genMD5()
    def genMD5(self):
        import math
        file = open(self.fileName,"ab")
        size = file.tell()
        file.close()
        file = open(self.fileName,"rb")
        l=[]
        numberOfChunks=size/self.chunkSize
        for i in range(math.ceil(numberOfChunks)):
            oldloc = file.tell()
            data = file.read(self.chunkSize)
            checkSum=self.MD5Sum.CheckSum(data)
            newloc = file.tell()
            l.append([checkSum.get_md5(),oldloc,newloc])
        return l
    def getMD5(self):
        return self.MD5