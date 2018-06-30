import os,ROOT,pickle
from .Utils.processCmds import processCmd

class Hadder(object):
    def haddSampleDir(self,dir_path):
        processCmd('sh '+os.path.join(dir_path,"hadd.sh"))

    def makeHaddScript(self,dir_path,sampleNames,outputInfo):
        haddText="hadd -f {0} ".format(dir_path+"/"+outputInfo.TFileName)
        basedir = os.path.dirname(dir_path)+"/"
        for sampleName in sampleNames:
            haddText += " {0}/*_{1}".format(basedir+sampleName,outputInfo.TFileName)+" "
            haddText += "\n"
        outTextFile = open(dir_path+"/hadd.sh","w")
        outTextFile.write(haddText)
