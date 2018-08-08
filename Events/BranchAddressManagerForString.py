import ROOT
import re
import array

##__________________________________________________________________||
class BranchAddressManagerForString(object):
    """The branch address manager for ROOT TTree
    This class manages ROOT.vector objects used for branch addresses
    of ROOT TTree. The main purpose of this class is to prevent
    multiple objects from being created for the same branch.
    All instances of this class share the data.
    """

    addressDict = { }

    def getString(self, tree, branchName):
        """return the ROOT.vector object for the branch.
        """

        if (tree, branchName) in self.__class__.addressDict:
            return self.__class__.addressDict[(tree, branchName)]

        itsString = self._getString(tree, branchName)
        self.__class__.addressDict[(tree, branchName)] = itsString

        return itsString

    def _getString(self, tree, branchName):

        leafNames = [l.GetName() for l in tree.GetListOfLeaves()]
        list_fd = tree.GetListOfFriends()
        try: 
            if list_fd.GetSize():
                for fd in list_fd:
                    leafNames.extend([k.GetName() for k in fd.GetTree().GetListOfLeaves()])
        except ReferenceError: pass

        if branchName not in leafNames:
            return None

        leaf = tree.GetLeaf(branchName)
        typename = leaf.GetTypeName() # e.g., "vector<string>"
        if typename != "string": return None
        
        tree.SetBranchStatus(leaf.GetName(), 1)
        itsString = ROOT.vector('char')()
        tree.SetBranchAddress(leaf.GetName(), itsString)

        return itsString


