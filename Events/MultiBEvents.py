# Lucien Lo <kin.ho.lo@cern.ch>
from BEvents import BEvents
from BranchBuilder import BranchBuilder

class MultiBEvents(object):
    def __init__(self, files, trees, maxEvents = -1):
        self.files = files
        self.trees = trees
        total_number_evt = sum([tree.GetEntries() for tree in self.trees])
        self.nEvents = min(total_number_evt, maxEvents) if (maxEvents > -1) else total_number_evt

        self.EvtClassDict = {}
        total_sum_entries = 0
        for tree in self.trees:
            total_sum_entries += tree.GetEntries()
            self.EvtClassDict[total_sum_entries] = BEvents(tree)
        self.iEvent = -1
    
    def __getitem__(self, i):
        if i >= self.nEvents:
            self.iEvent = -1
            raise IndexError("the index is out of range: " + str(i))
        self.iEvent = i
        for entries in self.EvtClassDict:
            if self.iEvent < entries: break
        return self.EvtClassDict[entries]

    def __iter__(self):
        for self.iEvent in xrange(self.nEvents):
            for entries in self.EvtClassDict:
                if self.iEvent < entries: break
            yield self.EvtClassDict[entries]
        self.iEvent = -1
