from ..EventReader import EventLoop
from .UFEventReader import UFEventReader

class AllEvents(object):
    def __call__(self, event): return True

class UFComponentReader(object):
    def __init__(self, eventBuilder, eventLoopRunner, sequence):
        self.eventBuilder       = eventBuilder
        self.eventLoopRunner    = eventLoopRunner
        self.sequence           = sequence
        self.eventSelection     = AllEvents()
        self.EventLoop          = EventLoop
        pass

    def begin(self):
        self.eventLoopRunner.begin()

    def read(self, dataset):
        reader         = UFEventReader(self.sequence)
        eventLoop      = self.EventLoop(self.eventBuilder, self.eventSelection, dataset, reader)
        self.eventLoopRunner.run(eventLoop)

    def end(self):
        self.eventLoopRunner.end()