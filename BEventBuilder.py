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
        for config in component.fdConfigs:
            tree.AddFriend(config.treeName,config.getFilePath())
        return BEvents(tree, component.maxEvents, component.beginEntry)

##____________________________________________________________________________||
