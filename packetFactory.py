class packetFactory:
    def __init__(self,sequenceStart=0):
        self.sequence=sequenceStart-1
    def create(self,data,sequence=None):
        import pickle
        if(sequence==None):
            self.sequence+=1
            sequence=self.sequence
        return sequence,pickle.dumps({"s":sequence,"p":data})
    def open(self,packet):
        import pickle
        item = pickle.loads(packet)
        return item["s"],item["p"]