from Core.Collector import Collector

import os,ROOT

class EndSequence(object):
    def __init__(self):
        self.moduleList = []
        self.collector = Collector()

    def run(self,inputInfo):
        self.collector.makeSampleList(inputInfo.outputDir)
        self.collector.openFiles(self.collector.samples,inputInfo)
        for module in self.moduleList:
            module(self.collector)
        self.collector.closeFiles()

    def add(self,module):
        self.moduleList.append(module)

    def __len__(self):
        return len(self.moduleList)

    def __getitem__(self,index):
        if index >= len(self):
            raise IndexError
        else:
            return self.moduleList[index]
