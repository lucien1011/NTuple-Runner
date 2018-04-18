# Lucien Lo <lucienlo@cern.ch>

##____________________________________________________________________________||
import os

##____________________________________________________________________________||
class FileInfo(object):
    def __init__(self, path,inUFTier2=False):
        self.path = path
        self.name = os.path.basename(path).replace(".root","")
        self.inUFTier2 = inUFTier2

    def file_path(self):
        if self.inUFTier2:
            return self.uberftp_path()
        else:
            return self.path

    def uberftp_path(self):
        return "root://cmsio3.rc.ufl.edu/"+self.path.replace("/cms/data","")

