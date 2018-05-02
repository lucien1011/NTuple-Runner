from .Component import Component

class Dataset(Component):
    def __init__(self, path, name, keyword="",exclude="",inUFTier2=True,isMC=True,sumw=None,xs=None):
        super(Dataset,self).__init__(path,name,keyword,exclude,inUFTier2)
        self.sumw = sumw
        self.xs = xs
        self.fb_to_pb_factor = 1000
