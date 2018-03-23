from DataFormats.FWLite import Events

class EDMEvents(Events):
    def setup(self):
        self.iEvent = -1
        self.nEvents = self.size()

    def __getitem__(self, i):
        if i >= self.size():
            self.iEvent = -1
            raise IndexError("the index is out of range: " + str(i))
        self.iEvent = i
        self.to(self.iEvent)
        return self
    
    def __iter__(self):
        for self.iEvent in xrange(self.nEvents):
            self.to(self.iEvent)
            yield self
        self.iEvent = -1
