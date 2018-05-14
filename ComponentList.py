##____________________________________________________________________________||
import os
from .Utils.UFTier2Utils import listdir_uberftp
from .FileInfo import FileInfo
import copy

class Component(object):
    def __init__(self,name,path,treeName,keyword="",exclude="",inUFTier2=True):
        self.name = name
        self.path = path
        self.treeName = treeName
        self.inUFTier2 = inUFTier2
        if self.inUFTier2:
            self.fileNames = [n for n in listdir_uberftp(path) if n.endswith(".root") and keyword in n]
        else:    
            self.fileNames = [n for n in os.listdir(path) if n.endswith(".root") and keyword in n] 
        if exclude:
            self.fileNames = [n for n in self.fileNames if exclude not in n]   
        self._fileDict = { }

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

class ComponentList(object):
    def __init__(self,component_list):
        self.list = component_list

    def __len__(self):
        return len(self.list)

    def __getitem__(self,index):
        if index >= len(self):
            raise IndexError
        else:
            return self.list[index]
