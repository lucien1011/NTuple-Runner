# Lucien Lo <kin.ho.lo@cern.ch>
import os
import ROOT
from ..Events import BEvents

##____________________________________________________________________________||
class BEventBuilder(object):
    def __init__(self, treeName, maxEvents = -1):
        self._treeName = treeName
        self._maxEvents = maxEvents

    def build(self, component):
        chain = ROOT.TChain(self._treeName)
        for fileInfo in component.fileInfos():
            chain.Add(fileInfo.file_path()) 
        return BEvents(chain, self._maxEvents)

##____________________________________________________________________________||
