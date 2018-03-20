# Lucien Lo <lucienlo@cern.ch>

##____________________________________________________________________________||
import os
from ..Utils.UFTier2Utils import listdir_uberftp
from FileInfo import FileInfo
import copy

##____________________________________________________________________________||
class Component(object):
    def __init__(self, path, name, keyword="tree",inUFTier2=True):
        self.path = path
        self.name = name
        self.keyword = keyword
        self.inUFTier2 = inUFTier2
        if self.inUFTier2:
            self.fileNames = [n for n in listdir_uberftp(self.path) if n.endswith(".root") and keyword in n]
        else:    
            self.fileNames = [n for n in os.listdir(self.path) if n.endswith(".root") and keyword in n]

        self._fileDict = { }
        self._cfg = None

    def __getattr__(self, name):
        if name not in self._fileDict:
            if name not in self.fileNames:
                raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))
            path = os.path.join(self.path, name)
            self._fileDict[name] = FileInfo(path,self.inUFTier2)
        return self._fileDict[name]

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def fileInfos(self):
        return [getattr(self, n) for n in self.fileNames]

    def makeComponentFromEachFile(self,prefix=""):
        componentList = []
        for fileName in self.fileNames:
            tmpCmp = copy.deepcopy(self)
            tmpCmp.fileNames = [fileName]
            tmpCmp.name = prefix+fileName.replace(".root","")
            componentList.append(tmpCmp)
        return componentList

##____________________________________________________________________________||
