from Core.Collector import Collector
from Hadder import Hadder
from .BaseModule import BaseModule

import os,ROOT

class EndSequence(BaseModule):
    def __init__(self,skipHadd=False,haddAllSamples=False,haddDataSamples=False,skipComponentHadd=False):
        self.moduleList = []
        self.collector = Collector()
        self.hadder = Hadder()
        self.skipHadd = skipHadd
        self.haddAllSamples = haddAllSamples
        self.haddDataSamples = haddDataSamples
        self.allSampleName = "AllSample"
        self.allDataName = "Data"
        self.skipComponentHadd = skipComponentHadd

    def run(self,inputInfo,componentList,mergeSampleDict={},mergeSigSampleDict={}):
        self.collector.makeSampleList(componentList)
        self.collector.makeMergedSampleList(componentList,mergeSampleDict,mergeSigSampleDict)
        for sampleName in self.collector.mergeSamples:
            self.makedirs(inputInfo.outputDir+sampleName)
        if not self.skipHadd:
            if not self.skipComponentHadd:
                for sampleName in self.collector.samples:
                    print "Hadding "+sampleName
                    self.makedirs(inputInfo.outputDir+sampleName)
                    self.hadder.makeHaddScript(inputInfo.outputDir+sampleName,[sampleName],inputInfo)
                    self.hadder.haddSampleDir(inputInfo.outputDir+sampleName)
            if self.haddAllSamples:
                print "Hadding "+self.allSampleName
                self.makedirs(inputInfo.outputDir+self.allSampleName)
                self.hadder.makeHaddScript(inputInfo.outputDir+self.allSampleName,self.collector.samples,inputInfo)
                self.hadder.haddSampleDir(inputInfo.outputDir+self.allSampleName)
            if self.haddDataSamples and self.collector.dataSamples:
                print "Hadding "+self.allDataName
                self.makedirs(inputInfo.outputDir+self.allDataName)
                self.hadder.makeHaddScript(inputInfo.outputDir+self.allDataName,self.collector.dataSamples,inputInfo)
                self.hadder.haddSampleDir(inputInfo.outputDir+self.allDataName)
            for sampleName in self.collector.mergeSamples+self.collector.mergeSigSamples:
                print "Hadding (and merging) "+sampleName
                if sampleName in self.collector.mergeSamples:
                    tmpDict = self.collector.mergeSampleDict
                elif sampleName in self.collector.mergeSigSamples:
                    tmpDict = self.collector.mergeSigSampleDict
                self.hadder.makeHaddScript(inputInfo.outputDir+sampleName,tmpDict[sampleName],inputInfo)
                self.hadder.haddSampleDir(inputInfo.outputDir+sampleName)
        self.collector.openFiles(self.collector.samples,inputInfo)
        self.collector.openFiles(self.collector.mergeSamples,inputInfo)
        self.collector.openFiles(self.collector.mergeSigSamples,inputInfo)
        if self.haddAllSamples: self.collector.openFiles([self.allSampleName,],inputInfo)
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
