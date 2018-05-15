import os
from .UFTier2Utils import listdir_uberftp
from ..ComponentList import Component

def makeComponents(sampleName,dir_path,treeName,inUFTier2):
    if inUFTier2:
        fileNames = [ dir_path+"/"+n for n in listdir_uberftp(dir_path) if n.endswith(".root") ]
    else:
        fileNames = [ dir_path+"/"+n for n in os.listdir(dir_path) if n.endswith(".root") ]
    cmpList = []
    for fileName in fileNames:
        tmpCmp = Component(sampleName,fileName,treeName,inUFTier2=inUFTier2)
        cmpList.append(tmpCmp)
    return cmpList
