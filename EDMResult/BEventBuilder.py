# Lucien Lo <kin.ho.lo@cern.ch>
import os
import ROOT
from Core.EDMResult.EDMEvents import EDMEvents

##____________________________________________________________________________||
class BEventBuilder(object):
    def build(self, component):
        if len(component.fileInfos()) != 1: raise RuntimeError, "Do not support multiple file for EDM result at the moment"
        events = EDMEvents(component.fileInfos()[0].file_path())
        events.setup()
        return events

##____________________________________________________________________________||
