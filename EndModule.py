import os

class EndModule(object):
    def __call__(self,collector):
        pass

    @staticmethod
    def makedirs(outputDir):
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))
