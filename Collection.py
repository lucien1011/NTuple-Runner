import ROOT

class Object(object):
    """Class that allows seeing a set branches plus possibly an index as an Object"""
    def __init__(self,event,objName,index,divider="_"):
        self._event   = event
        self._objName = objName+divider
        self._index   = index
        self._p4      = None
        pass

    def __getattr__(self,quantity):
        if quantity != "phyLabel":
            return getattr(self._event,self._objName+quantity)[self._index]
        else:
            return self._objName[:-1] 

    def p4(self):
        if self._p4 == None:
            self._p4 = ROOT.TLorentzVector()
            self._p4.SetPtEtaPhiM(self.pt,self.eta,self.phi,self.mass)
            pass
        return self._p4
        pass

    def getFriendValue(self,postfix,quantity):
        return getattr(self._event,self._objName[:-1]+postfix+self._objName[-1]+quantity)[self._index]

    def getIndex(self):
        return self._index

class Collection(object):
    def __init__(self,event,objName,divider="_",length_var=None):
        self._event   = event   
        self._objName = objName
        self._divider = divider
        if not length_var:
            self._length_var = self._objName+self._divider+"pt"
        else:
            self._length_var = length_var
        self._count_length = not bool(length_var)
        self._phyDict = {}
        self._validateInput()

    def __getitem__(self,index):
        if index >= len(self):
            raise IndexError
        else:
            if index not in self._phyDict:
                self._phyDict[index] = Object(self._event,self._objName,index,divider=self._divider)
            return self._phyDict[index]

    def __len__(self):
        if self._count_length:
            return len(getattr(self._event,self._length_var))
        else:
            return getattr(self._event,self._length_var)[0]

    def _validateInput(self):
        if not hasattr(self._event,self._length_var):
            raise AttributeError, "Object {} does not exist in tree".format(self._objName)
