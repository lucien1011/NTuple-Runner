from .ComponentList import ComponentList
from .Events import BEvents
import ROOT

class Dataset(object):
    def __init__(self,name,componentList,isMC=True,sumw=None,xs=None,maxEvents=-1,build_type="TChain"):
        self.name = name
        self.componentList = componentList
        self.isMC = isMC
        self.sumw = sumw
        self.xs = xs
        self.fb_to_pb_factor = 1000
        self.maxEvents = maxEvents
        self.build_type = build_type

    def build_events(self):
        if self.build_type == "TChain":
            for component in self.componentList:
                if component.treeName != self.componentList[0].treeName:
                    raise RuntimeError,"Not all the file have the same tree name for the TChain Event Building"
            chain = ROOT.TChain(self.componentList[0].treeName)
            for component in self.componentList:
                for fileInfo in component.fileInfos():
                    chain.Add(fileInfo.file_path())
            return BEvents(chain,self.maxEvents)
        else:
            raise RuntimeError, "Sorry other method of building Events class is not supported at the moment"

    def setSumWeight(self,fileName,histPath="SumWeight"):
        inputFile = ROOT.TFile(fileName,"READ")
        inputHist = inputFile.Get(histPath)
        if self.sumw: print "Overwriting sumw in datast "+self.name
        self.sumw = inputHist.Integral()
        inputFile.Close()
        
