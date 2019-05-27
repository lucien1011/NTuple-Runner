import os,ROOT,pickle,csv

supportRootObjs = ["TH1D","TH2D",]
pickleObjs = ["list","dict",]
textFileObjs = ["TextFile",]
csvFileObjs = ["CSVFile",]

class CSVFile(object):
    def __init__(self,pyFile,writer):
        self.pyFile = pyFile
        self.writer = writer

class Writer(object):
    def __init__(self,dataset,outputInfo):
        self.outputInfo = outputInfo
        self.dataset = dataset
        self.outputDir = self.outputInfo.outputDir+"/"+self.dataset.parent.name+"/"
        self.TFile = None
        self.objs = {}
        self.rootObjs = {}
        self.pickleObjs = {}
        self.textFileObjs = {}
        self.csvFileObjs = {}
    
    @staticmethod
    def makedirs(outputDir):
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))

    def makeTFile(self,fileName="test.root"): 
        self.makedirs(self.outputDir)
        self.TFile = ROOT.TFile(self.outputDir+"/"+fileName,"RECREATE")

    def initObjects(self):
        if hasattr(self.outputInfo,"TFileName"):
            self.makeTFile(fileName=self.dataset.name+"_"+self.outputInfo.TFileName)

    def closeTFile(self):
        if self.TFile:
            self.TFile.Close()

    def closeAll(self):
        self.closeTFile()

    def book(self,keyName,objType,*args):
        if keyName not in self.objs:
            self.objs[keyName] = self.createObj(objType,*args)
            if objType in supportRootObjs:
                self.rootObjs[keyName] = self.objs[keyName]
            if objType in pickleObjs:
                self.pickleObjs[keyName] = self.objs[keyName]
            if objType in textFileObjs:
                self.textFileObjs[keyName] = self.objs[keyName]
            if objType in csvFileObjs:
                self.csvFileObjs[keyName] = self.objs[keyName]
        else:
            raise RuntimeError, "Object with internal name "+keyName+" exists in the writer"
            
    def createObj(self,objType,*args):
        if objType == "list":
            obj = []
            return obj
        elif objType == "dict":
            obj = {}
            return obj
        elif objType == "TextFile":
            obj = open(*args)
            return obj
        elif objType == "CSVFile":
            obj = self.makeCSVObj(*args)
            return obj
        elif objType in supportRootObjs:
            obj = getattr(ROOT,objType)(*args)
            return obj 

    def write(self):
        self.TFile.Write()
        for keyName,obj in self.pickleObjs.iteritems():
            outputPath = self.outputDir+"/"+keyName+".pkl"
            pickle.dump(obj,open(outputPath,"w"))
        for keyName,obj in self.textFileObjs.iteritems():
            obj.close()
        for keyName,obj in self.csvFileObjs.iteritems():
            obj.pyFile.close()

    def makeCSVObj(self,fileName,writeOption):
        pyFile = open(os.path.join(self.outputDir,fileName),writeOption)
        writer = csv.writer(pyFile)
        return CSVFile(pyFile,writer)

