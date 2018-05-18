from Core.Collector import Collector
from Hadder import Hadder

import os,ROOT

class EndSequence(object):
    def __init__(self):
        self.moduleList = []
        self.collector = Collector()
        self.hadder = Hadder()

    def run(self,inputInfo,componentList):
        self.collector.makeSampleList(componentList)
        for sampleName in self.collector.samples:
            print "Hadding "+sampleName
            self.hadder.makeHaddScript(inputInfo.outputDir+sampleName,sampleName,inputInfo)
            self.hadder.haddSampleDir(inputInfo.outputDir+sampleName)
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
