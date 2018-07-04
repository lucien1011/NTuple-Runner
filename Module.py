import os

class Module(object):
    def __init__(self,name):
        self.name = name
    
    def begin(self):
        pass

    def beginEvents(self,events):
        pass

    def end(self):
        pass

    def analyze(self,event):
        pass

    @staticmethod
    def makedirs(outputDir):
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))
