# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
import os

##____________________________________________________________________________||
class Analyzer(object):
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

##____________________________________________________________________________||