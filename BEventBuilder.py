# Lucien Lo <kin.ho.lo@cern.ch>
import os
import ROOT
from .Events import BEvents

##____________________________________________________________________________||
class BEventBuilder(object):
    def build(self, component):
        inputPath = component.fileName
        file = ROOT.TFile.Open(inputPath)
        tree = file.Get(component.treeName)
        for (filePath,treePath) in component.fdPaths:
            tree.AddFriend(treePath,filePath)
        return BEvents(tree, component.maxEvents)

##____________________________________________________________________________||
