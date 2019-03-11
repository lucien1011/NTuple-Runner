from .ComponentList import ComponentList
from .BaseDataset import BaseDataset
from .Events import BEvents
from .Events import MultiBEvents
from .FileInfo import FileInfo
import ROOT
import copy,os

class Dataset(BaseDataset):
    def __init__(self,name,componentList,isMC=True,sumw=None,xs=None,maxEvents=-1,build_type="TTree",lumi=1.,json=None,isSignal=False,plotLabel="",xsFactor=None,skipWeight=False):
        super(Dataset,self).__init__(name,isMC,isSignal)
        self.componentList = componentList
        self.sumw = sumw
        self.xs = xs
        self.fb_to_pb_factor = 1000
        self.maxEvents = maxEvents
        self.build_type = build_type
        self.lumi = lumi
        self.json = json
        self.isSignal = isSignal
        self.plotLabel = plotLabel if plotLabel else self.name
        self.xsFactor = xsFactor
        self.skipWeight = skipWeight

    def setSumWeight(self,inputFileName,histPath="SumWeight",inUFTier2=False):
        fileInfo = FileInfo(inputFileName,inUFTier2)
        fileName = fileInfo.file_path()
        inputFile = ROOT.TFile.Open(fileName,"READ")
        inputHist = inputFile.Get(histPath)
        if self.sumw: print "Overwriting sumw in datast "+self.name
        self.sumw = inputHist.Integral()
        inputFile.Close()

    def setSumWeightByDir(self,inputDir,histPath="histos/nevents",inUFTier2=False):
        allFilePaths = [os.path.join(inputDir,f) for f in os.listdir(inputDir) if ".root" in f]
        self.sumw = 0.
        for filePath in allFilePaths:
            inputFile = ROOT.TFile.Open(filePath,"READ")
            inputHist = inputFile.Get(histPath)
            self.sumw += inputHist.Integral()
            inputFile.Close()

    def setSumWeightByTxt(self,inputFile,histPath="histos/nevents",inUFTier2=False):
        txtFile = open(inputFile,"r")
        txtFileLines = txtFile.readlines()
        self.sumw = 0.
        for lines in txtFileLines:
            self.sumw = float(lines)
        txtFile.close()

    def saveSumWeightToPath(self,outputPath):
        txtFile = open(outputPath,"w")
        txtFile.write(str(self.sumw))
        txtFile.close()

    def setSumWeightFromHeppySkimReport(self,textFilePath):
        eventsFile = open(textFilePath,"r").readlines()
        for line in eventsFile:
            if "All Events" in line:
                nevent = float(line.split()[2])
            if "Sum Weights" in line:
                sweight = float(line.split()[2])
        # self.nEvent[sample] = counters['Sum Weights']
        assert nevent is not None and sweight is not None, "Can't find event count or sum weights in text file provided "+textFilePath
        if self.sumw: print "Overwriting sumw in datast "+self.name
        #self.datasetNEvents = nevent
        self.sumw = sweight

    def makeComponents(self):
        componentList = []
        for icmp,cmp in enumerate(self.componentList):
            tmpCmp = copy.deepcopy(self)
            tmpCmp.componentList = [cmp]
            tmpCmp.name = self.name+"_"+str(icmp)
            tmpCmp.fileName = cmp.fileName
            tmpCmp.treeName = cmp.treeName
            tmpCmp.maxEvents = cmp.maxEvents
            tmpCmp.parent = self
            tmpCmp.fdConfigs = cmp.fdConfigs
            tmpCmp.fdFiles = cmp.fdFiles
            tmpCmp.fdTrees = cmp.fdTrees
            tmpCmp.beginEntry = cmp.beginEntry
            tmpCmp.reportInterval = cmp.reportInterval
            componentList.append(tmpCmp)
        return componentList

    def add(self,obj):
        if self.isMC != obj.isMC: raise RuntimeError, "Can't add dataset with MC and data together"
        if self.xs != obj.xs: raise RuntimeError, "Can't add dataset with different xs"
        if self.sumw != None and obj.sumw != None: self.sumw += obj.sumw
        self.componentList.extend(obj.componentList)
