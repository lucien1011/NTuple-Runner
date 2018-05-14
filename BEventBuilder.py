# Lucien Lo <kin.ho.lo@cern.ch>
import os
import ROOT
from .Events import BEvents

##____________________________________________________________________________||
class BEventBuilder(object):
    def build(self, dataset):
        return dataset.build_events()

##____________________________________________________________________________||
