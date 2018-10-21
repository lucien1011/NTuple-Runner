import os

class EndModule(object):
    def __call__(self,collector):
        pass

    @staticmethod
    def makedirs(outputDir):
        if not os.path.exists(os.path.abspath(outputDir)):
            os.makedirs(os.path.abspath(outputDir))

    @staticmethod
    def makedirs_with_file_path(outputPath):
        dir_path = os.path.abspath(os.path.dirname(outputPath))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
