from .EventReader import EventLoop
from .UFEventReader import UFEventReader

class AllEvents(object):
    def __call__(self, event): return True

class UFComponentReader(object):
    def __init__(self, eventBuilder, eventLoopRunner, sequence, writer, selection=None):
        self.eventBuilder       = eventBuilder
        self.eventLoopRunner    = eventLoopRunner
        self.sequence           = sequence
        self.eventSelection     = AllEvents() if not selection else selection
        self.EventLoop          = EventLoop
        self.writer             = writer
        pass

    def begin(self):
        self.eventLoopRunner.begin()

    def read(self, dataset):
        components      = dataset.makeComponents()
        for component in components:
            reader          = UFEventReader(component,self.sequence,self.writer)
            eventLoop       = self.EventLoop(self.eventBuilder, self.eventSelection, component, reader)
            self.eventLoopRunner.run(eventLoop)

    def end(self):
        self.eventLoopRunner.end()
