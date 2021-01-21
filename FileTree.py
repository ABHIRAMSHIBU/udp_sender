class fileTree:
    def __init__(self, file, chunksize, read=True):
        self.filename = file
        if (read):
            self.file = open(file, "rb")
        else:
            self.file = open(file, "wb")
        self.chunksize = chunksize

    def getNode(self, nodeid):
        start = nodeid * self.chunksize
        self.file.seek(start)
        node = self.file.read(self.chunksize)
        end = self.file.tell()
        return node

    def setNode(self, nodeid, node):
        start = nodeid * self.chunksize
        self.file.seek(start)
        bytes = self.file.write(node)
        end = self.file.tell()
        return bytes

    def getTotalNodes(self):
        import math
        f = open(self.filename, "ab")
        size = f.tell()
        f.close()
        return math.ceil(size / self.chunksize)
