# Lucien Lo <lucienlo@cern.ch>

##____________________________________________________________________________||
class BaseDataset(object):
    def __init__(self,name,isMC=True,isSignal=False):
        self.name = name
        self.isMC = isMC
        self.isData = not self.isMC
        self.isSignal = isSignal
        if self.isSignal and self.isData:
            raise RuntimeError, "Dataset "+self.name+" can't be data and signal at the same time"

##____________________________________________________________________________||
