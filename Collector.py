import os,ROOT
from .mkdir_p import mkdir_p 

class Collector(object):
    def __init__(self):
        self.objDict = {}
        self.fileDict = {}
        self.saveObjDict = {}

    def addObj(self,key,obj):
        if key not in self.saveObjDict:
            self.saveObjDict[key] = obj
        else:
            raise RuntimeError,"Overwriting object in objDict in Collector"

    def makeSampleList(self,componentList):
        self.samples = [cmp.name for cmp in componentList]
        self.mcSamples = [cmp.name for cmp in componentList if cmp.isMC]
        self.dataSamples = [cmp.name for cmp in componentList if cmp.isData]
        self.signalSamples = [cmp.name for cmp in componentList if cmp.isSignal and cmp.isMC]
        self.bkgSamples = [cmp.name for cmp in componentList if not cmp.isSignal and cmp.isMC]
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

    def saveFile(self,inputInfo,sample,fileName):
        inputPath = inputInfo.outputDir+"/"+sample+"/"+fileName
        mkdir_p(os.path.dirname(inputPath))
        outFile = ROOT.TFile(inputPath,"RECREATE")
        for key,item in self.saveObjDict.iteritems():
        #for key in self.saveObjDict:
            #item = ROOT.gDirectory.Get(key)
            item.Write()
        outFile.Close()
