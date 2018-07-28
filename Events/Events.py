# Tai Sakuma <tai.sakuma@cern.ch>

##____________________________________________________________________________||
class Events(object):
    """An iterative object for events.

    You can use this class to iterate over entries in a ROOT TTree.

    You can instantiate this class with a TTree object and an
    optionally a maximum number of entries to loop over::

        inputFile = ROOT.TFile.Open(inputPath)
        tree = inputFile.Get(treeName)
        events = Events(tree)

    Then, the "for" loop for the tree entries can be::

        for event in events:

    Note: "event" and "events" are the same object. In each iteration,
    "event" (and "events") is loaded with the next entry in the tree.

    A content of the tree, e.g., a branch, can be accessed as an
    attribute of "event"::

          event.jet_pt

    In order to access to a particular entry, you can use an index.
    For example, to get 11th entry (the index for the first entry is
    0)::

        event = events[10]

    Note: Again "event" and "events" are the same object.

    """

    def __init__(self, tree, maxEvents = -1, beginEntry = 0):
        self.file = tree.GetDirectory().GetFile() # so a file won't close
        self.tree = tree
        self.beginEntry = beginEntry
        if maxEvents > -1:
            self.nEvents = min(self.tree.GetEntries(), maxEvents) - self.beginEntry
        else:
            self.nEvents = self.tree.GetEntries() - self.beginEntry
        if self.nEvents < 0:
            raise RuntimeError,"nEvents is negative"
        self.iEvent = -1

    def __getitem__(self, i):
        if i >= self.nEvents:
            self.iEvent = -1
            raise IndexError("the index is out of range: " + str(i))
        self.iEvent = i

        self.tree.GetEntry(self.iEvent)
        return self

    def __iter__(self):
        for self.iEvent in xrange(self.beginEntry,self.beginEntry+self.nEvents):
            self.tree.GetEntry(self.iEvent)
            yield self
        self.iEvent = -1

    def __getattr__(self, name):
        return getattr(self.tree, name)

##____________________________________________________________________________||
