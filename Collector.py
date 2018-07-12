import os,ROOT

class Collector(object):
    def __init__(self):
        self.objDict = {}
        self.fileDict = {}

    def makeSampleList(self,componentList):
        self.samples = [cmp.name for cmp in componentList]
        self.mcSamples = [cmp.name for cmp in componentList if cmp.isMC]
        self.dataSamples = [cmp.name for cmp in componentList if cmp.isData]
        self.signalSamples = [cmp.name for cmp in componentList if cmp.isSignal]
        self.bkgSamples = [cmp.name for cmp in componentList if not cmp.isSignal]
        self.sampleDict = {cmp.name: cmp for cmp in componentList}

    def makeMergedSampleList(self,componentList,mergeCmpDict):
        self.mergeSamples = []
        for sampleName in mergeCmpDict:
            if all([name not in self.samples for name in mergeCmpDict[sampleName]]): continue
            self.mergeSamples.append(sampleName)
        self.mergeSampleDict = {}
        for sampleName in self.mergeSamples:
            self.mergeSampleDict[sampleName] = []
            for name in mergeCmpDict[sampleName]:
                if name not in self.samples: continue
                self.mergeSampleDict[sampleName].append(name)
    
    def openFiles(self,samples,inputInfo):
        for sample in samples:
            if sample in self.fileDict: continue
            inputPath = inputInfo.outputDir+"/"+sample+"/"+inputInfo.TFileName
            self.fileDict[sample] = ROOT.TFile(inputPath,"READ")
    
    def getObj(self,sample,pathInFile):
        key = "/".join([sample,pathInFile])
        if key not in self.objDict:
            self.objDict[key] = self.fileDict[sample].Get(pathInFile)
        return self.objDict[key]

    def closeFiles(self):
        for fileToClose in self.fileDict.values():
            fileToClose.Close()
