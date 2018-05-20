
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
