##____________________________________________________________________________||
import os
from .Utils.UFTier2Utils import listdir_uberftp
from .FileInfo import FileInfo
import copy

class FriendTreeConfig(object):
    def __init__(self,path,treeName,inUFTier2=False):
        self.path = path
        self.treeName = treeName
        self.inUFTier2 = inUFTier2
        self.fileInfo = FileInfo(self.path,self.inUFTier2)

    def getFilePath(self):
        return self.fileInfo.file_path()

class Component(object):
    def __init__(self,name,path,treeName,inUFTier2=True,maxEvents=-1,fdConfigs=[]):
        self.name = name
        self.path = path
        self.treeName = treeName
        self.inUFTier2 = inUFTier2
        self.fileInfo = FileInfo(path,inUFTier2)
        self.fileName = self.fileInfo.file_path()
        self.maxEvents = maxEvents
        self.fdConfigs = fdConfigs 
        self.fdFiles = []
        self.fdTrees = []
        self.beginEntry = 0
        self.reportInterval = 1000

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
    
    def extend(self,obj):
        self.list.extend(obj)
